// Actual navigation functions, fake DOM/network only. No API or GUI calls.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const read=name=>fs.readFileSync(path.join(__dirname,'../fusion',name),'utf8');
for(const name of ['navigation_web/navigation.js','navigation_web/menu.js','replay_web/replay.js','live_web/live.js'])new vm.Script(read(name));
module.exports=(async()=>{
  const targets=[],buttons=[],order=[];let allow=false;let status;
  const container={append:b=>buttons.push(b)};
  const c={URL,window:{location:{assign:url=>{order.push('navigate');targets.push(url);}}},
    document:{createElement:()=>({setAttribute:()=>{}}),querySelector:s=>s==='.topbar'?{after:x=>{status=x;}}:container},
    fetch:async()=>{order.push('fetch');return {ok:true,json:async()=>({menu_url:'http://127.0.0.1:18805/'})};}};
  vm.createContext(c);vm.runInContext(read('navigation_web/navigation.js'),c);
  const back=c.window.KineticNavigation.install(async()=>{order.push('stop');await Promise.resolve();return allow;});
  assert.equal(buttons.length,3);await back();assert.equal(targets.length,0);assert.equal(order.join(','),'stop');
  allow=true;await back();assert.equal(targets[0],'http://127.0.0.1:18805/');assert.equal(order.join(','),'stop,stop,fetch,navigate');
  const recorded=read('replay_web/replay.js');
  const stop=recorded.slice(recorded.indexOf('function stopRecordedPlayback(){'),recorded.indexOf('const recordedFrame='));
  const cleared=[];const r={replayLeaving:false,generation:4,replayTimer:1,aiTimer:2,toastTimer:3,clearTimeout:id=>cleared.push(id),movie:{},replayPreview:true,busy:true,started:true,effects:[1]};
  vm.createContext(r);vm.runInContext(stop,r);assert.equal(r.stopRecordedPlayback(),true);
  assert.equal(r.generation,5);assert.equal(r.movie,null);assert.equal(r.started,false);assert.equal(r.replayLeaving,true);assert.deepEqual(cleared,[1,2,3]);
  const live=read('live_web/live.js');const leaving=live.slice(live.indexOf('async function leaveLive(){'),live.indexOf('const liveFrame='));
  let settle;const deferred=new Promise(resolve=>settle=resolve);const lc=[];
  const l={liveLeaving:false,liveStopped:false,generation:1,livePollTimer:1,livePreviewTimer:2,aiTimer:3,toastTimer:4,
    clearTimeout:id=>lc.push(id),movie:{},livePreview:true,started:true,busy:true,liveToken:'not-an-api-key',
    $:()=>({}),livePost:async route=>{assert.equal(route,'/live/leave');return deferred;}};
  vm.createContext(l);vm.runInContext(leaving,l);const waiting=l.leaveLive();
  assert.equal(l.liveLeaving,true);assert.equal(l.movie,null);assert.equal(l.generation,2);assert.deepEqual(lc,[1,2,3,4]);
  settle({safe_to_navigate:true,state:{live:{phase:'cancelled'},observation:{balls:[]}}});assert.equal(await waiting,true);
  let resultOverlays=0;
  const m={started:false,$:()=>({classList:{contains:()=>false}}),showResult:()=>{resultOverlays++;}};
  vm.createContext(m);vm.runInContext(read('navigation_web/menu.js').match(/^const menuResult=.*$/m)[0],m);
  m.showResult();assert.equal(resultOverlays,0);
  m.started=true;m.$=()=>({classList:{contains:()=>true}});m.showResult();assert.equal(resultOverlays,1);
  return 'PASS: safe navigation, stopped timers, modal Back controls and delayed result cannot cover Main Menu';
})();
