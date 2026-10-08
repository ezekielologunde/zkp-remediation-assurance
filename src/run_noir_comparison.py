"""Reproduce documented Noir example in a bounded local container."""
import hashlib,json,pathlib,shutil,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
BOX=ROOT/'data/proof-sandbox/noir-runtime'
OUT=ROOT/'analysis/noir-comparison-v0'
IMAGE='sha256:0dd364ba7e10242f07755449e3a3d0e35f9efd987952737b90def6709ab0c5ce'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=False)
    src=ROOT/'data/piranhas-source/noir/1-attest-(Pi-zkRA)'
    shutil.copytree(src,BOX/'original')
    manifest=BOX/'original/Nargo.toml'
    old='schnorr = { tag = "v0.1.3", git = "https://github.com/noir-lang/schnorr.git" }'
    text=manifest.read_text();assert text.count(old)==1
    manifest.write_text(text.replace(old,'schnorr = { path = "../schnorr" }'))
    files=list(src.rglob('*.nr'))+[src/'Nargo.toml',src/'Prover.toml',BOX/'nargo.tar.gz',BOX/'bb.tar.gz',manifest,ROOT/'protocol/noir-comparison-v0.md',pathlib.Path(__file__)]
    (OUT/'freeze.json').write_text(json.dumps(dict(image=IMAGE,sha256={p.relative_to(ROOT).as_posix():sha(p) for p in files},dependency_commit='07ab027a52ea75a93f20bb849b6a1da93791d0a3'),indent=2)+'\n')
    steps=[]
    def run(name,args):
        cmd=['docker','run','--rm','--network','none','--cpus','4','--memory','4g','--mount',f'type=bind,source={BOX},target=/work','-w','/work',IMAGE]+args
        start=time.perf_counter();r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
        (OUT/(name+'.log')).write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
        steps.append(dict(name=name,command=cmd,exit_code=r.returncode,seconds=time.perf_counter()-start));print(name,r.returncode,flush=True)
        return r.returncode
    status='not_started'
    try:
        code='import pathlib,tarfile; p=pathlib.Path("bin"); p.mkdir(exist_ok=False); [tarfile.open(x).extractall(p,filter="data") for x in ["nargo.tar.gz","bb.tar.gz"]]'
        assert run('extract',['python','-c',code])==0
        assert run('nargo-version',['/work/bin/nargo','--version'])==0
        if run('bb-version',['/work/bin/bb','--version'])!=0:
            status='bb_runtime_unavailable'
        if run('compile',['/work/bin/nargo','compile','--program-dir','/work/original'])!=0:
            status='original_compile_failed';return
        if run('execute-original',['/work/bin/nargo','execute','--program-dir','/work/original'])!=0:
            status='original_witness_failed';return
        status='original_witness_succeeded_proof_not_run'
    finally:
        (OUT/'receipt.json').write_text(json.dumps(dict(status=status,steps=steps),indent=2)+'\n')
        (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
        print(status,flush=True)
if __name__=='__main__':main()
