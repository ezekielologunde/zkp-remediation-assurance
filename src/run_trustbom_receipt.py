"""Bounded local real-receipt reproduction, with immutable failed-run receipts."""
import hashlib,json,pathlib,shutil,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'data/proof-sandbox/trustbom-source/proving-service'
BOX=ROOT/'data/proof-sandbox/trustbom-run'
OUT=ROOT/'analysis/trustbom-receipt-v0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=False);shutil.copytree(SRC,BOX)
    (BOX/'examples').mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'src/trustbom_receipt_probe.rs',BOX/'examples/audit_probe.rs')
    image=subprocess.check_output(['docker','image','inspect','zkp-trustbom-audit:local','--format','{{.Id}}'],text=True).strip()
    inputs=[p for p in BOX.rglob('*') if p.is_file()]
    inputs+=[pathlib.Path(__file__),ROOT/'protocol/trustbom-receipt-pilot-v0.md']
    inputs += [ROOT/'data/proof-sandbox/risc0-runtime'/p for p in ['cargo-risczero.tgz','rust-toolchain.tar.gz','Dockerfile.direct']]
    (OUT/'freeze.json').write_text(json.dumps(dict(image=image,sha256={p.relative_to(ROOT).as_posix():sha(p) for p in inputs}),indent=2)+'\n')
    cmd=['docker','run','--rm','--name','zkp-trustbom-receipt-v0','--cpus','4','--memory','6g','--env','RISC0_DEV_MODE=0','--env','RISC0_SERVER_PATH=/usr/local/bin/r0vm','--env','CARGO_BUILD_JOBS=2','--mount',f'type=bind,source={BOX},target=/work','-w','/work',image,'cargo','run','--locked','--release','--example','audit_probe','--','benchmark/data/merkleproofs/batch_proof_2.json']
    start=time.perf_counter();status='incomplete';code=None
    try:
        with (OUT/'execution.log').open('w',encoding='utf-8') as log:
            r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=900)
        code=r.returncode
        log=(OUT/'execution.log').read_text()
        status='complete' if code==0 and '"real_receipt_verified":true' in log else 'execution_failed'
    except subprocess.TimeoutExpired:
        stopped=subprocess.run(['docker','stop','zkp-trustbom-receipt-v0'],capture_output=True,text=True)
        status='timed_out_container_stop_requested'
        (OUT/'timeout-stop.log').write_text(stopped.stdout+'\n'+stopped.stderr)
    finally:
        generated={p.relative_to(ROOT).as_posix():sha(p) for p in [BOX/'audit-receipt.json',BOX/'Cargo.lock',BOX/'methods/guest/Cargo.lock'] if p.exists()}
        (OUT/'receipt.json').write_text(json.dumps(dict(status=status,exit_code=code,seconds=time.perf_counter()-start,command=cmd,generated_sha256=generated),indent=2)+'\n')
        (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
        print(status,code,flush=True)
if __name__=='__main__':main()
