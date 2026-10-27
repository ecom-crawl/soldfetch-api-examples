# SoldFetch API examples

Runnable eBay search and item examples. These clients call the hosted [SoldFetch API](https://soldfetch.com); this repository does not contain the service implementation.

## Run

Set `SOLDFETCH_API_KEY` in your shell. Never commit the value. Examples use only standard libraries (Node 20+, Python 3.9+, Go 1.22+).

```bash
export SOLDFETCH_API_KEY="YOUR_SOLDFETCH_API_KEY"
bash examples/curl/quickstart.sh
node examples/node/01-search.mjs
node examples/node/02-item.mjs
node examples/node/03-active-listings.mjs
node examples/node/04-usage.mjs
python3 examples/python/01_search.py
python3 examples/python/02_item.py 377534750427
python3 examples/python/03_pagination.py
(cd examples/go && go run .)
```

Run examples individually. Each successful search or item lookup costs one request. The pagination example permits two charged pages. Usage lookup is free. `bash examples/curl/bulk-search.sh` streams two keywords, costing up to two requests. Old sample item IDs may become unavailable; use an ID from your search results.

Clients enforce the SoldFetch origin, reject credential-bearing redirects, and use timeouts. They do not automatically retry. Node and Python helpers accept an idempotency key so a deliberate retry can reuse the same key; a new operation needs a new key. The Go example makes one request without retries.

Preserve currency, condition, retrieval time, and warnings. Displayed prices are not verified accepted-offer amounts. Search sale dates and exact product identity are unverified. Category-only sold searches can return an uncharged 503. Stop pagination on empty/repeated pages or `hasNextPage=false`, and keep `count` constant.

## Check

```bash
npm test
npm run test:live
```

Offline tests check request construction, credential handling, and pagination stop conditions. Live checks fetch the public contract and verify unauthenticated rejection; they do not spend requests. To verify a real search deliberately, set a key and run one example above.

[Documentation](https://docs.soldfetch.com) · [MCP](https://github.com/ricciflow-api/soldfetch-mcp) · [Skills](https://github.com/ricciflow-api/soldfetch-agent-skills) · [MIT](LICENSE)
