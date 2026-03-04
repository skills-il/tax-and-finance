---
name: israeli-payment-orchestrator
description: >-
  Orchestrate Israeli payment gateways (Cardcom, Tranzila, PayMe, Meshulam,
  iCredit, Pelecard) with unified routing, fallback, and installments
  (tashlumim). Use when user asks about multi-gateway payment integration,
  "slikat kartisim", "tashlumim", payment routing, Shva network, BOI Directive
  357, gateway comparison, or building a payment abstraction layer for Israeli
  merchants. Provides unified API patterns, installment handling, Shva clearing
  rules, and regulatory compliance. Do NOT use for single gateway setup (use
  cardcom-payment-gateway or tranzila-payment-gateway instead).
license: MIT
compatibility: >-
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
  Python 3.8+ for helper scripts.
metadata:
  author: skills-il
  version: 1.0.0
  category: tax-and-finance
  tags:
    he:
      - תשלומים
      - סליקה
      - שב"א
      - כרטיסי-אשראי
      - תשלומים
      - ישראל
    en:
      - payments
      - gateway
      - shva
      - credit-cards
      - installments
      - israel
  display_name:
    he: תזמור תשלומים ישראלי
    en: Israeli Payment Orchestrator
  display_description:
    he: >-
      תזמור שערי תשלום ישראליים (Cardcom, Tranzila, PayMe, Meshulam, iCredit,
      Pelecard) עם ניתוב אחיד, fallback ותשלומים. כולל השוואת שערים, טיפול
      בתשלומים ועמידה בהנחיות בנק ישראל.
    en: >-
      Orchestrate Israeli payment gateways (Cardcom, Tranzila, PayMe, Meshulam,
      iCredit, Pelecard) with unified routing, fallback, and installments
      (tashlumim). Use when user asks about multi-gateway payment integration,
      "slikat kartisim", "tashlumim", payment routing, Shva network, BOI
      Directive 357, gateway comparison, or building a payment abstraction layer
      for Israeli merchants. Provides unified API patterns, installment handling,
      Shva clearing rules, and regulatory compliance. Do NOT use for single
      gateway setup (use cardcom-payment-gateway or tranzila-payment-gateway
      instead).
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Payment Orchestrator

## Instructions

### Step 1: Assess Payment Requirements
Ask the user about their payment needs:

| Requirement | Hebrew | Description | Impact on Gateway Choice |
|-------------|--------|-------------|-------------------------|
| Installments (tashlumim) | תשלומים | Split payment into monthly installments | Not all gateways support all installment types |
| Recurring billing | חיוב חוזר | Subscription / standing order | Requires token storage and Shva approval |
| Multi-currency | רב-מטבעי | Accept NIS + foreign currencies | Limited gateway support for dual currency |
| Iframe / redirect | דף סליקה | Hosted payment page vs embedded | Affects PCI scope |
| Bit / Apple Pay | ביט / אפל פיי | Alternative payment methods | Gateway-specific integrations |
| High volume | נפח גבוה | Over 1,000 transactions/day | Need SLA guarantees and fallback |

### Step 2: Compare Gateways
Use `scripts/compare_gateways.py` to generate a comparison matrix, or reference the table below:

| Gateway | API Style | Installments | Recurring | Hosted Page | Bit Support | Typical Fee |
|---------|-----------|-------------|-----------|-------------|-------------|-------------|
| Cardcom | REST JSON | Full (regular, credit, club) | Yes | Yes (iframe) | No | 0.6-0.8% |
| Tranzila | REST/Form POST | Regular, credit | Yes | Yes (redirect) | No | 0.5-0.7% |
| PayMe | REST JSON | Regular, credit | Yes | Yes (iframe) | Yes | 0.7-1.0% |
| Meshulam | REST JSON | Regular | Yes | Yes (iframe + redirect) | Yes | 0.6-0.9% |
| iCredit | REST JSON | Regular, credit | Yes | Yes (redirect) | No | 0.5-0.8% |
| Pelecard | REST JSON | Regular, credit, club | Yes | Yes (iframe) | No | 0.5-0.7% |

Fee notes: Rates are indicative. Actual rates depend on business volume, industry, and negotiation.

### Step 3: Design the Orchestration Layer
Build a unified payment abstraction:

```python
# Unified payment interface pattern
class PaymentRequest:
    amount: float            # סכום - in agorot (NIS cents)
    currency: str            # מטבע - "ILS" default
    installments: int        # תשלומים - 1 = regular, 2-36 = installments
    installment_type: str    # סוג תשלומים - "regular", "credit", "club"
    card_token: str          # טוקן כרטיס - for recurring
    description: str         # תיאור עסקה
    customer_id: str         # מזהה לקוח
    idempotency_key: str     # מפתח אידמפוטנטי - prevent duplicates

class PaymentResult:
    success: bool
    gateway_used: str        # שער תשלום שנבחר
    transaction_id: str      # מזהה עסקה
    approval_number: str     # מספר אישור
    shva_reference: str      # מספר שב"א
    installment_details: dict
```

### Step 4: Implement Gateway Routing
Define routing rules for selecting the optimal gateway:

| Rule | Priority | Logic | Example |
|------|----------|-------|---------|
| Cost optimization | Medium | Route to cheapest gateway for transaction type | Small payments to lowest-fee gateway |
| Feature match | High | Route based on required features | Club installments only to Cardcom/Pelecard |
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
    ranked = sorted(healthy, key=lambda g: g.fee_for(request))
    # 4. Return best match (or raise if none available)
    return ranked[0] if ranked else raise NoGatewayAvailable()
```

### Step 5: Handle Installments (Tashlumim)
Israeli installment types have specific Shva network rules:

| Type | Hebrew | Shva Code | How It Works | Who Pays Interest |
|------|--------|-----------|--------------|-------------------|
| Regular installments | תשלומים רגילים | 8 | Merchant gets full amount upfront, bank collects from customer monthly | Customer (no interest by default) |
| Credit installments | קרדיט | 2 | Customer pays bank in installments with interest, merchant gets full amount | Customer pays interest to bank |
| Club installments | מועדון | 3 | Issuer-specific program (Isracard, CAL, Max) | Varies by program |
| "Payments without interest" | תשלומים ללא ריבית | 8 | Merchant subsidizes interest cost | Merchant absorbs cost |

Implementation notes:
- Maximum installments: typically 36, some gateways limit to 12 or 24
- Minimum per-installment: Shva may enforce minimum amounts per installment
- Installment approval: some installment counts require issuer pre-approval

### Step 6: Implement Fallback and Retry Logic
Design resilient payment processing:

```python
# Fallback strategy
GATEWAY_PRIORITY = ["cardcom", "tranzila", "payme"]

async def process_with_fallback(request: PaymentRequest) -> PaymentResult:
    last_error = None
    for gateway_name in GATEWAY_PRIORITY:
        gateway = get_gateway(gateway_name)
        if not gateway.is_healthy():
            continue  # דלג על שער לא זמין
        try:
            result = await gateway.charge(request)
            if result.success:
                return result
            # Declined by bank -- do NOT retry with another gateway
            if result.is_bank_decline():
                return result
        except GatewayTimeoutError:
            last_error = f"{gateway_name} timeout"
            continue  # נסה שער הבא
        except GatewayError as e:
            last_error = str(e)
            continue
    raise AllGatewaysFailedError(last_error)
```

Important: Never retry a **bank decline** (customer insufficient funds, stolen card, etc.) with a different gateway. Only retry on **gateway technical errors**.

### Step 7: Ensure Regulatory Compliance
Comply with Bank of Israel and Shva regulations:

| Regulation | Hebrew | Requirement | Impact |
|------------|--------|-------------|--------|
| BOI Directive 357 | הוראה 357 | Transaction data retention, reporting | Store all transaction details 7 years |
| PCI DSS | תקן PCI | Card data security | Use tokenization, never store full card numbers |
| Shva regulations | תקנות שב"א | Clearing and settlement rules | Adhere to clearing windows and dispute timelines |
| Consumer Protection | הגנת הצרכן | Refund rights, clear pricing | Display installment terms clearly |
| Anti-fraud | מניעת הונאה | 3D Secure, velocity checks | Implement 3DS2 for CNP transactions |

## Examples

### Example 1: Multi-Gateway Setup
User says: "I need to accept payments with installments, with fallback if one gateway goes down"
Actions:
1. Assess: Need installments (regular + credit) and high availability
2. Compare: Cardcom (primary, full installment support) + Tranzila (fallback)
3. Design: Unified PaymentRequest with installment_type field
4. Implement: Route installment payments to Cardcom, failover to Tranzila
5. Run `python scripts/compare_gateways.py --features installments,recurring`
Result: Orchestration layer with primary/fallback routing and installment handling

### Example 2: Gateway Migration
User says: "We use Tranzila but want to add PayMe for Bit payments"
Actions:
1. Assess: Current Tranzila setup + need Bit support
2. Design: Add PayMe as secondary gateway for Bit-eligible transactions
3. Route: Bit payments to PayMe, card payments to Tranzila
4. Implement: Unified response mapping between both gateway formats
Result: Dual-gateway setup with feature-based routing

### Example 3: Cost Optimization
User says: "Which gateway is cheapest for our 500 daily transactions averaging 200 NIS?"
Actions:
1. Calculate: Monthly volume = 500 * 30 * 200 = 3,000,000 NIS
2. Compare: Run `python scripts/compare_gateways.py --volume 500 --avg-amount 200`
3. Factor: Installment mix, chargeback rates, settlement timing
4. Recommend: Based on total cost of ownership including integration effort
Result: Cost comparison with recommendation based on business profile

### Example 4: Installment Configuration
User says: "Customer wants to pay 5,000 NIS in 10 interest-free installments"
Actions:
1. Identify: Regular installments (tashlumim regilim), 10 payments of 500 NIS
2. Check: Gateway support for 10 installments (all major gateways support this)
3. Note: Merchant absorbs interest cost for "interest-free" installments
4. Calculate: Merchant cost = typically 1-3% of transaction for interest subsidy
5. Implement: Set installments=10, installment_type="regular" in PaymentRequest
Result: Installment payment configured with cost breakdown for merchant

## Bundled Resources

### Scripts
- `scripts/compare_gateways.py` -- Generates comparison matrix of Israeli payment gateways based on features, fees, and volume. Run: `python scripts/compare_gateways.py --help`

### References
- `references/gateway-matrix.md` -- Detailed feature comparison of Israeli payment gateways: API formats, installment support, recurring billing, hosted pages, settlement timelines, and fee structures. Consult when evaluating or switching gateways.

## Troubleshooting

### Error: "Installment type not supported"
Cause: Requested installment type (credit/club) not available on selected gateway
Solution: Check gateway capabilities in Step 2 table. Club installments only available on Cardcom and Pelecard. Route to appropriate gateway.

### Error: "Shva clearing rejected"
Cause: Transaction violates Shva network rules (invalid installment count, amount below minimum)
Solution: Verify installment count is within allowed range. Check minimum per-installment amount. Ensure transaction currency is ILS for domestic cards.

### Error: "Gateway timeout on fallback"
Cause: All configured gateways are experiencing issues
Solution: Implement circuit breaker pattern with health checks. Consider adding a third gateway. Monitor gateway status endpoints and alert on degradation.

### Error: "Duplicate transaction detected"
Cause: Retry logic sent same payment to multiple gateways
Solution: Always use idempotency keys. Check transaction status before retrying. Never retry bank declines -- only retry gateway technical errors.
