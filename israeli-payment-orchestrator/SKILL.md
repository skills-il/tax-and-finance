---
name: israeli-payment-orchestrator
description: Orchestrate Israeli payment gateways (Cardcom, Tranzila, PayMe, Meshulam, iCredit, Pelecard) with unified routing, fallback, and installments (tashlumim). Use when user asks about multi-gateway payment integration, "slikat kartisim", "tashlumim", payment routing, Shva network, BOI payment-services regulation, gateway comparison, or building a payment abstraction layer for Israeli merchants. Provides unified API patterns, installment handling, Shva clearing rules, and regulatory compliance. Do NOT use for single gateway setup (use cardcom-payment-gateway or tranzila-payment-gateway instead).
license: MIT
version: 1.3.0
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex. Python 3.8+ for helper scripts.
---

# Israeli Payment Orchestrator

## Instructions

### Step 1: Assess Payment Requirements
Ask the user about their payment needs:

| Requirement | Hebrew | Description | Impact on Gateway Choice |
|-------------|--------|-------------|-------------------------|
| Installments (tashlumim) | תשלומים | Split payment into monthly installments | Not all gateways support all installment types |
| Bit / Apple Pay | ביט / אפל פיי | Alternative payment methods | Gateway-specific integrations |

### Step 2: Compare Gateways
Use `scripts/compare_gateways.py` to generate a comparison matrix, or reference the table below:

| Gateway | API Style | Installments | Recurring | Hosted Page | Bit | Amount field unit |
|---------|-----------|-------------|-----------|-------------|-----|-------------------------------|
| Cardcom | REST JSON | Regular, credit | Yes | Redirect or iframe (Low Profile) | Yes (`UrlToBit`) | Major units (decimal) |
| Tranzila | Form-encoded CGI (legacy) + REST JSON (API V2) | Regular, credit | Yes | Iframe, redirect or Hosted Fields | Yes (dedicated Bit API; `bit_pay=1` on the iframe) | Major units (decimal) |
| PayMe | REST JSON | Unverified | Unverified | Unverified | Unverified | Unverified, confirm first |
| Meshulam (Grow) | multipart/form-data | Regular, credit | Yes | Iframe + redirect | Yes (`cancelBitTransaction` exists) | Major units (decimal) |
| iCredit | WCF `.svc` service | Unverified | Unverified | Unverified | Unverified | Unverified, confirm first |
| Pelecard | REST JSON | Regular, credit | Yes | Redirect or iframe | Yes, per `pelecard-payment-gateway` | Minor units (agorot) |

**On pricing: this skill does not publish fee bands.** None of the six gateways publishes a rate card. The merchant discount rate is contractual and quoted per merchant on volume, industry and chargeback profile, and earlier versions of this skill carried per-gateway bands that no vendor stands behind. A comparison table that names a cheapest gateway on invented numbers ranks on nothing, and the ordering flips on a difference smaller than any real negotiation. Send the user to each gateway for a written quote.

**"Unverified" is not "no".** Where no public source establishes a capability either way, this skill says so rather than guessing a negative. **PayMe and iCredit are unverified across most of the row**, not because they lack the features but because neither publishes a reachable API reference. Treat every PayMe or iCredit design decision as needing vendor confirmation first.

**The per-gateway skills are the authority on their own gateway.** For field names, error codes, auth handshakes and endpoint paths, defer to `cardcom-payment-gateway`, `tranzila-payment-gateway`, `grow-payment-gateway` and `pelecard-payment-gateway`. PayMe and iCredit have no dedicated skill, which is why several of their cells read "unverified".

### Step 3: Design the Orchestration Layer
Build a unified payment abstraction:

```python
# Unified payment interface pattern
class PaymentRequest:
    action: str              # פעולה - "sale" (charge now) or "authorize" (hold now,
                             # capture later). Two different gateway calls, see Step 7.
    amount: int              # סכום - store ONE canonical unit, agorot, as an integer
                             # and convert per gateway on the way out (see below)
    currency: str            # מטבע - "ILS" default
    installments: int        # תשלומים - 1 = regular, 2-36 = installments
    installment_type: str    # סוג תשלומים - "regular", "credit", "club"
    card_token: str          # טוקן כרטיס - for recurring
    description: str         # תיאור עסקה
    customer_id: str         # מזהה לקוח
    idempotency_key: str     # מפתח אידמפוטנטי - prevent duplicates

class PaymentResult:
    outcome: str             # תוצאה - "approved" | "declined" | "unknown"
                             # NOT a bool: "unknown" is a real third state, see Step 6
    gateway_used: str        # שער תשלום שנבחר
    transaction_id: str      # מזהה עסקה
    approval_number: str     # מספר אישור
    shva_reference: str      # מספר שב"א
    gateway_status_code: str # קוד סטטוס גולמי - keep the vendor's own code, not just
    raw_response: dict       # the normalised outcome, so a parked or mis-mapped
                             # transaction stays auditable afterwards
    installment_details: dict
```

**Normalize the money unit in the adapter, never in the caller.** The gateways disagree on what the amount field carries: Pelecard takes agorot (minor units), while Grow takes decimal shekels. The per-gateway skills (`pelecard-payment-gateway`, `grow-payment-gateway`) are the authority on each; PayMe and iCredit have no skill and no reachable public docs, so establish their unit with a one-shekel test charge before going live. Keep one canonical integer unit inside the orchestrator and convert in each gateway adapter. A shared `float` amount across adapters that disagree by a factor of one hundred is an error generator in both directions, and the mistake is silent until a customer complains.

### Step 4: Implement Gateway Routing
Define routing rules for selecting the optimal gateway:

| Rule | Priority | Logic | Example |
|------|----------|-------|---------|
| Reversal and settlement cost | Medium | Route on costs the merchant can actually know, from its own contracts | A charge that is likely to be cancelled goes to a gateway whose batch stays open longest, because a void clears nothing while a credit clears twice |
| Feature match | High | Route based on required features | Bit-eligible sales to a gateway whose terminal has Bit enabled |
| Availability | Critical | Route away from failed/degraded gateways | If Tranzila is down, failover to Cardcom |
| Volume balancing | Low | Distribute load across gateways | 60/40 split between primary and secondary |
| Card type | High | Some gateways handle specific cards better | Diners Club routing |

Routing logic:
```python
def select_gateway(request: PaymentRequest, gateways: list) -> str:
    # 1. Filter by feature support (tashlumim type, Bit, etc.)
    eligible = [g for g in gateways if g.supports(request)]
    # 2. Remove unhealthy gateways
    healthy = [g for g in eligible if g.is_healthy()]
    # 3. Sort by cost for this transaction type
    ranked = sorted(healthy, key=lambda g: g.priority_for(request))
    # Rank on merchant-configured priority, NOT on a fee table.
    # No Israeli gateway publishes rates, so a "cheapest gateway" sort
    # can only be built on invented numbers. See Step 2.
    # 4. Return best match (or raise if none available)
    if not ranked:
        raise NoGatewayAvailable()
    return ranked[0]
```

### Step 5: Handle Installments (Tashlumim)
The installment mode is carried in the **CreditType** field (`cred_type` on Tranzila's legacy surface), which is distinct from the transaction type (סוג עסקה).

**Only three CreditType values are published by any vendor.** Cardcom's own v11 API schema documents `CreditType` as "1 - Single payment / 6 - Credit payments / 8 - Regular payments", and Tranzila's current parameter table publishes exactly the same three ("1 - Credit card, 6 - Credit, 8 - installments").

| Type | Hebrew | CreditType | How It Works | Who Pays Interest |
|------|--------|-----------|--------------|-------------------|
| Single payment | תשלום אחד | 1 | One immediate charge | n/a |
| Credit installments | קרדיט | 6 | The card company finances; customer pays it in installments with interest | Customer pays interest to the issuer |
| Regular installments | תשלומים | 8 | Merchant is paid the full amount, issuer collects from the customer monthly | Customer, no interest by default |
| "Payments without interest" | תשלומים ללא ריבית | 8 | Same wire value as regular installments; the merchant absorbs the financing cost commercially | Merchant absorbs cost |

**Do not send 2, 3, 4, 5 or 9.** Earlier versions of this skill listed them as a "canonical enum" on the strength of a third-party integration library rather than a vendor document. They appear in no current vendor parameter table and Cardcom's schema contains none of them; Tranzila's own parameter table publishes only `1`, `6` and `8`, and its response-code table answers anything else with `017 Unauthorized credit type for this transaction`. In particular there is **no routable "club installments = 9"**: club and issuer-loyalty programmes are a terminal and issuer configuration, not a CreditType your code selects. If a merchant needs one, that is a conversation with the acquirer, not a field value.

Implementation notes:
- Installment ceilings are terminal and issuer configuration, not a gateway constant. Ask the acquirer for the ceiling on the specific terminal rather than hard-coding one.
- Issuer credit (CreditType 6) carries its own floor on the instalment count. Tranzila documents a minimum of 3 credit instalments and notes that the cardholder must hold credit authorization from their issuer, so a credit sale can fail for a reason that has nothing to do with the gateway. Per-instalment minimum AMOUNTS are issuer and terminal configuration; the per-gateway skills carry them, do not hard-code one here.
- "Interest-free instalments" is a commercial arrangement with the acquirer, not a wire value: the customer pays no interest because the merchant absorbs the financing cost. Do not quote a subsidy percentage, it is per merchant and is not published.
- API V2 surfaces may not use `cred_type` at all. Tranzila's, for instance, uses `payment_plan` plus `installments_number`. Decide which surface you are on before copying a parameter name across.

### Step 6: Implement Fallback and Retry Logic
Design resilient payment processing:

```python
# Fallback strategy
GATEWAY_PRIORITY = ["cardcom", "tranzila"]   # documented gateways only, see below

async def process_with_fallback(request: PaymentRequest) -> PaymentResult:
    last_error = None
    for gateway_name in GATEWAY_PRIORITY:
        gateway = get_gateway(gateway_name)
        if not gateway.is_healthy():
            continue  # דלג על שער לא זמין
        try:
            result = await gateway.charge(request)
            if result.outcome in ("approved", "declined"):
                return result       # both are settled answers, stop here
            # outcome == "unknown": the charge MAY have gone through.
            # Do not fail over. Park it for reconciliation.
            await park_for_reconciliation(request, gateway_name)
            raise OutcomeUnknown(gateway_name)
        except GatewayTimeoutError:
            # A timeout is NOT a failure. It is an unknown outcome.
            await park_for_reconciliation(request, gateway_name)
            raise OutcomeUnknown(gateway_name)
        except GatewayConnectFailed as e:
            # The request never reached the gateway, so nothing was charged.
            last_error = str(e)
            continue  # נסה שער הבא
    raise AllGatewaysFailedError(last_error)
```

Three rules, and the third is the one that costs money:

1. Never retry a **bank decline** (insufficient funds, stolen card) on a different gateway. The answer will not change and velocity checks will start flagging the card.
2. Retry only when the request **provably never reached the gateway** (DNS failure, connection refused, TLS failure).
3. **Never put an unverified gateway in a failover chain.** A gateway belongs in the priority list only once you have confirmed three things: what unit its amount field carries, which of its own fields carries your idempotency key, and how you reverse a charge on it. Fail over to a gateway whose money unit you have not confirmed and the fallback path itself becomes the factor-of-one-hundred bug.
4. **A timeout is not a failure.** It is a third outcome, and failing it over is the classic duplicate-charge bug. Pelecard makes the distinction explicit in its own status codes: `302` means "debit was successful but merchant is not responding", so money DID move; `301` and `303` leave the outcome genuinely unknown. Only `302` asserts a charge. An orchestrator that maps all three to "failed, try the next gateway" will double-charge every customer whose first attempt was slow. Park the transaction, resolve it against the gateway's own lookup, and only then decide.

**Parking is only half the job; design the reconciliation before you ship the retry.** `park_for_reconciliation` is not a stub you fill in later, it is what turns an unknown outcome back into money or goods. Three things have to exist before the first charge, not after the first incident:

- **A key you persisted BEFORE the call, that you can look the transaction up by afterwards.** The gateway's own transaction id does not exist yet at the moment the request times out, so it cannot be that key. Use a passthrough field you control. **Two different fields with two opposite rules live here, and mixing them up is the double charge itself.** A *correlator* identifies one attempt, so it is unique per attempt and reconciliation is a prefix match on the order id: Pelecard's `ParamX` works this way, as `<order-id>-<attempt-n>`. An *idempotency key* is what the gateway dedupes on, so it must be STABLE per logical charge and re-sent unchanged on every retry: Grow's `transactionUniqueIdentifier` works this way, and minting a fresh one per attempt defeats Grow's own duplicate detection. Check which of the two a given field is in the per-gateway skill before you generate it.
- **The same key on the retry.** On a timeout or a 5xx, re-sending with a FRESH idempotency key is how a customer gets billed twice. Re-send the same one, or reconcile first.
- **A per-gateway lookup, a polling window, and a terminal decision** (capture and ship, refund, or escalate to a human). `references/gateway-matrix.md` names the lookup call for each gateway. An unknown still unknown at the end of the window is an operations task, and someone has to own it. Those three messages are Pelecard's own wording, retrievable without credentials from `/services/GetErrorMessageEn` with parameter `errorCode`; an unassigned code comes back as Pelecard's misspelled `UnkownError`, which is how you tell a real code from an invented one. Build the equivalent three-state map for every gateway you route to, from that gateway's own code table, before you write any retry logic.

### Step 7: Handle Authorizations, Voids, Refunds and Partial Refunds

**An authorization is not a sale, and releasing one is not a refund.** Most of these gateways support a two-step flow: hold the amount now, collect it later (Pelecard `ActionType` `J5`, Tranzila `verify_mode=5` / `tranmode=V`, Cardcom `Operation: SuspendedDeal`). Two failures follow from ignoring it. An orchestrator that records an authorization as "approved" and never issues the capture never collects the money, and the hold expires quietly. And an orchestrator that releases a hold with its refund call is using the wrong operation: Tranzila releases a limit with `txn_type=reversal`, not `cancel`, and Pelecard releases one with `/services/DeleteIshur`, not `DeleteTran`. Carry `action` on the request (Step 3) and give the adapter a `capture()` and a `release()` alongside `void()` and `refund()`. `references/gateway-matrix.md` holds the per-gateway calls.

Reversing money that HAS been taken is the operation an orchestrator uniquely owns, and it is the one that differs most between gateways. There are two mechanically different actions, and picking the wrong one costs the merchant twice.

- A **void** (ביטול) cancels a transaction before it settles. It never reaches the clearing network, so it carries no clearing fee and the customer typically never sees a charge.
- A **refund / credit** (זיכוי) is a new, opposite transaction on an already-settled charge. It clears in its own right, so the merchant pays clearing on both legs.

The dividing line is settlement, and it arrives fast: on most terminals the batch closes the same business day. A router that optimizes on cost (Step 4) while ignoring this is optimizing half the ledger.

| Gateway | Void, before settlement | Refund / credit, after | Partial refund |
|---------|------------------------|------------------------|----------------|
| Cardcom | `Transactions/RefundByTransactionId` with `CancelOnly: true` ("cancellation only, before deposit of the transaction") | same endpoint without `CancelOnly` | Yes, `PartialSum`. `AllowMultipleRefunds` defaults to false |
| Tranzila | `txn_type=cancel` on API V2 | legacy `tranmode=C{index}` (needs the separate `CreditPass` credential); `txn_type=credit` on API V2 | Yes |
| PayMe | Unverified | `api/refund-sale` exists | Unverified |
| Meshulam (Grow) | No card void. Bit only: `cancelBitTransaction`, which requires `pageCode`; confirm its full parameter set in `grow-payment-gateway` | `refundTransaction`, amount field is `refundSum` and `sum` is rejected | Yes, but blocked once the transaction is settled or transmitted, and once funds are at the bank it needs manual approval. Grow signals each case with its own error code; see `grow-payment-gateway` |
| iCredit | Unverified | Unverified | Unverified |
| Pelecard | `/services/DeleteTran`, while the batch is still open. `/services/GetTransDataBeforeBc` shows what is still voidable | No refund endpoint exists on `/PaymentGW`. A credit is a new opposite transaction; do not guess its path | No. `DeleteTran` is whole-transaction only |

Three things to design for:

- **Never assume symmetry.** The refund call is not the charge call with a minus sign. On Pelecard specifically, sending a negative total is more likely to produce a second charge than a reversal.
- **Bit refunds are their own path** on every gateway that supports Bit, because Bit is an account-to-account push rather than a card authorization.
- **"Unverified" cells are real gaps in this table, not implied noes.** For PayMe and iCredit, confirm with the vendor before you build a reversal flow on top of an assumption.
- **Keep your own refunded-to-date ledger per transaction and refuse an over-refund before you call.** The gateways disagree on whether they stop you: Cardcom defaults `AllowMultipleRefunds` to false, while Grow accepts successive partials until the total exceeds the original. Relying on the gateway to catch it means one of the six will not.
- **A refund often needs a second credential the charge did not.** Tranzila's legacy credit path needs a separate `CreditPass` that has to be enabled on the terminal, and Cardcom's `RefundByTransactionId` requires `ApiPassword`, which its charge endpoints do not take at all. A reversal flow that was never tested end to end usually fails on exactly this.
- **Refunding an instalment sale is acquirer-specific and is not amount divided by count.** Whether the issuer stops collecting the remaining payments, and how the merchant's already-paid full amount is clawed back, differ by acquirer. Establish it before a refund flow goes live on a tashlumim deal.
- **The refund deadline is a legal one, not a gateway one**, and the duty is on ISSUING the refund rather than on the customer receiving it. Since a credit settles on the issuer's own cycle, a queued credit has to be monitored rather than fired and forgotten. `pelecard-payment-gateway` carries a sourced summary of the Consumer Protection Law distance-selling rules; treat it as a summary rather than the statute.

Run `python scripts/compare_gateways.py --refunds` to print this matrix.

### Step 8: Ensure Regulatory Compliance
Comply with Bank of Israel and Shva regulations:

| Regulation | Hebrew | Requirement | Impact |
|------------|--------|-------------|--------|
| Transaction data retention | שמירת נתוני עסקאות | Retain transaction records for the statutory period | The retention period is set by tax and bookkeeping law, not by the gateway or by PCI. Confirm the current period with the Tax Authority or the merchant's accountant before designing a purge policy; do not copy a number from an integration guide |
| PCI DSS | תקן PCI | Card data security | Use tokenization, never store full card numbers. Israeli acquirers may add local requirements on top of the international standard |
| Consumer Protection | הגנת הצרכן | Statutory cancellation rights on distance sales | The cancellation window, the refund deadline, any cap on a cancellation fee, and whether particular consumer groups get a longer window are all set by the Consumer Protection Law and its regulations, not by the gateway. This skill deliberately encodes none of them. Establish every one of them from the Consumer Protection Authority or from counsel before building a refund flow around them |
| Anti-fraud | מניעת הונאה | 3D Secure, velocity checks | Implement 3DS2 for CNP transactions |

## Examples

### Example 1: Multi-Gateway Setup
User says: "I need to accept payments with installments, with fallback if one gateway goes down"
Actions:
1. Assess: instalments (regular and credit) plus high availability.
2. Compare: `python scripts/compare_gateways.py --features installments,recurring`. Pick two gateways whose cells are documented rather than unverified.
3. Design: one canonical amount unit, one idempotency key mapped onto each gateway's own field, and a three-state outcome.
4. Implement: route instalment sales to the primary, fail over only on a provable connect failure.
Result: Orchestration layer with primary/fallback routing and instalment handling

### Example 2: Adding Bit
User says: "We use Tranzila but want to add PayMe so we can accept Bit"
Actions:
1. Challenge the premise first. Tranzila already supports Bit, through a dedicated Bit API and a `bit_pay=1` flag on the iframe. So does Cardcom (`UrlToBit`), Grow and Pelecard. Adding a whole second gateway to obtain a feature the current one has is a large integration for nothing.
2. Check the terminal, not the gateway. Bit has to be enabled on the merchant's terminal by the acquirer. "The API supports it" and "your terminal is provisioned for it" are different questions, and the second is the one that blocks.
3. Establish Bit's own constraints before routing to it, from the acquirer and from the per-gateway skill rather than from this table. Bit is an account-to-account push, so the constraints that apply to it are not the card constraints: expect limits on instalments, on currency, and on transaction and monthly amounts, and expect its reversal path to differ from the card one. Get the actual numbers for the merchant's own terminal. A router that treats Bit as a boolean will send a sale Bit cannot carry and fail at the worst moment.
4. Only if the terminal genuinely cannot be provisioned does a second gateway become the answer, and then it is a commercial decision, not a technical one.
Result: In most cases, one enablement call instead of a second integration

### Example 3: Cost Comparison
User says: "Which gateway is cheapest for our 500 daily transactions averaging 200 NIS?"
Actions:
1. Say plainly that no one can answer this from public information. None of the six publishes a rate card, and the rate is negotiated per merchant on volume, industry and chargeback profile. Any table that names a winner is inventing the inputs.
2. Give them what actually decides it: the monthly volume to negotiate with, here 500 * 30 * 200 = 3,000,000 NIS, and the instruction to get a written quote from each gateway at that volume.
3. Name the costs the discount rate hides, which routinely dominate at this size: merchant-subsidized interest-free instalments, the settlement cycle's working-capital cost, per-refund and chargeback charges, and the fact that a charge-then-credit pair clears twice while a void clears never.
4. Compare on capability where capability is knowable: `python scripts/compare_gateways.py --example`.
Result: A negotiating position and a capability comparison, not a false ranking

## Bundled Resources

### Scripts
- `scripts/compare_gateways.py` -- Prints a capability matrix of the six gateways and a void/refund/partial-refund matrix. Filters on documented features and refuses an unrecognised feature name rather than silently matching everything. It deliberately does no cost estimation. Run: `python scripts/compare_gateways.py --help`, `--example`, `--refunds`, `--features bit`

### References
- `references/gateway-matrix.md` -- Cross-gateway comparison: API formats and base URLs, auth schemes, installment support, Bit and wallet support, amount units, the authorize / capture / release calls, the void / refund / partial-refund matrix, the per-gateway transaction-lookup used for reconciliation, and the Pelecard status codes that decide whether money moved. It deliberately carries no fee table. Consult when evaluating or switching gateways.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Cardcom v11 API schema | https://secure.cardcom.solutions/swagger/v11/swagger.json | The authoritative field list: `CreditType` values, `UrlToBit`, and the `RefundByTransactionId` request with `PartialSum` and `CancelOnly` |
| Tranzila Documentation | https://docs.tranzila.com/ | Which of the four surfaces you are on, the published `cred_type` values, and the API V2 four-header HMAC auth |
| PayMe | https://payme.io/ | PayMe publishes no openly reachable developer-docs URL (`payme.io/developers` 301s to the homepage and `docs.paymeservice.com` answers a Cloudflare 1014). Request the API reference from PayMe directly, and confirm the money unit and the refund parameter names with them before the first charge |
| Meshulam (Grow) Reference | https://developers.grow.business/reference/overview | Production base = secure.meshulam.co.il, `refundSum` on refunds, and the error codes that gate partial refunds |
| Rivhit (iCredit) | https://www.rivhit.co.il/ | iCredit is a Rivhit product. Its API is a WCF `.svc` service; the refund surface is not publicly documented |
| Pelecard services index | https://gateway21.pelecard.biz/services | The live endpoint list, including `DeleteTran` and `GetTransDataBeforeBc`. `gateway20` and `gateway21` are generations, not environments |
| Bank of Israel: Payment Systems Oversight | https://www.boi.org.il/en/economic-roles/supervision-and-regulation/payment-systems-oversight/ | Which systems are "controlled payment systems" and therefore inside the BOI's oversight perimeter, plus the oversight directives and the access requirements for connecting to a payment system. Note that this page does not settle who supervises a non-bank payment-service provider; establish that with the regulator directly rather than assuming it from here |

## Gotchas
- **HTTP 200 does not mean the payment succeeded, on any of these gateways.** Tranzila states it outright at the top of its response-code table: those are application error codes, and the response code will be success (200). Grow returns 200 with `status: "0"` and an `err` object. Pelecard's `init` returns 200 with `Error.ErrCode`. Tranzila's legacy CGI returns 200 with an HTML alert page rather than JSON at all. Normalizing this is the orchestrator's job and it is the single most common way an agent-written integration reports a failed charge as paid. Parse the body, never the status.
- Each Israeli payment gateway in this skill (Cardcom, Tranzila, PayMe, Meshulam, iCredit, Pelecard) has a completely different API format: Cardcom uses JSON, Tranzila uses form-encoded key-value pairs on its legacy surface and JSON on API V2, Meshulam uses multipart/form-data with a separate page-code parameter, and iCredit is a WCF `.svc` service. Agents may apply one gateway's format to another.
- **A hostname is not an environment switch.** On Pelecard, `gateway20` and `gateway21` are gateway generations and return byte-identical responses; what decides whether a call is a test or a real charge is the terminal number and credentials. An agent that "switches to the sandbox host" and then runs test data will put real charges through.
- **An idempotency key needs a vendor field behind it.** Every gateway has its own duplicate-detection mechanism and its own duplicate error code. A key that your orchestrator generates but never maps onto the gateway's own field is decoration: the gateway will happily accept the same charge twice. On Grow the duplicate-detection field is `transactionUniqueIdentifier`, which must stay stable across retries of the same logical charge; on Pelecard the passthrough `ParamX` is a per-attempt correlator rather than a dedupe key, and dedupe happens on the returned transaction id instead. The two are not interchangeable. For the others, look the field and the duplicate code up in the per-gateway skill before relying on retry safety.
- Israeli payment processing requires Israeli business registration (osek murshe/patur). Agents may suggest setting up payment processing before verifying the business has proper registration with the Tax Authority.
- Bit (Israel's dominant mobile payment) refunds use a different API endpoint than credit card refunds on most gateways. Agents may use the credit card refund endpoint for Bit transactions.
- **Saved-card tokens are NOT portable across gateways.** A Cardcom token, a Tranzila `TranzilaTK`, and a PayMe `buyer_key` are proprietary and mutually incompatible, each usable only on the gateway that issued it. This means the fallback/failover pattern in this skill applies to first-charge and one-time transactions only. A tokenized or recurring charge cannot fail over to a second gateway, recurring billing is pinned to its originating gateway. True cross-gateway resilience for saved cards requires network tokenization or a multi-vault strategy, not this token field. Agents may wrongly assume a stored token works on any gateway in the priority list.
- **A gateway's client-side "success" is spoofable, always re-verify server-side.** Do not trust the browser redirect or a client-posted status as proof of payment. Confirm every transaction with a server-to-server query to the issuing gateway (for Meshulam/Grow, `getPaymentProcessInfo`/approve; for others, the gateway's transaction-lookup or webhook-signature/notify verification) before fulfilling the order. Webhook/IPN payloads must be authenticated per each gateway's scheme, they are not interchangeable.
- **3DS2 is an asynchronous challenge flow, not a single call.** A card-not-present charge may return "frictionless" (approved inline) or trigger a challenge that redirects the customer to the issuer and returns via a callback URL. The orchestrator must persist the transaction, resume on the callback, and keep the challenge return on the SAME gateway that started it (the 3DS session is gateway-scoped). Agents may model 3DS as a synchronous boolean and lose challenged transactions.

## Troubleshooting

### Error: "Installment type not supported" / Tranzila `017`
Cause: Most often the CreditType value itself, not the gateway. Only `1`, `6` and `8` are published by any vendor; `2`, `3`, `4`, `5` and `9` circulate in third-party libraries but appear in no current vendor parameter table, and Tranzila answers them with `017 Unauthorized credit type for this transaction`.
Solution: Send `8` for regular installments or `6` for issuer-financed credit. If the merchant genuinely needs a club or loyalty programme, that is a terminal and acquirer configuration rather than a field value, so route the request to the acquirer rather than retrying with another number. Verified negative: switching gateways does not fix a rejected CreditType, because the value is rejected upstream of the gateway.

### Error: "Gateway timeout on fallback"
Cause: Either every configured gateway is degraded, or, far more often, one gateway timed out and the orchestrator treated that as a failure and moved on.
Solution: Separate the two. A timeout leaves the outcome unknown and must be parked for reconciliation, not failed over (Step 6). Only a provable connect failure justifies moving to the next gateway. Once that distinction is in place, add a circuit breaker with health checks and alert on degradation.

### Error: "Duplicate transaction detected"
Cause: Retry logic sent the same payment twice, usually after treating a timeout as a failure.
Solution: Map your idempotency key onto the gateway's own duplicate-detection field, and treat a timeout as an unknown outcome rather than a failure (Step 6). Look the transaction up before retrying anything. Never retry a bank decline.

### Error: A refund call returns success but the customer says the money never came back
Cause: Likeliest cause, not confirmed for every gateway: the credit was queued rather than completed, or it was a void on an already-settled transaction. Verified negative: on Pelecard this is NOT a `/PaymentGW` refund endpoint failing, because no such endpoint exists.
Solution: Establish which side of settlement the original transaction is on before choosing the call (Step 7), and reconcile against the gateway's own transaction lookup rather than the reversal call's own response.