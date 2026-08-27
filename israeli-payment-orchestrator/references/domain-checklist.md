# Domain Checklist: israeli-payment-orchestrator

Scope: design a multi-gateway payment abstraction for Israeli merchants (routing, fallback, installments, reversals, compliance). Category: tax-and-finance (payments/architecture).

## Must cover (core)

- The 6 gateways with CORRECT API styles: Cardcom REST JSON, Tranzila form-encoded CGI plus REST JSON on API V2, PayMe REST JSON, Meshulam/Grow multipart/form-data, iCredit WCF `.svc`, Pelecard REST JSON. Source: each vendor's own docs, and the per-gateway sibling skills.
- CORRECT Bit support per gateway. Cardcom's v11 schema returns `UrlToBit`; Tranzila has a dedicated Bit API and `bit_pay=1`; Grow and Pelecard both document Bit. iCredit is unverified. Source: `secure.cardcom.solutions/swagger/v11/swagger.json`, sibling skills.
- CreditType values limited to what a vendor publishes: `1`, `6`, `8`. Source: Cardcom v11 schema (`SdkTransactionInfo.CreditType`), Tranzila's iframe parameter table. Values 2/3/4/5/9 must be explicitly warned against, since Tranzila answers them with an unauthorized-credit-type error.
- **Money-unit normalization per gateway.** Pelecard takes agorot, Grow takes decimal shekels. An orchestrator sharing one amount field across adapters that disagree by a factor of one hundred is a direct financial-damage path. Source: sibling skills.
- **A capability cell must carry its own warrant.** Every yes/no in the capability and refund matrices must be traceable to a vendor document, a live probe with a negative control, or a named sibling skill. Where none exists the cell reads 'unverified', which is NOT a soft no. This rule was added 2026-08-27 after an Independent Judge found the PayMe and iCredit rows filled with confident positives on the two gateways the skill itself declares undocumented.
- **HTTP 200 does not mean success.** Grow returns 200 with `status:"0"`; Pelecard `init` returns 200 with `Error.ErrCode`; Tranzila legacy returns 200 with HTML. Normalizing this is the orchestrator's defining job.
- **The three-state outcome.** approved / declined / unknown. A timeout is unknown, not failed. Pelecard's own credential-free lookup (`/services/GetErrorMessageEn`, parameter `errorCode`) gives `302` as 'Debit was successful but merchant is not responding', `301` as 'Session to Pelecard Timed Out' and `303` as 'Merchant is not responding', so only `302` asserts that money moved. Failing an unknown over to a second gateway double-charges. Every gateway needs its own three-state map built from its own code table.
- Unified PaymentRequest/Result abstraction; idempotency keys mapped onto each gateway's own duplicate-detection field, not free-floating.
- Gateway routing (feature-match, availability/failover) and the never-retry-a-bank-decline rule.
- **Void vs refund vs partial refund, per gateway, with the settlement boundary that selects between them.** A void carries no clearing fee; a credit clears in its own right and is paid for twice. Cardcom `CancelOnly`/`PartialSum`, Grow `refundSum` with its own settled/transmitted error codes, Pelecard `DeleteTran` with no `/PaymentGW` refund endpoint at all. PayMe and iCredit are unverified and must be labelled so.
- Vault tokens are not portable across gateways, so failover applies to first-charge only.
- Regulatory compliance: the Bank of Israel regulates, assesses and audits the controlled payment systems; PCI DSS tokenization; 3DS2 for card-not-present. Who supervises a non-bank payment-service provider is NOT settled by the BOI oversight page (checked 2026-08-27: the page contains no mention of the securities regulator or of a 2023 payment-services law), so it must be established with the regulator directly and must not be asserted in the skill from that source.

## Should cover (advanced)

- Bit's own constraints as routing inputs (single payment, ILS only, ceilings, separate refund path), not a boolean.
- Circuit-breaker and health checks; cross-gateway reconciliation of parked unknown-outcome transactions.
- Consumer Protection Law cancellation rights on distance sales, pointing at the regulator for the current window and fee cap rather than encoding a number.

## Out of scope (explicit)

- **Single-gateway setup.** Re-litigated 2026-08-27: still out of scope, and now enforced positively rather than by silence. The per-gateway skills are named in the body as the authority for field names, error codes and endpoint paths, so a user who asks a single-gateway question is routed rather than answered thinly. Would an ordinary user ask? Yes, constantly, which is why the routing pointer is now explicit.
- **Fee bands and cost ranking.** Re-litigated 2026-08-27, and this cycle REVERSED the prior position. Earlier versions carried a per-gateway fee table and a cost-estimating script; both have been removed. No gateway publishes a rate card, the rate is contractual per merchant, and the bands this skill printed were traceable to no vendor at all. Applying the "never route to the source a number you could capture" rule the other way: this number cannot be captured, so publishing one was the error. The skill now names the situation and sends the user to each gateway.
- **PayMe and iCredit endpoint-level detail.** These two have no dedicated sibling skill and no publicly documented API surface comparable to the other four. Would an ordinary user ask? Yes. The answer is therefore an explicit "unverified, confirm with the vendor before building on it", never a guessed field name and never an implied "not supported".

## Authoritative sources

- Cardcom v11 OpenAPI schema: https://secure.cardcom.solutions/swagger/v11/swagger.json (CreditType, UrlToBit, RefundByTransactionId)
- Tranzila developer guide: https://docs.tranzila.com/ (the cred_type table and the 017 response code are on /docs/payments-and-billing/iframe-integration-directng and /docs/payments-and-billing/transaction-response-codes)
- Grow (Meshulam) Light API reference: https://developers.grow.business/reference/overview
- Pelecard services index: https://gateway21.pelecard.biz/services
- PayMe: https://payme.io/products/ (payme.io/developers 301s to the homepage and docs.paymeservice.com answers a Cloudflare 1014, so there is no reachable developer-docs page; request the reference from PayMe)
- Rivhit (iCredit): https://www.rivhit.co.il/
- Bank of Israel payment-systems oversight: https://www.boi.org.il/en/economic-roles/supervision-and-regulation/payment-systems-oversight/
- Sibling skills in this repo: cardcom-payment-gateway, tranzila-payment-gateway, grow-payment-gateway, pelecard-payment-gateway
