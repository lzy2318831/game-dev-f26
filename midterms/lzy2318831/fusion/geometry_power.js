'use strict';
// Geometry-only waiting-state preference. Changing this never starts a request.
let geometryPowerBusy=false,geometryPowerFailed=false;
const geometryPowerBox=document.createElement('div');
geometryPowerBox.innerHTML='<label for="geometryPower">Candidate power</label> <select id="geometryPower" disabled><option value="2">2x - student demonstration preference</option><option value="1">1x - stabilized fallback</option><option value="adaptive">Adaptive energy - experimental</option></select><p id="geometryPowerNote">Stronger settings increase scratch/device-chain risk; they are not proven win-rate improvements. Adaptive distance v2 sets contact/pot/bank power30-40 at0-150units,40-80 at150-350,80-100 at350-1000; escape/device routes retain2x. Change before confirming a fresh match.</p>';
document.querySelector('#intro .modal').append(geometryPowerBox);
const geometryPowerSelect=$('geometryPower');
geometryPowerSelect.onchange=async()=>{
  if(geometryPowerBusy||liveLeaving||liveInfo?.phase!=='waiting')return;
  geometryPowerBusy=true;geometryPowerSelect.disabled=true;
  for(const id of ['liveStart','startButton'])$(id).disabled=true;
  try{
    const body=geometryPowerSelect.value==='adaptive'?{power_mode:'adaptive'}:{power_multiplier:Number(geometryPowerSelect.value)};
    const next=await geometryBound(livePost('/live/power',body));
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
  if(liveInfo?.power_mode==='adaptive'){
    geometryPowerSelect.value='adaptive';
    $('liveBudget').textContent+=' | Candidate power: Adaptive energy v2 (30-100; experimental).';
  }else if(multiplier){
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
  const label=liveInfo?.power_mode==='adaptive'?'Adaptive energy (experimental)':`${liveInfo?.power_multiplier||2}x`;
  $('resultDetail').textContent+=` Candidate power ${label}. Return to Main Menu and reopen Live LLM to change the next match's setting.`;
};
