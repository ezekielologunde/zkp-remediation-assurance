"""Fixed local circuit controls. Outputs refuse overwrite."""
import hashlib,json,pathlib,shutil,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
BOX=ROOT/'data/proof-sandbox'
OUT=ROOT/'analysis/root-binding-v0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=False)
    inputs=[ROOT/'protocol/root-binding-pilot-v0.md',pathlib.Path(__file__),ROOT/'src/generate_root_cases.cjs']
    inputs += [BOX/p for p in ['input.json','build/attest.r1cs','build/attest_js/attest.wasm','control/final.zkey','control/vk.json','mutation-runtime/package-lock.json']]
    (OUT/'freeze.json').write_text(json.dumps({str(p.relative_to(ROOT)):sha(p) for p in inputs},indent=2)+'\n')
    shutil.copyfile(BOX/'mutation-runtime/package-lock.json',OUT/'package-lock.json')
    steps=[];cases=[]
    def run(name,args):
        start=time.perf_counter()
        r=subprocess.run(['node']+args,cwd=BOX,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        log=r.stdout+'\n'+r.stderr
        (OUT/(name+'.log')).write_text(log,encoding='utf-8')
        steps.append(dict(name=name,command=['node']+args,exit_code=r.returncode,seconds=time.perf_counter()-start))
        print(name,r.returncode,flush=True)
        return r.returncode,log
    def snark(name,args):return run(name,['node_modules/snarkjs/build/cli.cjs']+args)
    try:
        assert run('generate',[str(ROOT/'src/generate_root_cases.cjs')])[0]==0
        for name,expected in [('original',True),('stale_root',False),('recomputed_root',True),('invalid_signature',False)]:
            prefix='root-binding/'+name
            code,log=run(name+'-witness',['build/attest_js/generate_witness.js','build/attest_js/attest.wasm',prefix+'.json',prefix+'.wtns'])
            result=dict(case=name,expected_witness_success=expected,witness_success=code==0,proof_verified=False)
            cases.append(result)
            assert (code==0)==expected
            if not expected:
                assert 'Assert Failed' in log or 'Assert failed' in log
                continue
            c,log=snark(name+'-check',['wtns','check','build/attest.r1cs',prefix+'.wtns'])
            assert c==0 and 'WITNESS IS CORRECT' in log
            assert snark(name+'-prove',['groth16','prove','control/final.zkey',prefix+'.wtns',prefix+'-proof.json',prefix+'-public.json'])[0]==0
            c,log=snark(name+'-verify',['groth16','verify','control/vk.json',prefix+'-public.json',prefix+'-proof.json'])
            result['proof_verified']=c==0 and 'OK!' in log
            assert result['proof_verified']
        a=json.loads((BOX/'root-binding/original-public.json').read_text())
        b=json.loads((BOX/'root-binding/recomputed_root-public.json').read_text())
        assert a==b and len(a)==3
        status='complete'
    except Exception as e:
        status=type(e).__name__+': '+str(e)
        raise
    finally:
        files={p.relative_to(ROOT).as_posix():sha(p) for p in (BOX/'root-binding').glob('*') if p.is_file()}
        (OUT/'receipt.json').write_text(json.dumps(dict(status=status,cases=cases,steps=steps,generated_sha256=files),indent=2)+'\n')
        (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
if __name__=='__main__':main()
