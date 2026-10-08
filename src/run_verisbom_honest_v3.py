import pathlib,json,hashlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1];D=R/'data/proof-sandbox/verisbom-run-v0';O=R/'analysis/verisbom-honest-v3';O.mkdir(exist_ok=False)
E=R/'data/proof-sandbox/verisbom-results-v3';E.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
image=subprocess.check_output(['docker','image','inspect','zkp-verisbom-audit:ubuntu','--format','{{.Id}}'],text=True).strip()
files=[pathlib.Path(__file__),R/'src/resume_verisbom_honest.py',R/'protocol/verisbom-honest-v0.md',R/'data/verisbom-runtime-inputs.json']
(O/'freeze.json').write_text(json.dumps(dict(image=image,sha256={str(p.relative_to(R)):sha(p) for p in files}),indent=2))
shell='set -eu; cd /work; python3 /probe.py; cp honest.proof.proof expected.json witness.json selected-sbom.json /evidence/'
cmd=['docker','run','--rm','--name','zkp-verisbom-honest-v3','--network','none','--cpus','4','--memory','12g','--mount',f'type=bind,source={D},target=/source,readonly','--mount',f'type=bind,source={R/"src/resume_verisbom_honest.py"},target=/probe.py,readonly','--mount',f'type=bind,source={O},target=/out','--mount',f'type=bind,source={E},target=/evidence','--mount','type=volume,source=zkp-verisbom-build-v0,target=/compiled,readonly','--mount','type=volume,source=zkp-verisbom-work-v0,target=/work',image,'bash','-c',shell]
t=time.monotonic()
try:
 with (O/'execution.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=900)
 code=p.returncode
except subprocess.TimeoutExpired:
 subprocess.run(['docker','stop','zkp-verisbom-honest-v3'],capture_output=True);code=-1
(O/'receipt.json').write_text(json.dumps(dict(exit_code=code,seconds=time.monotonic()-t,command=cmd,generated_sha256={str(p.relative_to(R)):sha(p) for p in E.iterdir() if p.is_file()}),indent=2))
(O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2));print(code)
