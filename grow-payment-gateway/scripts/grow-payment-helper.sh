#!/usr/bin/env bash
# Grow Payment Gateway Helper Script
# Quick Light API calls for testing and debugging Grow integrations.
#
# Usage:
#   export GROW_USER_ID="your-user-id"
#   export GROW_PAGE_CODE="your-page-code"
#   export MESHULAM_API_KEY="your-api-key"   # optional, platform setups only
#   export GROW_ENV="sandbox"                 # default; "production" also needs GROW_ALLOW_PRODUCTION=1
#
#   ./grow-payment-helper.sh create-payment 149.90 "Test payment" "Israel Israeli" 0501234567 \
#       "https://example.com/success" "https://example.com/cancel"
#   ./grow-payment-helper.sh get-transaction TRANSACTION_ID TRANSACTION_TOKEN
#   ./grow-payment-helper.sh approve callback-fields.txt
#   ./grow-payment-helper.sh refund TRANSACTION_ID TRANSACTION_TOKEN 50.00
#   ./grow-payment-helper.sh charge-token 99.00 "Israel Israeli" 0501234567 100001 < card-token.txt
#
# The Grow Light API answers HTTP 200 for every call, including failures, and
# reports the outcome in the body (status 1 = success, status 0 = error). This
# script inspects the body and exits non-zero on an API error.
#
# Every form field is handed to curl through a config file read from stdin
# (curl -K -) as a literal "form-string": nothing secret appears in the process
# list, and a value starting with "@" or "<" is sent as text, never read as a
# local file. Token fields are masked in the printed response.
#
# Payment links are not wrapped here: the documented CreatePaymentLink and
# UpdatePaymentLink endpoints live on a different host with a different
# contract (see SKILL.md Step 8).

set -euo pipefail

usage() {
  echo "Grow Payment Gateway Helper"
  echo ""
  echo "Commands:"
  echo "  create-payment <sum> <description> <full_name> <phone> <success_url> <cancel_url>"
  echo "  get-transaction <transaction_id> <transaction_token>"
  echo "  get-process <process_id> <process_token>"
  echo "  approve <callback_fields_file>"
  echo "  refund <transaction_id> <transaction_token> <amount>"
  echo "  cancel-bit <process_id> <process_token>"
  echo "  charge-token <sum> <full_name> <phone> <unique_id> [payment_num] [group_id]   (card token on stdin)"
  echo ""
  echo "approve: <callback_fields_file> holds the server update's data fields, one"
  echo "name=value per line (transactionId=..., transactionToken=..., sum=..., ...)."
  echo "Grow's docs say to send pageCode plus ALL data received in the server update."
  echo ""
  echo "charge-token: the card token is read from stdin; it is data.cardToken from the"
  echo "callback, NOT transactionToken. <unique_id> must be a NEW integer for every"
  echo "attempt (a reused value is rejected even if the first attempt failed)."
  echo "[group_id] stays stable for one logical charge and must be unique across your"
  echo "business (for example a charge-row primary key), never a bare date. Both must be"
  echo "positive integers with no leading zeros, below 4,294,967,295."
  echo ""
  echo "Environment: GROW_ENV=${GROW_ENV:-sandbox}"
}

command="${1:-help}"
shift || true

case "$command" in
  help|-h|--help) usage; exit 0 ;;
  create-payment|get-transaction|get-process|approve|refund|cancel-bit|charge-token) ;;
  *) echo "Error: unknown command '${command}'" >&2; usage >&2; exit 2 ;;
esac

# GROW_API_KEY was renamed to MESHULAM_API_KEY and is no longer read.
if [ -z "${MESHULAM_API_KEY:-}" ] && [ -n "${GROW_API_KEY:-}" ]; then
  echo "Error: GROW_API_KEY was renamed to MESHULAM_API_KEY. Rename the variable in your environment (export MESHULAM_API_KEY=... and unset GROW_API_KEY) and run again." >&2
  exit 1
fi

# The two hosts are pinned. There is deliberately no base-URL override, so a
# credential can never be sent anywhere except Grow's own Light API hosts.
case "${GROW_ENV:-sandbox}" in
  sandbox)
    API_BASE="https://sandbox.meshulam.co.il/api/light/server/1.0" ;;
  production)
    if [ "${GROW_ALLOW_PRODUCTION:-}" != "1" ]; then
      echo "Error: GROW_ENV=production calls the live gateway (real money). Set GROW_ALLOW_PRODUCTION=1 to confirm." >&2
      exit 1
    fi
    API_BASE="https://secure.meshulam.co.il/api/light/server/1.0" ;;
  *)
    echo "Error: GROW_ENV must be 'sandbox' or 'production'" >&2; exit 1 ;;
esac

if [ -z "${GROW_USER_ID:-}" ] || [ -z "${GROW_PAGE_CODE:-}" ]; then
  echo "Error: GROW_USER_ID and GROW_PAGE_CODE must be set" >&2
  exit 1
fi

require_int() {
  case "$2" in
    ''|*[!0-9]*) echo "Error: $1 must be a positive integer, got '$2'" >&2; exit 1 ;;
  esac
}

# Grow's identifier rule (err.id 1013): a positive integer, no leading zeros,
# below 4,294,967,295. Epoch milliseconds do NOT fit.
require_grow_id() {
  require_int "$1" "$2"
  case "$2" in
    0*) echo "Error: $1 must not have leading zeros, got '$2'" >&2; exit 1 ;;
  esac
  if [ "${#2}" -gt 10 ] || { [ "${#2}" -eq 10 ] && [[ "$2" > "4294967294" ]]; }; then
    echo "Error: $1 must be below 4,294,967,295, got '$2'" >&2; exit 1
  fi
}

# Collected form fields, appended as curl config "form-string" lines.
FORM=""
field() {
  local name="$1" value="$2"
  case "$name$value" in
    *$'\n'*|*$'\r'*) echo "Error: field '$name' contains a line break" >&2; exit 1 ;;
  esac
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  FORM+="form-string = \"${name}=${value}\""$'\n'
}

# POST the collected fields and exit non-zero if the API reports an error.
# MESHULAM_API_KEY, when set, is added as the apiKey form field.
call_api() {
  local endpoint="$1" body http cfg
  if [ -n "${MESHULAM_API_KEY:-}" ]; then
    field apiKey "${MESHULAM_API_KEY}"
  fi
  cfg="url = \"${API_BASE}/${endpoint}\""$'\n'"request = \"POST\""$'\n'"${FORM}"
  body=$(printf '%s' "$cfg" | curl -sS --connect-timeout 10 --max-time 60 -w $'\n%{http_code}' -K -) || {
    echo "Error: request to ${endpoint} failed or timed out. For a token charge, reconcile before retrying (SKILL.md Step 5.6)." >&2; exit 1; }
  http="${body##*$'\n'}"
  body="${body%$'\n'*}"

  printf '%s\n' "$body" | python3 -I -c '
import sys, json
raw = sys.stdin.read()
try:
    data = json.loads(raw)
except json.JSONDecodeError:
    sys.stderr.write("Error: non-JSON response (first 300 chars):\n" + raw[:300] + "\n"); sys.exit(1)
def mask(o):
    if isinstance(o, dict):
        return {k: ("***" + str(v)[-4:] if isinstance(v, (str, int)) and str(v) and k.lower().endswith("token") else mask(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [mask(x) for x in o]
    return o
print(json.dumps(mask(data), indent=4, ensure_ascii=False))
if str(data.get("status")) != "1":
    err = data.get("err")
    if isinstance(err, dict):
        eid = err.get("id")
        if isinstance(eid, dict):
            detail = "err.id=%s %s" % (eid.get("id"), eid.get("content"))
        else:
            detail = "err.id=%s %s" % (eid, err.get("message"))
    else:
        detail = "err=%r" % (err,)
    sys.stderr.write("Error: Grow API reported failure (%s)\n" % detail)
    sys.exit(1)
' || exit 1

  if [ "$http" != "200" ]; then
    echo "Note: unexpected HTTP status ${http} (the Light API normally answers 200)" >&2
  fi
}

case "$command" in
  create-payment)
    field pageCode "${GROW_PAGE_CODE}"
    field userId "${GROW_USER_ID}"
    field sum "${1:?Sum required}"
    field description "${2:?Description required}"
    field "pageField[fullName]" "${3:?Full name required (at least two names)}"
    field "pageField[phone]" "${4:?Israeli mobile number required}"
    field successUrl "${5:?Success URL required}"
    field cancelUrl "${6:?Cancel URL required}"
    call_api createPaymentProcess
    ;;

  get-transaction)
    field pageCode "${GROW_PAGE_CODE}"
    field transactionId "${1:?Transaction ID required}"
    field transactionToken "${2:?Transaction token required}"
    call_api getTransactionInfo
    ;;

  get-process)
    field pageCode "${GROW_PAGE_CODE}"
    field processId "${1:?Process ID required}"
    field processToken "${2:?Process token required}"
    call_api getPaymentProcessInfo
    ;;

  approve)
    # Grow: send the pageCode and all data received from the server update.
    FIELDS_FILE="${1:?Callback fields file required (name=value per line)}"
    [ -r "$FIELDS_FILE" ] || { echo "Error: cannot read $FIELDS_FILE" >&2; exit 1; }
    field pageCode "${GROW_PAGE_CODE}"
    have_id=0; have_token=0
    while IFS= read -r line || [ -n "$line" ]; do
      line="${line%$'\r'}"
      case "$line" in ''|'#'*) continue ;; *=*) ;; *) echo "Error: bad line in $FIELDS_FILE (expected name=value)" >&2; exit 1 ;; esac
      name="${line%%=*}"; value="${line#*=}"
      [ "$name" = "pageCode" ] && continue
      [ "$name" = "transactionId" ] && have_id=1
      [ "$name" = "transactionToken" ] && have_token=1
      field "$name" "$value"
    done < "$FIELDS_FILE"
    if [ "$have_id" != 1 ] || [ "$have_token" != 1 ]; then
      echo "Error: $FIELDS_FILE must contain transactionId and transactionToken" >&2; exit 1
    fi
    call_api approveTransaction
    ;;

  refund)
    # The amount parameter is refundSum; "sum" is not accepted here.
    field userId "${GROW_USER_ID}"
    field pageCode "${GROW_PAGE_CODE}"
    field transactionId "${1:?Transaction ID required}"
    field transactionToken "${2:?Transaction token required}"
    field refundSum "${3:?Refund amount required}"
    call_api refundTransaction
    ;;

  cancel-bit)
    # Keyed by the PROCESS, not the transaction.
    field pageCode "${GROW_PAGE_CODE}"
    field processId "${1:?Process ID required}"
    field processToken "${2:?Process token required}"
    call_api cancelBitTransaction
    ;;

  charge-token)
    SUM="${1:?Sum required}"
    FULL_NAME="${2:?Full name required (at least two names)}"
    PHONE="${3:?Israeli mobile number required}"
    UNIQUE_ID="${4:?Unique id required: a new integer per attempt, persisted before the call}"
    PAYMENT_NUM="${5:-1}"
    GROUP_ID="${6:-}"
    require_grow_id "unique_id" "$UNIQUE_ID"
    require_int "payment_num" "$PAYMENT_NUM"
    [ -t 0 ] && echo "Paste the card token (data.cardToken) and press Enter:" >&2
    IFS= read -r CARD_TOKEN || true
    CARD_TOKEN="${CARD_TOKEN%$'\r'}"
    [ -n "$CARD_TOKEN" ] || { echo "Error: card token required on stdin" >&2; exit 1; }

    field userId "${GROW_USER_ID}"
    field cardToken "$CARD_TOKEN"
    field sum "$SUM"
    field description "Token charge"
    field paymentType 2
    field paymentNum "$PAYMENT_NUM"
    field "pageField[fullName]" "$FULL_NAME"
    field "pageField[phone]" "$PHONE"
    field transactionUniqueIdentifier "$UNIQUE_ID"
    if [ -n "$GROUP_ID" ]; then
      require_grow_id "group_id" "$GROUP_ID"
      field transactionGroupIdentifier "$GROUP_ID"
    fi
    call_api createTransactionWithToken
    ;;
esac
