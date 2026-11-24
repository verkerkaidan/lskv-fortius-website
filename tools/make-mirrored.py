#!/usr/bin/env python3
"""Create a mirrored (image-left) variant of a two-column pattern. Usage: make-mirrored.py <src content file> <slug> <title>"""
import sys, os, re, json, subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE=os.path.expanduser('~/Studio/fortius-local-copy'); STUDIO='/Applications/Studio.app/Contents/Resources/bin/studio-cli.sh'
src,slug,title=sys.argv[1:4]
s=open(os.path.join(ROOT,src)).read()
a=s.index('<!-- wp:column ')
m=s.index('<!-- /wp:column -->',a)+len('<!-- /wp:column -->')
b=s.index('<!-- wp:column ',m)
e=s.index('<!-- /wp:column -->',b)+len('<!-- /wp:column -->')
c1,gap,c2=s[a:m],s[m:b],s[b:e]
out=s[:a]+c2+gap+c1+s[e:]
out=out.replace('"patternName":"core/block/489",','')
out=re.sub(r'("metadata":\{"name":")[^"]*"',lambda x:x.group(1)+title.replace('&','\\u0026')+'"',out,1)
os.makedirs(os.path.join(ROOT,'src','patterns'),exist_ok=True); os.makedirs(os.path.join(ROOT,'dist','patterns'),exist_ok=True)
open(os.path.join(ROOT,'src','patterns',slug+'.html'),'w').write(out)
json.dump({'__file':'wp_block','title':title,'content':out,'syncStatus':'unsynced'},open(os.path.join(ROOT,'dist','patterns',slug+'.json'),'w'),ensure_ascii=False,indent=1)
def wp(*a): return subprocess.run([STUDIO,'wp',*a],cwd=SITE,capture_output=True,text=True,check=True).stdout
f=os.path.join(ROOT,'src','patterns',slug+'.html')
pid=wp('post','create',f,'--post_type=wp_block','--post_status=publish','--post_title='+title,'--porcelain').strip()
wp('post','meta','update',pid,'wp_pattern_sync_status','unsynced')
print(pid)
