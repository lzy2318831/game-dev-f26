'use strict';
// Geometry-only waiting-state preference. Changing this never starts a request.
let geometryPowerBusy=false,geometryPowerFailed=false;
const geometryPowerBox=document.createElement('div');
geometryPowerBox.innerHTML='<label for="geometryPower">Candidate power</label> <select id="geometryPower" disabled><option value="2">2x - student demonstration preference</option><option value="1">1x - stabilized fallback</option></select><p id="geometryPowerNote">2x increases scratch/device-chain risk; it is not a proven win-rate improvement. Change before confirming a fresh match.</p>';
document.querySelector('#intro .modal').append(geometryPowerBox);
const geometryPowerSelect=$('geometryPower');
geometryPowerSelect.onchange=async()=>{
  if(geometryPowerBusy||liveLeaving||liveInfo?.phase!=='waiting')return;
  geometryPowerBusy=true;geometryPowerSelect.disabled=true;
  for(const id of ['liveStart','startButton'])$(id).disabled=true;
  try{
    const next=await geometryBound(livePost('/live/power',{power_multiplier:Number(geometryPowerSelect.value)}));
    if(liveLeaving)return;
    liveInfo=next.live;state=next;
  }catch(e){
    geometryPowerFailed=true;toast(e.message);
    $('geometryPowerNote').textContent='Power update was not confirmed. Reload this page or return to Main Menu before confirming a match.';
  }
  finally{geometryPowerBusy=false;if(!liveLeaving)liveLabels();}
};
const geometryPowerLabels=liveLabels;
liveLabels=()=>{
  geometryPowerLabels();
  const multiplier=liveInfo?.power_multiplier;
  if(multiplier){
    geometryPowerSelect.value=String(multiplier);
    $('liveBudget').textContent+=` | Candidate power ${multiplier}x${multiplier===2?' (student preference; increased scratch risk)':' (stabilized fallback)'}.`;
  }
  geometryPowerSelect.disabled=geometryPowerBusy||geometryPowerFailed||liveLeaving||liveInfo?.phase!=='waiting';
  if(geometryPowerBusy||geometryPowerFailed)for(const id of ['liveStart','startButton'])$(id).disabled=true;
};
const geometryPowerConfirm=confirmLive;
confirmLive=()=>{if(!geometryPowerBusy&&!geometryPowerFailed)return geometryPowerConfirm();};
const geometryPowerResult=showResult;
showResult=()=>{
  geometryPowerResult();
  $('resultDetail').textContent+=` Candidate power ${liveInfo?.power_multiplier||2}x. Return to Main Menu and reopen Live LLM to change the next match's setting.`;
};
