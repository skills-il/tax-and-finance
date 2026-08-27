# Changelog

## 1.6.0 - 2026-08-27

The allocation-number rule was stated three different ways in one skill, and the version a reader hit depended on which section they opened.

- **The main allocation-number paragraph contradicted itself.** It opened "For osek murshe, tax invoices exceeding **5,000 NIS** must include an allocation number" and then closed "From June 2026 this threshold drops to 5,000 NIS", so the threshold was 5,000 both before and after the step. The Jan 2026 row (10,000) was missing entirely, which meant a NIS 7,000 invoice issued in March 2026 was flagged as missing a number it never needed. Replaced with the full staged table (25,000 from 5 May 2024, 20,000 from 1 Jan 2025, 10,000 from 1 Jan 2026, 5,000 from 1 Jun 2026) and an explicit statement that the threshold in force on the invoice **issue date** governs, not today's.
- The Hebrew Gotcha carried the same self-contradiction in its own words ("מ-1.6.2026 ... מעל 5,000 ש\"ח (יורד ל-5,000 ש\"ח מיוני 2026)"), and the Hebrew main paragraph had the Jan-May 2026 step but not the 2024 or 2025 rows. Both now carry the full ladder.
- The English Gotcha at the bottom of the file was already correct, which is why this survived: a reader who opened Gotchas got the right answer and a reader who opened the Invoicing section did not. Same skill, same day, two different rules.
- **Evidence file schema normalised.** 21 of 32 entries had no `claim_id`, and the allocation entry described only the last three steps of the ladder. Both fixed, and the 25,000 opening row now has its own entry recording that it is corroborated across four sibling skills rather than re-fetched.

Verified unchanged and correct: the osek patur / esek za'ir ceiling of 122,833 NIS for 2026 (120,000 in 2024 and 2025), which is quoted verbatim from Kol Zchut in the evidence file and matches the figure carried by three other skills in this repo; the 18% VAT rate; and the projection-governs-not-percentage rule for the threshold crossing.
