'use strict';
const $=id=>document.getElementById(id);
const canvas=$('table'),ctx=canvas.getContext('2d');
const W=1112,H=612,O=56,TAU=Math.PI*2;
const colors=['#f5f5ef','#efc447','#4f91e5','#e86169','#9f75dc','#e7994d','#50bda2'];
let state=null,shown=[],started=false,busy=false,drag=null,aim=0,mouse={x:700,y:250},power=0;
let movie=null,effects=[],noticeUntil=0,aiTimer=null,mode='hvb',lastTime=0,toastTimer;
let generation=0;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const hex=(h,a)=>{const x=h.replace('#','');return `rgba(${parseInt(x.slice(0,2),16)},${parseInt(x.slice(2,4),16)},${parseInt(x.slice(4,6),16)},${a})`;};
function roundRect(x,y,w,h,r,fill,stroke,width=1){ctx.beginPath();ctx.roundRect(x,y,w,h,r);if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke();}}
function line(x,y,x2,y2,color,width=1){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x2,y2);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke();}
function circle(x,y,r,fill,stroke,width=1){ctx.beginPath();ctx.arc(x,y,r,0,TAU);if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke();}}
function text(value,x,y,size,color,align='center',weight=500){ctx.font=`${weight} ${size}px "Segoe UI",Arial,sans-serif`;ctx.fillStyle=color;ctx.textAlign=align;ctx.textBaseline='middle';ctx.fillText(value,x,y);}
function toast(message){$('toast').textContent=message;$('toast').classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('show'),3300);}
async function api(path,data){const options=data===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)};const response=await fetch(path,options);const body=await response.json();if(!response.ok)throw Error(body.error||'Connection failed');return body;}
function updateHUD(){if(!state)return;for(const m of ['hvh','hvb'])$(m).classList.toggle('selected',m===mode);const o=state.observation;for(let i=1;i<=2;i++){const p=`p${i}`;$(`score${i}`).innerHTML=String(o.scores[p]).padStart(3,'0')+'<small>POINTS</small>';$(`card${i}`).classList.toggle('active',o.active_player===p&&o.status==='ongoing');$(`shots${i}`).replaceChildren(...Array.from({length:6},(_,k)=>{const el=document.createElement('span');el.className='shot-dot'+(k<o.shots_remaining[p]?' available':'');return el;}));$(`tag${i}`).textContent=o.active_player===p&&o.status==='ongoing'?(i===2&&mode==='hvb'?'THINKING':'YOUR TURN'):'';}
  $('name1').textContent=mode==='hvh'?'Player One':'You';$('name2').textContent=mode==='hvh'?'Player Two':'Geometric AI';
  const used=12-o.shots_remaining.p1-o.shots_remaining.p2;$('roundLabel').innerHTML=String(Math.min(12,used+1)).padStart(2,'0')+' <i>/ 12</i>';$('roundProgress').style.width=`${used/12*100}%`;
  $('statusLabel').textContent=!started?'READY TO PLAY':busy?'BALLS IN MOTION':o.status==='terminal'?'MATCH COMPLETE':`PLAYER ${o.active_player.slice(1)} · LINE UP YOUR SHOT`;
  if(busy)$('aimReadout').textContent='SHOT IN PLAY · FOLLOW THE CIRCUIT';
  animateScoreChanges();
}
function setPower(p){power=p;$('powerNumber').innerHTML=(p?String(p):'—')+' <small>%</small>';$('powerFill').style.width=p+'%';$('powerHint').textContent=drag?'Release to shoot · right-click to cancel.':'Click on the table and pull back to charge.';}
async function reset(nextMode=mode){const ticket=++generation;resetDeviceFeedback();clearTimeout(aiTimer);movie=null;busy=true;drag=null;effects=[];setPower(0);$('gameOver').classList.add('hidden');try{const next=await api('/api/reset',{mode:nextMode});if(ticket!==generation)return;state=next;busy=false;mode=state.mode;shown=state.observation.balls;started=true;$('intro').classList.add('hidden');updateHUD();announce('Your table. Your angle.','Six shots each. Make them count.',1300);scheduleAI();}catch(e){if(ticket!==generation)return;busy=false;toast(e.message);}}
function announce(title,detail,duration=1800){$('noticeTitle').textContent=title;$('noticeDetail').textContent=detail;$('notice').classList.add('visible');noticeUntil=performance.now()+duration;}
function scheduleAI(){if(!state||!started||busy||state.observation.status==='terminal')return;if(mode==='hvb'&&state.observation.active_player==='p2'){aiTimer=setTimeout(()=>fire(null,true),1000);}}
async function fire(action,baseline=false){if(busy||!started||!state||state.observation.status==='terminal')return;const ticket=generation;resetDeviceFeedback();busy=true;drag=null;setPower(0);$('notice').classList.remove('visible');updateHUD();try{const result=await api('/api/shot',baseline?{baseline:true}:{action});if(ticket!==generation)return;const frames=result.shot.frames;movie={frames,events:result.shot.events,start:performance.now(),index:0,eventIndex:0,result,previous:shown,ticket};}catch(e){if(ticket!==generation)return;busy=false;toast(e.message);updateHUD();}}
async function finishMovie(result,ticket){if(ticket!==generation)return;movie=null;try{const next=await api('/api/ready',{});if(ticket!==generation)return;state=next;}catch(e){if(ticket!==generation)return;toast('Playback finished. Reconnect or start a new match.');state=result.state;}shown=state.observation.balls;busy=false;updateHUD();const shot=state.observation.last_shot;if(shot){if(shot.foul)announce('Scratch. Fresh start.','Shot points voided · cue ball respotted.');else if(shot.breakdown.multi||shot.breakdown.assisted||shot.breakdown.multiplier)announce(`${shot.multiplier===2?'Orbit combo!':'Combo!'} +${shot.points}`,`${shot.breakdown.pots+shot.breakdown.multiplier} pots · ${shot.breakdown.bumpers+shot.breakdown.lanes+shot.breakdown.spinner} devices · ${shot.breakdown.multi+shot.breakdown.assisted} combo`);else if(shot.points)announce(`Nice shot. +${shot.points}`,shot.potted.length?'Pocket secured. Next player up.':'Circuit collected. Next player up.');else announce('Next angle. Next chance.',`Player ${state.observation.active_player.slice(1)} to the table.`,1300);}
  resetDeviceFeedback();if(shot&&$('shotValue'))$('shotValue').textContent=shot.foul?'FOUL · SHOT VOID':`LAST SHOT +${shot.points}`;
  if(state.outcome.status==='terminal'){setTimeout(()=>showResult(),1800);}else scheduleAI();}
function showResult(){if(!state||state.outcome.status!=='terminal')return;const o=state.outcome;$('resultTitle').textContent=o.failure?'Table paused.':o.draw?'Perfectly matched.':mode==='hvb'?(o.winner==='p1'?'The table is yours.':'A worthy opponent.'):`Player ${o.winner.slice(1)} takes it.`;$('resultDetail').textContent=o.failure?o.reason.replaceAll('_',' '):o.reason==='table_cleared'?'Every ball found a home. That’s a wrap.':'Twelve shots. A story in every angle.';$('resultScore1').textContent=o.scores.p1;$('resultScore2').textContent=o.scores.p2;if($('resultStats')){const m=o.metrics;$('resultStats').textContent=`POCKETS ${m.p1.pots} : ${m.p2.pots}  ·  CIRCUIT ${m.p1.bumper_points+m.p1.lane_points+m.p1.spinner_points} : ${m.p2.bumper_points+m.p2.lane_points+m.p2.spinner_points}  ·  BONUS ${m.p1.combo_points+m.p1.multiplier_points} : ${m.p2.combo_points+m.p2.multiplier_points}`;}$('gameOver').classList.remove('hidden');}
function localPoint(event){const r=canvas.getBoundingClientRect();return{x:(event.clientX-r.left)*W/r.width-O,y:(event.clientY-r.top)*H/r.height-O};}
function humanReady(){return started&&!busy&&state&&state.observation.status==='ongoing'&&(mode==='hvh'||state.observation.active_player==='p1')&&$('help').classList.contains('hidden');}
canvas.addEventListener('pointermove',event=>{mouse=localPoint(event);if(!humanReady())return;if(drag){const dx=drag.start.x-mouse.x,dy=drag.start.y-mouse.y;drag.pull=clamp(dx*Math.cos(drag.angle)+dy*Math.sin(drag.angle),0,180);setPower(Math.round(drag.pull/180*100));}else{const cue=shown.find(b=>b.id===0);if(cue&&Math.hypot(mouse.x-cue.x,mouse.y-cue.y)>12)aim=Math.atan2(mouse.y-cue.y,mouse.x-cue.x);}});
canvas.addEventListener('pointerdown',event=>{if(event.button!==0||!humanReady())return;const p=localPoint(event);if(p.x<0||p.x>1000||p.y<0||p.y>500)return;const cue=shown.find(b=>b.id===0);if(Math.hypot(p.x-cue.x,p.y-cue.y)>12)aim=Math.atan2(p.y-cue.y,p.x-cue.x);drag={start:p,angle:aim,pull:0};canvas.setPointerCapture(event.pointerId);canvas.focus();});
canvas.addEventListener('pointerup',event=>{if(!drag)return;const saved=drag;drag=null;setPower(0);if(saved.pull<8){toast('Aim, click, then pull backward to add power.');return;}fire({angle:(Math.round(saved.angle*180/Math.PI)+360)%360,power:Math.max(1,Math.round(saved.pull/180*100))});});
function cancel(){drag=null;setPower(0);}
canvas.addEventListener('pointercancel',cancel);canvas.addEventListener('contextmenu',event=>{event.preventDefault();cancel();});window.addEventListener('blur',cancel);window.addEventListener('keydown',event=>{if(event.key==='Escape'){cancel();$('help').classList.add('hidden');}});
$('startButton').onclick=()=>reset();$('restartButton').onclick=()=>reset();$('playAgain').onclick=()=>reset();$('helpButton').onclick=()=>{$('help').classList.remove('hidden');cancel();};$('closeHelp').onclick=()=>$('help').classList.add('hidden');
for(const m of ['hvh','hvb'])$(m).onclick=()=>{if(busy){toast('Let the current shot finish first.');return;}mode=m;for(const v of ['hvh','hvb'])$(v).classList.toggle('selected',v===m);if(started)reset(m);else{state.mode=m;updateHUD();}};

function drawTable(now){
  ctx.clearRect(0,0,W,H);ctx.save();
  const hit=effects.findLast(e=>e.type==='bumper'&&now-e.born<160);
  if(hit){const age=now-hit.born,k=(1-age/160)*1.8;ctx.translate(Math.sin(age*.13)*k,Math.cos(age*.1)*k*.65);}
  let g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#101c2d');g.addColorStop(1,'#080e18');roundRect(6,10,W-12,H-14,40,g,'#2c3e55',1);
  ctx.shadowColor='#000b';ctx.shadowBlur=20;ctx.shadowOffsetY=8;
  let metal=ctx.createLinearGradient(0,10,W,H);metal.addColorStop(0,'#b28c4f');metal.addColorStop(.18,'#ead093');metal.addColorStop(.4,'#6c562f');metal.addColorStop(.67,'#caaa69');metal.addColorStop(1,'#725b37');roundRect(17,19,W-34,H-36,32,metal,'#dec58c',1);
  ctx.shadowBlur=0;ctx.shadowOffsetY=0;roundRect(24,26,W-48,H-50,26,'#192b3c','#2b3c4a',1);roundRect(35,37,W-70,H-72,22,'#0a1725','#ab915e',1);
  let felt=ctx.createRadialGradient(480,270,50,500,280,600);felt.addColorStop(0,'#16435a');felt.addColorStop(.55,'#10364b');felt.addColorStop(1,'#0a2336');roundRect(O,O,1000,500,12,felt,'#285267',1);
  ctx.save();ctx.beginPath();ctx.rect(O,O,1000,500);ctx.clip();
  // Subtle original woven texture, deterministic decoration only.
  ctx.globalAlpha=.07;for(let y=O;y<O+500;y+=4)line(O,y,O+1000,y,'#82b8c8',.35);ctx.globalAlpha=1;
  let edge=ctx.createLinearGradient(0,O,0,O+45);edge.addColorStop(0,'#0007');edge.addColorStop(1,'#0000');ctx.fillStyle=edge;ctx.fillRect(O,O,1000,45);let edge2=ctx.createLinearGradient(0,O+455,0,O+500);edge2.addColorStop(0,'#0000');edge2.addColorStop(1,'#0007');ctx.fillStyle=edge2;ctx.fillRect(O,O+455,1000,45);
  ctx.restore();aurumInlays(now);
  for(const x of [O+125,O+250,O+375,O+625,O+750,O+875])for(const y of [O-25,O+525]){ctx.save();ctx.translate(x,y);ctx.rotate(Math.PI/4);ctx.fillStyle='#d2b97d';ctx.fillRect(-2.5,-2.5,5,5);ctx.restore();}
  for(const y of [O+125,O+250,O+375])for(const x of [O-25,O+1025]){circle(x,y,2.5,'#d2b97d');}
  for(const [x0,y0] of state?.observation.table.pockets||[[0,0],[500,0],[1000,0],[0,500],[500,500],[1000,500]]){const x=x0+O,y=y0+O;ctx.shadowColor='#000';ctx.shadowBlur=14;circle(x,y,32,'#050b10','#aa8d55',3);ctx.shadowBlur=0;let hole=ctx.createRadialGradient(x-4,y-7,2,x,y,29);hole.addColorStop(0,'#0b1420');hole.addColorStop(.7,'#03060b');hole.addColorStop(1,'#000');circle(x,y,28,hole,'#1f2b36',1);ctx.beginPath();ctx.arc(x,y,33,Math.PI*1.05,Math.PI*1.7);ctx.strokeStyle='#f2d39777';ctx.lineWidth=1;ctx.stroke();}
  aurumDevices(now);
  for(const bumper of state?.observation.bumpers||[])mechanicalBumper(bumper,now);
  if(movie){const index=movie.index;for(const b of shown){const trail=[];for(let k=Math.max(0,index-10);k<index;k+=2){const p=movie.frames[k].balls.find(v=>v.id===b.id);if(p)trail.push(p);}for(let k=1;k<trail.length;k++)line(O+trail[k-1].x,O+trail[k-1].y,O+trail[k].x,O+trail[k].y,hex(b.id===0?'#b8edfa':colors[b.id],k/trail.length*.2),b.id===0?3:2);}}
  for(const b of shown)drawBall(b);
  if(humanReady())drawAim();
  for(const fx of effects)deviceFeedback(fx,now);
  ctx.restore();
}
function drawBall(b){const x=b.x+O,y=b.y+O,r=11;ctx.save();
  ctx.shadowColor='#000b';ctx.shadowBlur=8;ctx.shadowOffsetX=2;ctx.shadowOffsetY=4;ctx.beginPath();ctx.ellipse(x+1,y+2,r*1.06,r*.92,0,0,TAU);ctx.fillStyle='#02101b';ctx.fill();ctx.shadowBlur=0;ctx.shadowOffsetX=0;ctx.shadowOffsetY=0;
  const base=colors[b.id];let g=ctx.createRadialGradient(x-4,y-5,.5,x+2,y+3,r*1.25);g.addColorStop(0,b.id?'#fffff2':'#fff');g.addColorStop(.14,b.id?base:'#fbfcf6');g.addColorStop(.55,b.id?base:'#e6eef0');g.addColorStop(1,b.id?'#132435':'#879ea9');circle(x,y,r,g,'#d2edf440',.7);
  ctx.beginPath();ctx.arc(x,y,r-.7,.25,2.3);ctx.strokeStyle=b.id?'#03121e55':'#425d6a44';ctx.lineWidth=1.2;ctx.stroke();
  if(b.id){let number=ctx.createRadialGradient(x-.8,y-.5,0,x+.3,y+.3,5.3);number.addColorStop(0,'#fffff2');number.addColorStop(1,'#d6dcca');circle(x+.3,y+.5,4.9,number,'#ffffff44',.4);text(String(b.id),x+.3,y+.5,7,'#193044','center',750);}
  ctx.globalAlpha=.78;ctx.beginPath();ctx.ellipse(x-3.5,y-4.7,3.5,1.5,-.45,0,TAU);ctx.fillStyle='#fff';ctx.fill();ctx.globalAlpha=.3;ctx.beginPath();ctx.arc(x,y,9.3,3.3,4.45);ctx.strokeStyle='#b9f3f7';ctx.lineWidth=.8;ctx.stroke();ctx.globalAlpha=.28;circle(x+4.5,y+3.5,1.4,'#8aebf1');ctx.restore();}
function rayCircle(origin,dir,center,r){const dx=origin.x-center.x,dy=origin.y-center.y;const a=dx*dir.x+dy*dir.y;const c=dx*dx+dy*dy-r*r;const discriminant=a*a-c;if(discriminant<0)return Infinity;const t=-a-Math.sqrt(discriminant);return t>0?t:Infinity;}
function drawAim(){const cue=shown.find(b=>b.id===0);if(!cue)return;const a=drag?drag.angle:aim,dx=Math.cos(a),dy=Math.sin(a);let length=1300,hit=null;
  for(const b of shown){if(!b.id)continue;const t=rayCircle(cue,{x:dx,y:dy},b,22);if(t<length){length=t;hit={...b,kind:'ball'};}}
  for(const b of state.observation.bumpers){const t=rayCircle(cue,{x:dx,y:dy},b,40);if(t<length){length=t;hit={...b,kind:'bumper'};}}
  for(const rail of state.observation.devices?.guides||[]){const t=rayGuide(cue,{x:dx,y:dy},rail);if(t<length){length=t;hit={x:cue.x+dx*t,y:cue.y+dy*t,kind:'rail'};}}
  for(const [v,d,lo,hi] of [[cue.x,dx,11,989],[cue.y,dy,11,489]]){if(Math.abs(d)>.00001){const t=((d>0?hi:lo)-v)/d;if(t>0&&t<length){length=t;hit=null;}}}
  length=Math.min(length,800);const ex=cue.x+dx*length,ey=cue.y+dy*length;
  ctx.save();ctx.setLineDash([5,7]);line(O+cue.x+dx*17,O+cue.y+dy*17,O+ex,O+ey,'#c7edf78c',1.25);ctx.setLineDash([]);circle(O+ex,O+ey,11,null,'#c7edf75c',1);
  if(hit&&hit.kind==='ball'&&length<800){const nx=(hit.x-ex)/Math.hypot(hit.x-ex,hit.y-ey),ny=(hit.y-ey)/Math.hypot(hit.x-ex,hit.y-ey);if(hit.kind==='ball'){ctx.setLineDash([3,6]);line(O+hit.x,O+hit.y,O+hit.x+nx*85,O+hit.y+ny*85,'#e8cb8766',1);ctx.setLineDash([]);}}
  const pull=drag?drag.pull:0;const start=22+pull*.35,end=start+145;
  const sx=O+cue.x-dx*start,sy=O+cue.y-dy*start,fx=O+cue.x-dx*end,fy=O+cue.y-dy*end;
  ctx.shadowColor='#0009';ctx.shadowBlur=5;ctx.shadowOffsetY=3;line(fx,fy,sx,sy,'#16202e',8);ctx.shadowBlur=0;ctx.shadowOffsetY=0;
  let wood=ctx.createLinearGradient(fx,fy,sx,sy);wood.addColorStop(0,'#25394b');wood.addColorStop(.28,'#283747');wood.addColorStop(.32,'#c8a669');wood.addColorStop(.35,'#665039');wood.addColorStop(.42,'#ba9a60');wood.addColorStop(1,'#f0deac');line(fx,fy,sx,sy,wood,5);line(sx-dx*5,sy-dy*5,sx,sy,'#73d8e3',5.5);
  $('aimReadout').textContent=drag?`POWER ${power}% · RELEASE TO FIRE`:`ANGLE ${(Math.round(a*180/Math.PI)+360)%360}° · FIND YOUR LINE`;
  ctx.restore();}
function animate(now){if(movie){const elapsed=(now-movie.start)/1000;const frames=movie.frames;while(movie.index<frames.length-1&&frames[movie.index+1].t<=elapsed)movie.index++;
  const a=frames[movie.index],b=frames[Math.min(movie.index+1,frames.length-1)];const f=b.t>a.t?clamp((elapsed-a.t)/(b.t-a.t),0,1):0;shown=a.balls.map(ball=>{const next=b.balls.find(v=>v.id===ball.id);return next?{id:ball.id,x:ball.x+(next.x-ball.x)*f,y:ball.y+(next.y-ball.y)*f}:ball;});
  while(movie.eventIndex<movie.events.length&&movie.events[movie.eventIndex].t<=elapsed){receiveDeviceEvent(movie.events[movie.eventIndex++],now);}
  if(elapsed>=frames[frames.length-1].t+.12){const result=movie.result,ticket=movie.ticket;movie=null;finishMovie(result,ticket);}}
  effects=effects.filter(fx=>now-fx.born<1500);if(now>noticeUntil)$('notice').classList.remove('visible');
  drawTable(now);lastTime=now;requestAnimationFrame(animate);}
function resize(){const dpr=Math.min(window.devicePixelRatio||1,2);canvas.width=W*dpr;canvas.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);}
window.addEventListener('resize',resize);resize();
api('/api/state').then(initial=>{state=initial;mode=state.mode;shown=initial.observation.balls;updateHUD();requestAnimationFrame(animate);}).catch(e=>toast('Local engine unavailable. Keep the Python server running and reload.'));
