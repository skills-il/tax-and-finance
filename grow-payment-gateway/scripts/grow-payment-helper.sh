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
#   ./grow-payment-helper.sh get-transaction TRANSACTION_ID
#   ./grow-payment-helper.sh approve TRANSACTION_ID
#   ./grow-payment-helper.sh refund TRANSACTION_ID 50.00
#   ./grow-payment-helper.sh create-link 99.00 "Invoice #123"

set -euo pipefail

# Determine base URL
if [ "${GROW_ENV:-sandbox}" = "production" ]; then
  BASE_URL="https://secure.meshulam.co.il"
else
  BASE_URL="https://sandbox.meshulam.co.il"
fi

API_BASE="${BASE_URL}/api/light/server/1.0"

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

    curl -s -X POST "${API_BASE}/createPaymentProcess" \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "userId=${GROW_USER_ID}" \
      -F "sum=${SUM}" \
      -F "description=${DESC}" \
      -F "successUrl=${SUCCESS_URL}" \
      -F "cancelUrl=${CANCEL_URL}" | python3 -m json.tool
    ;;

  get-transaction)
    TXN_ID="${1:?Transaction ID required}"

    curl -s -X POST "${API_BASE}/getTransactionInfo" \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "transactionId=${TXN_ID}" | python3 -m json.tool
    ;;

  get-process)
    PROCESS_ID="${1:?Process ID required}"

    curl -s -X POST "${API_BASE}/getPaymentProcessInfo" \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "processId=${PROCESS_ID}" | python3 -m json.tool
    ;;

  approve)
    TXN_ID="${1:?Transaction ID required}"

    curl -s -X POST "${API_BASE}/approveTransaction" \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "transactionId=${TXN_ID}" | python3 -m json.tool
    ;;

  refund)
    TXN_ID="${1:?Transaction ID required}"
    REFUND_SUM="${2:?Refund amount required}"

    curl -s -X POST "${API_BASE}/refundTransaction" \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "transactionId=${TXN_ID}" \
      -F "refundSum=${REFUND_SUM}" | python3 -m json.tool
    ;;

  cancel-bit)
    TXN_ID="${1:?Transaction ID required}"

    curl -s -X POST "${API_BASE}/cancelBitTransaction" \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "transactionId=${TXN_ID}" | python3 -m json.tool
    ;;

  create-link)
    SUM="${1:?Sum required}"
    DESC="${2:?Description required}"

    curl -s -X POST "${API_BASE}/createPaymentLink" \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "userId=${GROW_USER_ID}" \
      -F "sum=${SUM}" \
      -F "description=${DESC}" | python3 -m json.tool
    ;;

  charge-token)
    TOKEN="${1:?Token required}"
    SUM="${2:?Sum required}"

    curl -s -X POST "${API_BASE}/createTransactionWithToken" \
      -F "pageCode=${GROW_PAGE_CODE}" \
      -F "userId=${GROW_USER_ID}" \
      -F "token=${TOKEN}" \
      -F "sum=${SUM}" | python3 -m json.tool
    ;;

  help|*)
    echo "Grow Payment Gateway Helper"
    echo ""
    echo "Commands:"
    echo "  create-payment <sum> <description> <success_url> <cancel_url>"
    echo "  get-transaction <transaction_id>"
    echo "  get-process <process_id>"
    echo "  approve <transaction_id>"
    echo "  refund <transaction_id> <amount>"
    echo "  cancel-bit <transaction_id>"
    echo "  create-link <sum> <description>"
    echo "  charge-token <token> <sum>"
    echo ""
    echo "Environment: ${GROW_ENV:-sandbox} (${BASE_URL})"
    ;;
esac
