#!/usr/bin/env python3
"""Collect everything that has to be pasted into WordPress.com into dist/."""
import json, os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = lambda *p: os.path.join(ROOT, *p)
def merge(b, x):
    for k, v in x.items():
        if isinstance(v, dict) and isinstance(b.get(k), dict) and k != 'palette': merge(b[k], v)
        else: b[k] = v
    return b
g = merge(json.load(open(d('baseline','global-styles.original.json'))), json.load(open(d('src','global-styles.json'))))
css = open(d('src','additional.css')).read()
# WordPress.com refuses to store block-style-variation overrides (Style 1-5) in Global Styles,
# so the live CSS carries the same rules as plain CSS.
SECS = {1:('base','accent-4','accent-4','accent-3','accent-4','accent-2','accent-4'),
        2:('accent-3','accent-4','accent-4','accent-4','accent-3','base','accent-4'),
        3:('accent-4','accent-5','base','accent-3','accent-4','accent-2','accent-4'),
        4:('accent-5','accent-4','accent-4','accent-3','accent-4','accent-2','accent-4'),
        5:('contrast','accent-5','base','accent-3','accent-4','accent-2','accent-4')}
v = lambda n: 'var(--wp--preset--color--%s)' % n
fb = '\n/* ---------- Section Styles 1-5 (mirrors Global Styles variations; WordPress.com does not store those) ---------- */\n'
for n,(bg,tx,hd,bb,bt,hb,ht) in SECS.items():
    sel = ':is(.wp-block-group, .wp-block-columns, .wp-block-column).is-style-section-%d' % n
    fb += '%s {\n  background-color: %s;\n  color: %s;\n}\n' % (sel, v(bg), v(tx))
    fb += '%s :is(h1, h2, h3, h4, h5, h6, .wp-block-heading) {\n  color: %s;\n}\n' % (sel, v(hd))
    fb += '%s .wp-block-button:not(.is-style-outline) .wp-block-button__link {\n  background-color: %s;\n  border-color: %s;\n  color: %s;\n}\n' % (sel, v(bb), v(bb), v(bt))
    fb += '%s .wp-block-button:not(.is-style-outline) .wp-block-button__link:hover {\n  background-color: %s;\n  border-color: %s;\n  color: %s;\n}\n' % (sel, v(hb), v(hb), v(ht))
css_live = css + fb
g['styles']['css'] = css_live
os.makedirs(d('dist','content'), exist_ok=True)
json.dump(g, open(d('dist','global-styles.json'),'w'), ensure_ascii=False, indent=1)
open(d('dist','additional.css'),'w').write(css_live)
LIVE='https://lskvfortius.nl'
def fix(p):
    t=open(p).read()
    if 'localhost:8881' in t: open(p,'w').write(t.replace('http://localhost:8881',LIVE))
for root, _dirs, files in os.walk(d('src','content')):
    rel = os.path.relpath(root, d('src','content'))
    os.makedirs(d('dist','content',rel), exist_ok=True)
    for f in files:
        shutil.copy(os.path.join(root, f), d('dist','content',rel,f)); fix(d('dist','content',rel,f))
if os.path.isdir(d('dist','patterns')):
    for f in os.listdir(d('dist','patterns')): fix(d('dist','patterns',f))
print('dist ready')
