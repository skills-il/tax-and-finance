# Bank of Israel Representative Rate (Sha'ar Yatzig)

The headline USD/ILS conversion for dual-listed comparison MUST use the BoI
representative rate. The Bank of Israel publishes it on each foreign-currency
business day, based on the rate prevailing in the market at the time it is set.
The BoI page does not state the setting time in its text, so do not assert one;
check the BoI site. The rate has no binding legal status, it is an indicator.

## Why not intraday?
Intraday quotes are indicative and vary by venue. The representative rate is
the consistent official reference both sides reconcile against.

## Usage
    us_in_ils = us_price_usd * boi_representative_rate * ratio   # ratio = 1 for dual-listed ordinaries
Fetch the daily representative rate from the Bank of Israel and cache it for
about an hour. Mark any intraday figure as indicative only. The ratio is 1:1 for
dual-listed ordinary shares (the same fungible security on both exchanges); only a
true ADR carries a non-1 ratio, read from its SEC Form F-6.
