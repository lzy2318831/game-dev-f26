// Final failure presentation only. No browser, network, or model calls.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(path.join(__dirname,'../fusion/geometry_status.js'),'utf8');
const nodes={liveStatus:{},liveBudget:{},liveStart:{},startButton:{},resultTitle:{},resultDetail:{}};
const c={setTimeout,clearTimeout,liveLabels:()=>{},showResult:()=>{},liveInfo:{reason:'no_reliable_candidate'},$:id=>nodes[id]};
vm.createContext(c);vm.runInContext(source,c);c.liveLabels();c.showResult();
assert.match(nodes.liveStatus.textContent,/No supported shot candidate/);
assert.match(nodes.resultDetail.textContent,/no other agent/);
c.liveInfo.reason='invalid_candidate_selection';c.showResult();
assert.match(nodes.resultDetail.textContent,/no replacement move or retry/);
c.liveInfo.reason='user_cancelled';c.liveLabels();
assert.match(nodes.liveStatus.textContent,/No further requests/);
assert.equal(c.geometryFailureMessage('unknown-reason'),null);
for(const reason of ['request_timeout','parent_watchdog','http_timeout'])
  assert.match(c.geometryFailureMessage(reason),/timed out/);
console.log('PASS: geometry failure/result messages, no-candidate stop and cancellation labels');
(async()=>{
  const calls=[];let reloads=0,confirmations=0;
  c.liveToken=null;c.liveLeaving=false;c.toast=()=>{};
  c.api=async()=>({nonce:'old',state:{live:{phase:'failed'}}});
  c.livePost=async path=>{calls.push(path);return path==='/live/leave'?{safe_to_navigate:true}:{nonce:'fresh',state:{live:{phase:'waiting'}}};};
  const fresh=await c.geometryLoadInfo();
  assert.equal(fresh.nonce,'fresh');assert.deepEqual(calls,['/live/leave','/live/new']);
  assert.ok(!calls.includes('/live/start'));
  c.liveInfo={phase:'failed',reason:'http_error'};c.state={outcome:{failure:true}};c.showResult();
  assert.match(nodes.resultTitle.textContent,/match incomplete/);
  c.window={location:{reload:()=>reloads++}};c.confirmLive=()=>confirmations++;
  await c.geometryNewOrConfirm();assert.equal(reloads,1);assert.equal(confirmations,0);
  c.liveLeaving=false;c.liveInfo={phase:'waiting',calls:0,match_number:3,server_budget:{
    calls:12,call_cap:12,committed_or_reserved_usd:.1,cost_cap_usd:.5,can_start:false}};
  const intro={};c.document={querySelector:()=>intro};
  c.liveLabels();assert.match(nodes.liveStatus.textContent,/Server-wide/);
  assert.match(intro.textContent,/Server-wide/);assert.ok(!intro.textContent.includes('key not configured'));
  assert.match(nodes.liveBudget.textContent,/12\/12/);
  console.log('PASS: fresh-page session preparation, no automatic consent, incomplete failure and cumulative server budget');
})().catch(error=>{console.error(error);process.exitCode=1;});
