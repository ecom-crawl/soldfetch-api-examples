import json
import sys
from soldfetch_client import get
item_id = sys.argv[1] if len(sys.argv) > 1 else '377534750427'
print(json.dumps(get('/v1/item/' + item_id, {'ebaySite': 'ebay.com'}), indent=2))
