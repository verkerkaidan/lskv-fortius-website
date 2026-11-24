import re,glob,sys
T=re.compile(r'is-style-section-[135]\b|fortius-page-hero|fortius-partners\b|fortius-cards')
def strip_json(m):
    s=m.group(0)
    return re.sub(r'"(left|right)":"[^"]*",?','',s).replace(',}','}')
n=0
for f in glob.glob('src/content/*.html'):
    if '-tpl-' in f: continue
    t=open(f).read(); o=t
    out=[]
    for line in t.split('\n'):
        if T.search(line):
            if line.startswith('<!-- wp:group') or line.startswith('<!-- wp:cover'):
                line=re.sub(r'"padding":\{[^{}]*\}',strip_json,line)
            line=re.sub(r'padding-(left|right):[^;"]*;?','',line)
            line=line.replace('style=""','')
        out.append(line)
    t='\n'.join(out)
    if t!=o: open(f,'w').write(t); n+=1; print(f)
