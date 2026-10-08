import json,subprocess,pathlib
x=json.loads(pathlib.Path('/work/expected.json').read_text())
subprocess.run(['/work/bomz','--mode','verify','--circuit','circuits/step.r1cs','--output','honest.proof.proof','--root-pm',x['root_pm'],'--root-audit',x['root_audit'],'--expected-hash',x['expected_hash']],cwd='/work',check=True,timeout=600)
print('HONEST_COMPLETE')
