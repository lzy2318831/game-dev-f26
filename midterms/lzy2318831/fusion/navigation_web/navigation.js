'use strict';
// Shared Back button. Navigates only after the controller reports it is safe.
window.KineticNavigation={install(stop){
  let navigating=false;
  const buttons=[];
  const status=document.createElement('p');status.className='navigation-status';status.setAttribute('role','status');
  document.querySelector('.topbar').after(status);
  async function back(){
    if(navigating)return;navigating=true;buttons.forEach(b=>b.disabled=true);
    status.textContent='Stopping playback / safely closing the agent session…';
    try{
      if(await stop()===false){status.textContent='Still stopping. Stay here; try Back again once the request settles.';return;}
      const r=await fetch('/navigation/info');if(!r.ok)throw Error('Main-menu address unavailable.');
      const info=await r.json();if(!info.menu_url)throw Error('Open this viewer from the combined game launcher to return to its menu.');
      const target=new URL(info.menu_url);
      if(target.protocol!=='http:'||!['127.0.0.1','localhost'].includes(target.hostname))throw Error('Invalid local menu address.');
      window.location.assign(target.href);
    }catch(e){status.textContent=`Return paused: ${e.message} The session remains stopped; no new model request is authorized.`;}
    finally{navigating=false;buttons.forEach(b=>b.disabled=false);}
  }
  for(const container of [document.querySelector('.top-actions'),document.querySelector('#intro .modal'),document.querySelector('#gameOver .modal')]){
    if(!container)continue;const b=document.createElement('button');b.className='quiet-button back-menu-button';b.textContent='Back to Main Menu';b.onclick=back;container.append(b);buttons.push(b);
  }
  return back;
}};
