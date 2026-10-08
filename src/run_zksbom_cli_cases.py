import pathlib,subprocess,json,hashlib,time
R=pathlib.Path(__file__).resolve().parents[1];O=R/'analysis/zksbom-cli-cases-v0';O.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
E=R/'data/proof-sandbox/zksbom-label-wrapper-v1';L=R/'data/proof-sandbox/zksbom-label-fixture-v0/labels.json';image=subprocess.check_output(['docker','image','inspect','zkp-zksbom-cli:v0','--format','{{.Id}}'],text=True).strip()
files=[pathlib.Path(__file__),R/'src/zksbom_cli_cases.py',R/'protocol/zksbom-cli-v0.md',L]+list(E.iterdir())
(O/'freeze.json').write_text(json.dumps(dict(image=image,inputs={str(p.relative_to(R)):sha(p) for p in files}),indent=2))
cmd=['docker','run','--rm','--network','none','--cpus','4','--memory','8g','--mount','type=volume,source=zkp-zksbom-cli-v0,target=/work,readonly','--mount',f'type=bind,source={E},target=/evidence,readonly','--mount',f'type=bind,source={L},target=/labels.json,readonly','--mount',f'type=bind,source={R/"src/zksbom_cli_cases.py"},target=/cases.py,readonly','--mount',f'type=bind,source={O},target=/out',image,'bash','-c','set -eu; sha256sum /work/target/release/zksbom-verifier; python3 /cases.py']
t=time.monotonic()
with (O/'execution.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=600)
(O/'receipt.json').write_text(json.dumps(dict(command=cmd,exit_code=p.returncode,seconds=time.monotonic()-t),indent=2));print(p.returncode)
