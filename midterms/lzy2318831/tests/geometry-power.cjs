// UI-only setting regression: synthetic local responses, no model transport.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const nodes=Object.fromEntries(['geometryPower','geometryPowerNote','liveBudget','liveStart','startButton','resultDetail'].map(id=>[id,{}]));
const requests=[];let confirmations=0;
const c={Number,String,liveLeaving:false,liveInfo:{phase:'waiting',power_multiplier:2},state:{},
  document:{createElement:()=>({}),querySelector:()=>({append(){}})},$:id=>nodes[id],toast:()=>{},
  geometryBound:async p=>p,liveLabels:()=>{nodes.liveBudget.textContent='Budget';},showResult:()=>{nodes.resultDetail.textContent='Result';},
  confirmLive:()=>confirmations++,livePost:async(path,body)=>{requests.push([path,body.power_multiplier]);return {live:{phase:'waiting',power_multiplier:body.power_multiplier}};}};
vm.createContext(c);vm.runInContext(fs.readFileSync('fusion/geometry_power.js','utf8'),c);
(async()=>{
  c.liveLabels();assert.equal(nodes.geometryPower.value,'2');assert.equal(nodes.geometryPower.disabled,false);
  assert.match(nodes.liveBudget.textContent,/2x.*scratch risk/);
  nodes.geometryPower.value='1';await nodes.geometryPower.onchange();
  assert.deepEqual(requests,[['/live/power',1]]);assert.equal(c.liveInfo.power_multiplier,1);
  assert.ok(!requests.some(([path])=>path==='/live/start'));
  c.confirmLive();assert.equal(confirmations,1);
  c.liveInfo.phase='thinking';c.liveLabels();assert.equal(nodes.geometryPower.disabled,true);
  await nodes.geometryPower.onchange();assert.equal(requests.length,1);
  c.liveInfo.phase='waiting';
  c.livePost=async(path,body)=>{
    assert.equal(path,'/live/power');assert.equal(body.power_mode,'adaptive');
    return {live:{phase:'waiting',power_mode:'adaptive',power_multiplier:null}};
  };
  nodes.geometryPower.value='adaptive';await nodes.geometryPower.onchange();
  assert.equal(nodes.geometryPower.value,'adaptive');assert.match(nodes.liveBudget.textContent,/Adaptive energy/);
  c.showResult();assert.match(nodes.resultDetail.textContent,/Adaptive energy/);
  c.liveInfo={phase:'waiting',power_multiplier:1};
  c.liveInfo.phase='waiting';c.livePost=async()=>{throw Error('HTTP failure');};
  await nodes.geometryPower.onchange();assert.equal(nodes.liveStart.disabled,true);
  c.confirmLive();assert.equal(confirmations,1);
  assert.match(nodes.geometryPowerNote.textContent,/not confirmed.*Reload/);
  c.showResult();assert.match(nodes.resultDetail.textContent,/power 1x/);
  console.log('PASS: preferred2x,1x switch without dispatch,active lock,setting failure blocks consent,result label');
})().catch(e=>{console.error(e);process.exitCode=1;});
