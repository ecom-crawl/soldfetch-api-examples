"""At most two charged pages. Keep count and filters fixed."""
import json
from soldfetch_client import get

def collect(get_page=get, max_pages=2):
    if not 1 <= max_pages <= 100:
        raise ValueError('max_pages must be 1–100')
    seen = set()
    for page in range(1, max_pages + 1):
        result = get_page('/v1/scrape', {'keyword': 'sony wh-1000xm5', 'ebaySite': 'ebay.com', 'count': 20, 'page': page})
        items = result.get('items', [])
        fresh = [item for item in items if item.get('itemId') and item['itemId'] not in seen]
        if not fresh:
            return
        for item in fresh:
            if item['itemId'] not in seen:
                seen.add(item['itemId'])
                yield item
        if result.get('hasNextPage') is False:
            return

if __name__ == '__main__':
    print(json.dumps(list(collect()), indent=2))
