import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1];n=0

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(p,v):
 global n
 assert sha(p)==v,str(p);n+=1
A=json.loads((R/'data/zksbom-contract-audit.json').read_text());S=R/'data/zkSBOM-source'
for k,v in A['source_sha256'].items():ck(S/k,v)
for k,v in A['submodule_sha256'].items():ck(S/'zksbom-verifier/third_party/oZKS'/k,v)
for d in sorted((R/'analysis').glob('zksbom-*')):
 if not d.is_dir():continue
 f=d/'freeze.json'
 if f.exists():
  for k,v in json.loads(f.read_text())['inputs'].items():ck(R/k,v)
 f=d/'receipt.json'
 if f.exists():
  for k,v in json.loads(f.read_text()).get('generated',{}).items():ck(R/k,v)
 f=d/'manifest.json'
 if f.exists():
  for k,v in json.loads(f.read_text()).items():ck(d/k,v)
for name in ['zksbom-wrapper-v1','zksbom-label-wrapper-v1']:
 d=R/'analysis'/name;assert json.loads((d/'receipt.json').read_text())['exit_code']==0
 log=(d/'execution.log').read_text();assert 'THREE_WRAPPER_CONTROLS_PASSED' in log
 for text in ['member result=0 expected=0 key_match=1','nonmember result=1 expected=1 key_match=1','stale_proof_new_commitment result=2 expected=2 key_match=1']:assert text in log
D=R/'analysis/zksbom-cli-cases-v0';rows=json.loads((D/'cases.json').read_text());assert len(rows)==6
assert [r['proof_valid_message'] for r in rows]==[True,True,False,True,False,True]
for r in rows:
 log=(D/(r['case']+'.log')).read_text();assert ('Proof is valid.' in log)==r['proof_valid_message'];assert r['exit_code']==0
assert rows[0]['member_message'] and rows[1]['nonmember_message']
labels=json.loads((R/'data/proof-sandbox/zksbom-label-fixture-v0/labels.json').read_text())
for name,k,v in zip(labels['names'],labels['keys'],labels['payloads']):
 payload=hashlib.blake2b(name.encode(),digest_size=32).digest();assert payload.hex()==v
 assert hashlib.blake2b(name.encode()+payload,digest_size=32).hexdigest()==k
# Explicit consumer requirement: exactly the expected nonempty dependency, valid proof,
# and an explicit member/nonmember result. This is an output-level baseline, not another verifier.
expected=[labels['names'][0],labels['names'][1],labels['names'][0],labels['names'][0],labels['names'][0],labels['names'][0]]
baseline=[]
for r,e in zip(rows,expected):
 log=(D/(r['case']+'.log')).read_text();deps=[l[len('Dependency: '):] for l in log.splitlines() if l.startswith('Dependency: ')]
 baseline.append(r['proof_valid_message'] and deps==[e] and (r['member_message'] != r['nonmember_message']))
assert baseline==[True,True,False,False,False,False]
out=dict(status='passed',hash_checks=n,native_wrapper_cases=6,cli_cases=6,cli_all_exit_zero=True,explicit_query_baseline=baseline,baseline_scope='Saved-output consumer requirement, not additional cryptographic verification or an upstream promised policy',source_unchanged=True)
(R/'analysis/zksbom-verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
