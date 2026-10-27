# Changelog

All notable changes to this skill are documented here.

## [1.0.0] - 2026-10-27

### Added

- Initial release: mid-year tax coordination for salaried people with two or more payers. Covers which payer gets the credit points on Form 101 and the basic points by gender plus the reliefs claimed at that one payer. The estimate compares month-by-month withholding against the annual liability on the 2026 brackets, with the 2025 table for comparison, and handles payers that start mid-year or follow one another. It explains the Form 101 pay categories and the daily table, the online service versus Form 116 at the assessing office, and what to do with the certificates. It covers the 2026 transition after the bracket widening, routes the cases the estimator does not cover (disability exemption, olim temporary order, qualifying settlement, pension exempt share), and notes that Bituach Leumi coordination is separate.
- `scripts/coordination_estimate.py`, a stdlib estimator that reproduces the three worked examples in SKILL.md.
