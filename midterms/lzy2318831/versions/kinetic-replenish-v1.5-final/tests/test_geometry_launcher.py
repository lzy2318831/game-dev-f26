"""Windows launcher regression; real interpreter probes, no server/API calls."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(shutil.which('powershell'), 'Windows PowerShell launcher test')
class LauncherResolution(unittest.TestCase):
    def run_resolution(self,override,discovered):
        launcher=Path('run-geometry-live.ps1').resolve()
        script=r'''
$ErrorActionPreference='Stop'
$tokens=$null; $errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile($env:LAUNCHER_UNDER_TEST,[ref]$tokens,[ref]$errors)
$definition=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Resolve-GeometryPython'},$true)
if ($null -eq $definition) { throw 'Interpreter resolver missing' }
Invoke-Expression $definition.Extent.Text
function Get-Command { param($Name,$CommandType,[switch]$All,$ErrorAction)
    if ($Name -eq 'python') {
        foreach ($source in ($env:DISCOVERED_PYTHONS | ConvertFrom-Json)) { [pscustomobject]@{Source=$source} }
    }
}
$result=Resolve-GeometryPython
if ($result -isnot [string]) { throw 'Expected exactly one executable string' }
Write-Output ('RESOLVED='+$result)
'''
        env=dict(os.environ,GEOMETRY_PYTHON=override,LAUNCHER_UNDER_TEST=str(launcher),
                 DISCOVERED_PYTHONS=json.dumps(discovered))
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'check.ps1';path.write_text(script,encoding='utf-8')
            return subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(path)],
                env=env,capture_output=True,text=True,timeout=30)

    def test_environment_override_precedes_alias_and_other_installation(self):
        result=self.run_resolution(sys.executable,[r'C:\Users\student\AppData\Local\Microsoft\WindowsApps\python.exe',r'C:\OtherPython\python.exe'])
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('RESOLVED='+sys.executable,result.stdout)

    def test_combined_windowsapps_and_install_path_is_not_invoked(self):
        alias=r'C:\Users\student\AppData\Local\Microsoft\WindowsApps\python.exe'
        result=self.run_resolution(alias+' '+sys.executable,[alias,sys.executable])
        self.assertEqual(result.returncode,0,result.stderr)
        resolved=[line for line in result.stdout.splitlines() if line.startswith('RESOLVED=')]
        self.assertEqual(resolved,['RESOLVED='+sys.executable])

    def test_multiple_application_results_resolve_individually(self):
        alias=r'C:\Users\student\AppData\Local\Microsoft\WindowsApps\python.exe'
        result=self.run_resolution('',[alias,sys.executable])
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('RESOLVED='+sys.executable,result.stdout)

    def test_no_valid_interpreter_stops(self):
        result=self.run_resolution(r'C:\missing\python.exe',[])
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Python 3.11+',result.stderr)

    def test_same_verified_interpreter_runs_freeze_and_mock_server(self):
        # Execute the actual launcher against temporary, inert module fixtures.
        # No sockets, model calls, key prompt, or changes to the real game package.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);launcher=root/'run-geometry-live.ps1'
            launcher.write_bytes(Path('run-geometry-live.ps1').read_bytes())
            package=root/'fusion';package.mkdir();(package/'__init__.py').write_text('')
            recorder="import sys,json\nfrom pathlib import Path\nwith Path('invocations.jsonl').open('a') as out: out.write(json.dumps([sys.executable,sys.argv])+chr(10))\n"
            (package/'freeze.py').write_text(recorder);(package/'geometry_live.py').write_text(recorder)
            env=dict(os.environ,GEOMETRY_PYTHON=sys.executable)
            result=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(launcher),'-Mock'],
                env=env,capture_output=True,text=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stderr)
            records=[json.loads(s) for s in (root/'invocations.jsonl').read_text().splitlines()]
            self.assertEqual(len(records),2)
            self.assertTrue(all(Path(row[0])==Path(sys.executable) for row in records))
            self.assertTrue(records[0][1][0].endswith('freeze.py'))
            self.assertEqual(records[1][1][-1],'--mock')
            self.assertNotIn('--enable-paid',result.stdout)


if __name__=='__main__':unittest.main()
