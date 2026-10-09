#!/usr/bin/env bash
set -euo pipefail
: "${SOLDFETCH_API_KEY:?Set SOLDFETCH_API_KEY}"
# Each successful keyword costs one request. Do not retry the entire stream automatically.
curl --fail-with-body --no-buffer --max-time 130 'https://soldfetch.com/api/bulk-search' \
  -H "Authorization: Bearer $SOLDFETCH_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{"keywords":["sony wh-1000xm5","bose quietcomfort"],"count":20}'
