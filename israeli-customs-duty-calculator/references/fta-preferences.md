# Israeli FTA Preferences Cheat Sheet

Israel has signed free-trade agreements with most of its major trading partners. A valid origin proof removes the customs duty (not VAT or purchase tax).

## US-Israel Free Trade Agreement (1985)

- First US bilateral FTA.
- Origin rule: sum of US materials cost and direct US processing costs must be at least 35 percent of the appraised value.
- Origin proof: US Origin Invoice Declaration stated on the commercial invoice (or shipping list / proforma). The Green Form (Form A) is no longer used; **the January 10, 2018 discontinuation date previously stated here is not on the cited page and has been withdrawn.**
- Signature: the US exporter or manufacturer must sign. Verification may be requested by Israeli Customs.

Source: https://www.trade.gov/us-israel-free-trade-agreement

## EU-Israel Association Agreement

**Corrected in v1.4.0. Earlier versions of this file were wrong on both limbs.** They said the applicable rules were the "PEM Convention, 2012 version", that "Israel has NOT yet ratified the revised PEM Convention", and that EUR-MED certificates are "not needed". The European Commission pages cited below say the opposite on the ratification point and supersede the version point:

> "Israel signed the Regional Convention on 10 October 2013, and it has also ratified it."

> "Two sets of alternative rules of origin apply until 31 December 2025. As of 1 January 2026, only the revised PEM Convention will apply"

So, as things stand:

- The Convention was established in **2011**, not 2012.
- Israel signed it on **10 October 2013** and has ratified it.
- The transitional period in which two alternative rule sets ran side by side **ended on 31 December 2025**. From **1 January 2026 the revised PEM Convention is the only set of rules applying.** Any origin analysis this skill's users inherited from before that date needs redoing under the revised rules.
- Origin proof: EUR.1 movement certificate, stamped by the exporter's customs authority. Wet-ink signature required; Israel does not accept electronic signatures.
- An invoice declaration is available to a non-approved exporter only up to a value ceiling, and to an approved exporter at any value. **The ceiling is not verified in this file.** A figure of 6,000 euros is widely quoted and was previously stated here as fact with no source; treat it as a lead and confirm it with the exporter's customs authority.
- Whether EUR-MED certificates now have a role under the revised regime is likewise not settled here. Do not repeat the old "not needed" line.

Sources: https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/israel_en and https://trade.ec.europa.eu/access-to-markets/en/content/rules-origin-revised-pan-euro-mediterranean-convention

Source: https://trade.ec.europa.eu/access-to-markets/en/content/rules-origin-revised-pan-euro-mediterranean-convention

## UK-Israel Trade and Partnership Agreement (2019)

- Signed post-Brexit, mirrors the EU agreement rules.
- Origin proof: EUR.1 or an invoice declaration under a value ceiling that is not verified in this file.
- Approved-exporter status is available for frequent exporters.

Source: https://www.gov.uk/guidance/summary-of-the-uk-israel-trade-and-partnership-agreement

## Canada-Israel FTA (CIFTA)

- CIFTA has been in force for many years and was later modernized. **The 1997 original and the 1 September 2019 modernization dates previously stated here are not supported by either CBSA page cited below and have been withdrawn.** Get the date from Global Affairs Canada or the Israeli Ministry of Economy if it matters to your case.
- Origin proof: CBSA form B239, titled "Free Trade Agreement - Certificate of Origin (CIFTA only)". It is explicitly not for use under NAFTA. The form carries a blanket-period field (a from-and-to date range the exporter sets) rather than a fixed statutory validity.
- **Retracted:** earlier versions of this file said the certificate is "valid four years from signature" and sourced both the form number and the validity to the CBSA rules-of-origin memorandum. That memorandum is a link page to the Regulations and states neither. The form number is now sourced to the form itself; the four-year validity is withdrawn as unverified. Take the blanket period from the certificate you actually hold.

Sources: form https://www.cbsa-asfc.gc.ca/publications/forms-formulaires/b239-eng.html ; rules of origin (only) https://www.cbsa-asfc.gc.ca/publications/dm-md/d11/d11-5-6-eng.html

## EFTA-Israel (Switzerland, Norway, Iceland, Liechtenstein)

- Origin proof: EUR.1 movement certificate. **Unverified in this file** and carried over from an earlier cycle with no citation. Confirm with the exporter before acting on it.

## Mercosur-Israel

- Reported to be in force, with a Mercosur-Israel movement certificate as origin proof. **Both the in-force status and the proof are unverified in this file.** **Unverified in this file** and carried over with no citation, as is the "June 2010" entry-into-force date that used to appear in SKILL.md. Confirm with the exporter before acting on either.

## Settlement-origin exclusion on the EU agreement

This is the most litigated origin rule on the EU-Israel agreement, and it runs in the export direction, so it bites an Israeli seller rather than an Israeli buyer. The EU's own statement of it:

> "Goods originating from Israeli settlements in territories that have been under Israeli administration since June 1967 are not entitled to benefit from any preferential tariff treatment"

The mechanism is a Technical Arrangement between the EU and Israeli customs authorities, in force since 2004, under which proofs of origin issued in Israel must identify the place where the production process relevant for origin took place. The Commission publishes a list, by name and postal code, of the areas concerned, updated from time to time. An importer cannot claim preference for goods originating there.

Practical consequence for an exporter: the EUR.1 or invoice declaration has to carry the production locality and postal code, and giving the head-office address instead of the production site is what gets a claim rejected on audit. Outbound documentation is `israeli-export-shipping-kit`'s subject; this note exists so the rule is not silently absent from the FTA sheet.

Source: https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/israel_en

## Common pitfalls

- Invoice declaration above the value ceiling without approved-exporter status: rejected. Know the ceiling before choosing that proof.
- EUR.1 signed electronically: rejected by Israeli Customs.
- Non-originating components exceed the de minimis tolerance: product loses origin.
- Wrong origin rule applied (textile rules are different from general industrial rules).
- Supplier declaration missing for cumulation: origin cannot be proved.
