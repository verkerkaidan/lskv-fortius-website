#!/usr/bin/env python3
"""Replace hardcoded hex colours / orphan slugs in stored blocks with palette presets.
Reads each post from the local Studio site, writes the result to src/content/<id>-<slug>.html and updates the post."""
import subprocess, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.expanduser('~/Studio/fortius-local-copy')
STUDIO = '/Applications/Studio.app/Contents/Resources/bin/studio-cli.sh'
POSTS = {25:'home', 728:'over-ons', 11:'contact', 404:'lid-worden', 624:'english', 487:'pattern-kernwaarden', 454:'pattern-foto-tekst-wit',
         450:'pattern-trainingstijden', 470:'pattern-prijzen', 471:'pattern-faq', 473:'pattern-aanmeldformulier', 489:'pattern-bestuur', 501:'pattern-hero', 505:'pattern-hero-no-buttons',
         59:'part-header', 60:'part-footer', 152:'tpl-single', 149:'tpl-search', 143:'tpl-404', 92:'tpl-page', 90:'tpl-index', 88:'tpl-home', 85:'tpl-archive'}
RENAMES = {'section-inner': 'fortius-section-inner', 'quote-card-headline': 'fortius-quote-headline', 'quote-card-body': 'fortius-quote-body', 'quote-card': 'fortius-quote', 'quote-strip-wrap': 'fortius-quote-strip', 'quote-grid': 'fortius-quote-grid', 'quote-marquee': 'fortius-quote-marquee', 'who-we-are-image-placeholder': 'fortius-about-image', 'hero-image-placeholder': 'fortius-hero-media', 'samenwerkingen-logos': 'fortius-partners-logos', 'samenwerkingen-logo-item': 'fortius-partners-logo', 'fortius-section-samenwerkingen': 'fortius-partners', 'cta-schedule-item': 'fortius-schedule-item', 'cta-schedule-day': 'fortius-schedule-day', 'cta-schedule-time': 'fortius-schedule-time', 'cta-schedule': 'fortius-schedule', 'section-cta': 'is-style-section-2 fortius-cta', 'cover-logo-angled-left': 'fortius-cover-angled', 'is-style-outline-black': 'is-style-outline', 'is-style-outline-dark': 'is-style-outline'}
CLASS_MAP = {**RENAMES, 'fortius-section-dark':'is-style-section-1','fortius-section-white':'is-style-section-3','fortius-section-offwhite':'is-style-section-5',
             'fortius-section-overons':None,'kicker':'is-style-text-annotation',
             'ai-ignore':None,'md:order-0':None,'order-1':None,'is-clone':None}
SURFACES={'fortius-post-card','fortius-post-body','fortius-comments','fortius-page-header','fortius-page-content','fortius-404','fortius-more-posts','fortius-pagination-wrap'}
CUR=['']
def fix_classes(c):
    def tok(m):
        out=[]
        for t in m.group(2).split():
            if t.startswith('ai-show-if-'): continue
            n=CLASS_MAP.get(t,t)
            if n is None: continue
            out.extend(n.split())
        if 'is-style-section-5' in out:
            if 'fortius-archive-header' in out or SURFACES & set(out): out=[t for t in out if t!='is-style-section-5']
        if CUR[0].startswith('tpl-') and 'is-style-section-5' in out and (out==['is-style-section-5'] or 'wp-block-group' in out) and 'fortius-archive-body' not in out: out=out+['fortius-archive-body']
        if CUR[0] and not CUR[0].startswith('tpl-'): out=[t for t in out if t!='fortius-archive-body']
        if 'is-style-outline' in out: out=[t for t in out if t!='is-style-fill']
        seen=[];[seen.append(t) for t in out if t not in seen]
        return m.group(1)+' '.join(seen)+'"'
    return re.sub(r'("className":"|class=")([^"]*)"',tok,c)
HEX = {'121212':'base','1b1b1b':'base','0d0d0f':'base','1a1a1a':'base',
       'f0f0f0':'contrast','eceae6':'contrast','eeeeee':'contrast',
       'ffffff':'accent-4','8a8a86':'accent-1','a8a8a8':'accent-1','9c9c9c':'accent-1',
       '3a3a38':'accent-5','26262b':'accent-5','353535':'accent-5',
       'c81e2c':'accent-3','c8102e':'accent-3','e00000':'accent-3',
       '8f1520':'accent-2','8f0000':'accent-2','800000':'accent-2',
       'c9c9ce':'accent-6','d9d9d9':'accent-6'}
SLUG_FIX = {'white':'accent-4','accent-6-orig':'accent-4'}
def wp(*a, **k):
    return subprocess.run([STUDIO,'wp',*a], cwd=SITE, capture_output=True, text=True, check=True, **k).stdout
def migrate(c, post_id):
    def jsonhex(m): return '"var:preset|color|%s"' % HEX[m.group(1).lower()]
    c = re.sub(r'"#([0-9a-fA-F]{6})"', lambda m: jsonhex(m) if m.group(1).lower() in HEX else m.group(0), c)
    def csshex(m): return 'var(--wp--preset--color--%s)' % HEX[m.group(1).lower()]
    c = re.sub(r'#([0-9a-fA-F]{6})\b', lambda m: csshex(m) if m.group(1).lower() in HEX else m.group(0), c)
    for a,b in SLUG_FIX.items():
        c = c.replace('"backgroundColor":"%s"'%a,'"backgroundColor":"%s"'%b).replace('has-%s-background-color'%a,'has-%s-background-color'%b)
        c = c.replace('"textColor":"%s"'%a,'"textColor":"%s"'%b).replace('has-%s-color'%a,'has-%s-color'%b)
    c = c.replace('"duotone":["var:preset|color|base","var:preset|color|contrast"]','"duotone":["#1B1B1B","#F0F0F0"]')  # duotone needs literal hex
    return fix_classes(c)
if __name__ == '__main__':
    for pid, slug in POSTS.items():
        old = wp('post','get',str(pid),'--field=post_content')
        CUR[0]=slug
        new = migrate(old, pid)
        out = os.path.join(ROOT,'src','content',f'{pid}-{slug}.html')
        open(out,'w').write(new)
        if new != old:
            wp('post','update',str(pid),out)
        print(pid, slug, 'changed' if new!=old else 'unchanged')
