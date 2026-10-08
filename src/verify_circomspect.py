import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
result={}
for n in ['circomspect-v0','circomspect-v1']:
 O=R/'analysis'/n;m=json.loads((O/'manifest.json').read_text());f=json.loads((O/'freeze.json').read_text())
 for p,h in m.items():assert hashlib.sha256((O/p).read_bytes()).hexdigest()==h,p
 for p,h in f['sha256'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
 result[n]={'manifest_hashes':len(m),'frozen_hashes':len(f['sha256'])}
O=R/'analysis/circomspect-v1';issues={}
for n in ['original','repair']:
 data=json.loads((O/(n+'.sarif')).read_text());rs=data['runs'][0]['results']
 issues[n]=[dict(rule=x.get('ruleId'),level=x.get('level'),message=x['message'].get('text')) for x in rs]
 assert len(rs)==2 and {x['ruleId'] for x in rs}=={'CS0003','CS0004'}
 assert (O/(n+'.exit')).read_text().strip()=='1'
result['issues']=issues;result['status']='verified';result['scope']='Top-level Attest templates; informational findings, no whole-project or other-tool claim'
(R/'analysis/circomspect-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('22 hash checks and both SARIF results verified')
