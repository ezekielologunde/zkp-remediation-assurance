"""Amended local setup control. Fresh entropy is never written to receipts."""
import hashlib
import json
import pathlib
import secrets
import subprocess
import time

ROOT=pathlib.Path(__file__).resolve().parents[1]
BOX=ROOT/'data/proof-sandbox'
OUT=ROOT/'analysis/piranhas-setup-control-v0'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=False)
    target=BOX/'control';target.mkdir(exist_ok=False)
    source_files=['build/attest.r1cs','build/witness.wtns','build/test.ptau','package-lock.json']
    freeze=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        inputs={f:sha(BOX/f) for f in source_files},driver_sha256=sha(pathlib.Path(__file__)),
        amendment_sha256=sha(ROOT/'protocol/piranhas-setup-control-amendment.md'))
    (OUT/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    records=[];conclusion={}
    def step(name,args,entropy=False,required=True):
        command=['node','node_modules/snarkjs/build/cli.cjs']+args
        safe=list(command)
        if entropy:
            command+=['-e='+secrets.token_hex(32)]
            safe+=['-e=<fresh-local-entropy-not-recorded>']
        print('Starting '+name,flush=True);start=time.perf_counter()
        r=subprocess.run(command,cwd=BOX,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600)
        text=r.stdout+'\n'+r.stderr
        (OUT/(name+'.log')).write_text(text,encoding='utf-8')
        records.append(dict(step=name,command=safe,exit_code=r.returncode,seconds=time.perf_counter()-start))
        print(json.dumps(records[-1]),flush=True)
        if required and r.returncode:raise RuntimeError(name+' failed')
        return r.returncode,text
    try:
        step('phase1-contribution',['powersoftau','contribute','build/test.ptau','control/contributed.ptau','--name=local-test'],entropy=True)
        step('phase2-prepare',['powersoftau','prepare','phase2','control/contributed.ptau','control/final.ptau'])
        step('groth16-setup',['groth16','setup','build/attest.r1cs','control/final.ptau','control/initial.zkey'])
        step('zkey-contribution',['zkey','contribute','control/initial.zkey','control/final.zkey','--name=local-test'],entropy=True)
        step('key-export',['zkey','export','verificationkey','control/final.zkey','control/vk.json'])
        vk=json.loads((target/'vk.json').read_text())
        assert all(point!=['0','1','0'] for point in vk['IC'][2:4])
        step('prove',['groth16','prove','control/final.zkey','build/witness.wtns','control/proof.json','control/public.json'])
        command=['groth16','verify','control/vk.json','control/public.json','control/proof.json']
        _,original=step('verify-original',command)
        _,repeat=step('verify-identical-inputs',command)
        public=json.loads((target/'public.json').read_text())
        changed=list(public);changed[1]=str(int(changed[1])+1)
        (target/'changed-public.json').write_text(json.dumps(changed))
        code,changed_log=step('verify-changed-key',['groth16','verify','control/vk.json','control/changed-public.json','control/proof.json'],required=False)
        conclusion=dict(original_verified='OK!' in original,repeated_inputs_verified='OK!' in repeat,
                        changed_public_key_rejected='Invalid proof' in changed_log and 'OK!' not in changed_log,
                        public_inputs=3,public_key_ic_points_nonidentity=True,local_test_setup_only=True)
        assert conclusion['original_verified'] and conclusion['repeated_inputs_verified'] and conclusion['changed_public_key_rejected']
    except Exception as exc:
        conclusion.update(status='incomplete',error=type(exc).__name__+': '+str(exc),no_security_conclusion=True)
    finally:
        result=dict(steps=records,conclusion=conclusion,generated_sha256={p.relative_to(BOX).as_posix():sha(p) for p in target.iterdir() if p.is_file()})
        (OUT/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
        (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
        print(json.dumps(conclusion),flush=True)


if __name__=='__main__':main()
