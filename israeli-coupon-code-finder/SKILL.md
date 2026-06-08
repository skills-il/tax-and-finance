---
name: israeli-coupon-code-finder
description: "Hunt for currently-valid discount and coupon codes for an Israeli online-store checkout, verify each candidate, and return one ranked summary instead of asking five chatbots the same question. Runs a fixed Israeli source map (coupon aggregators, cashback platforms, credit-card benefit hubs, gift-card stacking, store-direct levers, seasonal sale windows) plus a Hebrew search playbook, then checks every candidate for expiry, minimum cart, new-customer-only, and stacking rules. Use when a user is about to buy on an Israeli store and asks to find coupon codes, a discount code, kod kupon, kupon hanacha, or 'is this coupon site legit'. Never invents codes: it only reports codes found via live web search, each with source and date. Do NOT use for ongoing savings strategy or cashback-account setup (israeli-smart-saver), cross-store price comparison (israeli-product-price-comparator), or grocery prices (israeli-grocery-price-intelligence)."
license: MIT
compatibility: "Needs a live web-search tool to find real codes. With no web access it returns the source map and search playbook only, and says so. If a read-only browser tool is available, it can confirm the top code on the store's own page (never to enter payment details or place an order). Works with Claude Code, Claude.ai, Cursor, ChatGPT, Gemini."
---

# Israeli Coupon Code Finder

## Problem

Before buying online, many Israelis open Gemini, Claude, ChatGPT, Perplexity, and Grok and type the same "find me a coupon for this store" request into each, then try the results one by one at checkout. It is slow, the answers are inconsistent, and the codes are often expired, fake, or scraped from a scam site that just wants the shopper's card details. This skill makes ONE agent do the hunt properly: it knows where Israeli codes actually live, searches them in one pass, verifies each candidate, and hands back a single ranked summary the shopper can trust.

## Instructions

This is a methodology skill. The coupon codes themselves are NOT stored here, they change daily. The skill supplies the source map, the search playbook, the verification rubric, and the output format. The actual codes come from the agent's live web search each run.

### Step 0: Anti-fabrication rules (CRITICAL, read first)

These are hard rules. Breaking them produces real harm (a shopper types a fake code, or trusts a scam site).

- NEVER invent, guess, or "reconstruct" a coupon code. A code may only appear in the output if it was found in a real web-search result THIS run.
- Every code in the output MUST carry its source link and the date it was seen.
- If no web-search tool is available, or the search returns nothing usable, say so plainly and hand back the source map and store-direct levers instead. Do NOT fill the gap with plausible-looking codes.
- Codes expire fast. Always close with a "verify at checkout" note. A code that is not honored at checkout is not a discount.
- If asked to evaluate a coupon site, apply the scam red-flags rubric below before recommending it.

### Step 1: Pin the checkout context

Ask for, or infer from the request: the store (and its country site), the cart value range, the product category, and whether the shopper is a new or returning customer. New-customer-only codes are the most common false positive, so the customer status matters. If the store is a global one shipping to Israel, note that customs/VAT and shipping can erase a coupon's value, weigh that before celebrating a code.

### Step 2: Run the Israeli source map in one pass

Search these source types together, not one chatbot at a time. This is the whole point of the skill.

| Source type | What to look for | Verified examples to search |
|-------------|-----------------|------------------------------|
| Coupon aggregators | Per-store code pages, "secret" codes, current deals | Couponim (couponim.co.il), and other Hebrew "קופונים" sites surfaced by the search |
| Cashback platforms | A rebate that stacks on top of (or instead of) a code. The shopper must enter the store THROUGH the platform's tracked link before checkout, or the rebate never registers | Cashback.co.il |
| Loyalty points and store credit | An accumulated points wallet, store credit, or a welcome credit at the store often beats any public code. For the exact store named (e.g. Terminal X), check the shopper's own account first | The store's own account and app |
| Credit-card benefit hubs | A cardholder discount at this store that beats any public code. The issuer layer is fragmented, so check the shopper's own card | Max benefits hub (max.co.il/benefits), Isracard, and the equivalent program from the shopper's own issuer |
| Gift-card stacking | A discounted gift card you buy then pay with | BuyMe (buyme.co.il) |
| Consumer / employee clubs | Member pricing the shopper may already be entitled to | Moadon Chaver (hvr.co.il) for career soldiers and retirees; any ovdim (works-council) benefit portal |
| Store-direct levers | First-order newsletter/SMS/WhatsApp-join code, app-only code, abandoned-cart email, loyalty-club price, student or chayal (soldier) pricing | The store's own site and app |
| Telegram coupon channels | Rotating codes posted by deal channels | Search live; do NOT assume a specific channel exists |

### Step 3: Hebrew search playbook

Israeli codes are indexed under Hebrew queries. Search both languages. Use templates like these (swap in the store name):

```
קוד קופון <חנות> <שנה>
קופון <חנות> הנחה
<חנות> מבצעים קוד הנחה
<store-name> coupon code israel
<store-name> promo code
```

Also search for the seasonal window if one is near: בלאק פריידי (Black Friday), סייבר מאנדיי, יום הרווקים (Singles Day), סוף עונה / סייל סוף עונה, and the holiday sales (מבצעי החגים). Timing a purchase to a real sale window often beats any single code.

### Step 4: Verify every candidate before it reaches the output

For each code the search surfaces, check and record:

- Expiry date (drop anything visibly expired).
- Minimum-cart threshold (does the shopper's cart clear it?).
- New-customer-only / first-order-only flag.
- Category or brand exclusions.
- Single-use vs reusable, and whether it stacks with sale items. Treat non-stacking as the default: most codes are void on already-discounted items and will not combine with a club price.
- Source freshness: a code posted this week beats one with no date.
- If the host has a browser tool, confirm the top candidate on the store's OWN offers or sales page (read-only) before presenting it. The store's own page is the source of truth and beats an aggregator: the official code often differs from the one aggregators push. NEVER use the browser to enter payment or personal details, apply the code at a real checkout, or place an order, that stays with the shopper.

Mark confidence High / Medium / Low based on how recent and well-sourced the code is. A code confirmed on the store's own page is High; a code with no date and no terms is Low at best.

### Step 5: Return ONE ranked summary

Hand back a single table, best candidate first, plus a "try this first" pick and the verify-at-checkout reminder. Use this shape:

| Code | Source (link) | Date seen | Discount | Conditions | Confidence |
|------|---------------|-----------|----------|-----------|------------|
| (real code from search) | (link) | (date) | (value) | (min cart, new-customer, exclusions) | High/Med/Low |

If a cashback rebate, a credit-card benefit, or a discounted gift card would beat the best code, say so in one line below the table. If nothing valid was found, say that honestly and list the store-direct levers (newsletter signup, app, loyalty club) to try instead.

### Step 6: Scam-site red flags (apply before trusting any coupon site)

Warn the shopper if a coupon site shows any of these:

- Asks for credit-card or ID details before showing a code.
- "Complete a survey" or "install our extension" to unlock a code (broad-permission extensions harvest data). A legitimate cashback platform is different: it tracks your click or runs its own extension, but it never makes you fill a survey or enter card details to "unlock" a code.
- Codes that consistently fail at checkout (the site farms clicks, not savings).
- Lookalike / typosquat domains imitating a real store.
- No business identification details at all (a real Israeli seller must disclose who they are).
- Pressure countdown timers manufacturing false urgency.

### Step 7: Know the shopper's legal backstop

Under Israel's Consumer Protection Law, an online (remote) purchase can be cancelled within 14 days of receiving the product or the transaction-details document. When the cancellation is not due to a defect, the fee is capped at 5% of the price paid or 100 NIS, whichever is lower. When the cancellation IS due to a defect, or to a mismatch between the product and what the seller described, the business may not charge any cancellation fee. People with disabilities, shoppers aged 65 or older, and new immigrants get an extended window of 4 months, but this extension applies when the transaction included a conversation (by phone, chat, or email) with a business representative, and the seller may ask for proof of eligibility. This is the real safety net: a shopper who is pushed into a bad purchase by a fake "today only" coupon can usually still cancel. A "discount" is also only honest if measured against the genuine recent price, treat an inflated "original price" next to a big percentage as a red flag, not a deal.

## Examples

### Example 1: Find a code for a specific checkout
User says: "I'm about to check out on Terminal X, find me a working coupon."
Actions:
1. Pin context: Terminal X, fashion, ask cart value and new/returning.
2. Run the source map: search Couponim and other Hebrew aggregators for Terminal X codes, plus the store's own newsletter/app levers and any near seasonal window.
3. Verify each hit (expiry, min cart, new-customer-only).
4. Return one ranked table, note if a credit-card benefit beats the code, end with verify-at-checkout.

### Example 2: Electronics, compare the lever
User says: "Any discount codes for Ivory or Bug right now?"
Actions:
1. Search the aggregators for Ivory and Bug codes.
2. Add a one-line note that a Max (or the shopper's own card) benefit, or a Cashback.co.il rebate, may beat a public code on electronics.
3. Rank and return; flag that cross-store price gaps are out of scope (point to israeli-product-price-comparator).

### Example 3: Is this coupon site safe?
User says: "I found a site promising huge discounts on everything, is it legit?"
Actions:
1. Apply the scam red-flags rubric (card-before-code, survey-to-unlock, typosquat domain, no business details).
2. Explain the 14-day remote-sale cancellation right as the real backstop.
3. Point to verified sources (Couponim, Cashback.co.il) instead.

## Bundled Resources

### References
- `references/domain-checklist.md` -- the verified Israeli coupon/cashback/benefit source map, the consumer-protection legal anchors, and the named entities the skill may safely cite. Consult when extending the source map or updating the legal section.
- `references/source-map.md` -- quick-reference table of source types, what each is good for, and the Hebrew search terms that surface them.

### Scripts
- `scripts/rank_codes.py` -- takes a JSON list of candidate codes (code, source, date, discount, conditions) and prints the ranked summary table plus a "try this first" pick. Run: `python scripts/rank_codes.py --help`

## Gotchas

- **Agents fabricate codes.** Faced with "find a coupon", a model will happily emit a real-looking string like `SAVE20`. That is the single biggest failure mode here. No code without a live source and date, ever.
- **New-customer-only codes look universal.** Aggregators rarely label them. A code that "works" in a screenshot often only works on a first order. Always check and surface the new-customer flag.
- **A coupon is not always the best lever.** On electronics especially, a credit-card cardholder benefit or a cashback rebate frequently beats the public code. Check those before declaring victory.
- **Stale aggregator pages.** Many "קופון 2024" pages still rank in search. Trust the posting date, not the page's freshness claims.
- **Global-store codes can be a trap for Israeli shoppers.** A code on a US/CN store can be wiped out by shipping plus the customs/VAT that applies once the order crosses the de-minimis threshold. Factor total landed cost, not the sticker discount. On a domestic Israeli store the opposite holds: the displayed price already includes VAT, so a percent-off applies straight to the shown price, do not add VAT on top.
- **".co.il vs .com" drift.** Some Israeli brands redirect their .co.il to a global .com or a separate shop subdomain. Confirm you are on the real store before trusting a code or entering details.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Kol-Zchut, remote-sale cancellation | https://www.kolzchut.org.il/he/ביטול_עסקה_שנעשתה_באינטרנט_או_בטלפון | The 14-day window, the 5% / 100 NIS fee cap, and the 4-month extension for seniors, people with disabilities, and new immigrants |
| Couponim | https://couponim.co.il | A live Israeli coupon-aggregator surface to search for per-store codes |
| Cashback.co.il | https://www.cashback.co.il | Whether a cashback rebate stacks on, or beats, a coupon for this store |
| BuyMe | https://buyme.co.il | A discounted gift card you can buy and pay with for an effective discount |
| Max benefits | https://www.max.co.il/benefits/lobby | A cardholder discount at this store (and the equivalent from the shopper's own card issuer) |

## Troubleshooting

### Error: "I found codes but I'm not sure they are real"
Cause: The search surfaced an aggregator page with no posting date and no terms.
Solution: Mark such codes Low confidence, never present them as verified, and prefer dated codes. If nothing is dated, fall back to store-direct levers (newsletter, app, loyalty club) and say so.

### Error: "No web search is available"
Cause: The host agent has no live web tool this run.
Solution: Do NOT invent codes. Return the source map and the Hebrew search playbook so the shopper can run them, and the store-direct levers that need no code.

### Error: "The code did not work at checkout"
Cause: Expired, new-customer-only, below the minimum cart, or excluded category.
Solution: Re-check the conditions column, try the next ranked candidate, and remind the shopper that codes expire fast. Consider a cashback or card benefit instead.
