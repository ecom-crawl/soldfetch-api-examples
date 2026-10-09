import json
from soldfetch_client import get
print(json.dumps(get('/v1/scrape', {'keyword': 'sony wh-1000xm5', 'ebaySite': 'ebay.com', 'count': 20}), indent=2))
