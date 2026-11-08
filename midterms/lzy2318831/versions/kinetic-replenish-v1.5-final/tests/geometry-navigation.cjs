// Failure-modal ownership and hung settlement regression; fake network only.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const preferred=path.join(__dirname,'../fusion/geometry_navigation.js');
const source=fs.readFileSync(fs.existsSync(preferred)?preferred:path.join(__dirname,'../fusion/navigation_web/navigation.js'),'utf8');
function fixture(){
  const make=()=>({children:[],className:'',classList:{contains:()=>false},setAttribute(){},after(){},append(x){if(x.parent)x.parent.children=x.parent.children.filter(v=>v!==x);this.children.push(x);x.parent=this;}});
  const top=make(),intro=make(),result=make(),play=make();result.append(play);play.textContent='Back to Main Menu';
  const ids={'.topbar':top,'.top-actions':top,'#intro .modal':intro,'#gameOver .modal':result,'#playAgain':play,
    '#intro':{classList:{contains:()=>true}},'#gameOver':{classList:{contains:()=>false}}};
  let destination=null;
  const c={URL,Promise,AbortController,clearTimeout,MutationObserver:class{observe(){}},
    setTimeout:(fn)=>setTimeout(fn,1),window:{KineticMenuURL:'http://127.0.0.1:8835/',location:{assign:v=>destination=v}},
    document:{createElement:make,querySelector:s=>ids[s]},fetch:()=>new Promise(()=>{})};
  vm.createContext(c);vm.runInContext(source,c);return {c,result,play,destination:()=>destination};
}
(async()=>{
  const failures=[];
  for(const reason of ['complete','simulation_limit','http_error','invalid_candidate_selection','request_timeout','user_cancelled','server_budget_exhausted']){
  const f=fixture();f.c.liveInfo={phase:reason==='complete'?'complete':'failed',reason};const back=f.c.window.KineticNavigation.install(()=>new Promise(()=>{}));
  f.play.onclick=back;
  try{assert.equal(f.result.children.filter(x=>x.textContent==='Back to Main Menu').length,1);}catch(e){failures.push('duplicate result Back owners: '+e.message);}
  back();await new Promise(resolve=>setTimeout(resolve,30));
  try{assert.equal(f.destination(),'http://127.0.0.1:8835/');}catch(e){failures.push('hung leave traps navigation: '+e.message);}
  }
  if(failures.length)throw Error(failures.join('\n'));
  console.log('PASS: one result Back owner; hung settlement cannot trap navigation');
})().catch(e=>{console.error(e.message);process.exitCode=1;});
