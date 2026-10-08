import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
O=R/'analysis/contract-controls-v2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'manifest.json').read_text())
for p,h in m.items():assert sha(O/p)==h,p
f=json.loads((O/'freeze.json').read_text())['sha256']
for p,h in f.items():assert sha(R/p)==h,p
assert json.loads((O/'receipt.json').read_text())['exit_code']==0
cases=[json.loads(x) for x in (O/'execution.log').read_text().splitlines() if x.startswith('{')]
expected={'original':True,'expected_root':False,'expected_policy':False,'expected_compliance':False,'expected_image':False,'altered_journal':False}
assert len(cases)==6
assert {x['case']:x['accepted'] for x in cases}==expected
assert all(x['accepted']==x['expected'] for x in cases)
sources=json.loads((R/'analysis/contract-source-map.json').read_text())
for x in sources:
 p=R/x['path'];assert sha(p)==x['sha256']
 lines=p.read_text(encoding='utf-8').splitlines()
 for a in x['anchors']:assert lines[a['line']-1].strip()==a['text']
result=dict(status='passed',case_count=len(cases),manifest_hashes=len(m),frozen_hashes=len(f),source_hashes=len(sources),source_anchors=sum(len(x['anchors']) for x in sources),scope='Local adapter with saved real receipt; not HTTP handler or deployment test')
(R/'analysis/contract-controls-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
