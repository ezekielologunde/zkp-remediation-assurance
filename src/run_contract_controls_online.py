import hashlib,json,pathlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1]
O=R/'analysis/contract-controls-v2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
O.mkdir(exist_ok=False)
paths=['src/trustbom_contract_probe.rs','src/run_contract_controls_online.py','protocol/contract-controls-v0.md','data/proof-sandbox/trustbom-linux-results-v3/audit-receipt.json','data/proof-sandbox/trustbom-source/proving-service/benchmark/data/merkleproofs/batch_proof_2.json']
image=subprocess.check_output(['docker','image','inspect','zkp-trustbom-audit:local','--format','{{.Id}}'],text=True).strip()
(O/'freeze.json').write_text(json.dumps(dict(image=image,sha256={p:sha(R/p) for p in paths}),indent=2))
cmd=['docker','run','--rm','--name','zkp-contract-controls-v2','--cpus','4','--memory','6g','--env','RISC0_DEV_MODE=0','--mount','type=volume,source=zkp-trustbom-work-v1,target=/work','--mount','type=volume,source=zkp-trustbom-registry-v1,target=/usr/local/cargo/registry','--mount',f'type=bind,source={R/paths[0]},target=/probe.rs,readonly','--mount',f'type=bind,source={R/paths[3]},target=/receipt.json,readonly',image,'bash','-c','set -eu; mkdir -p /root/.risc0/toolchains; cp -a /opt/risc0-rust /root/.risc0/toolchains/v1.88.0-rust-x86_64-unknown-linux-gnu; cp /probe.rs /work/examples/contract_probe.rs; cd /work; cargo run --locked --release --example contract_probe']
start=time.monotonic()
try:
    with (O/'execution.log').open('w') as f: result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=240)
    code=result.returncode
except subprocess.TimeoutExpired:
    subprocess.run(['docker','stop','zkp-contract-controls-v2'],capture_output=True);code=-1
(O/'receipt.json').write_text(json.dumps(dict(exit_code=code,seconds=time.monotonic()-start,command=cmd),indent=2))
(O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2))
print('exit',code)
