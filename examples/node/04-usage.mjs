import { get } from './soldfetch-client.mjs';
console.log(JSON.stringify(await get("/usage",{}), null, 2));
