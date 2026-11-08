// Optional Node built-in-only check of the actual adapter timer, not browser QA.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../fusion/replay_web/replay.js'),'utf8');
new vm.Script(source); // Parse the complete viewer adapter.
const schedule=source.match(/^scheduleAI=.*$/m)[0];
function context(busy,status){
  const c={started:true,busy,state:{outcome:{status}},replayPaused:false,replayTimer:42,
    replayNext:()=>{},cleared:[],clearTimeout:id=>c.cleared.push(id),setTimeout:()=>99};
  vm.createContext(c);vm.runInContext(schedule,c);return c;
}
const preview=context(true,'ongoing');preview.scheduleAI();
assert.equal(preview.replayTimer,42);assert.equal(preview.cleared.length,0);
const final=context(false,'terminal');final.scheduleAI();
assert.equal(final.replayTimer,42);assert.equal(final.cleared.length,0);
const next=context(false,'ongoing');next.scheduleAI();assert.equal(next.replayTimer,99);
console.log('PASS: complete replay.js syntax; preview/final timers preserved; automatic progression schedules');
