# Domain coverage checklist: Israeli customs and import taxation

Anchor for the Expert Review. Every row states what the skill must cover, what it should cover, and what it deliberately does not.

## Must cover (core)

| Item | Why it is core |
|---|---|
| Personal-import exemption threshold and its current value | The single most-asked question in the domain, and the figure moved four times in seven months |
| The full band table: up to 75 / 75 to 500 / 500 to 1,000 / above 1,000 USD, plus tobacco and alcohol at any value | Kol Zchut personal-import rights guide. A missing band mis-taxes an entire cohort |
| The two different bases: threshold tested on goods value alone, tax computed on goods plus shipping plus insurance | Same source. Conflating them was a real defect in v1.1.0 |
| FX conversion at the Bank of Israel representative rate **plus 0.5 percent** | Same source, verbatim. Omitting it understates every landed cost |
| The cascading order CIF, duty, purchase tax, VAT | Statutory computation order |
| That purchase tax is levied on a reconstructed wholesale price, not on CIF plus duty | Purchase Tax (Goods and Services) Law 1952. Without this the script's purchase-tax line reads as final when it is a floor |
| The 72-hour anti-splitting rule | Same source. It is the workaround every consumer tries |
| Tobacco and alcohol carve-out from the exemption, and that their tariff is specific or compound rather than ad valorem | Same source plus the tariff's own structure. The skill cannot price them and must say so |
| 8-digit Israeli HS structure and that digits 7 to 8 are Israel-specific | Shaar Olami |
| Items conditional on a competent authority's approval, with the authority named | Same source. A parcel that cannot be released has no landed cost |
| Refund on returned or exchanged goods: the four conditions, the 6-month limit, the USD 250 export-form threshold | Same source. A live entitlement that lapses by inaction |
| The appeal route against the assessment, and that it is distinct from an objection to the carrier's commission | Same source. Naming an appeal without naming its route is worse than silence |
| That customs may reject the declared value, and that a false declaration bites even an innocent buyer | Same source |
| That a parcel of mixed items is assessed item by item | Same source |
| FTA preference removes duty only, never VAT or purchase tax | All agreement texts |
| The EU origin regime actually in force, including the 1 January 2026 revised-PEM cutover | European Commission. v1.3.0 and earlier stated the opposite and said Israel had not ratified, which the Commission page contradicts |

## Should cover (advanced)

| Item | Why |
|---|---|
| Courier versus postal clearance and who bears the commission | Fees routinely exceed the tax on a small parcel |
| The Eilat resident VAT-refund route | Free-zone entitlement, same personal-area filing route |
| Origin proofs per agreement and their signature requirements | EUR.1 wet-ink is a recurring rejection cause |
| The EU settlement-origin exclusion and the 2004 Technical Arrangement | The most litigated origin rule on that agreement, even though it bites on export |
| Checking the order confirmation for tax already collected at checkout | Prevents quoting a second bill on money already paid |

## Out of scope (explicit)

| Item | Rationale |
|---|---|
| Temporary import under an ATA carnet or a customs deposit | A distinct regime with its own base, guarantee and re-export deadline. This skill computes an ad-valorem landed cost and would overstate the charge. Step 1 now warns and routes to a broker. Re-open if a sourced carnet procedure becomes available |
| Goods exported for repair or warranty service and re-imported | Duty attaches to the repair value, not the article value, so the skill's cascade is the wrong model entirely. Same warning and routing |
| Oleh chadash and toshav chozer personal-effects exemption | A large, form-driven entitlement with its own eligibility window. It deserves its own skill rather than a cell in a table; the routing note points users out |
| Diplomatic and international-organisation exemption | Narrow population, separate statutory basis |
| Specific and compound tariff rates (NIS per kg, per litre, per unit) | Neither the prose nor the script can express them. Stated as an explicit scope limit rather than silently mispriced |
| The TAMA wholesale-price uplift rates | Not published in a form this skill could consume. Its absence is disclosed wherever the purchase-tax line appears: SKILL.md Step 6, the Hebrew mirror, the calculation block in `duty-rates-by-category.md`, the script docstring, the `--purchase-tax-rate` help text and the script's own output. Re-open when a rate table is sourced |
| Export documentation | `israeli-export-shipping-kit` |
| Domestic VAT reporting | `israeli-vat-reporting` |

## Authoritative sources

- Kol Zchut personal-import rights guide (bands, threshold, FX uplift, approvals, refunds, appeals)
- Shaar Olami tariff query and the Personal Import Tax calculator (Israel Tax Authority)
- European Commission trade pages for EU-Israel origin and the revised PEM Convention
- CBSA form B239 for the CIFTA certificate
- Bank of Israel representative rates
