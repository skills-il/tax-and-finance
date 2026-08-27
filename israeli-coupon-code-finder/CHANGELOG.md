# Changelog

## 1.2.0 - 2026-08-27

A link-rot sweep that came back clean, and two script defects that did not.

**Every named destination was verified alive by navigation, not by status code**, each with a per-host control request to a fabricated path so a soft-404 could not pass as a hit. couponim.co.il, cashback.co.il, buyme.co.il and max.co.il/benefits/lobby all returned 200 against controls that returned 404 with a different body, and their page titles still describe the service the skill claims (coupon aggregator, cashback platform, gift cards, card benefits). benefits.isracard.co.il and cal-online.co.il/benefits/ return 403 and 400 to a plain fetch with bodies **byte-identical** to their controls, so those two were confirmed in a real browser instead: both render their benefits hubs. No dead or renamed destination was found.

- **`scripts/rank_codes.py` silently dropped unrecognised keys.** Feeding it a plausible-looking candidate list with `expires`, `min_cart` and `new_customers_only` produced a fully-formed table with every column showing `-`, ending in "Try this first: SAVE20" for a code it knew nothing about. It now names the ignored keys on stderr, and refuses outright when an item carries none of the recognised keys rather than rendering a row of dashes.
- **The documented field name was wrong, which is what produced those dashes.** Both language files described the input as "(code, source, **date**, discount, conditions)" while the script reads **`date_seen`**. Anyone following the documentation got blank columns. The exact key set is now spelled out in both languages, with the `date_seen` trap called out, plus a note that `discount` and `conditions` are free text and that the script ranks and formats but does not parse dates or evaluate expiry.
- **A missing input file raised a raw `FileNotFoundError` traceback.** It now prints one line and exits 1.
- **"Moadon Chaver (hvr.co.il, operated by Isracard)" was an unverifiable ownership claim.** The site itself does not state it. Dropped. Replaced with what the visit actually established: hvr.co.il is the career-soldier and retiree club, and it sits **behind a member login** (teudat zehut plus password), so the shopper has to check it themselves and this skill cannot read it, which is more useful to say than who owns it.

The customs figures were re-checked against `israeli-product-price-comparator`, corrected in the same batch, and match exactly: 75 USD from 2 June 2026, the 130 USD window from 25 February to 1 June 2026, VAT-only from 75 to 500, and commercial treatment above 1,000.

## 1.1.1 - 2026-08-19

### Fixed

- Translated section headings that had been left in English in SKILL_HE.md, where they rendered as-is on the Hebrew page. Hebrew is the site's default locale, and the skill validator never checked the Hebrew file, so these went unnoticed.

