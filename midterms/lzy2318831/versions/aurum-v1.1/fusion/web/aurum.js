/* Aurum Circuit: original procedural playfield art, derived from public geometry. */
'use strict';
const bumperColor=b=>b.color==='gold'?'#e9c477':'#66e9f1';
const gold='#e9c477',cyan='#66e9f1';
let activeMultiplier=1,deviceShotPoints=0;
function resetDeviceFeedback(){activeMultiplier=1;deviceShotPoints=0;if($('orbitBadge')){$('orbitBadge').classList.remove('lit');$('orbitBadge').textContent='ORBIT · SPIN FOR 2×';}if($('shotValue'))$('shotValue').textContent='AURUM CIRCUIT / 01';}
function animateScoreChanges(){if(!state)return;for(const i of [1,2]){const el=$(`score${i}`),value=state.observation.scores[`p${i}`];if(el.dataset.previous!==undefined&&Number(el.dataset.previous)!==value)el.animate([{color:i===1?cyan:gold,transform:'scale(1.12)'},{color:'#edf4ff',transform:'scale(1)'}],{duration:600,easing:'ease-out'});el.dataset.previous=String(value);}}
function polygon(points,fill,stroke,width=1){ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke();}}
function screw(x,y,r=3){circle(x,y,r,'#263f4b','#a9b6b7',.7);line(x-r*.5,y,x+r*.5,y,'#0b1520',1);}
function glowingLine(x,y,x2,y2,color,width=1,blur=7){ctx.save();ctx.shadowColor=color;ctx.shadowBlur=blur;line(x,y,x2,y2,color,width);ctx.restore();}
function chevron(x,y,angle,color,scale=1){ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.beginPath();ctx.moveTo(-4*scale,-3*scale);ctx.lineTo(0,2*scale);ctx.lineTo(4*scale,-3*scale);ctx.strokeStyle=color;ctx.lineWidth=1.3;ctx.stroke();ctx.restore();}
function aurumInlays(now){if(!state?.observation.devices)return;ctx.save();ctx.translate(O,O);
  const plate=ctx.createLinearGradient(0,35,0,175);plate.addColorStop(0,'#081d2be8');plate.addColorStop(1,'#122d3b80');
  const top=[[185,43],[815,43],[853,81],[803,174],[197,174],[147,81]];
  polygon(top,plate,'#8ca7b224',.8);polygon(top.map(([x,y])=>[x,500-y]),'#091d2c99','#8ca7b224',.8);
  // Etched circuit traces are flush decoration, never collision walls.
  for(const sign of [1,-1]){const y=v=>sign===1?v:500-v;
    for(const x of [215,245,755,785]){line(x,y(66),x,y(142),'#8bc2c313',.8);line(x,y(142),x+(x<500?25:-25),y(165),'#8bc2c313',.8);circle(x,y(66),2,null,'#c1ac7233',.6);}
    for(const x of [330,670]){circle(x,y(112),49,null,'#c6b87c22',.8);ctx.setLineDash([2,7]);circle(x,y(112),55,null,'#91d4dc14',1);ctx.setLineDash([]);}
  }
  for(const right of [false,true]){ctx.save();if(right){ctx.translate(1000,0);ctx.scale(-1,1);}
    polygon([[20,105],[67,105],[76,130],[76,322],[138,372],[147,419],[81,444],[19,380]],'#061a29cc','#4b99ac3c',1);
    const laneGlow=ctx.createLinearGradient(20,0,79,0);laneGlow.addColorStop(0,'#45dce91a');laneGlow.addColorStop(.6,'#45dce903');laneGlow.addColorStop(1,'#45dce91f');
    polygon([[22,118],[70,118],[70,323],[135,377],[137,411],[77,429],[23,378]],laneGlow);
    for(let y=138;y<327;y+=13)line(25,y,31,y-5,'#8bc2d22d',1);
    line(37,137,37,324,'#61d9e52c',.8);
    for(let i=0;i<5;i++){const alpha=.15+.18*(.5+.5*Math.sin(now*.0015-i*.75));chevron(51,160+i*27,0,hex(cyan,alpha),1.25);}
    ctx.save();ctx.translate(59,216);ctx.rotate(-Math.PI/2);if(right)ctx.scale(-1,1);text('R E T U R N',0,0,7,'#87bfc578');ctx.restore();
    roundRect(27,342,38,17,3,'#0b2331','#77a1a539',.7);ctx.save();ctx.translate(46,351);if(right)ctx.scale(-1,1);text('+10',0,0,8,'#a6d0cdad');ctx.restore();
    for(const [x,y] of [[21,113],[74,129],[76,322],[138,405]])screw(x,y,2.5);
    ctx.restore();
  }
  ctx.save();ctx.globalAlpha=.15;
  for(const x of [183,817]){line(x,202,x,298,'#a5c9cf',.6);line(x,202,x+(x<500?26:-26),202,'#a5c9cf',.6);line(x,298,x+(x<500?26:-26),298,'#a5c9cf',.6);}
  line(408,228,592,228,'#b8c5b7',.6);line(435,286,565,286,'#b8c5b7',.6);
  text('A U R U M',500,245,22,'#d8e3d8','center',300);text('C I R C U I T',500,268,9,'#d8e3d8','center',500);ctx.restore();
  text('ORBIT ROUTE',500,39,7,'#c5bc948c');
  text('QUAD POP ARRAY',500,455,7,'#92b9c573');
  // Flush service covers, engraved markings and seam detail.
  for(const [x,y] of [[180,70],[820,70],[180,430],[820,430]]){roundRect(x-13,y-9,26,18,4,'#102735','#9bafac27',.7);line(x-7,y-3,x+7,y-3,'#809b9d3a',.6);line(x-7,y+2,x+7,y+2,'#809b9d3a',.6);}
  ctx.restore();
}
function drawGuide(rail,now){const [ax,ay]=rail.a,[bx,by]=rail.b;const color=rail.id.includes('orbit')?gold:cyan;
  const pulse=effects.findLast(e=>e.type==='rail'&&e.rail===rail.id&&now-e.born<300);
  const a={x:ax+O,y:ay+O},b={x:bx+O,y:by+O};
  ctx.save();ctx.lineCap='round';ctx.shadowColor='#000c';ctx.shadowOffsetY=3;ctx.shadowBlur=6;
  line(a.x,a.y,b.x,b.y,'#06121b',13);ctx.shadowOffsetY=0;ctx.shadowBlur=0;
  const tube=ctx.createLinearGradient(a.x-4,a.y-4,b.x+4,b.y+4);tube.addColorStop(0,'#d5d8bc');tube.addColorStop(.2,'#7a8e8d');tube.addColorStop(.45,'#2f4d58');tube.addColorStop(.66,'#9fbaae');tube.addColorStop(1,'#415d61');
  line(a.x,a.y,b.x,b.y,tube,8);line(a.x-1,a.y-1,b.x-1,b.y-1,pulse?color:'#d0e1d982',1.2);
  if(pulse)glowingLine(a.x,a.y,b.x,b.y,hex(color,.8),3,12);
  for(const p of [a,b]){circle(p.x,p.y,6,'#112632','#7b9da777',.7);screw(p.x,p.y,3.5);}
  ctx.restore();
}
function drawLanes(now){ctx.save();ctx.translate(O,O);for(const lane of state.observation.devices.lanes){
  const pulse=effects.some(e=>e.type==='lane'&&e.lane===lane.id&&now-e.born<650);
  const alpha=pulse?1:.5;ctx.save();ctx.globalAlpha=alpha;
  glowingLine(lane.x_min,lane.y,lane.x_max,lane.y,cyan,1,8);
  for(let x=lane.x_min+3;x<lane.x_max;x+=7)roundRect(x,lane.y-3,3,6,1,pulse?'#b9fbff':'#4190a0');
  for(const x of [lane.x_min-4,lane.x_max+4]){roundRect(x-3,lane.y-9,6,18,2,'#132b37','#bda46a',.6);circle(x,lane.y,1.5,cyan);}
  ctx.restore();}ctx.restore();}
function drawSpinner(now){const spinner=state.observation.devices.spinner;const x=(spinner.x_min+spinner.x_max)/2+O,y=spinner.y+O;
  const event=effects.findLast(e=>e.type==='spinner'&&now-e.born<1500);const age=event?(now-event.born)/1000:0;
  const rotation=event?age*22*Math.exp(-age*.8):0;const width=event?Math.max(3,Math.abs(Math.cos(rotation))*52):52;
  const color=activeMultiplier===2?gold:cyan;
  ctx.save();
  // Recessed support deck, riveted feet and a freely turning center paddle.
  roundRect(x-51,y-22,102,46,9,'#071a27','#718e9c66',1);
  for(const sign of [-1,1]){roundRect(x+sign*42-7,y-18,14,36,4,'#223b46','#92a2a5',.7);screw(x+sign*42,y-11,2.5);screw(x+sign*42,y+11,2.5);}
  line(x-40,y,x+40,y,'#d5c18d',3);line(x-36,y-1,x+36,y-1,'#f3e2b7',.7);
  ctx.shadowColor=color;ctx.shadowBlur=event?22:8;
  const paddle=ctx.createLinearGradient(x-width/2,y-10,x+width/2,y+10);paddle.addColorStop(0,'#819c9d');paddle.addColorStop(.18,'#1b4758');paddle.addColorStop(.55,'#0e293c');paddle.addColorStop(1,'#c9b57f');
  roundRect(x-width/2,y-11,width,22,3,paddle,color,1.3);ctx.shadowBlur=0;
  if(width>22)text('2×',x,y,13,event?'#fff3cb':'#b9eced','center',650);
  roundRect(x-39,y+29,78,15,3,'#0c2431','#8f9a7c52',.6);text('O R B I T',x,y+36,7,'#d1c393');
  text(activeMultiplier===2?'2× POT VALUE':'SPIN TO LIGHT 2×',x,y+51,6.5,hex(color,.75));
  for(const sign of [-1,1]){circle(x+sign*49,y+1,2,color);chevron(x+sign*65,y,sign<0?-Math.PI/2:Math.PI/2,hex(gold,.55),1.2);}
  ctx.restore();
}
function aurumDevices(now){if(!state?.observation.devices)return;for(const rail of state.observation.devices.guides)drawGuide(rail,now);drawLanes(now);drawSpinner(now);}
function mechanicalBumper(b,now){const x=b.x+O,y=b.y+O,color=bumperColor(b);
  const hit=effects.findLast(e=>e.type==='bumper'&&e.bumper===b.id&&now-e.born<800);const age=hit?(now-hit.born)/800:1;const pulse=hit?Math.pow(1-age,2):0;
  ctx.save();ctx.shadowColor='#000b';ctx.shadowBlur=8;ctx.shadowOffsetY=5;
  circle(x,y,39,'#0b1b29','#496371',1);ctx.shadowBlur=0;ctx.shadowOffsetY=0;
  for(let i=0;i<16;i++){const a=i*TAU/16;ctx.save();ctx.translate(x+Math.cos(a)*35,y+Math.sin(a)*35);ctx.rotate(a);roundRect(-2,-3.5,4,7,1,i%2?'#254252':'#0c202d');ctx.restore();}
  let metal=ctx.createLinearGradient(x-32,y-32,x+32,y+32);metal.addColorStop(0,'#d8d5b5');metal.addColorStop(.18,'#647c85');metal.addColorStop(.45,'#203946');metal.addColorStop(.75,'#93a8a8');metal.addColorStop(1,'#435d66');
  circle(x,y,32,metal,'#0a1724',1.4);circle(x,y,29,'#102c3c',hex(color,.9),2);
  ctx.shadowColor=color;ctx.shadowBlur=14+25*pulse;circle(x,y,25+1.8*pulse,'#0b2535',color,1.8+1.5*pulse);ctx.shadowBlur=0;
  const dome=ctx.createRadialGradient(x-8,y-11,1,x+4,y+4,30);dome.addColorStop(0,hex(color,.55+.2*pulse));dome.addColorStop(.4,hex(color,.18));dome.addColorStop(1,'#061522');circle(x,y,22,dome,hex(color,.25),.7);
  ctx.beginPath();ctx.ellipse(x-5,y-11,11,3,-.4,0,TAU);ctx.fillStyle='#d3ffff38';ctx.fill();
  text('✦',x,y-1,23,hit?'#f7ffe9':color);
  for(let i=0;i<4;i++){const a=i*Math.PI/2+Math.PI/4;screw(x+Math.cos(a)*35,y+Math.sin(a)*35,2.5);}
  ctx.beginPath();ctx.arc(x,y,33,-2.8,-.5);ctx.strokeStyle=hex(color,.9);ctx.lineWidth=2.5;ctx.stroke();
  roundRect(x-29,y+44,58,13,3,'#0a1c2b','#7b9a9d44',.6);text('+15  POP',x,y+51,6.5,hex(color,.85));
  ctx.restore();
}
function receiveDeviceEvent(event,now){effects.push({...event,born:now});
  if(event.type==='spinner'&&event.activated){activeMultiplier=2;deviceShotPoints+=event.points;}
  else if(event.type==='scratch'){deviceShotPoints=0;activeMultiplier=1;}
  else if(event.points)deviceShotPoints+=event.points;
  const badge=$('orbitBadge');if(badge){badge.classList.toggle('lit',activeMultiplier===2);badge.textContent=activeMultiplier===2?'ORBIT 2× ACTIVE':'ORBIT · SPIN FOR 2×';}
  if($('shotValue'))$('shotValue').textContent=busy?`SHOT ${deviceShotPoints.toString().padStart(3,'0')}`:'AURUM CIRCUIT / 01';
}
function deviceFeedback(fx,now){const age=(now-fx.born)/1000;if(age>1.3)return;const alpha=Math.max(0,1-age/1.3),x=fx.x+O,y=fx.y+O;
  let color=fx.type==='scratch'?'#f193a4':fx.type==='bumper'?(state.observation.bumpers.find(b=>b.id===fx.bumper)?.color==='gold'?gold:cyan):fx.type==='lane'?cyan:gold;
  ctx.save();ctx.globalAlpha=alpha;
  if(fx.type==='rail'){circle(x,y,4+age*17,null,'#ccdee6',.7);ctx.restore();return;}
  const ring=fx.type==='bumper'?27:15;
  circle(x,y,ring+age*65,null,color,Math.max(.5,2-age));
  for(let i=0;i<(fx.type==='bumper'?18:12);i++){const a=i*TAU/(fx.type==='bumper'?18:12)+(fx.ball||0),r=12+age*80;line(x+Math.cos(a)*r,y+Math.sin(a)*r,x+Math.cos(a)*(r+5+4*(i%3)),y+Math.sin(a)*(r+5+4*(i%3)),color,1.4);}
  const label=fx.type==='scratch'?'FOUL — SHOT VOID':fx.type==='spinner'?(fx.activated?'ORBIT 2×  +25':'SPIN'):fx.type==='lane'?(fx.points?'+10 RETURN':'RETURN'):fx.type==='pocket'?`+${fx.points||100}${fx.multiplier===2?' · 2× POT':''}`:fx.points?'+15':'';
  if(label){ctx.shadowColor=color;ctx.shadowBlur=9;text(label,x,y-27-age*24,fx.type==='spinner'?14:15,color,'center',650);}
  ctx.restore();
}
function rayGuide(origin,dir,rail){const a={x:rail.a[0],y:rail.a[1]},b={x:rail.b[0],y:rail.b[1]},r=11+rail.radius;let result=Math.min(rayCircle(origin,dir,a,r),rayCircle(origin,dir,b,r));
  const length=Math.hypot(b.x-a.x,b.y-a.y),tx=(b.x-a.x)/length,ty=(b.y-a.y)/length,nx=-ty,ny=tx;
  const distance=(origin.x-a.x)*nx+(origin.y-a.y)*ny,velocity=dir.x*nx+dir.y*ny;
  if(Math.abs(velocity)>1e-8)for(const side of [-1,1]){const t=(side*r-distance)/velocity;if(t>0){const along=(origin.x+dir.x*t-a.x)*tx+(origin.y+dir.y*t-a.y)*ty;if(along>=0&&along<=length)result=Math.min(result,t);}}
  return result;
}
