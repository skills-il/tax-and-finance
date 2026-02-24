# Tax & Finance Skills

AI agent skills for Israeli tax, invoicing, VAT, payroll, and financial systems.

Part of [Skills IL](https://github.com/skills-il) — curated AI agent skills for Israeli developers.

## Skills

| Skill | Description | Scripts | References |
|-------|-------------|---------|------------|
| [israeli-e-invoice](./israeli-e-invoice/) | Generate and validate e-invoices per SHAAM (Tax Authority) standards. Supports invoice types 300-400, allocation numbers, and compliance timeline. | `validate_invoice.py` | 3 |
| [israeli-vat-reporting](./israeli-vat-reporting/) | Prepare and validate Israeli VAT reports (Doch Maam). Input/output VAT calculation, Form 874, zero-rated exports, Eilat zone rules. | `calculate_vat.py` | 3 |
| [israeli-payroll-calculator](./israeli-payroll-calculator/) | Gross-to-net Israeli payroll with income tax (7 brackets), Bituach Leumi, health tax, pension, and credit points (nekudot zikui). | `calculate_payroll.py` | 3 |
| [shekel-currency-converter](./shekel-currency-converter/) | Convert currencies to/from NIS using Bank of Israel official rates. 30+ currencies, historical rates, cross-currency support. | `fetch_rates.py` | 2 |
| [israeli-tax-withholding](./israeli-tax-withholding/) | Nikui mas bemakor rates, withholding certificates, Form 856. Covers suppliers, freelancers, landlords, and cross-border payments. | `calculate_withholding.py` | 2 |
| [israeli-pension-advisor](./israeli-pension-advisor/) | Israeli pension system: keren pensia, bituach menahalim, keren hishtalmut. Contribution calculator and retirement projection. | `calculate_pension.py` | 2 |
| [israeli-bank-connector](./israeli-bank-connector/) | Analyze Israeli bank transactions and spending patterns. Categorizes Israeli merchants. Enhances israeli-bank-mcp servers. | `categorize_transactions.py` | 2 |

## Install

```bash
# Claude Code - install a specific skill
claude install github:skills-il/tax-and-finance/israeli-payroll-calculator

# Or clone the full repo
git clone https://github.com/skills-il/tax-and-finance.git
```

## Contributing

See the org-level [Contributing Guide](https://github.com/skills-il/.github/blob/main/CONTRIBUTING.md).

## License

MIT

---

Built with care in Israel.
