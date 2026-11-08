'use strict';
// One owned button, moved between panels. Navigation never waits indefinitely.
window.KineticNavigation={install(stop){
  const button=document.querySelector('#playAgain');
  const status=document.createElement('p');status.className='navigation-status';status.setAttribute('role','status');
  let navigating=false;
  const target=new URL(window.KineticMenuURL);
  if(target.protocol!=='http:'||!['127.0.0.1','localhost'].includes(target.hostname))throw Error('Invalid local menu address');
  function place(){
    const result=document.querySelector('#gameOver'),intro=document.querySelector('#intro');
    const container=!result.classList.contains('hidden')?document.querySelector('#gameOver .modal'):
      !intro.classList.contains('hidden')?document.querySelector('#intro .modal'):document.querySelector('.top-actions');
    container.append(status);container.append(button);
  }
  async function back(){
    if(navigating)return;navigating=true;button.disabled=true;
    status.textContent='Cancellation requested. Returning to Main Menu; a fresh match waits for settlement.';
    let timer;
    try{await Promise.race([Promise.resolve().then(stop),new Promise(resolve=>{timer=setTimeout(resolve,1500);})]);}
    catch(e){status.textContent='Return to menu; backend settlement is still pending.';}
    finally{clearTimeout(timer);window.location.assign(target.href);}
  }
  button.className='primary-button back-menu-button';button.textContent='Back to Main Menu';button.onclick=back;
  for(const id of ['#intro','#gameOver'])new MutationObserver(place).observe(document.querySelector(id),{attributes:true,attributeFilter:['class']});
  place();return back;
}};
