import { get } from './soldfetch-client.mjs';
console.log(JSON.stringify(await get("/v1/scrape",{"keyword": "sony wh-1000xm5", "ebaySite": "ebay.com", "count": 20, "sold": false}), null, 2));
