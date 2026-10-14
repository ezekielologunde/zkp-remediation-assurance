import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];D=R/'analysis/client-path-v0';count=0
for name,base in [('manifest',D),('freeze',R)]:
 for p,h in json.loads((D/(name+'.json')).read_text()).items():
  assert hashlib.sha256((base/p).read_bytes()).hexdigest()==h,p;count+=1
s=json.loads((D/'result.json').read_text())
a=json.loads((R/'data/verisbom-artifact-audit.json').read_text())
assert s['app_sha256']==a['text_source_sha256']['ase-artifact/Empirical/src/app.py']
expected=json.loads((R/'data/proof-sandbox/verisbom-results-v3/expected.json').read_text())
cases=['original','expected_root_only','metadata_only','metadata_and_expected_root'];rows=[]
for v,pattern in [('original',[True,False,False,True]),('bound',[True,False,True,False])]:
 for n,want in zip(cases,pattern):
  r=json.loads((D/(v+'-'+n+'.json')).read_text())
  assert r['success']==want
  assert int(r['computed_hash'],16)==int(expected['expected_hash'],16)
  calls=[c for c in r['commands'] if '--mode' in c['command']]
  assert len(calls)==1
  assert 'ZK Proof Math Valid' in calls[0]['stdout']
  assert calls[0]['exit_code']==(0 if want else 1)
  assert any(m['kind']=='success' and 'Verification Successful' in m['text'] for m in r['messages'])==want
  if want:assert not any(m['kind']=='error' for m in r['messages'])
  rows.append(dict(verifier=v,case=n,accepted=want))
out=dict(status='passed',hash_checks=count,cases=rows,source_matches_archived_manifest=True,
 scope='Independent parsing and hash checks of extracted-block integration evidence; not independent cryptography or full UI execution')
(R/'analysis/client-path-verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
