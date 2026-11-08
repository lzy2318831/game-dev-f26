"""Optional isolated-Chrome smoke test using Python's standard library.

Requires an explicitly started QA Chrome on localhost:9228, never attaches to
the user's ordinary browser profile. No browser or provider dependencies.
"""
import base64
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import time
from urllib.request import urlopen
from urllib.parse import urlparse


class CDP:
    def __init__(self,url):
        parsed=urlparse(url)
        if parsed.hostname not in ('localhost','127.0.0.1'): raise ValueError('Local QA target required')
        self.socket=socket.create_connection((parsed.hostname,parsed.port),timeout=20)
        self.socket.settimeout(20)
        key=base64.b64encode(os.urandom(16)).decode()
        self.socket.sendall(f'GET {parsed.path} HTTP/1.1\r\nHost: {parsed.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode())
        header=b''
        while not header.endswith(b'\r\n\r\n'): header+=self.socket.recv(1)
        if b' 101 ' not in header: raise RuntimeError('QA WebSocket handshake refused')
        self.sequence=0
        self.errors=[]

    def read(self,n):
        chunks=[]
        while n:
            chunk=self.socket.recv(n)
            if not chunk: raise EOFError('Chrome closed')
            chunks.append(chunk); n-=len(chunk)
        return b''.join(chunks)

    def send_frame(self,payload,opcode=1):
        length=len(payload)
        frame=bytes([128|opcode])
        if length<126: frame+=bytes([128|length])
        elif length<65536: frame+=bytes([128|126])+struct.pack('!H',length)
        else: frame+=bytes([128|127])+struct.pack('!Q',length)
        mask=os.urandom(4)
        frame+=mask+bytes(c^mask[i%4] for i,c in enumerate(payload))
        self.socket.sendall(frame)

    def receive(self):
        data=b''
        while True:
            first,second=self.read(2)
            length=second&127
            if length==126: length=struct.unpack('!H',self.read(2))[0]
            elif length==127: length=struct.unpack('!Q',self.read(8))[0]
            mask=self.read(4) if second&128 else None
            if length>10_000_000: raise RuntimeError('Oversized QA response')
            payload=self.read(length)
            if mask: payload=bytes(c^mask[i%4] for i,c in enumerate(payload))
            opcode=first&15
            if opcode==8: raise EOFError('Chrome closed')
            if opcode==9:
                self.send_frame(payload,10); continue
            if opcode in (0,1): data+=payload
            if first&128 and data: return json.loads(data)

    def command(self,method,params=None):
        self.sequence+=1
        self.send_frame(json.dumps(dict(id=self.sequence,method=method,params=params or {})).encode())
        while True:
            message=self.receive()
            if message.get('method')=='Runtime.exceptionThrown': self.errors.append(message['params'])
            if message.get('id')==self.sequence:
                if 'error' in message: raise RuntimeError(message['error'])
                return message.get('result',{})

    def evaluate(self,expression):
        result=self.command('Runtime.evaluate',dict(expression=expression,returnByValue=True,awaitPromise=True))
        if 'exceptionDetails' in result: raise RuntimeError(result['exceptionDetails'])
        return result['result'].get('value')

    def until(self,expression,seconds=10):
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            if self.evaluate(expression): return
            time.sleep(.1)
        raise AssertionError('Browser state did not arrive: '+expression)

    def screenshot(self,path):
        metrics=self.command('Page.getLayoutMetrics')['cssContentSize']
        result=self.command('Page.captureScreenshot',dict(format='png',captureBeyondViewport=True,
            clip=dict(x=0,y=0,width=metrics['width'],height=metrics['height'],scale=1)))
        path.write_bytes(base64.b64decode(result['data']))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-port',type=int,default=8765)
    parser.add_argument('--debug-port',type=int,default=9228)
    parser.add_argument('--evidence-dir',type=Path,default=Path('evidence/polish-1'))
    args=parser.parse_args()
    targets=json.load(urlopen(f'http://127.0.0.1:{args.debug_port}/json',timeout=5))
    targets=[t for t in targets if t.get('type')=='page' and t.get('url','').startswith(f'http://127.0.0.1:{args.game_port}/')]
    if len(targets)!=1: raise RuntimeError('Expected one isolated local game tab')
    c=CDP(targets[0]['webSocketDebuggerUrl'])
    evidence=args.evidence_dir.resolve()
    evidence.mkdir(parents=True,exist_ok=True)
    c.command('Page.enable'); c.command('Runtime.enable')
    c.command('Emulation.setDeviceMetricsOverride',dict(width=1440,height=1100,deviceScaleFactor=1,mobile=False))
    c.command('Page.reload',dict(ignoreCache=True))
    c.until("typeof state!=='undefined' && state!==null")
    c.evaluate("document.getElementById('hvb').click()")
    c.evaluate("document.getElementById('startButton').click()")
    c.until("started && !busy")
    time.sleep(1.5)
    layout_height=c.command('Page.getLayoutMetrics')['cssContentSize']['height']
    if layout_height>1100:
        print('Layout:',layout_height,c.evaluate("JSON.stringify([...document.querySelector('main').children].map(x=>[x.tagName,x.getBoundingClientRect().height,getComputedStyle(x).marginTop,getComputedStyle(x).marginBottom]))"))
        raise AssertionError('Desktop layout exceeds tested viewport')
    c.screenshot(evidence/'fusion-table.png')
    c.command('Emulation.setDeviceMetricsOverride',dict(width=1280,height=720,deviceScaleFactor=1,mobile=False))
    time.sleep(.15)
    laptop_height=c.command('Page.getLayoutMetrics')['cssContentSize']['height']
    if laptop_height>720:
        raise AssertionError('Laptop layout exceeds viewport: '+str(laptop_height))
    c.screenshot(evidence/'fusion-laptop.png')
    c.command('Emulation.setDeviceMetricsOverride',dict(width=1440,height=1100,deviceScaleFactor=1,mobile=False))
    time.sleep(.15)
    geometry=c.evaluate("(()=>{const r=canvas.getBoundingClientRect();const b=shown.find(b=>b.id===0);return {left:r.left,top:r.top,width:r.width,height:r.height,cue:b};})()")
    target=c.evaluate('state.observation.bumpers[0]')
    dx,dy=target['x']-geometry['cue']['x'],target['y']-geometry['cue']['y']
    norm=(dx*dx+dy*dy)**.5
    dx,dy=dx/norm,dy/norm
    def point(distance):
        return dict(x=geometry['left']+(geometry['cue']['x']+56+dx*distance)/1112*geometry['width'],
                    y=geometry['top']+(geometry['cue']['y']+56+dy*distance)/612*geometry['height'])
    start,end=point(180),point(60)
    c.command('Input.dispatchMouseEvent',dict(type='mouseMoved',**start))
    c.command('Input.dispatchMouseEvent',dict(type='mousePressed',button='left',buttons=1,clickCount=1,**start))
    c.command('Input.dispatchMouseEvent',dict(type='mouseMoved',button='left',buttons=1,**end))
    drag_power=c.evaluate('power')
    if not 60<=drag_power<=70: raise AssertionError('Drag did not charge power')
    c.command('Input.dispatchMouseEvent',dict(type='mouseReleased',button='left',buttons=0,clickCount=1,**end))
    c.until('busy && movie!==null')
    shot_events=c.evaluate('movie.events')
    if not any(e['type']=='bumper' for e in shot_events): raise AssertionError('Bumper not exercised')
    c.screenshot(evidence/'fusion-in-motion.png')
    # Wait for real playback and the automatically selected baseline reply.
    c.until("!busy && state.observation.shots_remaining.p1===5 && state.observation.shots_remaining.p2===5",seconds=50)
    c.screenshot(evidence/'fusion-after-shot.png')
    result=dict(drag_power=drag_power,first_shot_events=shot_events,
                state_after_human_and_baseline=c.evaluate('state'),desktop_layout_height=layout_height,laptop_layout_height=laptop_height)
    # Exercise the new traversable spinner through the real public UI action.
    c.evaluate("reset('hvh')")
    c.until('started && !busy')
    c.evaluate('fire({angle:328,power:45})')
    c.until('busy && movie!==null')
    spinner=c.evaluate("movie.events.find(e=>e.type==='spinner'&&e.activated)")
    if not spinner: raise AssertionError('Orbit route did not activate the spinner')
    c.evaluate(f"movie.start=performance.now()-{(spinner['t']+.03)*1000}")
    c.until('activeMultiplier===2')
    c.screenshot(evidence/'aurum-orbit-active.png')
    c.evaluate('movie.start-=movie.frames[movie.frames.length-1].t*1000+500')
    c.until('!busy')
    if c.evaluate('activeMultiplier')!=1: raise AssertionError('Multiplier leaked into next shot')
    result['spinner']=spinner
    result['multiplier_reset']=True
    # End-screen integration check. Only presentation time is accelerated;
    # all twelve shots still resolve in the authoritative Python engine.
    c.evaluate("reset('hvh')")
    c.until('started && !busy')
    for shot in range(12):
        if c.evaluate("state.outcome.status==='terminal'"): break
        c.evaluate(f"fire({{angle:{shot*127%360},power:65}})")
        c.until('busy && movie!==null')
        c.evaluate('movie.start-=movie.frames[movie.frames.length-1].t*1000+500')
        c.until('!busy')
    c.until("!document.getElementById('gameOver').classList.contains('hidden')",seconds=5)
    c.screenshot(evidence/'fusion-game-over.png')
    result['ending']=c.evaluate('state.outcome')
    result['end_screen_time_accelerated']=True
    # Reproduce a real reset/late-network-response race with 300 ms latency.
    c.evaluate("reset('hvh')")
    c.until('started && !busy')
    race=c.evaluate("""(async()=>{const original=window.fetch;let arrived;const shotArrived=new Promise(r=>arrived=r);window.fetch=async(...args)=>{const response=await original(...args);if(args[0]==='/api/shot'){arrived();await new Promise(r=>setTimeout(r,300));}return response;};fire({angle:0,power:30});await shotArrived;await reset('hvh');await new Promise(r=>setTimeout(r,500));window.fetch=original;return {staleMovie:movie!==null,busy,shots:state.observation.shots_remaining};})()""")
    if race['staleMovie'] or race['busy'] or race['shots']!={'p1':6,'p2':6}:
        print('Reset race:',race)
        raise AssertionError('Late shot response leaked into restarted match')
    result['reset_race']=race
    result['device_count']=c.evaluate('state.observation.bumpers.length')
    result['guide_count']=c.evaluate('state.observation.devices.guides.length')
    result['javascript_errors']=c.errors
    if c.errors: raise AssertionError('Browser JavaScript exception')
    (evidence/'fusion-browser-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('PASS: mouse drag, power, bumper, playback lock, baseline turn, full match ending, viewport fit; zero JS exceptions')
    c.socket.close()


if __name__=='__main__': main()
