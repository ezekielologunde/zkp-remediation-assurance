import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
x=json.loads((R/'data/corpus-ledger-v0.json').read_text());assert len(x['systems'])==5 and len({v['id'] for v in x['systems']})==5
z=json.loads((R/'data/zksbom-contract-audit.json').read_text());S=R/'data/zkSBOM-source'
for p,h in z['source_sha256'].items():assert sha(S/p)==h,p
for p,h in z['submodule_sha256'].items():assert sha(S/'zksbom-verifier/third_party/oZKS'/p)==h,p
v=json.loads((R/'data/verisbom-artifact-audit.json').read_text());D=R/'data/proof-sandbox/verisbom-source'
assert sha(D/'ase-artifact_new.zip')==v['sha256']
for p,h in v['text_source_sha256'].items():assert sha(D/'extracted'/p)==h,p
O=R/'analysis/zra-circomspect-v0';m=json.loads((O/'manifest.json').read_text());f=json.loads((O/'freeze.json').read_text())
for p,h in m.items():assert sha(O/p)==h,p
for p,h in f['sha256'].items():assert sha(R/p)==h,p
rs=json.loads((O/'original.sarif').read_text())['runs'][0]['results'];assert len(rs)==2 and {v['ruleId'] for v in rs}=={'CS0003','CS0004'}
result=dict(status='passed',screened_papers=5,executed_systems=3,pending_systems=2,zksbom_source_hashes=len(z['source_sha256']),ozks_dependency_hashes=len(z['submodule_sha256']),verisbom_source_hashes=len(v['text_source_sha256']),verisbom_archive_hash=True,zra_analyzer_hashes=len(m)+len(f['sha256']),limitations='Purposive sample; no prevalence or independence claim')
(R/'analysis/corpus-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
