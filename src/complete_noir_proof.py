import hashlib,json,pathlib,shutil,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
BOX=ROOT/'data/proof-sandbox/noir-runtime'
OUT=ROOT/'analysis/noir-proof-complete-v0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=False)
    image=subprocess.check_output(['docker','image','inspect','zkp-noir-audit:complete','--format','{{.Id}}'],text=True).strip()
    files=[BOX/'Dockerfile.jq',BOX/'bin/bb',BOX/'original/target/attest.json',BOX/'original/target/attest.gz',pathlib.Path(__file__),ROOT/'protocol/noir-environment-amendment-v0.md']
    (OUT/'freeze.json').write_text(json.dumps(dict(image=image,sha256={p.relative_to(ROOT).as_posix():sha(p) for p in files}),indent=2)+'\n')
    shutil.copyfile(BOX/'Dockerfile.jq',OUT/'Dockerfile')
    records=[];status='incomplete'
    def run(name,args,network=True):
        cmd=['docker','run','--rm','--cpus','4','--memory','4g','--env','HOME=/work/home','--mount',f'type=bind,source={BOX},target=/work','-w','/work']
        if not network:cmd+=['--network','none']
        cmd+=[image]+args
        print('Starting '+name,flush=True);start=time.perf_counter()
        r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=480)
        (OUT/(name+'.log')).write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
        records.append(dict(name=name,command=cmd,exit_code=r.returncode,seconds=time.perf_counter()-start));print(name,r.returncode,flush=True)
        return r.returncode
    try:
        assert run('packages',['dpkg-query','-W','curl','ca-certificates','jq','gzip'],False)==0
        base=['/work/bin/bb']
        assert run('write-vk',base+['write_vk','-v','-s','ultra_honk','-b','/work/original/target/attest.json','-o','/work/original/target','--output_format','bytes_and_fields','--honk_recursion','1','--init_kzg_accumulator'])==0
        assert run('prove',base+['prove','-v','-s','ultra_honk','-b','/work/original/target/attest.json','-w','/work/original/target/attest.gz','-o','/work/original/target','--output_format','bytes_and_fields','--honk_recursion','1','--recursive','--init_kzg_accumulator'])==0
        args=['verify','-s','ultra_honk','-k','/work/original/target/vk','-p','/work/original/target/proof']
        assert run('verify-original',base+args)==0
        proof=bytearray((BOX/'original/target/proof').read_bytes());proof[0]^=1
        (BOX/'tampered-proof').write_bytes(proof)
        assert run('verify-tampered',base+args[:-1]+['/work/tampered-proof'],False)!=0
        status='complete'
    finally:
        generated=[p for d in ['original/target','home'] for p in (BOX/d).rglob('*') if p.is_file()]
        if (BOX/'tampered-proof').exists():generated.append(BOX/'tampered-proof')
        (OUT/'receipt.json').write_text(json.dumps(dict(status=status,steps=records,generated_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in generated}),indent=2)+'\n')
        (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
        print(status,flush=True)
if __name__=='__main__':main()
