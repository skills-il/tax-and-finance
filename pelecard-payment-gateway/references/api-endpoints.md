# Pelecard API Endpoints

Everything below was verified live against `gateway21.pelecard.biz` on 2026-08-27, either by
probing the endpoint directly or by reading Pelecard's own public request builder at
`https://gateway21.pelecard.biz/services` (which ships the service list and a preset request body
for each one in `/Scripts/Services/Sandbox.js`). That script defines 57 distinct service URLs: 54
under `/services/`, plus `/PaymentGW/GetTransaction`, `/PaymentGW/ValidateByUniqueKey` and
`/PaymentEnquiry/CreateLink`.

## Hosts: environment is the TERMINAL, not the hostname

| Host | What it actually is |
|------|---------------------|
| `gateway21.pelecard.biz` | Current gateway generation. Serves the live API. |
| `gateway20.pelecard.biz` | Older gateway generation. Serves the **same** API surface. |
| `gateway20.pelecard.biz/sandbox` | A sandbox **UI page** (a request builder), not a separate API host. |
| `match-api.pelecard.biz` | Pelecard's newer "Match" REST surface. Its docs page returns HTTP 200 with ~37 characters of text (an empty client-side shell). Confirm the shape with Pelecard before depending on it. |

**Do not treat the hostname as an environment switch.** Both `gateway20` and `gateway21` answer
`PaymentGW/init`, `PaymentGW/GetTransaction` and `PaymentGW/ValidateByUniqueKey` identically, and a
404 on `gateway21` redirects to an error page on `gateway20`, so they are one system. Whether a
call is a test or a real charge is decided by **which terminal number and credentials you send**,
not by which host you post to. Ask Pelecard which host your test terminal was issued on, keep host
and terminal together in one config object, and never let code infer safety from a hostname.

## The two surfaces (different parameter casing -- this bites)

Pelecard has two server-to-server surfaces and they do **not** share a naming convention. Mixing
them up is the most common cause of a request that returns an error with no useful message.

| | `/PaymentGW/*` | `/services/*` |
|---|---|---|
| Credentials | `terminal`, `user`, `password` | `terminalNumber`, `user`, `password` |
| Transaction id | `TransactionId` | varies: `debitTrxId`, `voucherId`, `uid`, `trxRecordId` |
| Amount | `Total` | `total` |
| Currency | `Currency` | `currency` |
| Order correlation | `ParamX` | `paramX` |
| Shop | `ShopNo` | `shopNumber` |

A few `/services` endpoints (`UpdateToken`, `RetrieveToken`) use PascalCase for the credentials
(`TerminalNumber`, `User`, `Password`). Copy the preset from the live builder rather than guessing.

## `/PaymentGW/*` -- the iframe surface (3 endpoints, all verified live)

### `POST /PaymentGW/init` -- create the payment session

Body: the credentials triple plus the transaction parameters (see `payment-parameters.md`).

**Success** returns `URL` and `ConfirmationKey`. **Failure** returns those two fields as empty
strings plus an `Error` object:

```json
{"URL":"","ConfirmationKey":"","Error":{"ErrCode":501,"ErrMsg":"Login for user x failed"}}
```

Check `Error.ErrCode` before using `URL`. A blank `URL` with HTTP 200 is a failure, not a session.
Resolve `ErrCode` with `/services/GetErrorMessageEn` (see `error-codes.md`).

**`init` does NOT return a `PelecardTransactionId`.** The response has exactly two data fields.
There is no transaction until the customer actually transacts, so any reconciliation design that
assumes you can store a transaction id at session-create time is unbuildable. Correlate on your own
`ParamX` (and/or `UserKey`) instead, and look the transaction up later with `/services/TrxLookUp`.

### `POST /PaymentGW/GetTransaction` -- look a transaction up by id

Body: `terminal`, `user`, `password`, `TransactionId`.

Response envelope is **not** flat. It is:

```json
{"StatusCode":"501","ErrorMessage":"Login for user x failed","ResultData":{ ...66 fields... }}
```

Read `StatusCode` first (`"000"` = success), then the transaction fields inside `ResultData`.
Do not read amount or approval fields off the top level; they are not there.

### `POST /PaymentGW/ValidateByUniqueKey` -- validate without credentials

Body: `ConfirmationKey`, `UniqueKey`, `TotalX100`. **No credentials.** Returns a bare numeric
result.

**Do not build your reconciliation or outbound-idempotency net on this.** `UniqueKey` is an input to
the validation call, but this skill has NOT established which `PaymentGW/init` parameter sets one:
the documented passthrough fields are `ParamX`, `ShopNo`, `UserKey` and `UserData1`-`15`, none of
which is shown to become the `UniqueKey`. Use it only if Pelecard confirms how your terminal accepts
a merchant-supplied `UniqueKey`. The documented reconciliation route is `paramX` via
`/services/CheckGoodParamX` or `/services/TrxLookUp` (see SKILL.md Step 4).

`TotalX100` means "the amount multiplied by 100", i.e. minor units (agorot). This corroborates the
agorot convention independently of the dofinity wrapper: the builder's preset sends `TotalX100:
"100"` for the same 1 shekel that `/services/DebitRegularType` sends as `total: "100"`.

Contrary to older versions of this reference, `ValidateByUniqueKey` is **not** a gateway20-only
endpoint. It answers on both hosts.

Every other `/PaymentGW/*` path tested (`DebitRegular`, `DebitRegularCancel`, `Refund`,
`ConfirmDebit`, `CancelTransaction`, `GetToken`) 302-redirects to an HTTP 404 error page, exactly
as a deliberately fabricated control path does. **There is no `PaymentGW` refund endpoint.**

## `/services/*` -- the server-to-server surface

This is where every operation other than "create an iframe session" lives. 54 endpoints are listed
under `/services/` in the live builder. The ones an integration actually needs:

### Charge

| Endpoint | Purpose | Key parameters |
|----------|---------|----------------|
| `/services/DebitRegularType` | Standard sale (J4) | `terminalNumber`, `user`, `password`, `shopNumber`, `creditCard`, `creditCardDateMmYy`, `token`, `total`, `currency`, `cvv2`, `id`, `authorizationNumber`, `paramX`, `eci`, `xid`, `cavv` |
| `/services/DebitPaymentsType` | Installments sale | as above plus `paymentsNumber`, `firstPayment` |
| `/services/DebitCreditType` | Credit-type sale | as `DebitRegularType` |
| `/services/DebitIsracreditType` | Isracredit-type sale | as `DebitRegularType` |

Pass a saved `token` **instead of** `creditCard` to charge a stored card. That is the recurring
billing path, and it is a `/services` call, not an iframe parameter.

`eci` / `xid` / `cavv` are the 3D Secure 2 result values you carry **into** the debit after running
the authentication (see below). `authorizationNumber` carries a prior authorization into the debit,
which is the mechanism for capturing a J5 hold.

### Authorize (hold) and pending

| Endpoint | Purpose |
|----------|---------|
| `/services/AuthorizeCreditCard` | Authorize a card (J5). Places a hold; no money moves. |
| `/services/AuthorizeCreditType` / `AuthorizePaymentsType` / `AuthorizeIsracreditCard` | Authorize variants |
| `/services/PendingRegularType` (also `PendingCreditType`, `PendingPaymentsType`, `PendingIsracreditType`) | J9 pending transaction. Takes `authorizationNumber` and `userKey`. |
| `/services/ClearPendingByUserKey` | Clear a pending request by your `userKey` |
| `/services/ClearPendingByRecordId` | Clear a pending request by Pelecard's record id |

To capture a hold, submit a debit carrying the `authorizationNumber` the authorization returned.
Confirm the exact pairing for your terminal with Pelecard before going live; the parameter is
present on every debit type, but which authorization types your terminal is provisioned for is a
terminal setting.

### Void and refund

| Endpoint | Parameters | Use |
|----------|-----------|-----|
| `/services/DeleteTran` | `terminalNumber`, `user`, `password` + one of (`voucherId` + `creditCard` + `total`) / `debitTrxId` / `uid` | Delete a transaction from the open batch |
| `/services/DeleteIshur` | `terminalNumber`, `user`, `password`, `debitTrxId` | Delete an authorization (release a hold) |
| `/services/EmvReversal` | `terminalNumber`, `user`, `password`, `Uid` or `DebitTrxId` | EMV reversal |
| `/services/EmvFinishDebit` | `terminalNumber`, `user`, `password`, `Uid` | Finish an EMV debit |

See the void-vs-refund section in SKILL.md Step 6. There is no single "refund" endpoint; which
primitive applies depends on whether the transaction has been broadcast.

### Tokens

| Endpoint | Purpose | Parameters |
|----------|---------|------------|
| `/services/ConvertToToken` | Tokenize a card | `terminalNumber`, `user`, `password`, `creditCard`, `creditCardDateMmYy`, `addFourDigits` |
| `/services/RetrieveToken` | Fetch the token for a card | `TerminalNumber`, `User`, `Password`, `CreditCard` |
| `/services/UpdateToken` | Update a token after reissue / expiry roll | `TerminalNumber`, `User`, `Password`, `CreditCard`, `CreditCardDateMmYy`, `Token` |
| `/services/CheckCreditCardForToken` | Check a card is tokenizable before charging | `terminalNumber`, `user`, `password`, `CreditCard`, `CreditCardDateMmYy` |

`UpdateToken` is the "saved card was reissued" path. Without it, every card reissue is a lost
subscriber.

### Lookup and reconciliation

| Endpoint | Keyed on | Use |
|----------|----------|-----|
| `/services/TrxLookUp` | `paramX` | Find the transaction for one of your orders |
| `/services/CheckGoodParamX` | `paramX`, `shvaSuccessOnly` | Was this order paid successfully? |
| `/services/CheckGoodParamXList` | `paramX` list | Batch version |
| `/services/CheckGoodParamXEmv` | `paramX` | EMV variant |
| `/services/GetTransData` | `startDate`, `endDate` (`dd/MM/yyyy HH:mm`) | Transactions in a window |
| `/services/GetCompleteTransData` | `startDate`, `endDate` | Full transaction records in a window |
| `/services/GetTransDataBeforeBc` | date range | Transactions **not yet broadcast** |

`GetTransDataBeforeBc` ("before broadcast") is the endpoint that tells you what is sitting
unsettled in the open batch.

### Settlement, 3DS, operations

| Endpoint | Purpose |
|----------|---------|
| `/services/Broadcast` | Trigger the Shva broadcast (שידור) for the terminal. Takes only `terminalNumber`, `user`, `password`. |
| `/services/GetBroadcast` / `GetBroadcastsByDate` | Broadcast status / history |
| `/Services/Initiate3DSAuthenticationProcess` | Start 3DS2 authentication. Takes `RedirectUrl`, `BillingAmount`, `BillingCurrencyCode`, card or `Token`, cardholder name/email/phone/address, and browser fingerprint fields (`HttpAcceptHeader`, `BrowserScreenPixelsHeight/Width`, `BrowserLanguage`, `BrowserScreenBitDepth`, `EndUserIPAddress`, `UserAgent`). |
| `/services/GetErrorMessageEn` / `GetErrorMessageHe` | Official bilingual message for any status code. **No credentials.** |
| `/services/GetTerminalName` | Cheapest possible credential smoke test |
| `/services/ResetUserPassword` | Rotate the API password (they expire; see code `502`) |
| `/services/CreateInvoice`, `CreateICountInvoice`, `CreateEZCountInvoice` | Emit the tax invoice through Pelecard rather than a separate provider |
| `/Services/InitiateBankTransfer` | Open-banking bank transfer (returns ISO 20022 status codes `660`-`680`) |

The full list, with a preset request body for each, is at `https://gateway21.pelecard.biz/services`.
Use it as the primary reference; it is live, public, and always current.
