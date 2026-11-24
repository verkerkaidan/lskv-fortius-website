#!/usr/bin/env python3
"""Cut reusable sections out of the migrated pages, add generic per-style section patterns,
write src/patterns/*.html, dist/patterns/*.json (WordPress pattern-import format) and install locally."""
import re, os, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.expanduser('~/Studio/fortius-local-copy')
STUDIO = '/Applications/Studio.app/Contents/Resources/bin/studio-cli.sh'
def wp(*a): return subprocess.run([STUDIO,'wp',*a],cwd=SITE,capture_output=True,text=True,check=True).stdout

def top_blocks(s):
    out=[];depth=0;start=None
    for m in re.finditer(r'<!-- (/)?wp:([a-z0-9/-]+)( \{.*?\})?( /)? -->',s):
        close,name,attrs,selfc=m.groups()
        if close:
            depth-=1
            if depth==0: out.append(s[start:m.end()])
            continue
        if depth==0: start=m.start()
        if selfc:
            if depth==0: out.append(s[start:m.end()])
        else: depth+=1
    return out

def page(slug): return top_blocks(open(os.path.join(ROOT,'src','content',slug+'.html')).read())

def section(style,label,body_h,cta=True):
    btn = '''<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="#">Knop</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->''' if cta else ''
    return f'''<!-- wp:group {{"align":"full","className":"is-style-section-{style}","layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group alignfull is-style-section-{style}"><!-- wp:group {{"className":"fortius-section-inner","layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group fortius-section-inner"><!-- wp:paragraph {{"className":"is-style-text-annotation"}} -->
<p class="is-style-text-annotation">Label</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">{body_h}</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Schrijf hier je tekst.</p>
<!-- /wp:paragraph -->

{btn}</div>
<!-- /wp:group --></div>
<!-- /wp:group -->'''

home,over,contact,lid,eng=[page(p) for p in ('25-home','728-over-ons','11-contact','404-lid-worden','624-english')]
P=[
 ('sectie-donker','Sectie – Stijl 1 Donker','Kop van de sectie',section(1,'',  'Kop van de sectie')),
 ('sectie-rood','Sectie – Stijl 2 Rood','Kop van de sectie',section(2,'','Kop van de sectie')),
 ('sectie-wit','Sectie – Stijl 3 Wit','Kop van de sectie',section(3,'','Kop van de sectie')),
 ('sectie-donkergrijs','Sectie – Stijl 4 Donkergrijs','Kop van de sectie',section(4,'','Kop van de sectie')),
 ('sectie-licht','Sectie – Stijl 5 Licht','Kop van de sectie',section(5,'','Kop van de sectie')),
 ('pagina-hero','Pagina-hero (donkere banner)',None,over[0]),
 ('home-hero','Home-hero met foto',None,home[0]),
 ('kaarten-drie','Drie kaarten',None,home[2]),
 ('quote-strook','Quote-strook (marquee)',None,home[3]),
 ('partners-logos','Samenwerkingen met logo\'s',None,home[4]),
 ('contactgegevens','Contactgegevens + kaart',None,contact[1]),
 ('contact-donker','Contact – donkere sectie',None,contact[2]),
 ('lid-uitleg','Lid worden – uitleg (wit)',None,lid[1]),
 ('lid-licht','Lid worden – licht',None,lid[2]),
]
os.makedirs(os.path.join(ROOT,'src','patterns'),exist_ok=True);os.makedirs(os.path.join(ROOT,'dist','patterns'),exist_ok=True)
try: cat=json.loads(wp('term','get','wp_pattern_category','2','--format=json'))['slug']
except Exception: cat='lskvfortius'
existing={l.split('\t')[1]:l.split('\t')[0] for l in wp('post','list','--post_type=wp_block','--fields=ID,post_title','--format=csv').splitlines()[1:] for l in [l.replace(',','\t',1)]}
for slug,title,_,content in P:
    open(os.path.join(ROOT,'src','patterns',slug+'.html'),'w').write(content+'\n')
    json.dump({'__file':'wp_block','title':title,'content':content,'syncStatus':'unsynced'},open(os.path.join(ROOT,'dist','patterns',slug+'.json'),'w'),ensure_ascii=False,indent=1)
    f=os.path.join(ROOT,'src','patterns',slug+'.html')
    if title in existing:
        pid=existing[title];wp('post','update',pid,f)
    else:
        pid=wp('post','create',f,'--post_type=wp_block','--post_status=publish','--post_title='+title,'--porcelain').strip()
    wp('post','meta','update',pid,'wp_pattern_sync_status','unsynced')
    wp('post','term','set',pid,'wp_pattern_category',cat) if False else None
    print(pid,title)
