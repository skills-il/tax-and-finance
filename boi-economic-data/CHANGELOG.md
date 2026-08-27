# Changelog

## 1.4.0 - 2026-08-27

Corrected the interest-rate endpoint. Every previous version documented the `BIR` dataflow as
"Bank of Israel rate data". `BIR` is "Interest rates and business volume - exc. housing loans",
i.e. commercial-bank credit rates. The policy rate is the `BR` dataflow, daily series
`MNT_RIB_BOI_D`. Because `BIR` resolves and returns plausible percentages, the error could only
ever surface as a wrong number, never as a failure. Fixed in SKILL.md, SKILL_HE.md,
references/boi-api.md, references/domain-checklist.md, evidence.json and the script.

`--interest` now fetches the rate instead of printing links to the BOI website, and prints the
dates it changed (3.5% since 2026-07-09). This closes a gap deferred in both the 1.2.0 and 1.3.0
cycles, which had been searching for the headline series inside the wrong dataflow.

Added a CPI path. The headline index is the CBS index API, id 120010, and the skill now says so.
The BOI `PRI` dataflow, which the previous version pointed at for CPI, is not the published
index. New `--cpi` flag, with `--cpi-last N` to reach the base month a contract names.

Removed the script's fabricated-data fallback. On any parse failure it previously returned
hardcoded rates stamped with today's dates and printed them in the same format as real data.
It now exits non-zero on every failure path, and `--example` is the only source of sample
numbers and is labelled as such.

Documented three API behaviours that fail while looking like success: `lastNPeriods` is accepted
and silently ignored (use `lastNObservations`), an unbounded dataflow query returns the entire
history rather than an error (EXR is about 20 MB back to 1948-05-15), and the CBS index API
returns HTTP 200 for an unknown index id and for an undefined path. Added retry-with-backoff for
the CBS server's intermittent connection resets.

Corrected the claim that the older `sdmx/v2` path returns 404. It is live given the
`BOI.STATISTICS` agency and `1.0` version segments, and both paths accept `format=csv`.

Quotation units now come from the API's `UNIT_MULT` attribute rather than a hardcoded table, and
`--json` carries the unit, so the per-100 yen quote cannot be read as a per-1 rate.

Added the CPI linkage conventions a real calculation needs: madad yadua versus madad bagin, the
base period and the CBS linking coefficient across a rebase, and the floor clause. Added a
warning that the policy rate is not the rate a borrower pays.

Removed the assertion that the BOI edge server rejects the default urllib User-Agent; a request
carrying that exact agent string returns 200.

## 1.3.1 - 2026-08-11

Removed the CPI basket weight column. The CBS CPI page carries no weights and the index API exposes no weight field, so all six figures were unsourced.

