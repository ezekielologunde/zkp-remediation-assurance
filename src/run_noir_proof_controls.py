import hashlib,json,pathlib,re,shutil,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
BOX=ROOT/'data/proof-sandbox/noir-runtime'
OUT=ROOT/'analysis/noir-proof-controls-v0'
IMAGE='sha256:0dd364ba7e10242f07755449e3a3d0e35f9efd987952737b90def6709ab0c5ce'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=False)
    src=BOX/'original'
    files=[src/'Prover.toml',src/'target/attest.json',src/'target/attest.gz',BOX/'bin/bb',BOX/'bin/nargo',pathlib.Path(__file__),ROOT/'protocol/noir-proof-controls-v0.md']
    (OUT/'freeze.json').write_text(json.dumps({p.relative_to(ROOT).as_posix():sha(p) for p in files},indent=2)+'\n')
    steps=[];status='incomplete'
    def run(name,args,network=False):
        cmd=['docker','run','--rm','--cpus','4','--memory','4g','--env','HOME=/work/home','--mount',f'type=bind,source={BOX},target=/work','-w','/work']
        if not network:cmd+=['--network','none']
        cmd+=[IMAGE]+args
        start=time.perf_counter();r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=480)
        log=r.stdout+'\n'+r.stderr;(OUT/(name+'.log')).write_text(log,encoding='utf-8')
        steps.append(dict(name=name,command=cmd,exit_code=r.returncode,seconds=time.perf_counter()-start));print(name,r.returncode,flush=True)
        return r.returncode,log
    try:
        original=(src/'Prover.toml').read_text()
        response=re.search(r'(?m)^rsp\s*=\s*"([^"]+)"',original).group(1)
        first_sig=int(re.search(r'sig\s*=\s*\[\s*(\d+)',original).group(1))
        for case in ['response','signature']:
            dest=BOX/('mutated_'+case);shutil.copytree(src,dest,ignore=shutil.ignore_patterns('target'))
            if case=='response':
                replacement=str(int(response,0)+1)
                changed,n=re.subn(r'(?m)^(rsp\s*=\s*)"[^"]+"',lambda m:m[1]+'"'+replacement+'"',original)
            else:
                changed,n=re.subn(r'(sig\s*=\s*\[\s*)\d+',lambda m:m[1]+str((first_sig+1)%256),original)
            assert n==1
            (dest/'Prover.toml').write_text(changed)
            c,log=run(case+'-witness',['/work/bin/nargo','execute','--program-dir','/work/'+dest.name])
            assert c!=0 and 'assert' in log.lower()
        base=['/work/bin/bb']
        c,_=run('write-vk',base+['write_vk','-v','-s','ultra_honk','-b','/work/original/target/attest.json','-o','/work/original/target','--output_format','bytes_and_fields','--honk_recursion','1','--init_kzg_accumulator'],network=True);assert c==0
        c,_=run('prove',base+['prove','-v','-s','ultra_honk','-b','/work/original/target/attest.json','-w','/work/original/target/attest.gz','-o','/work/original/target','--output_format','bytes_and_fields','--honk_recursion','1','--recursive','--init_kzg_accumulator'],network=True);assert c==0
        args=['verify','-s','ultra_honk','-k','/work/original/target/vk','-p','/work/original/target/proof']
        c,_=run('verify-original',base+args,network=True);assert c==0
        proof=bytearray((src/'target/proof').read_bytes());proof[0]^=1
        (BOX/'tampered-proof').write_bytes(proof)
        c,_=run('verify-tampered',base+args[:-1]+['/work/tampered-proof']);assert c!=0
        status='complete'
    finally:
        generated=[p for d in ['original/target','mutated_response','mutated_signature','home'] for p in (BOX/d).rglob('*') if p.is_file()]
        (OUT/'receipt.json').write_text(json.dumps(dict(status=status,steps=steps,generated_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in generated}),indent=2)+'\n')
        (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
        print(status,flush=True)
if __name__=='__main__':main()
