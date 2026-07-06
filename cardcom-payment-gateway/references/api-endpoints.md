# Cardcom REST API V11 Endpoint Reference

All endpoint paths, request fields, and response fields below are taken from the
official Cardcom V11 OpenAPI specification at
`https://secure.cardcom.solutions/Api/v11/Docs`.

## Base URL & Authentication

- **Base:** `https://secure.cardcom.solutions/api/v11/`
- **Auth fields:** `TerminalNumber` (integer) + `ApiName` (string) on every request.
  `ApiPassword` (string) is required only for refunds and document creation.
- **Test terminal:** `1000` with the demo `ApiName`. Test card: `4580000000000000`.
- **Method:** All endpoints are `POST` with `Content-Type: application/json`
  (except a few `RecuringPayments` / `CompanyOperations` lookups that are `GET`).
- **Response shape:** Every response carries `ResponseCode` (integer, `0` = success)
  and `Description` (string explaining the code).

## LowProfile (Hosted Payment Page)

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `LowProfile/Create` | Create hosted payment page | `TerminalNumber`, `ApiName`, `Operation`, `Amount`, `SuccessRedirectUrl`, `FailedRedirectUrl`, `WebHookUrl`, `ISOCoinId`, `Language`, `ReturnValue`, `Document` | `ResponseCode`, `Description`, `LowProfileId`, `Url`, `UrlToBit`, `UrlToPayPal` |
| `LowProfile/GetLpResult` | Retrieve payment result | `TerminalNumber`, `ApiName`, `LowProfileId` | `ResponseCode`, `Description`, `TranzactionId`, `ReturnValue`, `TranzactionInfo`, `TokenInfo`, `DocumentInfo`, `SuspendedInfo` |

`Operation` enum: `ChargeOnly` (default), `ChargeAndCreateToken`, `CreateTokenOnly`,
`SuspendedDeal`, `Do3DSAndSubmit`.

## Transactions

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `Transactions/Transaction` | Charge a card or a token (server-to-server) | `TerminalNumber`, `ApiName`, `Amount`, `Token` or `CardNumber`, `CardExpirationMMYY`, `CVV2`, `ISOCoinId`, `Document`, `Advanced` | `ResponseCode`, `Description`, `TranzactionId`, `Token`, `ApprovalNumber`, `DocumentNumber`, `DocumentUrl` |
| `Transactions/RefundByTransactionId` | Refund a transaction | `ApiName`, `ApiPassword`, `TransactionId`, `PartialSum`, `CancelOnly`, `AllowMultipleRefunds` | `ResponseCode`, `Description`, `NewTranzactionId` |
| `Transactions/GetTransactionInfoById` | Get single transaction details | `TerminalNumber`, `ApiName`, `TransactionId` (the schema uses `InternalDealNumber`) | `ResponseCode`, `Description`, transaction fields |
| `Transactions/ListTransactions` | List transactions by date range | `TerminalNumber`, `ApiName`, date range fields | `ResponseCode`, `Description`, transaction list |
| `Transactions/SpecialTransactions` | Credit, installments, special deals | `TerminalNumber`, `ApiName`, `Amount`, transaction options | `ResponseCode`, `Description` |
| `Transactions/GetTransactionByExternalUniqTran` | Look up by your external uniq id | `TerminalNumber`, `ApiName`, `ExternalUniqTranId` | `ResponseCode`, `Description`, transaction fields |

For `Transaction`, J2/J5 validation-only operations return `ResponseCode` `700` or
`701` which also count as success.

## Documents

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `Documents/CreateDocument` | Create standalone invoice/receipt | `ApiName`, `ApiPassword`, `Document` (see document-types.md), `Cash`, `Cheques` | `ResponseCode`, `Description`, `DocumentType`, `DocumentNumber`, `AccountId`, `DocumentUrl` |
| `Documents/CancelDoc` | Cancel/void a document | `ApiName`, `ApiPassword`, document identifier fields | `ResponseCode`, `Description` |
| `Documents/SendAllDocumentsToEmail` | Email all docs for a deal | account/deal identifier, `Email` | `ResponseCode`, `Description` |
| `Documents/GetReport` | Download a document report | date range, doc type, format | `ResponseCode`, `Description`, report data |
| `Documents/CrossDocument` | Link related documents | document identifiers | `ResponseCode`, `Description` |
| `Documents/CreateDocumentUrl` | Get a URL for a document-creation form | document parameters | `ResponseCode`, `Description`, `Url` |
| `Documents/ExternalShopCreateDocument` | Create a document for an external shop integration | `Document`, shop fields | `ResponseCode`, `Description` |

There is no dedicated `Documents/CreateTaxInvoice` endpoint in the V11 schema. To
issue a tax invoice, call `Documents/CreateDocument` with
`DocumentTypeToCreate: "TaxInvoice"` (or `"TaxInvoiceAndReceipt"`); see
document-types.md for the full enum.

## RecuringPayments

Note the path spelling: `RecuringPayments` (single `r`), as it appears in the
official V11 schema.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `RecuringPayments/GetRecurringPayment` | GET | Get recurring charge details |
| `RecuringPayments/GetRecurringPaymentHistory` | GET | Payment history for a recurring plan |
| `RecuringPayments/IsBankNumberValid` | GET | Validate an Israeli bank account |
| `RecuringPayments/GetMuhlafimByDate` | POST | List replaced-card tokens by date |
| `RecuringPayments/GetMuhlafimFile` | POST | Download the replaced-card file |
| `RecuringPayments/ChangeStatusForHistoryRecurringToIrrevocable` | POST | Mark a recurring history entry irrevocable |

There is no `GetNewMuhlafim`, `UpdateMuhlafimDone`, or `SuspendedDealActivateOne`
endpoint in the V11 schema; do not invoke those.

## Financial

| Endpoint | Purpose |
|----------|---------|
| `Financial/CreditCardTransactions` | Credit card transaction report |
| `Financial/CreditCardTransactionsHalted` | Halted credit card transactions |
| `Financial/FinancialTransactions` | Financial transaction report |
| `Financial/BankDeposites` | Bank deposit records |
| `Financial/GetSlikaInvoices` | Processing-fee invoices |
| `Financial/GetMoneyTransfers` | Money transfer records |

## CompanyOperations

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `CompanyOperations/NewCompany` | POST | Register a new merchant |
| `CompanyOperations/GetCompanyStatus` | GET | Check merchant account status |
| `CompanyOperations/GetCompanyStatusV2` | GET | Merchant account status (v2) |
| `CompanyOperations/GetBanks` / `GetBanksBranches` / `GetCities` / `GetStreets` / `GetCountries` | GET | Reference data lookups |

## Common Parameters

| Parameter | Type | Notes |
|-----------|------|-------|
| `ISOCoinId` | int | `1` = ILS, `2` = USD, the rest follow the ISO currency list |
| `Language` | string | `he`, `en`, `ru`, `sp` (Low Profile page language) |
| `ReturnValue` | string | Your order id, returned unchanged in `GetLpResult` and webhooks |
| `NumOfPayments` | int | Installment count (tashlumim); `1` = single charge |

## Alternative Payment Methods on Low Profile

| Method | Exposure on Low Profile | Where to enable |
|--------|------------------------|-----------------|
| Bit | `UrlToBit` field on `CreateLowProfileResponse` | Cardcom admin panel, terminal settings |
| PayPal | `UrlToPayPal` field on `CreateLowProfileResponse` | Cardcom admin panel, terminal settings |
| Apple Pay | wallet button rendered inside the hosted Low Profile page | Cardcom admin panel, terminal settings |
| Google Pay | wallet button rendered inside the hosted Low Profile page | Cardcom admin panel, terminal settings |

Bit and PayPal have explicit URL fields you can render separately. Apple Pay and Google Pay are rendered inside the hosted Low Profile page itself once enabled on the terminal, so the API response does not expose dedicated URL fields for them.

## API Version

V11 is the current API as of 2026. There is no public V12. Legacy `.aspx` interfaces with integer document codes (e.g. `101`, `400`) and the `DealResponse` shape predate V11; do not use them in new integrations.

## API Docs

Official documentation: `https://secure.cardcom.solutions/Api/v11/Docs`
Support center: `https://support.cardcom.solutions`
