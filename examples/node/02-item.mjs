import { get } from './soldfetch-client.mjs';
console.log(JSON.stringify(await get("/v1/item/377534750427",{"ebaySite": "ebay.com"}), null, 2));
