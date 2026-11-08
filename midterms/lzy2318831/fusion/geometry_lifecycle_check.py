"""Opt-in isolated headless Chrome + real local HTTP, synthetic LLM only."""
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import time
from urllib.request import urlopen
from .browser_check import CDP
from .geometry_live import make_geometry_servers
from .geometry_agent import offline_response
from .runner import replay
from .llm import CallFailure

def synthetic_http_failure(payload,timeout):
    raise CallFailure('provider_error',dict(error_kind='http_error',http_status=429,network_attempted=False))

def synthetic_invalid_selection(payload,timeout):
    result=offline_response(payload,timeout)
    result['output'][0]['content'][0]['text']='{"candidate_id":999999}'
    return result

def synthetic_timeout(payload,timeout):
    time.sleep(2)
    return offline_response(payload,timeout)



def run(chrome,output,failure=False,scenario=None,power_switch=False,adaptive_switch=False,cue_check=False,balanced_table=False,historical_view=False):
    power_switch=power_switch or adaptive_switch
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    game,recorded,live=make_geometry_servers(0,0,0,transport=offline_response,root=output/'matches',power_multiplier=2 if power_switch else 1)
    if failure:
        # QA fixture: replay the saved genuine proposal sequence through the real
        # engine and HTTP lifecycle. Not production candidate generation.
        from .geometry_agent import GeometryPlayer
        class HistoricalFailurePlayer(GeometryPlayer):
            def request(self,observation,legal,history=()):
                payload=super().request(observation,legal,history)
                context=json.loads(payload['input'][1]['content'])
                angle,power=[(0,27),(278,3),(164,1),(266,4)][6-observation['shots_remaining']['p1']]
                context['candidates'][0].update(angle=angle,power=power,risk='QA historical failure reproduction only')
                payload['input'][1]['content']=json.dumps(context)
                return payload
        live.live_session.policy_type=HistoricalFailurePlayer
    if scenario:
        live.live_session.transport={'http_error':synthetic_http_failure,'invalid_candidate_selection':synthetic_invalid_selection,'request_timeout':synthetic_timeout,'user_cancelled':synthetic_timeout}[scenario]
        if scenario=='request_timeout':live.live_session.request_timeout=.15
    servers=(game,recorded,live);threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in servers]
    for thread in threads:thread.start()
    process=None;cdp=None
    try:
        with tempfile.TemporaryDirectory(prefix='kinetic-lifecycle-',ignore_cleanup_errors=True) as profile:
            process=subprocess.Popen([str(chrome),'--headless=new','--disable-gpu','--no-first-run',
                '--remote-debugging-port=0','--window-size=1360,900','--user-data-dir='+profile,'about:blank'],
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            port_file=Path(profile)/'DevToolsActivePort';deadline=time.monotonic()+20
            while not port_file.exists() and time.monotonic()<deadline:time.sleep(.1)
            port=int(port_file.read_text().splitlines()[0])
            with urlopen(f'http://127.0.0.1:{port}/json/list') as response:tabs=json.load(response)
            cdp=CDP(next(t['webSocketDebuggerUrl'] for t in tabs if t['type']=='page'))
            cdp.command('Page.enable');cdp.command('Runtime.enable')
            # QA-only clock acceleration. Physics and model selection stay on server.
            cdp.command('Page.addScriptToEvaluateOnNewDocument',dict(source="""
                window.confirm=()=>true;
                const qaNow=performance.now.bind(performance),qaFrame=requestAnimationFrame.bind(window),qaTimer=setTimeout.bind(window);
                Object.defineProperty(performance,'now',{value:()=>qaNow()*40});
                window.requestAnimationFrame=fn=>qaFrame(t=>fn(t*40));
                window.setTimeout=(fn,delay,...args)=>qaTimer(fn,delay===1000?1:delay===600?20:delay,...args);
            """))
            if cue_check:
                cdp.command('Page.addScriptToEvaluateOnNewDocument',dict(source="window.qaRealFrame=requestAnimationFrame;window.requestAnimationFrame=fn=>{window.qaNextFrame=fn;};"))
            menu=f'http://127.0.0.1:{game.server_port}/'
            cdp.command('Page.navigate',dict(url=menu));results=[]
            if historical_view:
                cdp.until("document.querySelector('a[href=\"/watch\"]')!==null",20)
                cdp.evaluate("document.querySelector('a[href=\"/watch\"]').click()")
                cdp.until("typeof replayInfo!=='undefined'&&replayInfo?.physics_version==='fusion-1.5.0-replenish'&&state",20)
                original=cdp.evaluate("({version:state.version,guides:state.observation.devices.guides,identity:document.getElementById('replayIdentity').textContent})")
                assert original['version']=='fusion-1.5.0-replenish' and len(original['guides'])==29
                assert {'left-entry','right-entry'}<={r['id'] for r in original['guides']}
                assert original['version'] in original['identity']
                (output/'historical-view-proof.json').write_text(json.dumps(original,indent=2))
                png=cdp.evaluate("drawTable(performance.now());canvas.toDataURL('image/png').split(',')[1]")
                (output/'original-v15-playfield.png').write_bytes(base64.b64decode(png))
                cdp.evaluate("document.getElementById('intro').classList.add('hidden');drawTable(performance.now())")
                cdp.screenshot(output/'original-v15-table.png')
                cdp.command('Page.navigate',dict(url=menu))
            for number in (1,2):
                cdp.until("Array.from(document.querySelectorAll('a[href=\"/live\"]')).some(a=>a.textContent==='Geometry-Assisted Live LLM')",20)
                cdp.evaluate("document.querySelector('a[href=\"/live\"]').click()")
                cdp.until(f"typeof liveInfo!=='undefined'&&liveInfo?.phase==='waiting'&&liveInfo.match_number==={number}",25)
                info=cdp.evaluate('liveInfo')
                assert info['mocked'] is True and info['calls']==0 and info['server_budget']['calls']==(1 if scenario else 4 if failure else 6)*(number-1)
                if balanced_table and number==1:
                    cdp.until("state&&state.observation?.devices?.guides",10)
                    table=cdp.evaluate("""(()=>{const ids=[],original=drawGuide;
                      drawGuide=(rail,now)=>{ids.push(rail.id);original(rail,now);};drawTable(performance.now());drawGuide=original;
                      return {version:state.version,guides:state.observation.devices.guides,drawn:ids,pockets:state.observation.table.pockets};})()""")
                    assert table['version']=='fusion-1.6.0-balanced' and len(table['guides'])==27
                    assert set(table['drawn'])=={r['id'] for r in table['guides']}
                    assert not {'left-entry','right-entry'}&set(table['drawn'])
                    assert all(side+'-'+part in table['drawn'] for side in ('left','right') for part in ('orbit-rise','orbit-crown','orbit-roof'))
                    assert len(table['pockets'])==6
                    (output/'rendered-table-proof.json').write_text(json.dumps(table,indent=2))
                    png=cdp.evaluate("drawTable(performance.now());canvas.toDataURL('image/png').split(',')[1]")
                    (output/'balanced-playfield.png').write_bytes(base64.b64decode(png))
                    cdp.evaluate("document.getElementById('intro').classList.add('hidden')")
                    cdp.screenshot(output/'balanced-table.png')
                    cdp.evaluate("document.getElementById('intro').classList.remove('hidden')")
                if power_switch:
                    expected_power='adaptive' if adaptive_switch and number==1 else 2 if number==1 else 1
                    if number==2 or adaptive_switch:
                        cdp.evaluate(f"document.getElementById('geometryPower').value='{expected_power}';document.getElementById('geometryPower').dispatchEvent(new Event('change'))")
                    condition="liveInfo.power_mode==='adaptive'" if expected_power=='adaptive' else f'liveInfo.power_multiplier==={expected_power}'
                    cdp.until(condition+'&&!geometryPowerBusy',10)
                    assert cdp.evaluate("document.getElementById('geometryPower').value")==str(expected_power)
                    label='Adaptive energy' if expected_power=='adaptive' else f'{expected_power}x'
                    assert label in cdp.evaluate("document.getElementById('liveBudget').textContent")
                    # Declining consent must dispatch no synthetic/model call either.
                    cdp.evaluate("window.confirm=()=>false;document.getElementById('liveStart').click()")
                    assert live.live_session.state()['live']['calls']==0
                    cdp.evaluate("window.confirm=()=>true")
                    cdp.screenshot(output/f'match-{number}-power-setting.png')
                cdp.evaluate("document.getElementById('liveStart').click()")
                if cue_check and number==1:
                    cdp.until("typeof movie!=='undefined'&&movie!==null",20)
                    stroke=cdp.evaluate("""(()=>{const t=movie.start,rows=[];
                      for(const dt of [0,140,220,259,260,300]){animate(t+dt);rows.push({dt,gap:movie.cuePose.gap,
                        physicsSeconds:movie.cuePose.physicsSeconds,cue:shown.find(b=>b.id===0),
                        png:[140,260,300].includes(dt)?canvas.toDataURL('image/png').split(',')[1]:null});}return rows;})()""")
                    for row in stroke:
                        png=row.pop('png')
                        if png:(output/f"cue-{row['dt']}ms.png").write_bytes(base64.b64decode(png))
                    assert all(r['cue']==stroke[0]['cue'] for r in stroke[:5]),stroke
                    assert stroke[1]['gap']>stroke[0]['gap'] and stroke[2]['gap']<stroke[1]['gap'],stroke
                    assert stroke[4]['gap']==11 and stroke[5]['cue']!=stroke[0]['cue'],stroke
                    (output/'cue-contact-proof.json').write_text(json.dumps(stroke,indent=2))
                    cdp.screenshot(output/'cue-after-contact.png')
                    cdp.evaluate("window.requestAnimationFrame=window.qaRealFrame;movie.start=performance.now()-300;requestAnimationFrame(animate)")
                elif cue_check:
                    cdp.evaluate("window.requestAnimationFrame=window.qaRealFrame;requestAnimationFrame(animate)")
                if scenario=='user_cancelled' and number==1:
                    cdp.until("liveInfo&&liveInfo.phase==='thinking'",10)
                    cdp.evaluate("document.getElementById('liveCancel').click()")
                cdp.until("liveInfo&&['complete','failed','cancelled'].includes(liveInfo.phase)",120)
                state=cdp.evaluate("({outcome:state.outcome,live:liveInfo,title:document.getElementById('resultTitle').textContent})")
                if scenario and number==1:
                    assert state['live']['phase'] in ('failed','cancelled'),state
                    assert state['live']['reason'] in (('request_timeout','parent_watchdog','http_timeout') if scenario=='request_timeout' else (scenario,)),state
                elif failure and number==1:
                    assert state['live']['phase']=='failed' and state['outcome']['reason']=='simulation_limit',state
                    assert state['outcome']['shots']==7 and 'incomplete' in state['title'].lower(),state
                else:
                    assert state['live']['phase']=='complete',state
                if not((failure or scenario) and number==1):assert state['outcome']['reason']=='shots_exhausted' and state['outcome']['shots']==12,state
                if not((failure or scenario) and number==1):assert state['outcome']['shots_remaining']==dict(p1=0,p2=0)
                assert state['live']['calls']==(1 if scenario and number==1 else 4 if failure and number==1 else 6)
                assert state['live']['server_budget']['calls']==((1 if number==1 else 7) if scenario else (4 if number==1 else 10) if failure else 6*number)
                if not((failure or scenario) and number==1):assert 'incomplete' not in state['title'].lower()
                cdp.screenshot(output/f'match-{number}-result.png');results.append(state)
                if cue_check and number==1:
                    live.live_session.worker.join()
                    # QA-only delayed audit settlement after a completed match.
                    late=threading.Thread(target=lambda:time.sleep(1.6),daemon=True)
                    live.live_session.worker=late;late.start()
                assert cdp.evaluate("Array.from(document.querySelectorAll('button')).filter(b=>b.textContent==='Back to Main Menu'&&b.getClientRects().length).length")==1
                if failure and number==1:
                    # A hung leave response must not trap the browser.
                    cdp.evaluate("window.qaFetch=fetch;window.fetch=(url,...args)=>url==='/live/leave'?new Promise(()=>{}):qaFetch(url,...args)")
                cdp.evaluate("document.querySelector('.back-menu-button').click()")
                cdp.until(f"location.port==='{game.server_port}'&&document.querySelector('a[href=\"/live\"]')!==null",25)
                if scenario and number==1:live.live_session.transport=offline_response
            if not failure and not scenario:
                cdp.evaluate("document.querySelector('a[href=\"/live\"]').click()")
                cdp.until("typeof liveInfo!=='undefined'&&liveInfo?.phase==='waiting'&&!liveInfo.can_start",20)
                assert cdp.evaluate("liveInfo.server_budget.calls")==12
                if cue_check:
                    assert 'Server-wide' in cdp.evaluate("document.querySelector('#intro p').textContent")
                if power_switch:
                    cdp.evaluate("document.getElementById('geometryPower').value='2';document.getElementById('geometryPower').dispatchEvent(new Event('change'))")
                    cdp.until("liveInfo.power_multiplier===2&&!geometryPowerBusy",10)
                    assert cdp.evaluate("liveInfo.server_budget.calls===12&&!liveInfo.can_start&&document.getElementById('liveStart').disabled")
                cdp.evaluate("document.querySelector('.back-menu-button').click()")
                cdp.until(f"location.port==='{game.server_port}'",20)
            traces=[]
            for path in sorted((output/'matches').glob('*/trace.json')):
                trace=json.loads(path.read_text());replay(trace)
                assert trace['kind']=='MOCKED_LIVE_DEMO_NOT_REAL_LLM'
                assert len([s for s in trace['steps'] if s['player']=='p1']) in ((0,6) if scenario else (4,6) if failure else (6,))
                assert len([s for s in trace['steps'] if s['player']=='p2']) in ((0,6) if scenario else (3,6) if failure else (6,))
                traces.append(path.relative_to(output).as_posix())
                if power_switch:
                    for step in trace['steps']:
                        if step['player']!='p1':continue
                        meta=step['model_metadata'];candidate=meta['selected_candidate']
                        assert meta['power_multiplier']==trace['power_multiplier']==trace['consent']['power_multiplier']
                        if trace.get('power_mode')=='adaptive':

                            if candidate.get('adaptive_profile')=='adaptive-distance-v2':
                                from .geometry_adaptive_power import distance_power
                                expected=distance_power(candidate['travel']) if candidate['route'] in ('contact','pot','bank-contact') else min(100,candidate['original_power']*2)
                            else:expected=min(100,max(candidate['original_power']*2,candidate['adaptive_floor']))
                            assert meta['power_mode']==trace['consent']['power_mode']=='adaptive'
                        else:expected=min(100,candidate['original_power']*trace['power_multiplier'])
                        assert step['action']==dict(angle=candidate['angle'],power=expected)
            assert len(traces)==2 and not cdp.errors,cdp.errors
            result=dict(kind='ACTUAL_HEADLESS_CHROME_SYNTHETIC_MODEL_NOT_PAID_EVALUATION',
                ui_power_switch=power_switch,power_settings=[r['live']['power_multiplier'] for r in results],
                power_modes=[r['live']['power_mode'] for r in results],
                cue_contact_browser_verified=cue_check,delayed_settlement_restart_verified=cue_check,
                balanced_table_render_verified=balanced_table,
                original_v15_viewer_verified=historical_view,
                synthetic_error=scenario,two_consecutive_matches=not(failure or scenario),simulation_limit_then_fresh_complete_match=failure,exactly_one_visible_back=True,hung_leave_did_not_trap_browser=failure,shots_each=[0,12] if scenario else [7,12] if failure else 12,opportunities_each_player=6,
                same_running_server=True,back_to_menu_twice=True,real_api_calls=0,
                qa_only='Rendering clock accelerated; confirmation accepted by QA stub in MOCK mode only.',
                results=results,traces=traces,browser_runtime_errors=cdp.errors)
            (output/'summary.json').write_text(json.dumps(result,indent=2))
            print(json.dumps({k:v for k,v in result.items() if k not in ('results',)},indent=2),flush=True)
            if process.poll() is None:
                if os.name=='nt':subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                else:process.terminate()
                process.wait(timeout=10)
    except Exception as error:
        detail=dict(error_type=type(error).__name__,message=str(error))
        if cdp:
            try:detail.update(page=cdp.evaluate('({url:location.href,title:document.title,text:document.body?.innerText})'),runtime_errors=cdp.errors)
            except Exception:pass
        (output/'failure.json').write_text(json.dumps(detail,indent=2))
        raise
    finally:
        if cdp:cdp.socket.close()
        if process and process.poll() is None:
            if os.name=='nt':subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            else:process.terminate()
            process.wait(timeout=10)
        live.live_session.leave()
        for server in servers:server.shutdown();server.server_close()
        for thread in threads:thread.join()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chrome',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--failure-reproduction',action='store_true')
    parser.add_argument('--scenario',choices=['http_error','invalid_candidate_selection','request_timeout','user_cancelled'])
    parser.add_argument('--power-switch',action='store_true')
    parser.add_argument('--adaptive-switch',action='store_true')
    parser.add_argument('--cue-check',action='store_true')
    parser.add_argument('--balanced-table',action='store_true')
    parser.add_argument('--historical-view',action='store_true')
    args=parser.parse_args();run(args.chrome,args.output,args.failure_reproduction,args.scenario,args.power_switch,args.adaptive_switch,args.cue_check,args.balanced_table,args.historical_view)


if __name__=='__main__':main()
