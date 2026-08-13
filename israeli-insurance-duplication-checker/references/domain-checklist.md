# Coverage contract, israeli-insurance-duplication-checker

Trimmed for shipping. The full research checklist, including the eleven-row
"known bad figures" table and the complete NOT FOUND list, is kept as a
build-time artifact next to the skill folder as `domain-checklist-full.md`. It is
not shipped because it quotes figures it exists to REJECT, and the fact-grounding
gate reads a quoted-to-reject figure as a live claim.

## The core rule the skill must encode

The statute sorts by payment mechanism, not by subject matter.

| Cover | Governing rule | Duplicates? |
|---|---|---|
| רכב, דירה, אחריות | ס' 59 directly, extended by ס' 67, non-derogable by ס' 64 | Yes, real waste |
| Reimbursement health, loss-based אכ"ע | ס' 56(א) via ס' 54(ב); ס' 59 is NOT imported | Yes, capped at actual loss |
| חיים, מחלות קשות, fixed-sum נכות | פרק ב' via ס' 54(א); no כפל provision, no ceiling | No, legitimate stacking |

## Who the skill is actually for

The שקל ראשון reform took effect in June 2024, applied to individual policies
only, and its opt-out window closed on 1.6.2025. Group policies were never
auto-converted and most group surgery cover is still מהשקל הראשון. Anyone who
bought an individual policy before February 2016 was never caught either. Those
two populations, group-policy holders and pre-2016 buyers, are the core audience.
Do not write the health section as though the reform fixed it for everyone.

## Non-negotiables

- The safe-cut rule: cancel only the layer the user can buy back. שב"ן must
  re-accept them; an underwritten private policy will not.
- אכ"ע: the fund's test is עיסוק סביר, so "you have it in your pension, cancel
  the private one" is wrong. Per-policy cap is 75%; cross-insurer offset triggers
  only above 100% of income from all sources, with a 30% floor.
- Fixed-sum cover stacks. Say so plainly rather than flagging it as waste.
- הר הביטוח holds no שב"ן data and lists no service subscriptions or card
  benefits. The only official domain is `harb.cma.gov.il`.
- Cancellation by the insured takes effect after three days, not fifteen. The
  consumer-protection distance-selling withdrawal does not apply to insurers.
- No Israeli card issuer requires the trip to be charged to the card.
- Car versus home liability is not a duplication; the home policy excludes
  vehicle liability by construction.

## Out of scope

- Comparing and buying new policies: `israeli-insurance-comparator`.
- Co-pays and costs inside the public system: `israeli-hmo-navigator`.
- The pension savings product itself: `israeli-pension-advisor`.

## Do not fill from memory

Consult `domain-checklist-full.md` before adding any figure. Items recorded there
as NOT FOUND, including the group-to-individual conversion window and terms, any
retroactive premium refund for שב"ן-duplicating cover, and any group-health
specific כפל rule, must not be asserted at any specificity.
