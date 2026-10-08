import json,pathlib,subprocess
x=json.loads(pathlib.Path('/evidence/expected.json').read_text());p=json.loads(pathlib.Path('/bundle/probe.json').read_text())
assert int(p['authenticated'][1],16)==int(x['root_pm'],16)
changed=p['changed_metadata'][1]
base=['/work/bomz','--mode','verify','--circuit','circuits/step.r1cs','--root-audit',x['root_audit'],'--expected-hash',x['expected_hash']]
cases=[('original','/evidence/honest.proof.proof',x['root_pm']),('expected_root_only','/evidence/honest.proof.proof',changed),('metadata_only','/bundle/changed-metadata.proof',x['root_pm']),('metadata_and_expected_root','/bundle/changed-metadata.proof',changed)]
rows=[]
for name,proof,root in cases:
 cmd=base+['--output',proof,'--root-pm',root];r=subprocess.run(cmd,cwd='/work',capture_output=True,text=True,timeout=120);log=r.stdout+'\n'+r.stderr;pathlib.Path('/out/'+name+'.log').write_text(log)
 rows.append(dict(case=name,command=cmd,exit_code=r.returncode,math_verified='ZK Proof Math Valid' in log,application_accepted='VERIFICATION AND SBOM BINDING SUCCESSFUL' in log,expected_root=root))
pathlib.Path('/out/cases.json').write_text(json.dumps(rows,indent=2))
assert all(r['math_verified'] for r in rows)
assert [r['application_accepted'] for r in rows]==[True,False,False,True]
print('FOUR_CASES_COMPLETE')
