#!/usr/bin/env python3
"""
Green Invoice API Client

A helper script for common Green Invoice (Morning) API operations:
- Authenticate and get JWT token
- Create documents (invoices, receipts, credit notes)
- Search and list documents
- Manage clients (create, search, list)

Usage:
    python3 green-invoice-client.py auth --key-id YOUR_KEY_ID --key-secret YOUR_SECRET
    python3 green-invoice-client.py create-document --token TOKEN --type 320 --client-name "Name" --client-email "email@example.com" --description "Service" --amount 5000
    python3 green-invoice-client.py search-documents --token TOKEN --from-date 2026-01-01 --to-date 2026-03-31
    python3 green-invoice-client.py create-client --token TOKEN --name "Client Name" --email "email@example.com"
    python3 green-invoice-client.py search-clients --token TOKEN --name "Client"
    python3 green-invoice-client.py get-document --token TOKEN --id DOCUMENT_ID

Environment:
    Set GREEN_INVOICE_ENV=sandbox to use sandbox environment.
    Default is production.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import os

PROD_BASE = "https://api.greeninvoice.co.il/api/v1"
SANDBOX_BASE = "https://sandbox.d.greeninvoice.co.il/api/v1"

DOCUMENT_TYPES = {
    10: "Price Quote",
    100: "Order",
    200: "Delivery Note",
    210: "Return Note",
    300: "Transaction Invoice",
    305: "Tax Invoice",
    320: "Tax Invoice-Receipt",
    330: "Credit Note",
    400: "Receipt",
    405: "Donation Receipt",
    500: "Purchase Order",
    600: "Deposit Receipt",
    610: "Deposit Withdrawal",
}

PAYMENT_TYPES = {
    -1: "Unpaid",
    0: "Withholding Tax",
    1: "Cash",
    2: "Check",
    3: "Credit Card",
    4: "Bank Transfer",
    5: "PayPal",
    10: "Payment App",
    11: "Other",
}


def get_base_url():
    env = os.environ.get("GREEN_INVOICE_ENV", "production")
    if env == "sandbox":
        return SANDBOX_BASE
    return PROD_BASE


def api_request(method, path, token=None, data=None):
    url = f"{get_base_url()}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            response_data = resp.read().decode("utf-8")
            if response_data:
                return json.loads(response_data)
            return {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def cmd_auth(args):
    """Authenticate and get JWT token."""
    result = api_request("POST", "/account/token", data={
        "id": args.key_id,
        "secret": args.key_secret,
    })
    token = result.get("token", "")
    if token:
        print(f"Token: {token}")
        print(f"\nUse with: --token {token[:20]}...")
    else:
        print("Authentication failed. Check your credentials.", file=sys.stderr)
        sys.exit(1)


def cmd_create_document(args):
    """Create a new document."""
    doc_type = args.type
    if doc_type not in DOCUMENT_TYPES:
        print(f"Invalid document type: {doc_type}", file=sys.stderr)
        print(f"Valid types: {json.dumps(DOCUMENT_TYPES, indent=2)}", file=sys.stderr)
        sys.exit(1)

    payload = {
        "type": doc_type,
        "lang": args.lang,
        "currency": args.currency,
        "vatType": args.vat_type,
        "signed": True,
        "attachment": True,
        "client": {
            "name": args.client_name,
            "emails": [args.client_email],
            "add": True,
        },
        "income": [
            {
                "description": args.description,
                "quantity": args.quantity,
                "price": args.amount,
                "currency": args.currency,
            }
        ],
    }

    if args.date:
        payload["date"] = args.date
    if args.due_date:
        payload["dueDate"] = args.due_date
    if args.tax_id:
        payload["client"]["taxId"] = args.tax_id
    if args.payment_type is not None:
        payload["payment"] = [{
            "type": args.payment_type,
            "price": args.amount * args.quantity,
            "currency": args.currency,
        }]
        if args.date:
            payload["payment"][0]["date"] = args.date

    result = api_request("POST", "/documents", token=args.token, data=payload)
    print(f"Document created successfully!")
    print(f"  Type: {DOCUMENT_TYPES.get(doc_type, doc_type)}")
    print(f"  ID: {result.get('id', 'N/A')}")
    print(f"  Number: {result.get('number', 'N/A')}")
    print(f"  Total: {result.get('total', 'N/A')} {args.currency}")


def cmd_search_documents(args):
    """Search documents."""
    payload = {
        "page": args.page,
        "pageSize": args.page_size,
    }
    if args.from_date:
        payload["fromDate"] = args.from_date
    if args.to_date:
        payload["toDate"] = args.to_date
    if args.type:
        payload["type"] = [args.type]
    if args.status is not None:
        payload["status"] = [args.status]

    result = api_request("POST", "/documents/search", token=args.token, data=payload)
    items = result.get("items", [])
    total = result.get("total", 0)

    print(f"Found {total} documents (showing page {args.page + 1}):\n")
    for doc in items:
        doc_type = DOCUMENT_TYPES.get(doc.get("type", 0), "Unknown")
        client = doc.get("client", {}).get("name", "N/A")
        print(f"  #{doc.get('number', 'N/A')} | {doc_type} | {client} | "
              f"{doc.get('total', 0)} {doc.get('currency', 'ILS')} | "
              f"{doc.get('date', 'N/A')}")


def cmd_get_document(args):
    """Get a single document by ID."""
    result = api_request("GET", f"/documents/{args.id}", token=args.token)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_create_client(args):
    """Create a new client."""
    payload = {
        "name": args.name,
        "emails": [args.email],
    }
    if args.tax_id:
        payload["taxId"] = args.tax_id
    if args.city:
        payload["city"] = args.city
    if args.address:
        payload["address"] = args.address
    if args.phone:
        payload["phone"] = args.phone
    if args.payment_terms is not None:
        payload["paymentTerms"] = args.payment_terms

    result = api_request("POST", "/clients", token=args.token, data=payload)
    print(f"Client created successfully!")
    print(f"  ID: {result.get('id', 'N/A')}")
    print(f"  Name: {result.get('name', 'N/A')}")


def cmd_search_clients(args):
    """Search clients."""
    payload = {
        "page": args.page,
        "pageSize": args.page_size,
    }
    if args.name:
        payload["name"] = args.name
    if args.email:
        payload["email"] = args.email

    result = api_request("POST", "/clients/search", token=args.token, data=payload)
    items = result.get("items", [])
    total = result.get("total", 0)

    print(f"Found {total} clients (showing page {args.page + 1}):\n")
    for client in items:
        emails = ", ".join(client.get("emails", []))
        print(f"  {client.get('name', 'N/A')} | {emails} | "
              f"Tax ID: {client.get('taxId', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="Green Invoice (Morning) API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Set GREEN_INVOICE_ENV=sandbox to use sandbox environment."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # auth
    auth_parser = subparsers.add_parser("auth", help="Authenticate and get JWT token")
    auth_parser.add_argument("--key-id", required=True, help="API Key ID")
    auth_parser.add_argument("--key-secret", required=True, help="API Key Secret")

    # create-document
    doc_parser = subparsers.add_parser("create-document", help="Create a new document")
    doc_parser.add_argument("--token", required=True, help="JWT token")
    doc_parser.add_argument("--type", type=int, required=True, help="Document type code")
    doc_parser.add_argument("--client-name", required=True, help="Client name")
    doc_parser.add_argument("--client-email", required=True, help="Client email")
    doc_parser.add_argument("--description", required=True, help="Item description")
    doc_parser.add_argument("--amount", type=float, required=True, help="Item price")
    doc_parser.add_argument("--quantity", type=float, default=1, help="Item quantity")
    doc_parser.add_argument("--currency", default="ILS", help="Currency code")
    doc_parser.add_argument("--lang", default="he", choices=["he", "en"])
    doc_parser.add_argument("--vat-type", type=int, default=0, help="VAT type (0=default, 1=exempt, 2=mixed)")
    doc_parser.add_argument("--date", help="Document date (YYYY-MM-DD)")
    doc_parser.add_argument("--due-date", help="Due date (YYYY-MM-DD)")
    doc_parser.add_argument("--tax-id", help="Client tax ID")
    doc_parser.add_argument("--payment-type", type=int, help="Payment type code")

    # search-documents
    search_doc_parser = subparsers.add_parser("search-documents", help="Search documents")
    search_doc_parser.add_argument("--token", required=True, help="JWT token")
    search_doc_parser.add_argument("--from-date", help="From date (YYYY-MM-DD)")
    search_doc_parser.add_argument("--to-date", help="To date (YYYY-MM-DD)")
    search_doc_parser.add_argument("--type", type=int, help="Document type filter")
    search_doc_parser.add_argument("--status", type=int, help="Document status filter")
    search_doc_parser.add_argument("--page", type=int, default=0, help="Page number")
    search_doc_parser.add_argument("--page-size", type=int, default=25, help="Page size")

    # get-document
    get_doc_parser = subparsers.add_parser("get-document", help="Get document by ID")
    get_doc_parser.add_argument("--token", required=True, help="JWT token")
    get_doc_parser.add_argument("--id", required=True, help="Document ID")

    # create-client
    client_parser = subparsers.add_parser("create-client", help="Create a new client")
    client_parser.add_argument("--token", required=True, help="JWT token")
    client_parser.add_argument("--name", required=True, help="Client name")
    client_parser.add_argument("--email", required=True, help="Client email")
    client_parser.add_argument("--tax-id", help="Client tax ID")
    client_parser.add_argument("--city", help="Client city")
    client_parser.add_argument("--address", help="Client address")
    client_parser.add_argument("--phone", help="Client phone")
    client_parser.add_argument("--payment-terms", type=int, help="Payment terms code")

    # search-clients
    search_client_parser = subparsers.add_parser("search-clients", help="Search clients")
    search_client_parser.add_argument("--token", required=True, help="JWT token")
    search_client_parser.add_argument("--name", help="Client name filter")
    search_client_parser.add_argument("--email", help="Client email filter")
    search_client_parser.add_argument("--page", type=int, default=0, help="Page number")
    search_client_parser.add_argument("--page-size", type=int, default=25, help="Page size")

    args = parser.parse_args()

    commands = {
        "auth": cmd_auth,
        "create-document": cmd_create_document,
        "search-documents": cmd_search_documents,
        "get-document": cmd_get_document,
        "create-client": cmd_create_client,
        "search-clients": cmd_search_clients,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
