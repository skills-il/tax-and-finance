# Supported Israeli Banks and Credit Card Companies

## Banks

| Bank | Hebrew | Code | MCP Support | Notes |
|------|--------|------|-------------|-------|
| Bank Hapoalim | bank hapoalim | 12 | israeli-bank-mcp | Largest bank |
| Bank Leumi | bank leumi | 10 | israeli-bank-mcp | Second largest |
| Israel Discount Bank | bank discount | 11 | israeli-bank-mcp | Includes Mercantile |
| Mizrahi-Tefahot | mizrahi tefahot | 20 | israeli-bank-mcp | Fourth largest |
| FIBI (First International) | benleumi rishon | 31 | israeli-bank-mcp | Includes Otsar Hahayal |
| Bank Yahav | bank yahav | 04 | Limited | Government employees |
| Bank Massad | bank masad | 46 | Limited | Teachers/education |

## Credit Card Companies

| Company | Hebrew | MCP Support | Notes |
|---------|--------|-------------|-------|
| Visa Cal (CAL) | visa cal | israeli-bank-mcp | Visa/MasterCard/Diners. Owned by Discount Bank (divestment pending) |
| Max (formerly Leumi Card) | max | israeli-bank-mcp | Mastercard/Visa. Owned by Clal Insurance (since 2023) |
| Isracard | isracard | israeli-bank-mcp | Isracard/Mastercard |
| American Express Israel | amex | israeli-bank-mcp | Amex cards |

## MCP Server Comparison

### israeli-bank-mcp (Motti Bechhofer)
- Most comprehensive coverage
- Based on israeli-bank-scrapers npm package
- Supports 2FA
- Active maintenance
- GitHub: github.com/mottibec/israeli-bank-mcp

### il-bank-mcp (Gilad Lekner)
- Docker-based deployment
- Adds transaction analysis features (spending breakdowns, recurring charge detection)
- Uses SQLite for local data storage
- GitHub: github.com/glekner/il-bank-mcp

### Asher MCP
- Alternative interface
- Same underlying scraper library
- Different API surface

## Authentication Notes
- All Israeli banks require 2FA (two-factor authentication)
- Bank scrapers use headless browser automation
- Sessions expire after ~15-30 minutes
- Some banks may temporarily block automated access
- Rate limiting varies by bank

## Data Available
- Account balances
- Transaction history (up to 12 months typically)
- Credit card transactions
- Standing orders
- Loan information (limited)
