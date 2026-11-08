"""Check final gameplay/visual artifacts without freezing pending LLM/report work."""
import hashlib
import json
from pathlib import Path


def main():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'fusion/gameplay-freeze.json').read_text())
    changed=[name for name,digest in manifest['sha256'].items()
             if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest]
    if changed: raise SystemExit('Gameplay freeze changed: '+', '.join(changed))
    print('PASS: final gameplay and visual freeze ('+str(len(manifest['sha256']))+' artifacts)')


if __name__=='__main__':main()
