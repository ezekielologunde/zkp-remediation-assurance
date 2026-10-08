import pathlib,json,hashlib,re
R=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
counts={}
for name in ['repair-v0','repair-v1','repair-proof-v0','repair-proof-control-v1']:
 O=R/'analysis'/name;m=json.loads((O/'manifest.json').read_text());f=json.loads((O/'freeze.json').read_text());r=json.loads((O/'receipt.json').read_text())
 for p,h in m.items():assert sha(O/p)==h,p
 for p,h in f.items():assert sha(R/p)==h,p
 for p,h in r.get('generated_sha256',{}).items():assert sha(R/p)==h,p
 counts[name]=dict(manifest=len(m),frozen=len(f),generated=len(r.get('generated_sha256',{})))
O=R/'analysis/repair-v1';r=json.loads((O/'receipt.json').read_text());assert r['status']=='complete'
steps={s['name']:s for s in r['steps']}
assert steps['original-witness']['code']==0
for name in ['stale_root','recomputed_root','changed_key','changed_tag','changed_challenge','invalid_signature']:
 assert steps[name+'-witness']['code']!=0
 assert 'assert failed' in (O/(name+'-witness.log')).read_text().lower()
assert 'WITNESS IS CORRECT' in (O/'r1cs-check.log').read_text()
assert 'OK!' in (R/'analysis/repair-proof-v0/verify.log').read_text()
assert 'Invalid proof' in (R/'analysis/repair-proof-control-v1/verify.log').read_text()
rr=json.loads((R/'analysis/repair-proof-control-v1/receipt.json').read_text());assert rr['status']=='complete'
assert sha(R/'data/proof-sandbox/repair-proof-v0/changed-public-v1.json')==rr['changed_public_sha256']
metrics={}
for name in ['original','repair']:
 t=(O/(name+'-inspect.log')).read_text();metrics[name]=sum(int(re.search('^'+k+r': (\d+)',t,re.M).group(1)) for k in ['non-linear constraints','linear constraints'])
result=dict(status='passed',hash_counts=counts,positive_witness=True,negative_witness_cases=6,positive_real_proof=True,public_challenge_rejected=True,constraints=metrics,constraint_delta=metrics['repair']-metrics['original'],constraint_increase_percent=100*(metrics['repair']/metrics['original']-1),limits='Local alternative hash instantiation; not production certification, privacy-equivalence or runtime benchmark')
(R/'analysis/repair-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
