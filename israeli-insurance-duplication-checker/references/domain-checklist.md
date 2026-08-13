# Coverage contract, israeli-insurance-duplication-checker

Trimmed for shipping. The full research checklist, including the eleven-row
"known bad figures" table and the complete NOT FOUND list, is kept as a
build-time artifact next to the skill folder as `domain-checklist-full.md`. It is
not shipped because it quotes figures it exists to REJECT, and the fact-grounding
gate reads a quoted-to-reject figure as a live claim.

## The core rule the skill must encode

The statute sorts by payment mechanism, not by subject matter. And the tier
attaches to the BENEFIT, not to the policy: one contract can sit in two tiers.

| Cover | Governing rule | Duplicates? |
|---|---|---|
| רכב, דירה, אחריות, מבנה במשכנתא | ס' 59 directly, extended by ס' 67, non-derogable by ס' 64 | Yes, real waste |
| Reimbursement health, dental, loss-based אכ"ע | ס' 56(א) via ס' 54(ב); ס' 59 is NOT imported | Yes, capped at actual loss |
| חיים, מחלות קשות, fixed-sum נכות, תאונות אישיות | פרק ב' via ס' 54(א); no כפל provision, no ceiling | No, legitimate stacking |
| Group סיעוד | BOTH: פיצוי at home, שיפוי in an institution | Split the row and tier each half |

## Who the skill is actually for

The שקל ראשון reform took effect in June 2024 and applied to individual policies
only, catching those bought after February 2016 whose holder was also in a שב"ן.
The reversal window ran to 31 May 2025, a year from the transfer, but some
insurers extended their own, so it is a question to ask rather than a closed door.
The GROUP market was affected far less and with delay, because group policies
update only every few years under the policyholder-insurer agreement, so much
group surgery cover is still מהשקל הראשון. **Do NOT assert that group policies
were never auto-converted**: that was checked in the 2026-08-13 cycle and no
source supports it, and one industry source points the other way. Anyone who
bought individually before February 2016 was not caught either. Group-policy
holders and pre-2016 buyers remain the core audience; have them check their own
policy rather than being told a categorical rule.

## Non-negotiables

- The safe-cut rule: cancel only the layer the user can buy back. שב"ן must
  re-accept them; an underwritten private policy will not; and an individual
  ביטוח סיעודי cannot be re-bought at any price because the product is no longer
  sold at all.
- אכ"ע: the fund applies a BROAD-occupation test (25% capacity impaired, unable
  to work in his own or any other suitable occupation for over 90 consecutive
  days), so "you have it in your pension, cancel the private one" is wrong.
  "עיסוק סביר" is shorthand, not the takanon's term. Per-policy cap is 75%; cross-insurer offset triggers
  only above 100% of income from all sources, with a 30% floor.
- Fixed-sum cover stacks. Say so plainly rather than flagging it as waste. The
  two exceptions that still need an audit: near-identical מחלות קשות condition
  lists (compare and cut on price), and שאירים cover for a member with no
  שאירים (a waiver exists, but re-adding it permits medical underwriting).
- הר הביטוח holds no שב"ן data, no סיעוד, no service subscriptions and no card
  benefits. The only official domain is `harb.cma.gov.il`. The pension internals
  come from המסלקה הפנסיונית instead, at `swiftness.co.il`.
- Run the inventory per ADULT. A household verdict from one file is unsafe.
- Cancellation by the insured takes effect after three days, not fifteen. The
  consumer-protection distance-selling withdrawal does not apply to insurers.
- Limitation is three years, five for חיים / מחלות ואשפוז / סיעוד, and lodging
  the claim with the insurer does NOT stop the clock.
- Charging the trip to the card is generally NOT a condition on Israeli cards.
  Treat that as the default, not a universal; confirm on the specific card.
- Car versus home liability is not a duplication; the home policy excludes
  vehicle liability by construction.
- Check residency status before applying the safe-cut rule to an oleh, תושב
  חוזר, relocation case or non-resident spouse.

## Out of scope, re-litigated 2026-08-13

Each row was re-tested against two questions: would an ordinary user plausibly
ASK for this, and has it become capturable since it was written.

- **Comparing and buying new policies**: `israeli-insurance-comparator`. Users do
  ask, but answering would be שיווק ביטוחי, a licensed activity. Stays out, and
  the "gaps found" deliverable is the safe way to name an absence without
  recommending a product. Confirmed 2026-08-13.
- **Co-pays and costs inside the public system**: `israeli-hmo-navigator`.
  Confirmed 2026-08-13.
- **The pension savings product itself** (management fees, investment tracks):
  `israeli-pension-advisor`. Note the boundary moved slightly this cycle: the
  RISK cover inside the pension (אכ"ע, שאירים) is now in scope, because it is
  duplication surface. The savings product is not. Confirmed 2026-08-13.
- **A claim that has been rejected and become a legal dispute**: out of scope for
  the audit, but the skill now names the regulator's complaints route and the
  limitation clock rather than stopping silently, because a user who discovers an
  unclaimed benefit during an audit can lose it by waiting. Narrowed 2026-08-13.

## Do not assert, at any specificity

These were searched for this cycle and NOT established. Do not fill from memory.

- Any date on which the kupot group סיעוד policy stops being sold or operated.
  A Ministry of Health draft letter of January 2025 proposed 1.7.2025 and
  1.1.2026; it never issued in final form, was not coordinated with the insurance
  regulator, and was dropped. The June 2026 State Comptroller report treats the
  arrangement as operating.
- Whether receiving גמלת סיעוד from ביטוח לאומי offsets a policy payout.
- Any successor arrangement to the group סיעוד policy.
- That GROUP health policies were never auto-converted by the שקל ראשון reform.
  Searched 2026-08-13, not supported; the sourced position is "less, and with
  delay". Restate, never assert the absolute.
- A per-card list of which Israeli credit cards embed travel cover. Named
  products were removed in the 2026-08-13 cycle as unsourced; send the user to
  their own card's benefit page.
- A single fee figure for a מסלקה request: the operator's own FAQ gives both
  20 ₪ and 14 ש"ח for the same one-off all-products request.
- Any reported cut to the at-home סיעוד benefit, or any change to the ADL
  threshold. Single-sourced to press and law-firm material only.
- A circular number or effective date for a תאונות אישיות uniform-policy reform.
- The group-to-individual conversion window and terms, any retroactive premium
  refund for שב"ן-duplicating cover, and any group-health specific כפל rule.
- Waiting periods for an oleh, תושב חוזר or non-resident spouse.
- Section numbers from a specific fund's תקנון as though they were the
  regulator's own numbering.
