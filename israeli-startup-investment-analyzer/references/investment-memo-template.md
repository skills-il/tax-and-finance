# Investment Memo Template

The skill produces a memo in this structure. Keep it tight: a screening memo is
1 to 2 pages, a full pre-term-sheet memo is 3 to 5 pages. Lead with the verdict,
then the evidence. Every number must trace to something the founder provided or a
named public source. Mark anything you could not verify as an open question, do
not paper over a gap with a guess.

---

## 1. One-line summary and verdict
- What the company does, in one sentence a non-expert understands.
- Stage, round (SAFE / priced, seed / A), amount raising, on what pre/post.
- Verdict: PURSUE / PASS / NEEDS MORE, with the single biggest reason.

## 2. Snapshot
| Field | Value |
|-------|-------|
| Founded / HQ / legal structure | (Israeli Ltd? Delaware HoldCo + Israeli OpCo?) |
| Team size | |
| Round | (SAFE/priced, amount, pre/post, lead) |
| Traction headline | (ARR/MRR, growth, logos) |
| Capital raised to date | |

## 3. Market and timing
- The problem and who has it. TAM / SAM bottom-up (reject top-down "small slice of a giant market" sizing).
- Why now: what changed (regulation, tech, behavior) that makes this winnable today.
- Risk: is the market real and growing, or a feature, or too early.

## 4. Team
- Founders: domain fit, prior outcomes, why this team wins.
- Gaps (missing CTO, no commercial founder, first-time in this market).
- Probing questions to ask on the call (founder dynamics, full-time, vesting).

## 5. Product and moat
- What is built vs roadmap. Differentiation. Defensibility (data, network, switching cost, IP).
- For deep-tech / IP-heavy: where does the IP legally sit, and is it encumbered (see Israel-specific section).

## 6. Traction and metrics sanity check
- Pull the real numbers and pressure-test them. Common deck inflations to catch:
  - "ARR" that is actually a pipeline, LOIs, or annualized from one big month.
  - Growth shown as a rate with no absolute base (a huge percentage on a couple of customers).
  - Burn and runway omitted, or runway quoted before the new raise.
  - Logos shown as customers when they are pilots / design partners.
- Compute or request: net revenue retention, gross margin, CAC payback, burn multiple.

## 7. Deal terms and cap-table sanity

Economics:
- Pre/post-money, round size, resulting ownership, option pool size and whether the
  top-up is pre-money (dilutes founders) or post-money.
- Founder ownership remaining and vesting / reverse-vesting status.
- For SAFEs: cap, discount, pre vs post-money SAFE, and the stacked dilution from
  all outstanding SAFEs converting at once (use scripts/cap_table_math.py).
- **Liquidation preference.** The term that most often turns a "good" headline exit
  into little or nothing for common and late money. Distinguish 1x non-participating
  (founder-friendly, the seed norm) from participating ("double dip") and from a
  multiple (2x, 3x). Add up the full preference stack carried from prior rounds and
  model the exit waterfall, not just the headline price.
- **Anti-dilution.** Broad-based weighted-average is the market standard. Full ratchet
  is a red flag. Note what a down round would do to the investor's stake, and that
  the absence of anti-dilution protection for the new money is itself negotiable.

Control:
- **Board composition.** Map the seats (e.g. founder / investor / independent split)
  and who controls the board now and after the round.
- **Protective / veto provisions.** The list of actions that need investor consent
  (selling the company, issuing senior stock, budget, new debt). This is where real
  control sits at seed, even with a minority stake.
- **Pro-rata, drag-along, tag-along / co-sale, ROFR.** Pro-rata (follow-on right),
  drag-along (can force the investor into a sale), tag-along / co-sale, and right of
  first refusal. Drag-along in particular decides whether the investor can be pulled
  into an exit they did not choose.
- Prior rounds and any unusual carried-forward terms (super pro-rata, founder secondary).

## 8. Israel-specific due diligence
Run the checklist in references/israeli-dd-landmines.md. Summarize findings:
- Innovation Authority (IIA) grant exposure: royalties owed, IP/know-how-out
  restrictions, redemption-fee exposure on a flip or exit.
- Corporate structure: OpCo/HoldCo flip status, where IP is owned, flip tax exposure.
- Option 102 plan: trustee track, pool health, any non-compliant grants.
- Companies Registrar status (active vs "violating company"), founder vesting,
  cap-table cleanliness.
- Tax status (Preferred / Preferred Technological Enterprise) if claimed.

## 9. Key risks and red flags
- Ranked. Separate "diligence can resolve this" from "this is a thesis risk".

## 10. Diligence questions for the founder
- A sharp, prioritized list (see references/diligence-questions.md). The goal is to
  resolve the top 5 risks, not to send 40 generic questions.

## 11. Recommendation
- PURSUE / PASS / NEEDS MORE, the conditions that would change the verdict, and
  (if relevant) suggested check size and what you would want to see before a term sheet.
