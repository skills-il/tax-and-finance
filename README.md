# Tax & Finance Skills

AI agent skills for Israeli tax, invoicing, VAT, payroll, and financial systems.

Part of [Skills IL](https://github.com/skills-il) - curated AI agent skills for Israeli developers.

## Skills

| Skill | Description | Scripts | References |
|-------|-------------|---------|------------|
| [boi-economic-data](./boi-economic-data/) | Bank of Israel API data: interest rates, exchange rates (Sha'ar Yatzig), CPI, and CBS economic indicators. | `fetch_boi_rates.py` | `boi-api.md` |
| [cardcom-payment-gateway](./cardcom-payment-gateway/) | Integrate Cardcom payment gateway for Israeli e-commerce with installments and invoice generation. | -- | -- |
| [il-invoice-organizer](./il-invoice-organizer/) | Auto-organize Israeli invoices: Hebrew text parsing, VAT extraction, Tax Authority categories, Osek Murshe recognition. | `categorize_invoices.py` | `expense-categories.md` |
| [israeli-bank-connector](./israeli-bank-connector/) | Analyze Israeli bank transactions and spending patterns. Categorizes Israeli merchants. | `categorize_transactions.py` | -- |
| [israeli-client-payment-chaser](./israeli-client-payment-chaser/) | Automate payment collection from Israeli clients with culturally appropriate Hebrew reminders. | -- | -- |
| [israeli-e-invoice](./israeli-e-invoice/) | Generate and validate e-invoices per SHAAM (Tax Authority) standards. Supports invoice types 300-400. | `validate_invoice.py` | -- |
| [israeli-freelancer-ops](./israeli-freelancer-ops/) | Israeli freelancer toolkit: Osek Patur/Murshe management, bimonthly VAT, annual filing, receipt tracking. | -- | -- |
| [israeli-payment-orchestrator](./israeli-payment-orchestrator/) | Unified API for Israeli payment gateways (Cardcom, Tranzila, PayMe, Meshulam, iCredit, Pelecard). | `compare_gateways.py` | `gateway-matrix.md` |
| [israeli-payroll-calculator](./israeli-payroll-calculator/) | Gross-to-net Israeli payroll with income tax brackets, Bituach Leumi, health tax, and pension. | `calculate_payroll.py` | -- |
| [israeli-pension-advisor](./israeli-pension-advisor/) | Israeli pension system: keren pensia, bituach menahalim, keren hishtalmut. Contribution calculator. | `calculate_pension.py` | -- |
| [israeli-startup-financial-model](./israeli-startup-financial-model/) | Financial projections for Israeli startups: IIA grants, R&D tax credits, Angels Law, employment costs. | `model_runway.py` | `iia-grants.md`, `tax-incentives.md` |
| [israeli-tax-withholding](./israeli-tax-withholding/) | Nikui mas bemakor rates, withholding certificates, Form 856 for suppliers and freelancers. | `calculate_withholding.py` | -- |
| [israeli-vat-reporting](./israeli-vat-reporting/) | Prepare and validate Israeli VAT reports (Doch Maam). Input/output VAT, Form 874, zero-rated exports. | `calculate_vat.py` | -- |
| [shekel-currency-converter](./shekel-currency-converter/) | Convert currencies to/from NIS using Bank of Israel official rates. 30+ currencies supported. | `fetch_rates.py` | -- |
| [tase-stock-analysis](./tase-stock-analysis/) | Analyze Israeli stocks on TASE, track TA-35/TA-125 indices, evaluate dual-listed companies. | `fetch_tase_data.py` | `tase-api.md`, `capital-gains.md` |
| [tranzila-payment-gateway](./tranzila-payment-gateway/) | Integrate Tranzila payment gateway for Israeli e-commerce with installments support. | -- | -- |

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
