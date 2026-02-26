# Cardcom REST API V11 Endpoint Reference

## Base URL & Authentication

- **Base:** `https://secure.cardcom.solutions/api/v11/`
- **Auth fields (every request):** `TerminalNumber`, `ApiName`, `ApiPassword`
- **Test terminal:** `1000`, ApiName: `bWlyb24gY2FyZGNvbQ==`, test card: `4580000000000000`
- **Method:** All endpoints are `POST` with `Content-Type: application/json`

## LowProfile (Hosted Payment Page)

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `LowProfile/Create` | Create hosted payment page | `Amount`, `SuccessRedirectUrl`, `FailedRedirectUrl`, `WebHookUrl`, `Document`, `CoinID`, `Language`, `ReturnValue` | `LowProfileCode`, `Url` |
| `LowProfile/GetLpResult` | Retrieve payment result | `LowProfileCode` | `DealResponse`, `Token`, `InternalDealNumber`, `InvoiceNumber`, `CardOwnerName`, `Last4Digits` |

## Transactions

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `Transactions/Transaction` | Charge a token (server-to-server) | `Token`, `CardValidityMonth`, `CardValidityYear`, `Amount`, `Document` | `DealResponse`, `InternalDealNumber`, `InvoiceNumber` |
| `Transactions/RefundByTransactionId` | Refund a transaction | `TransactionId`, `Amount`, `Document` (DocType=2 for credit note) | `DealResponse`, `InternalDealNumber` |
| `Transactions/ListTransactions` | List transactions by date range | `FromDate`, `ToDate`, `PageNumber`, `PageSize` | `Transactions[]`, `TotalCount` |
| `Transactions/GetTransactionInfoById` | Get single transaction details | `TransactionId` | `DealResponse`, `Amount`, `CardOwnerName`, `Last4Digits`, `Token` |
| `Transactions/SpecialTransactions` | Credit, installments, special deals | `Token`, `Amount`, `NumOfPayments`, `SpecialTransactionType` | `DealResponse`, `InternalDealNumber` |

## Documents

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `Documents/CreateDocument` | Create standalone invoice/receipt | `Document` (see document-types.md) | `InvoiceNumber`, `InvoiceType`, `Link` |
| `Documents/CreateTaxInvoice` | Create tax invoice specifically | `Document` with DocTypeToCreate=1 | `InvoiceNumber`, `Link` |
| `Documents/CancelDoc` | Cancel/void a document | `InvoiceNumber`, `InvoiceType` | `ResponseCode`, `Description` |
| `Documents/SendAllDocumentsToEmail` | Email all docs for a deal | `InternalDealNumber`, `Email` | `ResponseCode` |
| `Documents/GetReport` | Download document report | `FromDate`, `ToDate`, `DocType`, `Format` | `ReportUrl` or binary content |
| `Documents/CrossDocument` | Link related documents | `InvoiceNumber`, `CrossInvoiceNumber` | `ResponseCode` |
| `Documents/CreateDocumentUrl` | Get URL for document creation form | `DocTypeToCreate`, `ReturnValue` | `Url` |

## RecurringPayments

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `RecurringPayments/GetRecurringPayment` | Get recurring charge details | `RecurringPaymentId` | `Amount`, `Token`, `NextChargeDate`, `Status` |
| `RecurringPayments/GetRecurringPaymentHistory` | Payment history for a plan | `RecurringPaymentId` | `Payments[]` with dates, amounts, statuses |
| `RecurringPayments/GetMuhlafimFile` | Download failed charges file | `FromDate`, `ToDate` | File content (CSV/Excel) |
| `RecurringPayments/GetMuhlafimByDate` | List failed charges by date | `Date` | `FailedCharges[]` with reasons |
| `RecurringPayments/IsBankNumberValid` | Validate Israeli bank account | `BankNumber`, `BranchNumber`, `AccountNumber` | `IsValid`, `BankName` |

## Financial

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `Financial/CreditCardTransactions` | Download credit card transaction report | `FromDate`, `ToDate` | `Transactions[]` with settlement info |
| `Financial/BankDeposites` | Get bank deposit records | `FromDate`, `ToDate` | `Deposits[]` with amounts and dates |
| `Financial/GetSlikaInvoices` | Get processing fee invoices | `FromDate`, `ToDate` | `Invoices[]` |

## CompanyOperations

| Endpoint | Purpose | Key Request Fields | Key Response Fields |
|----------|---------|-------------------|-------------------|
| `CompanyOperations/NewCompany` | Register new merchant | `CompanyName`, `CompanyNumber`, `Email`, `Phone` | `TerminalNumber`, `ApiName`, `ApiPassword` |
| `CompanyOperations/GetCompanyStatus` | Check merchant account status | (auth fields only) | `Status`, `ActiveTerminals[]`, `Features[]` |

## Common Parameters

| Parameter | Type | Notes |
|-----------|------|-------|
| `CoinID` | int | 1=ILS, 2=USD, 3=EUR, 978=GBP |
| `Language` | string | `he`, `en`, `ar` |
| `ReturnValue` | string | Your order ID, returned unchanged in callbacks |
| `NumOfPayments` | int | Installment count (tashlumim), 1=single charge |

## API Docs

Official documentation: https://kb.cardcom.co.il/article/knowledgebase-api-v11/
