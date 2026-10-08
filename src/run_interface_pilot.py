"""Local-only example execution with preserved receipts; not protocol security testing."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT/'data/piranhas-source'
BOX = ROOT/'data/proof-sandbox'
OUT = ROOT/'analysis/piranhas-interface-pilot-v0'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=False)
    build = BOX/'build'
    build.mkdir(exist_ok=False)
    revision = subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD'],text=True).strip()
    assert revision == '62bd2af3b7501ab7458a682d8849206537a86d9e'
    names = ['attest.circom','merkleTree.circom','verifyKeySchnorrGroup.circom','input.json']
    for name in names:
        shutil.copyfile(SOURCE/'circom'/name,BOX/name)
    source_hashes = {name:sha(BOX/name) for name in names}
    freeze = dict(upstream_revision=revision,revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_hashes=source_hashes,driver_sha256=sha(pathlib.Path(__file__)),
        protocol_sha256=sha(ROOT/'protocol/piranhas-interface-pilot-v0.md'),
        package_lock_sha256=sha(BOX/'package-lock.json'),node=subprocess.check_output(['node','--version'],text=True).strip())
    (OUT/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    shutil.copyfile(BOX/'package-lock.json',OUT/'package-lock.json')
    circom = ['node','node_modules/circom2/cli.js']
    snark = ['node','node_modules/snarkjs/build/cli.cjs']
    records=[]
    def step(name,command,required=True):
        print('Starting '+name,flush=True)
        start=time.perf_counter()
        try:
            result=subprocess.run(command,cwd=BOX,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600)
            code=result.returncode
            output=result.stdout+'\n'+result.stderr
        except subprocess.TimeoutExpired:
            code=-1; output='Timed out after 600 seconds; no success assumed.'
        (OUT/(name+'.log')).write_text(output,encoding='utf-8')
        records.append(dict(step=name,command=command,exit_code=code,seconds=time.perf_counter()-start))
        print(json.dumps(records[-1]),flush=True)
        if required and code:
            raise RuntimeError(name+' failed; see retained log')
        return code,output
    conclusion={}
    try:
        step('compiler-version',circom+['--version'])
        step('compile',circom+['attest.circom','--r1cs','--wasm','--sym','-l','node_modules','-o','build'])
        step('r1cs-info',snark+['r1cs','info','build/attest.r1cs'])
        step('witness',['node','build/attest_js/generate_witness.js','build/attest_js/attest.wasm','input.json','build/witness.wtns'])
        step('witness-check',snark+['wtns','check','build/attest.r1cs','build/witness.wtns'])
        step('test-setup-init',snark+['powersoftau','new','bn128','15','build/test.ptau'])
        step('test-setup-phase2',snark+['powersoftau','prepare','phase2','build/test.ptau','build/test-final.ptau'])
        step('test-setup-groth16',snark+['groth16','setup','build/attest.r1cs','build/test-final.ptau','build/test.zkey'])
        step('verification-key',snark+['zkey','export','verificationkey','build/test.zkey','build/vk.json'])
        step('prove',snark+['groth16','prove','build/test.zkey','build/witness.wtns','build/proof.json','build/public.json'])
        verify=snark+['groth16','verify','build/vk.json','build/public.json','build/proof.json']
        _,original=step('verify-original-request',verify)
        _,relabelled=step('verify-different-external-request-label',verify)
        public=json.loads((build/'public.json').read_text())
        assert len(public)==3
        changed=list(public);changed[1]=str(int(changed[1])+1)
        (build/'changed-public.json').write_text(json.dumps(changed))
        rejected,log=step('verify-tampered-public-key',snark+['groth16','verify','build/vk.json','build/changed-public.json','build/proof.json'],required=False)
        conclusion=dict(public_signal_count=len(public),original_verified='OK!' in original,
                        identical_inputs_verified_again='OK!' in relabelled,tampered_public_key_rejected=rejected!=0 and 'Invalid proof' in log,
                        interpretation='External request label is not a verifier input here. Repetition alone is not a vulnerability or full-protocol result.',
                        test_setup_only=True)
    except Exception as exc:
        conclusion=dict(status='incomplete',error=str(exc),no_security_conclusion=True)
    finally:
        generated={p.relative_to(BOX).as_posix():sha(p) for p in build.rglob('*') if p.is_file()}
        (OUT/'receipt.json').write_text(json.dumps(dict(steps=records,conclusion=conclusion,generated_sha256=generated),indent=2)+'\n')
        (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
        print(json.dumps(conclusion),flush=True)


if __name__=='__main__':main()
