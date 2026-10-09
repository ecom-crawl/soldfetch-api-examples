import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
for (const [command,args] of [['node',['--test','tests/client.test.mjs']],['python3',['-m','unittest','discover','-s','tests','-v']],['bash',['-n','examples/curl/quickstart.sh']],['bash',['-n','examples/curl/bulk-search.sh']]]) {
 const result=spawnSync(command,args,{stdio:'inherit'});assert.equal(result.status,0,command+' failed');
}
