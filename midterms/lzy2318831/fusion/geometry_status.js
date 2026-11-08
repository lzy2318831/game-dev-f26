'use strict';
// Geometry-only fresh-match preparation; consent still owns model dispatch.
async function geometryBound(promise){
  let timer;
  try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('Backend still settling. Back to Main Menu remains available.')),2000);})]);}
  finally{clearTimeout(timer);}
}
async function geometryLoadInfo(){
  const info=await geometryBound(api('/live/settlement'));
  if(['complete','failed','cancelled','stopping'].includes(info.state.live.phase)||info.state.live.cancel_requested){
    liveToken=info.nonce;
    const deadline=Date.now()+8000;
    do{
      const settled=await geometryBound(livePost('/live/leave',{}));
      if(settled.settled!==false)return await geometryBound(livePost('/live/new',{}));
      $('liveStatus').textContent='Previous match is settling. No new model request is being sent.';
      await new Promise(resolve=>setTimeout(resolve,250));
    }while(!liveLeaving&&Date.now()<deadline);
    throw Error('Previous match is still settling. Check Live readiness again; Back to Main Menu remains available.');
  }
  return info;
}
function geometryLoadFailed(error){
  toast(error.message);
  $('liveStatus').textContent='Live service is not ready. No model request sent. '+error.message;
  const intro=document.querySelector('#intro p');if(intro)intro.textContent=$('liveStatus').textContent;
  for(const id of ['liveStart','startButton']){
    const button=$(id);button.textContent='Check Live readiness';button.disabled=false;
    button.onclick=()=>window.location.reload();
  }
}
async function geometryNewOrConfirm(){
  if(liveLeaving)return;
  if(!['complete','failed','cancelled'].includes(liveInfo?.phase))return confirmLive();
  liveLeaving=true;
  try{
    const settled=await geometryBound(livePost('/live/leave',{}));
    if(settled.settled===false)throw Error('Previous match is still settling.');
    await geometryBound(livePost('/live/new',{}));window.location.reload();
  }catch(e){liveLeaving=false;toast(e.message);}
}
for(const id of ['liveStart','startButton']){const button=$(id);if(button)button.onclick=geometryNewOrConfirm;}
function geometryFailureMessage(reason){
  const messages={
    simulation_limit:'Physics did not settle within the fixed simulation limit. Match incomplete; this is not a win or loss. Return to Main Menu; no automatic retry.',
    no_reliable_candidate:'No supported shot candidate in this position. Match stopped safely; no other agent selected a move.',
    invalid_candidate_selection:'The model returned an invalid candidate selection. Match stopped; no replacement move or retry.',
    request_timeout:'Model request timed out. Match stopped; a sent request may still be charged.',
    http_error:'Model/API request failed. Match incomplete; no retry or replacement move. A fresh match requires consent.',
    run_call_or_cost_budget:'Per-match request/cost allowance exhausted. Match incomplete; no extra request was sent.',
    server_budget_exhausted:'Cumulative server allowance exhausted. Match incomplete; new matches do not reset spending.',
    playback_ack_timeout:'Browser playback acknowledgment timed out. Match incomplete; no model request is retried.',
    session_timeout:'Match session deadline reached. Match incomplete; no model request is retried.',
    user_cancelled:'Match cancelled. No further requests; an in-flight request may still be charged.'
  };
  if(['parent_watchdog','http_timeout'].includes(reason))return messages.request_timeout;
  return messages[reason]||null;
}
const geometryOriginalLabels=liveLabels;
liveLabels=()=>{
  geometryOriginalLabels();
  if(typeof state!=='undefined'&&state?.version){
    const identity=$('liveIdentity');if(identity)identity.textContent+=` | Physics ${state.version}`;
  }
  const message=geometryFailureMessage(liveInfo?.reason);
  if(message)$('liveStatus').textContent=message;
  const budget=liveInfo?.server_budget;
  if(budget){
    $('liveBudget').textContent=`Match ${liveInfo.match_number}: ${liveInfo.calls}/6 requests, $0.25 estimated cap. Server total ${budget.calls}/${budget.call_cap} requests, $${budget.committed_or_reserved_usd.toFixed(6)}/$${budget.cost_cap_usd.toFixed(2)} charged/reserved. New matches do not reset server totals.`;
    if(!budget.can_start&&liveInfo.phase==='waiting'){
      const limit='Server-wide spending/call allowance cannot cover another full match. No request sent. New matches do not reset this allowance.';
      $('liveStatus').textContent=limit;
      const intro=typeof document==='undefined'?null:document.querySelector('#intro p');
      if(intro)intro.textContent=limit;
    }
    if(['complete','failed','cancelled'].includes(liveInfo.phase)){
      for(const id of ['liveStart','startButton']){const button=$(id);if(button){button.textContent='New match (fresh consent)';button.disabled=liveLeaving||!budget.can_start;}}
    }
  }
};
const geometryOriginalResult=showResult;
showResult=()=>{
  geometryOriginalResult();
  const message=geometryFailureMessage(liveInfo?.reason);
  const failed=liveInfo?.phase==='failed'||(typeof state!=='undefined'&&state?.outcome?.failure);
  if(failed){
    $('resultTitle').textContent='Live agent error - match incomplete';
    $('resultDetail').textContent=message||`Match incomplete: ${liveInfo?.reason||'provider/model failure'}. No retry or replacement move. Return to Main Menu for a freshly consented match.`;
  }else if(message){$('resultTitle').textContent='Geometry-Assisted LLM stopped';$('resultDetail').textContent=message;}
};
