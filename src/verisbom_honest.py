import pathlib,json,subprocess,os
D=pathlib.Path('/work');os.chdir(D)
def call(args):
 print('RUN',args,flush=True);subprocess.run(args,check=True,timeout=600)
import common
raw=json.loads(pathlib.Path('registry.json').read_text());pkgs=raw if isinstance(raw,list) else raw['packages'];pkg=pkgs[0]
pathlib.Path('registry.json').write_text(json.dumps([pkg]));pathlib.Path('selected-sbom.json').write_text(json.dumps([pkg]));name=pkg['name']
call(['python3','python/setup_pm_web.py','audit'])
pathlib.Path('propagated_compliance_audit.json').write_text(json.dumps({'p_allowed':{name:1}}))
call(['python3','python/setup_auditor_web.py','audit'])
call(['python3','python/prove_web.py','--input','selected-sbom.json','--tree','tree_pm_audit.json','--audit','policy_ALLOWED_audit.json','--db','crates_audit.db','--output','witness.json'])
w=json.loads(pathlib.Path('witness.json').read_text());pm=json.loads(pathlib.Path('tree_pm_audit.json').read_text())[-1][0];au=json.loads(pathlib.Path('policy_ALLOWED_audit.json').read_text())[-1][0]
def arr(a):return sum(int(v)<<(64*i) for i,v in enumerate(a))
assert arr(w['root'])==int(pm,16) and arr(w['audit_root'])==int(au,16)
leaf,_=common.hash_package_leaf(pkg);h=common._run_bin(D/'circuits/poseidon3_cpp/poseidon3',{'in':['0',str(int(leaf,16)),'0']});assert h
pathlib.Path('expected.json').write_text(json.dumps(dict(root_pm=pm,root_audit=au,expected_hash=h,package=name),indent=2))
call(['./bomz','--mode','prove','--circuit','circuits/step.r1cs','--input','witness.json','--witnessgenerator','circuits/step_cpp/step','--output','honest.proof'])
call(['./bomz','--mode','verify','--circuit','circuits/step.r1cs','--output','honest.proof','--root-pm',pm,'--root-audit',au,'--expected-hash',h])
print('HONEST_COMPLETE',flush=True)
