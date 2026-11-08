// Pure pose/clock regression extracted from the actual served game controller.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('fusion/web/game.js','utf8');
const start=source.indexOf('function cueStrokePose('),end=source.indexOf('\nfunction ',start+1);
assert.ok(start>=0,'controller has no forward cue-stroke phase');
const c={Math,clamp:(v,a,b)=>Math.max(a,Math.min(b,v))};vm.createContext(c);
vm.runInContext(source.slice(start,end),c);
const movie={start:1000,frames:[{balls:[{id:0,x:230,y:250}]}],result:{action:{angle:0,power:100},source:'model'}};
const pose=t=>c.cueStrokePose(movie,1000+t);
assert.ok(pose(140).gap>pose(0).gap,'visible pullback');
assert.ok(pose(220).gap<pose(140).gap,'visible forward stroke');
assert.equal(pose(259).physicsSeconds,0,'ball held before contact');
assert.equal(pose(260).gap,11,'cue reaches cue-ball surface');
assert.equal(pose(260).physicsSeconds,0);
assert.ok(pose(280).physicsSeconds>0,'ball starts only after contact');
assert.equal(pose(400).visible,false);
movie.result.source='human';assert.equal(pose(119).physicsSeconds,0);assert.equal(pose(120).gap,11);
console.log('PASS: cue pulls back, strikes forward, ball clock starts after contact');
