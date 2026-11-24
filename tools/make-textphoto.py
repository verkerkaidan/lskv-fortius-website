#!/usr/bin/env python3
"""Generic 'text + photo' section patterns (photo right / photo left), placeholder content, colour = Style 3 (change in editor).
Writes src/patterns, dist/patterns and installs local wp_block posts."""
import re, os, json, subprocess, base64
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE=os.path.expanduser('~/Studio/fortius-local-copy'); STUDIO='/Applications/Studio.app/Contents/Resources/bin/studio-cli.sh'
def wp(*a): return subprocess.run([STUDIO,'wp',*a],cwd=SITE,capture_output=True,text=True,check=True).stdout
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800"><rect width="1200" height="800" fill="#c9c9ce"/><path d="M0 0L1200 800M1200 0L0 800" stroke="#8a8a86" stroke-width="4"/><rect x="330" y="360" width="540" height="80" fill="#c9c9ce"/><text x="600" y="415" font-family="Arial,sans-serif" font-size="48" text-anchor="middle" fill="#3a3a38">[Placeholder Image]</text></svg>'''
URI='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
t=open(os.path.join(ROOT,'src','content','489-pattern-bestuur.html')).read()
t=t.replace('"patternName":"core/block/489",','')
t=re.sub(r'("metadata":\{"name":")[^"]*"',r'\1Tekst + foto"',t,1)
t=re.sub(r'<p class="is-style-text-annotation">.*?</p>','<p class="is-style-text-annotation">[Placeholder Label]</p>',t,1,flags=re.S)
t=re.sub(r'<h2 class="wp-block-heading">.*?</h2>','<h2 class="wp-block-heading">[Placeholder Slogan]</h2>',t,1,flags=re.S)
ps=re.findall(r'<!-- wp:paragraph -->\n<p>.*?</p>\n<!-- /wp:paragraph -->',t,flags=re.S)
t=t.replace(ps[0],'<!-- wp:paragraph -->\n<p>[Placeholder Text]</p>\n<!-- /wp:paragraph -->',1)
for p in ps[1:]: t=t.replace('\n\n'+p,'',1)
t=t.replace('"blockGap":"8px"','"blockGap":"16px"')
t=t.replace('<!-- wp:columns {"style"','<!-- wp:columns {"verticalAlignment":"center","style"',1).replace('<div class="wp-block-columns" style','<div class="wp-block-columns are-vertically-aligned-center" style',1)
t=re.sub(r'"id":\d+,"sizeSlug":"full"','"sizeSlug":"large"',t,1).replace('size-full','size-large')
t=re.sub(r'src="[^"]*" alt="" class="wp-image-\d+"','src="%s" alt=""'%URI,t,1)
t=t.replace('<!-- wp:column {"style"','<!-- wp:column {"verticalAlignment":"center","style"').replace('<div class="wp-block-column"','<div class="wp-block-column is-vertically-aligned-center"')
t=t.replace('"blockGap":{"top":"0","left":"40px"}','"blockGap":{"top":"2rem","left":"40px"}')
right=t
a=t.index('<!-- wp:column ');m=t.index('<!-- /wp:column -->',a)+len('<!-- /wp:column -->');b=t.index('<!-- wp:column ',m);e=t.index('<!-- /wp:column -->',b)+len('<!-- /wp:column -->')
left=t[:a]+t[b:e]+t[m:b]+t[a:m]+t[e:]
left=left.replace('<!-- wp:columns {"verticalAlignment":"center",','<!-- wp:columns {"verticalAlignment":"center","className":"fortius-photo-left",',1).replace('class="wp-block-columns are-vertically-aligned-center"','class="wp-block-columns are-vertically-aligned-center fortius-photo-left"',1)
os.makedirs(os.path.join(ROOT,'src','patterns'),exist_ok=True);os.makedirs(os.path.join(ROOT,'dist','patterns'),exist_ok=True)
existing={}
for l in wp('post','list','--post_type=wp_block','--fields=ID,post_title','--format=csv').splitlines()[1:]:
    i,_,ti=l.partition(','); existing[ti.strip('"')]=i
for slug,title,c in (('tekst-foto-rechts','Tekst + foto rechts',right),('tekst-foto-links','Tekst + foto links',left)):
    c=re.sub(r'("metadata":\{"name":")[^"]*"',lambda x:x.group(1)+title+'"',c,1)
    f=os.path.join(ROOT,'src','patterns',slug+'.html');open(f,'w').write(c)
    json.dump({'__file':'wp_block','title':title,'content':c,'syncStatus':'unsynced'},open(os.path.join(ROOT,'dist','patterns',slug+'.json'),'w'),ensure_ascii=False,indent=1)
    if title in existing: wp('post','update',existing[title],f); pid=existing[title]
    else: pid=wp('post','create',f,'--post_type=wp_block','--post_status=publish','--post_title='+title,'--porcelain').strip()
    wp('post','meta','update',pid,'wp_pattern_sync_status','unsynced'); print(title,pid)
