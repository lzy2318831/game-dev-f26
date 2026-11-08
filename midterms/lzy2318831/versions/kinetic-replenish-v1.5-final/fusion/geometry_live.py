"""Opt-in experimental geometry-assisted browser mode; no calls by default."""
import argparse
import threading
import json
import secrets
from copy import deepcopy
from .live_demo import LiveHandler, EntryHandler, make_live_servers, ASSETS
from .live_session import LiveSession
from .geometry_agent import GeometryPlayer, VARIANT, PROMPT_SHA256,ADAPTIVE_PROMPT_SHA256, offline_response,validate_power_multiplier
from .geometry_adaptive_power import ADAPTIVE_FORMULA
from .freeze import main as check_freeze
from .geometry_budget import ServerBudget,GeometryMatchLedger


class GeometrySession(LiveSession):
    def policy_type(self,**kwargs):
        return GeometryPlayer(power_multiplier=self.power_multiplier or 1,adaptive=self.adaptive,**kwargs)
    variant=VARIANT
    prompt_sha256=PROMPT_SHA256
    trace_kind='LIVE_BROWSER_GEOMETRY_ASSISTED_V1'
    evidence_folder='live-browser-geometry-v1'
    seat_name=VARIANT

    def __init__(self,root=None,enable_paid=False,transport=None,server_budget=None,match_number=1,power_multiplier=1,adaptive=False):
        self.server_budget=server_budget or ServerBudget();self.match_number=match_number
        validate_power_multiplier(power_multiplier)
        if type(adaptive) is not bool:raise ValueError('Adaptive flag must be boolean')
        self.adaptive=adaptive;self.power_multiplier=None if adaptive else power_multiplier
        self.prompt_sha256=ADAPTIVE_PROMPT_SHA256 if adaptive else PROMPT_SHA256
        super().__init__(root,enable_paid,transport)
        self._last_public_state=None
        self.state()

    def make_ledger(self,path):
        return GeometryMatchLedger(path,self.cancel_event,self.server_budget)

    def state(self):
        result=super().state();budget=self.server_budget.snapshot()
        result['live'].update(server_budget=budget,match_number=self.match_number,power_multiplier=self.power_multiplier,
            power_mode='adaptive' if self.adaptive else str(self.power_multiplier)+'x')
        result['live']['can_start'] &= budget['can_start']
        self._last_public_state=deepcopy(result)
        return result

    def peek_state(self):
        result=deepcopy(self._last_public_state)
        if self.cancel_event.is_set() and self.worker and self.worker.is_alive():
            result['live'].update(phase='stopping',can_start=False,reason='user_cancelled')
        return result

    def leave(self):
        # Signal first: reserve/commit guards see cancellation without this lock.
        self.cancel_event.set();self.playback_done.set()
        if self.lock.acquire(timeout=.05):
            try:
                if self.phase=='waiting':self.phase='cancelled';self.stop_reason='user_cancelled_before_confirmation'
                elif self.phase not in ('complete','failed','cancelled'):
                    self.phase='stopping';self.stop_reason='user_cancelled'
                self.playback_done.set()
            finally:self.lock.release()
        worker=self.worker
        if worker and worker is not threading.current_thread():worker.join(.4)
        state=self.peek_state();settled=worker is None or not worker.is_alive()
        if settled:state['live'].update(phase=self.phase,reason=self.stop_reason,can_start=False)
        return dict(safe_to_navigate=True,settled=settled,state=state)

    def start(self,confirmed,nonce):
        if not self.server_budget.snapshot()['can_start']:
            raise ValueError('Server budget cannot cover a fresh six-request/$0.25 match')
        return super().start(confirmed,nonce)

    def set_power_multiplier(self,value):
        value=validate_power_multiplier(value)
        return self.set_power_setting(value)

    def set_power_setting(self,value):
        if value!='adaptive':validate_power_multiplier(value)
        with self.lock:
            if self.phase!='waiting' or self.cancel_event.is_set() or (self.worker and self.worker.is_alive()):
                raise ValueError('Power can change only before a fresh match starts')
            self.adaptive=value=='adaptive';self.power_multiplier=None if self.adaptive else value
            self.prompt_sha256=ADAPTIVE_PROMPT_SHA256 if self.adaptive else PROMPT_SHA256
            return self.state()

    def _persist(self):
        if self.trace is not None:
            self.trace.update(server_budget=self.server_budget.snapshot(),match_number=self.match_number,
                power_multiplier=self.power_multiplier,power_mode='adaptive' if self.adaptive else str(self.power_multiplier)+'x',
                power_formula=ADAPTIVE_FORMULA if self.adaptive else 'min(100, original_power * power_multiplier)')
            self.trace.setdefault('consent',{})['power_multiplier']=self.power_multiplier
            self.trace['consent']['power_mode']='adaptive' if self.adaptive else str(self.power_multiplier)+'x'
        super()._persist()


class GeometryHandler(LiveHandler):
    def do_GET(self):
        if self.path=='/navigation.js' and self.valid_host():
            script='window.KineticMenuURL='+json.dumps(self.server.menu_url)+';\n'
            script+=(ASSETS.parent/'geometry_navigation.js').read_text(encoding='utf-8')
            self.reply(200,script.encode(),'text/javascript; charset=utf-8');return
        if self.path=='/live.js' and self.valid_host():
            script=(ASSETS/'live.js').read_text(encoding='utf-8')
            script=script.replace('kinetic-prompt-v2-risk-aware',VARIANT)
            script=script.replace('Real prompt-v2 live mode.','Experimental geometry-assisted live mode.')
            script=script.replace('Let the agent choose.','Geometry-assisted LLM: choose a candidate.')
            script=script.replace('Authorize ONE autonomous GPT-5.4 mini match:',
                'Authorize ONE Geometry-Assisted GPT-5.4 mini match:')
            script=script.replace("api('/live/info').then(info=>{","geometryLoadInfo().then(info=>{")
            script=script.replace('no retries? The key stays',
                'no retries? Server total is 12 requests/$0.50 estimated across matches. The key stays')
            script=script.replace('if(!window.confirm(message))return;',
                "if(!window.confirm(message+' Candidate power '+(liveInfo.power_mode||liveInfo.power_multiplier+'x')+'. Stronger power increases scratch risk.'))return;")
            script+='\n'+(ASSETS.parent/'geometry_status.js').read_text(encoding='utf-8')
            script+='\n'+(ASSETS.parent/'geometry_power.js').read_text(encoding='utf-8')
            self.reply(200,script.encode('utf-8'),'text/javascript; charset=utf-8');return
        super().do_GET()

    def do_POST(self):
        if self.path not in ('/live/new','/live/power'):return super().do_POST()
        expected={f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}
        if not self.valid_host() or self.headers.get('Origin') not in expected:
            self.reply(403,dict(error='Same-origin local request required'));return
        with self.server.match_lock:
            old=self.server.live_session;token=self.headers.get('X-Live-Token','')
            if not token or not secrets.compare_digest(token,old.nonce):
                self.reply(403,dict(error='Current match token required'));return
            try:
                size=int(self.headers.get('Content-Length','0'))
                if size<2 or size>512 or not self.headers.get('Content-Type','').startswith('application/json'):raise ValueError()
                body=json.loads(self.rfile.read(size))
                if self.path=='/live/power':
                    if isinstance(body,dict) and set(body)=={'power_mode'} and body['power_mode']=='adaptive':
                        self.reply(200,old.set_power_setting('adaptive'));return
                    if not isinstance(body,dict) or set(body)!={'power_multiplier'}:raise ValueError()
                    self.reply(200,old.set_power_multiplier(body['power_multiplier']));return
                if body!={}:raise ValueError()
                if old.phase not in ('complete','failed','cancelled') or (old.worker and old.worker.is_alive()):
                    raise ValueError('Previous match must finish or settle cancellation first')
                fresh=GeometrySession(old.root,old.enable_paid,old.transport,old.server_budget,old.match_number+1,old.power_multiplier or 1,old.adaptive)
                self.server.live_session=fresh
                self.reply(200,dict(nonce=fresh.nonce,state=fresh.state()))
            except (ValueError,TypeError):
                self.reply(400,dict(error='Settings/new-match request refused: use a settled fresh waiting match and power 1 or 2.'))


class GeometryEntryHandler(EntryHandler):
    def do_GET(self):
        if self.path=='/geometry-status':
            session=self.server.geometry_live_server.live_session
            self.reply(200,dict(live=session.peek_state()['live'],settled=not(session.worker and session.worker.is_alive())));return
        super().do_GET()

    def reply(self,status,body,content_type='application/json; charset=utf-8',cookie=None):
        if self.path=='/menu.js' and status==200:
            body=body.decode('utf-8').replace("['Live LLM Agent','/live']",
                "['Geometry-Assisted Live LLM','/live']").encode('utf-8')
            body+=b"\nfetch('/geometry-status').then(r=>r.json()).then(s=>{const p=document.createElement('p');p.className='modal-footnote';const b=s.live.server_budget;p.textContent=!s.settled?'Previous live work is settling; ordinary game modes remain available.':!b.can_start?'Live server allowance exhausted; no further paid match can start. Ordinary modes and replay remain available.':`Live server allowance: ${b.calls}/${b.call_cap} requests used; a new match needs fresh consent.`;document.querySelector('#intro .modal').append(p);}).catch(()=>{});"
        super().reply(status,body,content_type,cookie)


def make_geometry_servers(port=8835,replay_port=8837,live_port=8839,enable_paid=False,transport=None,root=None,power_multiplier=2):
    game,recorded,live=make_live_servers(port,replay_port,live_port,enable_paid,transport,root)
    live.RequestHandlerClass=GeometryHandler
    game.RequestHandlerClass=GeometryEntryHandler
    live.live_session=GeometrySession(root,enable_paid,transport,power_multiplier=power_multiplier)
    live.match_lock=threading.RLock()
    game.geometry_live_server=live
    return game,recorded,live


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',type=int,default=8835);p.add_argument('--replay-port',type=int,default=8837)
    p.add_argument('--live-port',type=int,default=8839)
    mode=p.add_mutually_exclusive_group();mode.add_argument('--enable-paid',action='store_true');mode.add_argument('--mock',action='store_true')
    args=p.parse_args();check_freeze()
    servers=make_geometry_servers(args.port,args.replay_port,args.live_port,args.enable_paid,offline_response if args.mock else None)
    game,recorded,live=servers
    threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in (recorded,live)]
    for t in threads:t.start()
    print(f'{VARIANT} | http://127.0.0.1:{game.server_port}/ | choose Geometry-Assisted Live LLM',flush=True)
    print('MOCK FIXTURES ONLY' if args.mock else 'Paid enabled, browser consent still required' if args.enable_paid else 'Paid DISABLED',flush=True)
    try:game.serve_forever()
    except KeyboardInterrupt:pass
    finally:
        live.live_session.cancel()
        if live.live_session.worker:live.live_session.worker.join(22)
        game.server_close()
        for s in (recorded,live):s.shutdown();s.server_close()
        for t in threads:t.join()


if __name__=='__main__':main()
