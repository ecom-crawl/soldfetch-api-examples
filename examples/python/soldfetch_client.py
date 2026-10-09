"""Standard-library SoldFetch client. No automatic retries or redirects."""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE_URL = "https://soldfetch.com"
ALLOWED = re.compile(r"/(?:v1/scrape(?:/category)?|v1/item/[0-9]{9,15}|usage|requests|v1/capabilities)")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def get(path, params=None, *, key=None, idempotency_key=None):
    if not ALLOWED.fullmatch(path):
        raise ValueError("Unsupported SoldFetch path")
    key = (key or os.environ.get("SOLDFETCH_API_KEY", "")).strip()
    if not key:
        raise ValueError("Set SOLDFETCH_API_KEY")
    params = {k: str(v).lower() if isinstance(v, bool) else v for k, v in (params or {}).items() if v is not None}
    url = BASE_URL + path + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + key, "Accept": "application/json",
        "Idempotency-Key": idempotency_key or str(uuid.uuid4()),
    })
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=65) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"SoldFetch HTTP {error.code}; request ID: {error.headers.get('x-request-id', 'unavailable')}") from None
    except urllib.error.URLError:
        raise RuntimeError("Could not reach SoldFetch; retry deliberately with the same idempotency key") from None
