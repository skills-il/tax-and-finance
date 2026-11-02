# Broker exports (קבצי ייצוא של ברוקרים)

Consult when preparing a broker file for `scripts/broker-gains-ils.py`. Export layouts vary by broker and change over time: read the user's actual header and map it; never assume a layout from this page.

## Trades files (`--trades`)

- One file per account. Give one `--map` for all files, or one per `--trades` in the same order.
- Canonical columns: `date, symbol, side, quantity, price, fee, currency`, optional `instrument`, `open_date`, `lot_ref`.
- `lot_ref`: on a buy row it is that lot's id; on a sale row it names the lot sold (regulation 5 specific lot). If the referenced lot holds fewer units than were sold, an open item says so before the rest is matched FIFO. If it is not found the sale falls back to `open_date`, and if that fails too the row is excluded and the totals are marked INCOMPLETE.
- No `instrument` column: every row is computed as a share and an open item asks the user to confirm the file holds only shares and ETFs.
- A statement that stacks several sections in one CSV: copy only the trades section, with its header row, into its own CSV.

## Closed-positions files (`--etoro`)

- One row per position, with open and close dates; the reader turns each row into a buy and a sale and matches them by position id.
- `--etoro-map` keys: `position_id, symbol, units, open_date, close_date, open_price, close_price, instrument, currency, direction`.
- `instrument` (type) is required. Without it nothing in the file is computed, unless `--assume-real-shares` states that every row is a real, unleveraged long share.
- `direction`: a value containing Short excludes the row. Without a direction column, an action text starting with Sell is treated as a short and excluded. A short is never computed with a long sign.
- Symbol: a leading Buy or Sell word is removed from the mapped symbol column (for example an action text). Use the resulting name in `--substantial` and in the income file, or map a ticker or ISIN column as the symbol where the file has one.
- Currency: prices are read in `--etoro-currency` (default `--currency`) unless a currency column is mapped. Check non-US listings.
- Spread and overnight fees are not read; an open item says so.
- Spreadsheet exports must be saved as CSV first.

## Income files (`--income`)

- One file per broker; repeat `--income`, with one `--income-map` for all or one per file.
- `amount` is the GROSS payment before withholding. If the report gives only the net amount received plus the tax, map the net column and add `amount_is_net=yes` to that file's `--income-map` (one `--income-map` per file). A bare `--income-net` works only with a single income file and is refused with several. When the tax is exactly the treaty rate of amount plus tax, the script flags the amount column as probably net and marks the totals INCOMPLETE.
- Withholding on separate rows: map the type column so those rows read as withholding; they are folded into the same symbol's dividend, or into interest when the row has no symbol.
- Sign convention: `--tax-sign auto` reads it per file from the sign of the total tax on payment rows (zero-amount refund rows are ignored for this). A refund with no payment in the year is flagged as probably belonging to an earlier year and is not credited.
- Rounding: an above-treaty difference smaller than one shekel or half a percent of the gross is treated as broker rounding and not flagged.
