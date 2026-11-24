#!/usr/bin/env python3
"""Merge src/global-styles.json + src/additional.css into the local Studio site's user Global Styles."""
import json, subprocess, sys, tempfile, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.expanduser('~/Studio/fortius-local-copy')
STUDIO = '/Applications/Studio.app/Contents/Resources/bin/studio-cli.sh'
POST = '35'

def wp(*a):
    return subprocess.run([STUDIO, 'wp', *a], cwd=SITE, capture_output=True, text=True, check=True).stdout

def deep_replace(base, delta):
    for k, v in delta.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict) and k not in ('palette',):
            deep_replace(base[k], v)
        else:
            base[k] = v
    return base

orig = json.load(open(os.path.join(ROOT, 'baseline', 'global-styles.original.json')))
delta = json.load(open(os.path.join(ROOT, 'src', 'global-styles.json')))
out = deep_replace(json.loads(json.dumps(orig)), delta)
out.setdefault('styles', {})['css'] = open(os.path.join(ROOT, 'src', 'additional.css')).read()
with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
    json.dump(out, f); path = f.name
wp('post', 'update', POST, path)
os.unlink(path)
wp('cache', 'flush')
print('applied; css bytes:', len(out['styles']['css']))
