import {test} from 'node:test';
import assert from 'node:assert/strict';
import {get} from '../examples/node/soldfetch-client.mjs';
test('encodes query values and keeps credentials in headers',async()=>{
 let observed;
 const result=await get('/v1/scrape',{keyword:'sony & bose',sold:false,count:20},{key:'test-only',idempotencyKey:'one-operation',fetchImpl:async(url,options)=>{observed={url,options};return new Response('{"items":[]}',{status:200});}});
 assert.deepEqual(result,{items:[]});assert.equal(observed.url.origin,'https://soldfetch.com');assert.equal(observed.url.searchParams.get('keyword'),'sony & bose');assert.equal(observed.url.searchParams.get('sold'),'false');assert.ok(!observed.url.href.includes('test-only'));assert.equal(observed.options.headers['Idempotency-Key'],'one-operation');assert.equal(observed.options.redirect,'error');
});
test('rejects arbitrary destinations before making a request',async()=>{
 for(const path of ['https://evil.example/','//evil.example/','/v1/item/../../usage','/api/admin'])await assert.rejects(get(path,{}, {key:'test-only',fetchImpl:()=>{throw new Error('must not fetch');}}),/Unsupported/);
});
test('does not retry a failure or expose server response secrets',async()=>{
 let calls=0;await assert.rejects(get('/usage',{}, {key:'test-only',fetchImpl:async()=>{calls++;return new Response('private response',{status:401,headers:{'x-request-id':'request-123'}});}}),/HTTP 401; request ID: request-123/);assert.equal(calls,1);
});
