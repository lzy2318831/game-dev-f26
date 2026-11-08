"""Read-only, hash-verified original v1.5 physics for historical evidence."""
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import sys
import threading

VERSION='fusion-1.5.0-replenish'
ROOT=Path(__file__).resolve().parents[1]/'versions/kinetic-replenish-v1.5-final'
NAME='_kinetic_fusion_v15'
_lock=threading.RLock()
_loaded=False


def verify():
    manifest=json.loads((ROOT/'snapshot-hashes.json').read_text())
    manifest.update(json.loads((ROOT/'evidence-hashes.json').read_text()))
    changed=[name for name,digest in manifest.items()
             if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest]
    if changed:raise ValueError('Original v1.5 archive changed: '+', '.join(changed))
    return len(manifest)


def module(name):
    global _loaded
    with _lock:
        if not _loaded:
            verify()
            spec=importlib.util.spec_from_file_location(NAME,ROOT/'fusion/__init__.py',
                submodule_search_locations=[str(ROOT/'fusion')])
            package=importlib.util.module_from_spec(spec);sys.modules[NAME]=package
            spec.loader.exec_module(package)
            if package.VERSION!=VERSION:raise ValueError('Original archive version mismatch')
            _loaded=True
        return importlib.import_module(NAME+'.'+name)
