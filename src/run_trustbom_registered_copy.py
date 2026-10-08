import hashlib,json,pathlib,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'data/proof-sandbox/trustbom-source/proving-service'
OUT=ROOT/'analysis/trustbom-receipt-linux-v3'
SAVED=ROOT/'data/proof-sandbox/trustbom-linux-results-v3'
NAME='zkp-trustbom-receipt-linux-v3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=False);SAVED.mkdir(exist_ok=False)
    image=subprocess.check_output(['docker','image','inspect','zkp-trustbom-audit:local','--format','{{.Id}}'],text=True).strip()
    files=[p for p in SRC.rglob('*') if p.is_file()]+[ROOT/'src/trustbom_receipt_probe.rs',pathlib.Path(__file__),ROOT/'protocol/trustbom-linux-build-amendment.md']
    (OUT/'freeze.json').write_text(json.dumps(dict(image=image,sha256={p.relative_to(ROOT).as_posix():sha(p) for p in files}),indent=2)+'\n')
    shell='set -eu\nmkdir -p /root/.risc0/toolchains\ncp -a /opt/risc0-rust /root/.risc0/toolchains/v1.88.0-rust-x86_64-unknown-linux-gnu\ncp -a /source/. /work/\nmkdir -p /work/examples\ncp /probe.rs /work/examples/audit_probe.rs\ncd /work\ncargo run --locked --release --example audit_probe -- benchmark/data/merkleproofs/batch_proof_2.json\ncp audit-receipt.json /evidence/\ncp Cargo.lock /evidence/host-Cargo.lock\ncp methods/guest/Cargo.lock /evidence/guest-Cargo.lock\n'
    (OUT/'command.sh').write_text(shell)
    cmd=['docker','run','--rm','--name',NAME,'--cpus','4','--memory','6g','--env','RISC0_DEV_MODE=0','--env','RISC0_SERVER_PATH=/usr/local/bin/r0vm','--env','CARGO_BUILD_JOBS=2','--mount',f'type=bind,source={SRC},target=/source,readonly','--mount',f'type=bind,source={ROOT / "src/trustbom_receipt_probe.rs"},target=/probe.rs,readonly','--mount',f'type=bind,source={SAVED},target=/evidence','--mount','type=volume,source=zkp-trustbom-work-v1,target=/work','--mount','type=volume,source=zkp-trustbom-registry-v1,target=/usr/local/cargo/registry',image,'bash','-c',shell]
    start=time.perf_counter();status='incomplete';code=None
    try:
        with (OUT/'execution.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=900)
        code=r.returncode
        log=(OUT/'execution.log').read_text()
        status='complete' if code==0 and '"real_receipt_verified":true' in log else 'execution_failed'
    except subprocess.TimeoutExpired:
        stopped=subprocess.run(['docker','stop',NAME],capture_output=True,text=True)
        (OUT/'timeout-stop.log').write_text(stopped.stdout+'\n'+stopped.stderr);status='timed_out_container_stop_requested'
    finally:
        (OUT/'receipt.json').write_text(json.dumps(dict(status=status,exit_code=code,seconds=time.perf_counter()-start,command=cmd,generated_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in SAVED.iterdir() if p.is_file()}),indent=2)+'\n')
        (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
        print(status,code,flush=True)
if __name__=='__main__':main()
