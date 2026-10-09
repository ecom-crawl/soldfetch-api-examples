#!/usr/bin/env bash
set -euo pipefail
: "${SOLDFETCH_API_KEY:?Set SOLDFETCH_API_KEY}"
curl --fail-with-body --max-time 65 --get 'https://soldfetch.com/v1/scrape' \
  --data-urlencode 'keyword=sony wh-1000xm5' \
  --data-urlencode 'ebaySite=ebay.com' \
  --data-urlencode 'count=20' \
  -H "Authorization: Bearer $SOLDFETCH_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)"
