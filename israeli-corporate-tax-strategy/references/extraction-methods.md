# Profit Extraction Methods: Detailed Comparison

Worked examples for each extraction method from an Israeli limited company (Chevra Baam).

## Assumptions for All Examples

- Company: Israeli Ltd (Chevra Baam)
- Shareholder: Single controlling shareholder owning the whole company (baal shlita)
- Tax year: 2026
- Shareholder has 2.25 base credit points (resident male)
- No other income sources (for simplicity)

## Example 1: Small Extraction (200,000 NIS Company Profit)

### Method A: Full Salary

Gross salary approximately 188,770 NIS/year (the 200,000 budget less controlling-shareholder employer NI of about 11,230)
- Income tax (progressive): approximately 27,146 NIS
- Credit points reduction: -6,534 NIS
- Net income tax: approximately 20,612 NIS
- Employee NI+health (controlling-shareholder rates, 4.25% / 11.96%): approximately 15,450 NIS
- Net to shareholder: approximately 152,707 NIS
- **Effective rate: approximately 23.6%**

### Method B: Full Dividend

- Corporate tax (23%): 46,000 NIS
- Distributable: 154,000 NIS
- Dividend tax (30%): 46,200 NIS
- Net to shareholder: 107,800 NIS
- **Effective rate: 46.1%**

### Result: Salary wins by ~44,907 NIS

For amounts within the lower tax brackets, salary is significantly better.

## Example 2: Medium Extraction (500,000 NIS Company Profit)

### Optimal Mix (Salary 228,000 + Dividend on Rest)

Salary portion: 228,000 gross (employer cost approximately 242,127)
- Employee tax: approximately 28,458 NIS (after credit points)
- Employee NI+health: approximately 20,142 NIS
- Net from salary: approximately 179,400 NIS

Remaining profit: approximately 257,873 NIS
- Corporate tax: 59,311 NIS
- Distributable: 198,562 NIS
- Dividend tax: 59,569 NIS
- Net from dividend: approximately 138,993 NIS

Total net: approximately 318,393 NIS
**Effective rate: approximately 36.3%**

Compared to pure dividend (46.1%, net 269,500) this saves approximately 48,893 NIS. These figures match `scripts/tax_comparison.py` to the shekel. Its 10,000-step optimizer lands near a 235,000 salary, within about 60 NIS of this hand-picked mix.

## Example 3: Management Fees Instead of Salary (200,000 NIS)

Billed by the shareholder personally as an osek murshe, with no business expenses and VAT reclaimed by the company, 200,000 of fees leaves about 152,528 NIS net, almost identical to salary: self-employed NI (7.70% / 18.00%) replaces employee plus employer NI, and 52% of the NI part is deductible (s.47A). Management fees only pull ahead when there are real business expenses to deduct. Run `python3 scripts/tax_comparison.py --profit 200000`.

## Key Decision Thresholds

| Annual Extraction Amount | Recommended Strategy |
|-------------------------|---------------------|
| Under 84,120 NIS | Pure salary (10% bracket, with credit points near 0%) |
| 84,120 - 228,000 NIS | Pure salary (up to 20% bracket, well below 46.1%) |
| 228,000 - 560,280 NIS | Salary at 228,000, dividend for rest |
| Above 560,280 NIS | Salary at 228,000, dividend for rest, surtax planning |
