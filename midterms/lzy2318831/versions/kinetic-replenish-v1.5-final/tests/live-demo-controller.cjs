// Built-in-only optional JavaScript check. No browser or provider requests.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../fusion/live_web/live.js'),'utf8');new vm.Script(source);
module.exports=(async()=>{
  const confirm=source.slice(source.indexOf('async function confirmLive(){'),source.indexOf('async function cancelLive(){'));
  let calls=0;
  const c={liveInfo:{can_start:true,mocked:false},liveLeaving:false,liveToken:'test-nonce',window:{confirm:()=>false},
    generation:0,toast:()=>{},livePost:async(p,b)=>{calls++;assert.equal(p,'/live/start');assert.equal(b.confirmed,true);return {live:{can_start:false}};},
    $:()=>({classList:{add:()=>{}}}),updateHUD:()=>{},state:null,started:false,busy:false,liveStopped:false};
  vm.createContext(c);vm.runInContext(confirm,c);await c.confirmLive();assert.equal(calls,0);
  c.window.confirm=()=>true;await c.confirmLive();assert.equal(calls,1);await c.confirmLive();assert.equal(calls,1);
  c.liveInfo={can_start:true,mocked:false};c.started=false;c.state=null;
  c.livePost=async()=>{c.liveLeaving=true;c.generation++;return {live:{can_start:false}};};
  await c.confirmLive();assert.equal(c.started,false);assert.equal(c.state,null);
  const poll=source.slice(source.indexOf('async function pollLive(){'),source.indexOf('finishMovie=async'));
  let previews=0;
  const p={livePolling:false,liveInfo:null,liveSeen:0,movie:null,livePreview:false,liveStopped:false,liveLeaving:false,generation:0,
    started:false,state:null,shown:[],busy:false,updateHUD:()=>{},toast:()=>{},
    $:()=>({classList:{add:()=>{}}}),setTimeout:(fn,delay)=>{if(delay===1000)previews++;return 1;},
    api:async url=>{if(url==='/api/state')return {live:{phase:'playback',sequence:1}};
      p.liveStopped=true;p.generation++;return {sequence:1};}};
  vm.createContext(p);vm.runInContext(poll,p);await p.pollLive();assert.equal(previews,0);
  return 'PASS: live.js syntax; rejection dispatches nothing; explicit confirmation once; cancelled delayed packet cannot animate';
})();
