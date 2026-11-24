import subprocess,glob,re,os,sys
sys.path.insert(0,'tools')
STUDIO='/Applications/Studio.app/Contents/Resources/bin/studio-cli.sh'
SITE=os.path.expanduser('~/Studio/fortius-local-copy')
for f in sorted(glob.glob('src/content/*.html')):
    pid=os.path.basename(f).split('-')[0]
    if len(sys.argv)>1 and pid not in sys.argv[1:]: continue
    subprocess.run([STUDIO,'wp','post','update',pid,os.path.abspath(f)],cwd=SITE,capture_output=True,check=True); print(pid)
