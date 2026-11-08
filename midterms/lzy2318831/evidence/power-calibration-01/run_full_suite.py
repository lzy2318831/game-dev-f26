"""Run every discovered test module in isolated offline Python processes."""
from concurrent.futures import ThreadPoolExecutor
import json,re,subprocess,sys,unittest
from pathlib import Path

def main():
    out=Path(__file__).resolve().parent
    sys.path.insert(0,str(Path('.').resolve()))
    sys.path.insert(0,str(Path('tests').resolve()))
    expected=unittest.defaultTestLoader.discover('tests').countTestCases()
    files=sorted(p.name for p in Path('tests').glob('test_*.py'))
    def run(name):
        r=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-p',name,'-v'],capture_output=True,text=True)
        log=r.stdout+r.stderr
        (out/('parallel-'+name+'.txt')).write_text(log)
        matches=re.findall(r'Ran (\d+) tests? in',log)
        return dict(module=name,returncode=r.returncode,tests=int(matches[-1]) if matches else 0)
    with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,files))
    result=dict(kind='COMPLETE_DISCOVERED_SUITE_MODULE_ISOLATION',expected_tests=expected,executed_tests=sum(r['tests'] for r in results),modules=results)
    result['passed']=result['executed_tests']==expected and all(r['returncode']==0 for r in results)
    (out/'python-module-results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(expected_tests=expected,executed_tests=result['executed_tests'],passed=result['passed'],failed=[r for r in results if r['returncode']]),indent=2))
    raise SystemExit(0 if result['passed'] else 1)

if __name__=='__main__':main()
