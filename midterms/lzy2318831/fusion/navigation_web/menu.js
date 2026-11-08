'use strict';
const menuHasLive=document.currentScript.dataset.live==='true';
document.querySelector('#intro .eyebrow').textContent='KINETIC CIRCUIT';
document.querySelector('#intro h2').textContent='Main Menu';
document.querySelector('#intro p').textContent='Choose a playable mode or an agent demonstration.';
const choices=document.querySelector('#intro .how-grid');choices.className='menu-grid';choices.replaceChildren();
for(const [label,value] of [['Human vs Human','hvh'],['Human vs Geometric AI','hvb'],['Human vs Smart AI','hvs']]){
  const b=document.createElement('button');b.className='primary-button';b.textContent=label;b.onclick=()=>reset(value);choices.append(b);
}
for(const [label,url] of [['Recorded LLM Replay','/watch'],...(menuHasLive?[['Live LLM Agent','/live']]:[])]){
  const a=document.createElement('a');a.className='primary-button';a.textContent=label;a.href=url;choices.append(a);
}
for(const p of document.querySelectorAll('#intro p'))if(p.querySelector('a[href="/watch"]'))p.remove();
$('startButton').hidden=true;
$('restartButton').textContent='Restart Match';
$('restartButton').onclick=()=>reset(mode);
const menuResult=showResult;showResult=()=>{if(started&&$('intro').classList.contains('hidden'))menuResult();};
function openMainMenu(){
  ++generation;clearTimeout(aiTimer);movie=null;busy=false;started=false;drag=null;effects=[];
  $('gameOver').classList.add('hidden');$('intro').classList.remove('hidden');
}
const mainButton=document.createElement('button');mainButton.className='quiet-button';mainButton.textContent='Main Menu';mainButton.onclick=openMainMenu;
document.querySelector('.top-actions').append(mainButton);
