import pathlib,json,hashlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1];O=R/'analysis/verisbom-bundle-probe-v0';O.mkdir(exist_ok=False);E=R/'data/proof-sandbox/verisbom-bundle-v0';E.mkdir(exist_ok=False)
source=R/'data/proof-sandbox/verisbom-run-v0/nova/src/main.rs';text=source.read_text();assert text.count('fn main()')==1
(E/'audit_bundle.rs').write_text(text.replace('fn main()','fn archived_main()')+(R/'src/verisbom_bundle_probe.rs').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
image=subprocess.check_output(['docker','image','inspect','zkp-trustbom-audit:local','--format','{{.Id}}'],text=True).strip()
files=[source,R/'src/verisbom_bundle_probe.rs',pathlib.Path(__file__),E/'audit_bundle.rs',R/'data/proof-sandbox/verisbom-results-v3/honest.proof.proof',R/'protocol/verisbom-output-binding-v0.md']
(O/'freeze.json').write_text(json.dumps(dict(image=image,sha256={str(p.relative_to(R)):sha(p) for p in files}),indent=2))
shell='set -eu; cd /work; mkdir -p src/bin; cp /probe.rs src/bin/audit_bundle.rs; CARGO_BUILD_JOBS=4 cargo build --locked --release --bin audit_bundle; sha256sum target/release/audit_bundle; target/release/audit_bundle'
cmd=['docker','run','--rm','--name','zkp-verisbom-bundle-v0','--cpus','4','--memory','12g','--mount','type=volume,source=zkp-verisbom-build-v0,target=/work','--mount','type=volume,source=zkp-verisbom-work-v0,target=/runtime,readonly','--mount',f'type=bind,source={E/"audit_bundle.rs"},target=/probe.rs,readonly','--mount',f'type=bind,source={E},target=/out','--mount',f'type=bind,source={R/"data/proof-sandbox/verisbom-results-v3"},target=/evidence,readonly',image,'bash','-c',shell]
t=time.monotonic()
try:
 with (O/'execution.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=900)
 code=p.returncode
except subprocess.TimeoutExpired:
 subprocess.run(['docker','stop','zkp-verisbom-bundle-v0'],capture_output=True);code=-1
(O/'receipt.json').write_text(json.dumps(dict(exit_code=code,seconds=time.monotonic()-t,command=cmd,generated_sha256={str(p.relative_to(R)):sha(p) for p in E.iterdir() if p.is_file()}),indent=2));(O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2));print(code)
