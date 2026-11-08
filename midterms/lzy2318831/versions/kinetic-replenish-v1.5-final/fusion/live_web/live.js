'use strict';
// Separate controller: original renderer, rules and recorded replay are unchanged.
let liveToken=null,liveInfo=null,livePolling=false,livePollTimer=null,livePreviewTimer=null;
let liveSeen=0,livePreview=false,liveSelected=null,liveStopped=false;
let liveLeaving=false;
const liveHUD=updateHUD,liveDraw=drawTable,liveResult=showResult;
const livePanel=document.createElement('section');livePanel.className='live-panel';
livePanel.innerHTML='<strong id="liveIdentity">LIVE LLM AGENT — confirmation required</strong><p>kinetic-prompt-v2-risk-aware · GPT-5.4 mini versus Geometric AI · no manual moves</p><div class="live-controls"><button id="liveStart" class="primary-button">Confirm bounded live match</button><button id="liveCancel" class="quiet-button">Cancel live match</button><b id="liveStatus">No requests sent.</b></div><small id="liveBudget">Maximum 6 requests and $0.25 estimated cost. No retries.</small><p id="liveAction">Selected shot will appear here.</p><ol id="liveHistory"></ol>';
document.querySelector('.heading-row').after(livePanel);
document.querySelector('.mode-switch').hidden=true;$('helpButton').hidden=true;
$('restartButton').textContent='Cancel live match';$('restartButton').onclick=cancelLive;
document.querySelector('#intro .eyebrow').textContent='SEPARATE LIVE LLM AGENT';
document.querySelector('#intro h2').textContent='Let the agent choose.';
document.querySelector('#intro p').textContent='The Python backend calls the real model only after explicit confirmation of one match: up to 6 requests and $0.25 estimated cost. No automatic retries.';
document.querySelector('#intro .how-grid').hidden=true;
document.querySelector('#intro .modal-footnote').textContent='API key stays in the local backend. Cancel blocks further calls; a sent request may still be billed.';
$('startButton').textContent='CONFIRM LIVE LLM MATCH';$('startButton').disabled=true;
document.querySelector('.arena-bottomline > span').textContent='AUTONOMOUS MODEL + GEOMETRIC • MANUAL SHOTS DISABLED';
$('playAgain').textContent='Close result';$('playAgain').onclick=()=>$('gameOver').classList.add('hidden');
canvas.setAttribute('aria-label','Autonomous live agent game. Manual shot input is disabled.');
humanReady=()=>false;fire=()=>toast('No manual moves in live-agent mode.');scheduleAI=()=>{};
reset=()=>confirmLive();$('liveStart').onclick=confirmLive;$('liveCancel').onclick=cancelLive;
async function livePost(path,body){
  const response=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-Live-Token':liveToken},body:JSON.stringify(body)});
  const result=await response.json();if(!response.ok)throw Error(result.error||'Local live request refused');return result;
}
function liveLabels(){
  if(!liveInfo)return;
  $('liveIdentity').textContent=liveInfo.mocked?'MOCKED API TEST — NOT REAL LLM INFERENCE':'LIVE LLM AGENT — REAL MODEL REQUESTS AFTER CONFIRMATION';
  $('liveBudget').textContent=`Requests ${liveInfo.calls}/6 · known estimate $${liveInfo.estimated_cost_usd.toFixed(6)} · charged/reserved $${liveInfo.committed_or_reserved_usd.toFixed(6)}/$0.25 · unknown costs ${liveInfo.unknown_cost_calls}`;
  $('liveStatus').textContent=liveInfo.phase==='thinking'?(liveInfo.mocked?'MOCKED MODEL IS THINKING':'LLM IS THINKING'):liveInfo.phase==='geometric'?'GEOMETRIC AI IS PLANNING':liveInfo.phase==='stopping'?'CANCELLING — WAITING FOR IN-FLIGHT REQUEST':liveInfo.phase.toUpperCase();
  if(liveInfo.phase==='waiting'&&!liveInfo.can_start)$('liveStatus').textContent='PAID MODE DISABLED OR SERVER KEY NOT CONFIGURED';
  if(liveInfo.reason)$('liveStatus').textContent+=` · ${liveInfo.reason}`;
  $('liveStart').disabled=liveLeaving||!liveInfo.can_start;$('startButton').disabled=liveLeaving||!liveInfo.can_start;
  $('liveCancel').disabled=['complete','failed','cancelled'].includes(liveInfo.phase);
}
updateHUD=()=>{
  liveHUD();if(!state)return;
  $('name1').textContent=liveInfo?.mocked?'Mocked LLM · test':'GPT-5.4 mini · live';$('name2').textContent='Geometric AI';
  for(const p of ['p1','p2'])$(`tag${p.slice(1)}`).textContent=state.observation.active_player===p&&state.outcome.status==='ongoing'?'AUTONOMOUS TURN':'';
  $('statusLabel').textContent=liveInfo?.phase==='thinking'?'LLM IS THINKING':movie?'BALLS IN MOTION':liveInfo?.phase==='geometric'?'GEOMETRIC IS PLANNING':liveInfo?.phase.toUpperCase()||'CONFIRMATION REQUIRED';
  $('powerHint').textContent='Agent-selected power. No mouse aiming or shooting.';
  if(liveSelected)$('aimReadout').textContent=`${liveSelected.player.toUpperCase()} ${liveSelected.action.angle}° / ${liveSelected.action.power}%`;
  liveLabels();
};
drawTable=now=>{liveDraw(now);if(livePreview&&shown.some(b=>b.id===0))drawAim();};
async function confirmLive(){
  if(liveLeaving)return;
  if(!liveInfo?.can_start||!liveToken){toast('Paid mode disabled, credentials absent, or this launch already used.');return;}
  const message=liveInfo.mocked?'Start MOCKED test match? Synthetic replies only; no paid requests.':'Authorize ONE autonomous GPT-5.4 mini match: up to 6 real API requests and $0.25 locally estimated cost, no retries? The key stays on your Python backend. Cancel stops further calls; sent requests may still be charged.';
  if(!window.confirm(message))return;
  const ticket=generation;
  try{const next=await livePost('/live/start',{confirmed:true});if(liveLeaving||ticket!==generation)return;state=next;liveInfo=next.live;started=true;busy=true;liveStopped=false;$('intro').classList.add('hidden');updateHUD();}
  catch(e){toast(e.message);}
}
async function cancelLive(){
  if(!liveToken)return;
  try{const next=await livePost('/live/cancel',{});if(liveLeaving)return;++generation;clearTimeout(livePreviewTimer);movie=null;livePreview=false;
    state=next;liveInfo=next.live;shown=next.observation.balls;busy=false;liveStopped=true;$('intro').classList.add('hidden');updateHUD();
    announce('Cancellation requested.','No more calls; an in-flight request may still be charged.',2500);
  }catch(e){toast(e.message);}
}
async function pollLive(){
  if(liveLeaving)return;
  if(livePolling){livePollTimer=setTimeout(pollLive,500);return;}livePolling=true;
  try{
    const next=await api('/api/state');if(liveLeaving)return;liveInfo=next.live;
    if(liveInfo.phase!=='waiting'){$('intro').classList.add('hidden');started=true;}
    if(liveInfo.phase==='playback'&&!movie&&!livePreview&&!liveStopped&&liveInfo.sequence!==liveSeen){
      const requestGeneration=generation;const packet=await api('/live/packet');
      if(liveStopped||requestGeneration!==generation)return;
      liveSeen=packet.sequence;liveSelected=packet;
      const ticket=generation;state=packet.before_state;shown=packet.shot.frames[0].balls;busy=true;livePreview=true;
      aim=packet.action.angle*Math.PI/180;setPower(packet.action.power);
      const label=`Shot ${packet.sequence}/12 · ${packet.player.toUpperCase()} ${packet.source==='model'?'LLM':'Geometric'}: ${packet.action.angle}°, power ${packet.action.power}%`;
      $('liveAction').textContent=label;const item=document.createElement('li');item.textContent=label;$('liveHistory').append(item);
      livePreviewTimer=setTimeout(()=>{if(ticket!==generation)return;livePreview=false;resetDeviceFeedback();
        movie={frames:packet.shot.frames,events:packet.shot.events,start:performance.now(),index:0,eventIndex:0,result:packet,previous:shown,ticket};
      },1000);
    }else if(!movie&&!livePreview){state=next;shown=next.observation.balls;busy=!['waiting','complete','failed','cancelled'].includes(liveInfo.phase);}
    updateHUD();
    if(!movie&&!livePreview&&['complete','failed'].includes(liveInfo.phase)&&!liveStopped){liveStopped=true;showResult();}
  }catch(e){toast('Connection lost. No model request is retried. Use Cancel or stop the backend.');}
  finally{livePolling=false;if(!liveLeaving)livePollTimer=setTimeout(pollLive,600);}
}
finishMovie=async(packet,ticket)=>{
  if(ticket!==generation)return;movie=null;state=packet.state;shown=state.observation.balls;busy=true;
  const shot=state.observation.last_shot;
  if(shot){announce(shot.foul?'Scratch — shot points voided':`Shot +${shot.points}`,`Score ${state.outcome.scores.p1} : ${state.outcome.scores.p2}`,1600);$('shotValue').textContent=shot.foul?'FOUL':`LAST SHOT +${shot.points}`;}
  try{const next=await livePost('/live/ready',{sequence:packet.sequence});if(liveLeaving||ticket!==generation)return;liveInfo=next.live;state=next;updateHUD();}
  catch(e){liveStopped=true;toast('Playback acknowledgment failed. No automatic retry; cancel the session.');}
};
showResult=()=>{
  liveResult();if(!state||state.outcome.status!=='terminal')return;
  const o=state.outcome;$('resultTitle').textContent=o.failure?'Live session stopped.':o.draw?'Live match drawn.':o.winner==='p1'?'LLM wins.':'Geometric wins.';
  if(liveInfo?.mocked)$('resultTitle').textContent='Mocked test: '+$('resultTitle').textContent;
  $('resultDetail').textContent=`${liveInfo?.mocked?'Synthetic test — no real inference.':'Real prompt-v2 live mode.'} ${o.reason}. Requests ${liveInfo?.calls}/6; no retries.`;
  $('resultName1').textContent=liveInfo?.mocked?'MOCKED LLM':'GPT-5.4 MINI';$('resultName2').textContent='GEOMETRIC AI';
};
async function leaveLive(){
  liveLeaving=true;liveStopped=true;++generation;
  clearTimeout(livePollTimer);clearTimeout(livePreviewTimer);clearTimeout(aiTimer);clearTimeout(toastTimer);
  movie=null;livePreview=false;started=false;busy=false;
  $('liveStatus').textContent='Cancelling and settling any in-flight request before returning…';
  if(!liveToken){const info=await api('/live/info');liveToken=info.nonce;}
  const result=await livePost('/live/leave',{});
  state=result.state;liveInfo=state.live;shown=state.observation.balls;
  return result.safe_to_navigate===true;
}
const liveFrame=animate;animate=now=>{if(!liveLeaving)liveFrame(now);};
const backLive=window.KineticNavigation.install(leaveLive);
$('playAgain').textContent='Back to Main Menu';$('playAgain').onclick=backLive;
api('/live/info').then(info=>{liveToken=info.nonce;if(liveLeaving)return;liveInfo=info.state.live;liveLabels();
  if(liveInfo.mocked){document.querySelector('#intro p').textContent='MOCKED API TEST. Synthetic responses only; no real model inference or API charges.';$('startButton').textContent='CONFIRM MOCKED TEST MATCH';}
  else if(!liveInfo.can_start&&liveInfo.phase==='waiting')document.querySelector('#intro p').textContent='Paid mode is disabled or the backend key is not configured. This launch cannot call the API. Use mocked mode for offline checks. Paid execution requires separate approval.';
  pollLive();
}).catch(e=>toast(e.message));
