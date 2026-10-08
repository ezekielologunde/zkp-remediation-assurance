import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
O=R/'analysis/zra-controls-v0';m=json.loads((O/'manifest.json').read_text());f=json.loads((O/'freeze.json').read_text());receipt=json.loads((O/'receipt.json').read_text())
for p,h in m.items():assert sha(O/p)==h,p
for p,h in f.items():assert sha(R/p)==h,p
for p,h in receipt['generated_sha256'].items():assert sha(R/p)==h,p
assert receipt['status']=='complete'
assert 'OK!' in (O/'verify.log').read_text()
for k in ['root','devAddr','challenge']:assert 'Invalid proof' in (O/('changed-'+k+'.log')).read_text()
assert 'assert' in (O/'changed-response.log').read_text().lower()
source=json.loads((R/'data/zra-source-audit.json').read_text())
for p,h in source['sha256'].items():assert sha(R/'data/proof-sandbox/zra-source'/p)==h,p
result=dict(status='passed',manifest_hashes=len(m),frozen_hashes=len(f),generated_hashes=len(receipt['generated_sha256']),source_hashes=len(source['sha256']),positive_proof=True,negative_public_cases=3,negative_witness_cases=1,limits='Shipped ra40 binaries/keys; no fresh source-build correspondence or on-chain execution')
(R/'analysis/zra-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
