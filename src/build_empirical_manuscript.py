import pathlib,subprocess,json,hashlib,sys
R=pathlib.Path(__file__).resolve().parents[1];P=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else R/'paper';O=P/'build';O.mkdir(exist_ok=True)
C=pathlib.Path(r'C:\Users\WT8\Documents\ChatGPT\Research\authorization-paper-build')
image=subprocess.check_output(['docker','image','inspect','zkp-verisbom-audit:ubuntu','--format','{{.Id}}'],text=True).strip()
cmd=['docker','run','--rm','--network','none','--cpus','2','--memory','2g','--env','XDG_CACHE_HOME=/compiler/cache','--mount',f'type=bind,source={C},target=/compiler,readonly','--mount',f'type=bind,source={P},target=/input,readonly','--mount',f'type=bind,source={O},target=/output',image,'/compiler/tectonic','--keep-logs','--outdir','/output','/input/main.tex']
r=subprocess.run(cmd,capture_output=True,text=True,timeout=180);(O/'stdout.txt').write_text(r.stdout);(O/'stderr.txt').write_text(r.stderr)
(O/'receipt.json').write_text(json.dumps(dict(command=cmd,exit_code=r.returncode,compiler_sha256=hashlib.sha256((C/'tectonic').read_bytes()).hexdigest(),source_sha256=hashlib.sha256((P/'main.tex').read_bytes()).hexdigest()),indent=2));print(r.stdout,r.stderr);sys.exit(r.returncode)
