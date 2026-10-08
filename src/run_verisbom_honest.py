import pathlib,json,hashlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1];D=R/'data/proof-sandbox/verisbom-run-v0';O=R/'analysis/verisbom-honest-v0';O.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
image=subprocess.check_output(['docker','image','inspect','zkp-trustbom-audit:local','--format','{{.Id}}'],text=True).strip()
files=[pathlib.Path(__file__),R/'src/verisbom_honest.py',R/'protocol/verisbom-honest-v0.md',R/'data/verisbom-runtime-inputs.json']
(O/'freeze.json').write_text(json.dumps(dict(image=image,sha256={str(p.relative_to(R)):sha(p) for p in files}),indent=2))
shell='set -eu; cp -a /source/. /work/; cp /probe.py /work/audit_probe.py; cd /work; chmod +x bomz circuits/poseidon_cpp/poseidon circuits/poseidon_multi_input_cpp/poseidon_multi_input circuits/poseidon3_cpp/poseidon3 circuits/step_cpp/step; python3 audit_probe.py; cp honest.proof expected.json witness.json selected-sbom.json /out/'
cmd=['docker','run','--rm','--name','zkp-verisbom-honest-v0','--network','none','--cpus','4','--memory','12g','--mount',f'type=bind,source={D},target=/source,readonly','--mount',f'type=bind,source={R/"src/verisbom_honest.py"},target=/probe.py,readonly','--mount',f'type=bind,source={O},target=/out','--mount','type=volume,source=zkp-verisbom-work-v0,target=/work',image,'bash','-c',shell]
t=time.monotonic()
try:
 with (O/'execution.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=900)
 code=p.returncode
except subprocess.TimeoutExpired:
 subprocess.run(['docker','stop','zkp-verisbom-honest-v0'],capture_output=True);code=-1
(O/'receipt.json').write_text(json.dumps(dict(exit_code=code,seconds=time.monotonic()-t,command=cmd),indent=2))
(O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2));print(code)
