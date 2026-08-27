#!/usr/bin/env bash
# Grow Payment Gateway Helper Script
# Quick API calls for testing and debugging Grow integrations
#
# Usage:
#   export GROW_USER_ID="your-user-id"
#   export GROW_PAGE_CODE="your-page-code"
#   export GROW_API_KEY="your-api-key"  # optional
#   export GROW_ENV="sandbox"           # or "production"
#
#   ./grow-payment-helper.sh create-payment 149.90 "Test payment" "https://example.com/success" "https://example.com/cancel"
#   ./grow-payment-helper.sh get-transaction TRANSACTION_ID TRANSACTION_TOKEN
#   ./grow-payment-helper.sh approve TRANSACTION_ID TRANSACTION_TOKEN
#   ./grow-payment-helper.sh refund TRANSACTION_ID TRANSACTION_TOKEN 50.00
#   ./grow-payment-helper.sh create-link 99.00 "Invoice #123"
#
# The Grow Light API answers HTTP 200 for every call, including failures, and
# reports the outcome in the body (status 1 = success, status 0 = error). This
# script therefore inspects the body and exits non-zero on an API error, so a
# failed call cannot look like a successful one.

set -euo pipefail

# Determine base URL
if [ "${GROW_ENV:-sandbox}" = "production" ]; then
  BASE_URL="https://secure.meshulam.co.il"
else
  BASE_URL="https://sandbox.meshulam.co.il"
fi

API_BASE="${BASE_URL}/api/light/server/1.0"

# Post a form request and exit non-zero if the API reports an error in the body.
# GROW_API_KEY, when set, is sent as the X-API-KEY header; Grow returns HTTP 403
# with the message "לא נשלח X-API-KEY" when a call that needs it is missing it.
call_api() {
  local endpoint="$1"; shift
  local -a auth=()
  if [ -n "${GROW_API_KEY:-}" ]; then
    auth=(-H "X-API-KEY: ${GROW_API_KEY}")
  fi

  local body http
  # ${auth[@]+"${auth[@]}"} keeps an empty array safe under `set -u` on bash 3.2.
  body=$(curl -sS -w $'\n%{http_code}' -X POST "${API_BASE}/${endpoint}" ${auth[@]+"${auth[@]}"} "$@") || {
    echo "Error: request to ${endpoint} failed" >&2; exit 1; }
  http="${body##*$'\n'}"
  body="${body%$'\n'*}"

  printf '%s\n' "$body" | python3 -c '
import sys, json
raw = sys.stdin.read()
try:
    data = json.loads(raw)
except json.JSONDecodeError:
    sys.stderr.write("Error: non-JSON response:\n" + raw[:500] + "\n"); sys.exit(1)
print(json.dumps(data, indent=4, ensure_ascii=False))
if str(data.get("status")) != "1":
    err = data.get("err")
    if isinstance(err, dict):
        detail = "err.id=%s %s" % (err.get("id"), err.get("message"))
    else:
        detail = "err=%r" % (err,)
    sys.stderr.write("Error: Grow API reported failure (%s)\n" % detail)
    sys.exit(1)
' || exit 1

  if [ "$http" != "200" ]; then
    echo "Note: unexpected HTTP status ${http} (the Light API normally answers 200)" >&2
  fi
}

# Validate required env vars
if [ -z "${GROW_USER_ID:-}" ] || [ -z "${GROW_PAGE_CODE:-}" ]; then
  echo "Error: GROW_USER_ID and GROW_PAGE_CODE must be set"
  echo "Usage: export GROW_USER_ID=... GROW_PAGE_CODE=... ./grow-payment-helper.sh <command> [args]"
  exit 1
fi

command="${1:-help}"
shift || true

case "$command" in
  create-payment)
    SUM="${1:?Sum required}"
    DESC="${2:?Description required}"
    SUCCESS_URL="${3:?Success URL required}"
    CANCEL_URL="${4:?Cancel URL required}"

    call_api createPaymentProcess \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "userId=${GROW_USER_ID}" \
      -F "sum=${SUM}" \
      -F "description=${DESC}" \
      -F "successUrl=${SUCCESS_URL}" \
      -F "cancelUrl=${CANCEL_URL}"
    ;;

  get-transaction)
    # Both identifiers are required; sending only one returns err.id 54.
    TXN_ID="${1:?Transaction ID required}"
    TXN_TOKEN="${2:?Transaction token required}"

    call_api getTransactionInfo \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "transactionId=${TXN_ID}" \
      -F "transactionToken=${TXN_TOKEN}"
    ;;

  get-process)
    PROCESS_ID="${1:?Process ID required}"
    PROCESS_TOKEN="${2:?Process token required}"

    call_api getPaymentProcessInfo \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "processId=${PROCESS_ID}" \
      -F "processToken=${PROCESS_TOKEN}"
    ;;

  approve)
    # approveTransaction needs BOTH ids from the callback.
    TXN_ID="${1:?Transaction ID required}"
    TXN_TOKEN="${2:?Transaction token required}"

    call_api approveTransaction \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "transactionId=${TXN_ID}" \
      -F "transactionToken=${TXN_TOKEN}"
    ;;

  refund)
    # The amount parameter is refundSum; "sum" is not accepted here.
    TXN_ID="${1:?Transaction ID required}"
    TXN_TOKEN="${2:?Transaction token required}"
    REFUND_SUM="${3:?Refund amount required}"

    call_api refundTransaction \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "transactionId=${TXN_ID}" \
      -F "transactionToken=${TXN_TOKEN}" \
      -F "refundSum=${REFUND_SUM}"
    ;;

  cancel-bit)
    # Keyed by the PROCESS, not the transaction.
    PROCESS_ID="${1:?Process ID required}"
    PROCESS_TOKEN="${2:?Process token required}"

    call_api cancelBitTransaction \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "processId=${PROCESS_ID}" \
      -F "processToken=${PROCESS_TOKEN}"
    ;;

  create-link)
    SUM="${1:?Sum required}"
    DESC="${2:?Description required}"

    call_api createPaymentLink \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "userId=${GROW_USER_ID}" \
      -F "sum=${SUM}" \
      -F "description=${DESC}"
    ;;

  charge-token)
    # paymentNum is required; 1 means a single non-instalment charge.
    # UNIQUE_ID is the idempotency key: on a timeout, re-send the SAME value
    # rather than generating a new one, or you risk double-charging the card.
    TOKEN="${1:?Token required}"
    SUM="${2:?Sum required}"
    PAYMENT_NUM="${3:-1}"
    UNIQUE_ID="${4:-$(date +%s)-$$}"

    call_api createTransactionWithToken \
      -F "userId=${GROW_USER_ID}" \
      -F "cardToken=${TOKEN}" \
      -F "sum=${SUM}" \
      -F "description=Token charge" \
      -F "paymentType=2" \
      -F "paymentNum=${PAYMENT_NUM}" \
      -F "transactionUniqueIdentifier=${UNIQUE_ID}"
    ;;

  help|*)
    echo "Grow Payment Gateway Helper"
    echo ""
    echo "Commands:"
    echo "  create-payment <sum> <description> <success_url> <cancel_url>"
    echo "  get-transaction <transaction_id> <transaction_token>"
    echo "  get-process <process_id> <process_token>"
    echo "  approve <transaction_id> <transaction_token>"
    echo "  refund <transaction_id> <transaction_token> <amount>"
    echo "  cancel-bit <process_id> <process_token>"
    echo "  create-link <sum> <description>"
    echo "  charge-token <token> <sum> [payment_num] [unique_id]"
    echo ""
    echo "Environment: ${GROW_ENV:-sandbox} (${BASE_URL})"
    ;;
esac
