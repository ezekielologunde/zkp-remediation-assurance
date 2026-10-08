import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1];count=0

def check(p,h):
 global count
 assert hashlib.sha256(p.read_bytes()).hexdigest()==h,str(p)
 count+=1
for d in sorted((R/'analysis').glob('verisbom-*')):
 if not d.is_dir():continue
 m=d/'manifest.json'
 if m.exists():
  for k,v in json.loads(m.read_text()).items():check(d/k,v)
 f=d/'freeze.json'
 if f.exists():
  for k,v in json.loads(f.read_text()).get('sha256',{}).items():check(R/k,v)
 receipt=d/'receipt.json'
 if receipt.exists():
  for k,v in json.loads(receipt.read_text()).get('generated_sha256',{}).items():check(R/k,v)
for k,v in json.loads((R/'data/verisbom-runtime-inputs.json').read_text()).items():check(R/'data/proof-sandbox/verisbom-run-v0'/k,v)
B=R/'data/proof-sandbox/verisbom-bundle-v0'
assert (B/'original-core.bin').read_bytes()==(B/'changed-core.bin').read_bytes()
p=json.loads((B/'probe.json').read_text());assert all(p[k] for k in ['proof_bytes_unchanged','original_metadata_matches_authenticated','changed_metadata_differs_authenticated'])
assert [i for i,(a,b) in enumerate(zip(p['authenticated'],p['changed_metadata'])) if a!=b]==[1]
assert int(p['changed_metadata'][1],16)==int(p['authenticated'][1],16)+1
x=json.loads((R/'data/proof-sandbox/verisbom-results-v3/expected.json').read_text())
assert [int(v,16) for v in p['authenticated']]==[int(x[k],16) for k in ['expected_hash','root_pm','root_audit']]
results={}
for name,pattern in [('acceptance',[True,False,False,True]),('repair',[True,False,True,False])]:
 d=R/f'analysis/verisbom-{name}-v0';rows=json.loads((d/'cases.json').read_text())
 assert len(rows)==4
 for row,expected in zip(rows,pattern):
  log=(d/(row['case']+'.log')).read_text()
  assert row['math_verified'] and 'ZK Proof Math Valid' in log
  assert row['application_accepted']==expected==('VERIFICATION AND SBOM BINDING SUCCESSFUL' in log)
  assert row['exit_code']==(0 if expected else 1)
 results[name]=pattern
out=dict(status='passed',sha256_checks=count,application_cases=8,real_proof_math_acceptances=8,proof_core_bytes_identical=True,acceptance_patterns=results,scope='Independent evidence parsing and hashing; cryptographic execution is performed by recorded Nova binaries, not a separate crypto implementation.')
(R/'analysis/verisbom-verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
