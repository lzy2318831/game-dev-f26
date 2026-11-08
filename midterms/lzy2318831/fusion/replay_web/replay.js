'use strict';
// Viewer adapter only. The original renderer and fixed-step Python engine stay frozen.
let replayInfo=null,replayPaused=false,replayTimer=null,replayPreview=false,replayShot=null;
let replayLeaving=false;
const originalHUD=updateHUD,originalDraw=drawTable,originalResult=showResult;
const replayPanel=document.createElement('section');
replayPanel.className='recorded-panel';
replayPanel.innerHTML='<strong>Recorded LLM Evaluation — NOT A LIVE API SESSION</strong><p id="replayIdentity">Verifying saved match…</p><div class="recorded-controls"><button id="replayPlay" class="quiet-button">Play</button><button id="replayPause" class="quiet-button">Pause after shot</button><button id="replayRestart" class="quiet-button">Restart</button><span id="recordedAction">Press START RECORDED MATCH. Both players run automatically.</span></div><small>No manual moves • Original saved decisions • Deterministic physics replay</small><ol id="recordedHistory"></ol>';
document.querySelector('.heading-row').after(replayPanel);
document.querySelector('.mode-switch').hidden=true;
$('helpButton').hidden=true;
$('restartButton').textContent='Restart Match';
$('startButton').textContent='START RECORDED MATCH';
$('playAgain').textContent='REPLAY SAME MATCH';
document.querySelector('#intro .eyebrow').textContent='RECORDED REAL LLM EVALUATION';
document.querySelector('#intro h2').textContent='Watch the agent play.';
document.querySelector('#intro p').textContent='Authentic GPT-5.4 mini decisions versus the original Geometric baseline. No API calls; no manual shot selection.';
document.querySelector('#intro .how-grid').hidden=true;
document.querySelector('#intro .modal-footnote').textContent='Recorded evaluation scenario • six alternating shots each';
document.querySelector('.arena-bottomline > span').textContent='RECORDED ACTIONS • AUTOMATIC PLAYBACK';
canvas.setAttribute('aria-label','Recorded real LLM match. Manual shots disabled.');
$('startButton').disabled=true;
humanReady=()=>false;
fire=()=>toast('Recorded replay: no manual actions accepted.');
scheduleAI=()=>{if(!started||busy||state?.outcome.status==='terminal')return;clearTimeout(replayTimer);if(!replayPaused)replayTimer=setTimeout(replayNext,1400);};
updateHUD=()=>{
  originalHUD();if(!state||!replayInfo)return;
  for(const p of ['p1','p2']){$(`name${p.slice(1)}`).textContent=p===replayInfo.llm_seat?'GPT-5.4 mini · recorded':'Geometric baseline · recorded';$(`tag${p.slice(1)}`).textContent=state.observation.active_player===p&&state.outcome.status!=='terminal'?'RECORDED TURN':'';}
  $('statusLabel').textContent=state.outcome.status==='terminal'?'RECORDED MATCH COMPLETE':!started?'RECORDED MATCH READY':replayPaused?'PAUSE AFTER CURRENT SHOT':replayPreview?'RECORDED SHOT PREVIEW':movie?'REPLAYING RECORDED BALL MOTION':'AUTOMATIC RECORDED PLAYBACK';
  $('powerHint').textContent='Recorded power, not manual input. No API requests.';
  if(replayShot)$('aimReadout').textContent=`RECORDED ${replayShot.action.angle}° / ${replayShot.action.power}%`;
};
drawTable=now=>{originalDraw(now);if(replayPreview&&shown.some(b=>b.id===0))drawAim();};
reset=async()=>{
  if(replayLeaving)return;
  const ticket=++generation;clearTimeout(replayTimer);clearTimeout(aiTimer);resetDeviceFeedback();
  movie=null;replayPreview=false;replayShot=null;replayPaused=false;busy=true;effects=[];drag=null;
  $('gameOver').classList.add('hidden');$('recordedHistory').replaceChildren();$('replayPause').textContent='Pause after shot';
  try{const next=await api('/replay/reset',{});if(ticket!==generation)return;
    state=next;mode='hvh';started=true;shown=state.observation.balls;busy=false;$('intro').classList.add('hidden');
    setPower(0);updateHUD();scheduleAI();
  }catch(e){busy=false;toast(e.message);}
};
async function replayNext(){
  if(replayLeaving)return;
  if(busy||replayPaused||!started||state.outcome.status==='terminal')return;
  const ticket=generation;busy=true;resetDeviceFeedback();updateHUD();
  try{
    const result=await api('/replay/next',{});if(ticket!==generation)return;
    replayShot=result;replayPreview=true;aim=result.action.angle*Math.PI/180;setPower(result.action.power);
    const r=result.recording,who=r.source==='model'?'LLM':'Geometric';
    $('recordedAction').textContent=`Shot ${r.shot}/12 · ${r.player.toUpperCase()} ${who}: angle ${result.action.angle}°, power ${result.action.power}% · recorded decision latency ${r.latency_seconds.toFixed(3)}s`;
    const item=document.createElement('li');item.textContent=$('recordedAction').textContent;$('recordedHistory').append(item);updateHUD();
    replayTimer=setTimeout(()=>{if(ticket!==generation)return;replayPreview=false;
      movie={frames:result.shot.frames,events:result.shot.events,start:performance.now(),index:0,eventIndex:0,result,previous:shown,ticket};updateHUD();
    },2300);
  }catch(e){busy=false;replayPaused=true;toast(e.message);updateHUD();}
}
finishMovie=async(result,ticket)=>{
  if(ticket!==generation)return;movie=null;
  try{const next=await api('/replay/ready',{});if(ticket!==generation)return;state=next;}
  catch(e){replayPaused=true;toast(e.message);return;}
  shown=state.observation.balls;busy=false;resetDeviceFeedback();updateHUD();
  const shot=state.observation.last_shot;
  if(shot){announce(shot.foul?'Recorded scratch — shot voided':`Recorded shot +${shot.points}`,`Score ${state.outcome.scores.p1} : ${state.outcome.scores.p2}`,1500);$('shotValue').textContent=shot.foul?'RECORDED FOUL':`RECORDED SHOT +${shot.points}`;}
  if(shot?.replenished?.length)toast(`Recorded refill: ${shot.replenished.length} balls`);
  if(state.outcome.status==='terminal')replayTimer=setTimeout(showResult,1800);else scheduleAI();
};
showResult=()=>{
  originalResult();if(!state||state.outcome.status!=='terminal')return;
  const o=state.outcome;const won=o.winner===replayInfo.llm_seat;
  $('resultTitle').textContent=o.draw?'Recorded draw.':won?'Recorded LLM win.':'Recorded Geometric win.';
  $('resultDetail').textContent=`Recorded real evaluation · ${replayInfo.trial} · ${o.reason}. No live API session.`;
  for(const p of ['p1','p2'])$(`resultName${p.slice(1)}`).textContent=p===replayInfo.llm_seat?'GPT-5.4 MINI':'GEOMETRIC BASELINE';
};
$('replayPause').onclick=()=>{replayPaused=!replayPaused;$('replayPause').textContent=replayPaused?'Resume automatic playback':'Pause after shot';if(!replayPaused)scheduleAI();updateHUD();};
$('replayPlay').onclick=()=>{if(!replayInfo)return;if(!started)return reset();replayPaused=false;$('replayPause').textContent='Pause after shot';scheduleAI();updateHUD();};
$('replayRestart').onclick=()=>{if(replayInfo)reset();};
function stopRecordedPlayback(){
  replayLeaving=true;++generation;clearTimeout(replayTimer);clearTimeout(aiTimer);clearTimeout(toastTimer);
  movie=null;replayPreview=false;busy=false;started=false;effects=[];return true;
}
const recordedFrame=animate;animate=now=>{if(!replayLeaving)recordedFrame(now);};
$('replayRestart').textContent='Restart Match';
window.KineticNavigation.install(stopRecordedPlayback);
api('/replay/info').then(info=>{if(replayLeaving)return;replayInfo=info;$('replayIdentity').textContent=`${info.physics_version||'original recorded physics'} | ${info.trial} · ${info.model} · LLM ${info.llm_seat.toUpperCase()} · trace SHA256 ${info.trace_sha256.slice(0,16)}…`;$('startButton').disabled=false;updateHUD();if(location.hash==='#autoplay')reset();}).catch(e=>toast(e.message));
