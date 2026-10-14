import hashlib,json,pathlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1]; O=R/'analysis/client-path-v0';O.mkdir(exist_ok=False)
image=subprocess.check_output(['docker','image','inspect','zkp-verisbom-audit:ubuntu','--format','{{.Id}}'],text=True).strip()
files=[R/'protocol/verisbom-client-path-v0.txt',R/'src/verisbom_client_path_probe.py',pathlib.Path(__file__)]
(O/'freeze.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
cmd=['docker','run','--rm','--network','none','--cpus','4','--memory','12g',
 '--mount','type=volume,source=zkp-verisbom-work-v0,target=/work,readonly',
 '--mount','type=volume,source=zkp-verisbom-build-v0,target=/compiled,readonly']
for source,target,ro in [(R/'src/verisbom_client_path_probe.py','/probe.py',True),(R/'data/proof-sandbox/verisbom-results-v3','/evidence',True),(R/'data/proof-sandbox/verisbom-bundle-v0','/bundle',True),(O,'/out',False)]:
 cmd+=['--mount',f'type=bind,source={source},target={target}'+(',readonly' if ro else '')]
cmd += [image,'python3','/probe.py']; start=time.monotonic()
r=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
(O/'execution.log').write_text(r.stdout+'\n'+r.stderr)
(O/'receipt.json').write_text(json.dumps(dict(command=cmd,image=image,exit_code=r.returncode,seconds=time.monotonic()-start),indent=2))
(O/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.is_file()},indent=2))
print(r.stdout,r.stderr);raise SystemExit(r.returncode)
