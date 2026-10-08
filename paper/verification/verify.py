import pathlib,json,hashlib,re
P=pathlib.Path(__file__).resolve().parents[1];E=P/'verification/evidence';s=(P/'main.tex').read_text();checks=[]
def ck(name,condition):
 assert condition,name
 checks.append(name)
m=json.loads((P/'verification/input-manifest.json').read_text())
for f,h in m.items():ck('hash:'+f,hashlib.sha256((E/f).read_bytes()).hexdigest()==h)
def j(f):return json.loads((E/f).read_text())
a=j('analysis/repair-verification.json')['constraints'];coords=re.search(r'coordinates \{\(Original,(\d+)\) \(Alternative,(\d+)\)\}',s)
ck('figure coordinates',coords is not None and list(map(int,coords.groups()))==[a['original'],a['repair']])
for kind,file in [('original','original-inspect.log'),('repair','repair-inspect.log')]:
 log=(E/'analysis/repair-v1'/file).read_text();counts=[int(v) for v in re.findall(r'^(?:non-linear|linear) constraints: (\d+)',log,re.M)]
 ck('raw compiler count '+kind,len(counts)==2 and sum(counts)==a[kind])
ck('constraint percent',f"{100*(a['repair']-a['original'])/a['original']:.2f}" in s)
vs=j('analysis/verisbom-acceptance-v0/cases.json');vr=j('analysis/verisbom-repair-v0/cases.json')
for i,(u,v) in enumerate(zip(vs,vr)):
 row=('Original' if i<2 else 'Changed')+' & '+('Original' if i%2==0 else 'Changed')+' & '+('Accept' if u['application_accepted'] else 'Reject')+' & '+('Accept' if v['application_accepted'] else 'Reject')
 ck('VeriSBOM table '+str(i),row in s)
 for d,r in [('verisbom-acceptance-v0',u),('verisbom-repair-v0',v)]:
  log=(E/'analysis'/d/(r['case']+'.log')).read_text();ck(d+':'+r['case'],('VERIFICATION AND SBOM BINDING SUCCESSFUL' in log)==r['application_accepted'] and 'ZK Proof Math Valid' in log)
z=j('analysis/zksbom-cli-cases-v0/cases.json')
for label,r in zip(['Honest member','Honest nonmember','Wrong label','Missing label','Changed commitment','Empty file'],z):
 ck('zkSBOM table '+r['case'],label+' & '+('Valid' if r['proof_valid_message'] else 'Invalid')+' & '+str(r['exit_code']) in s)
 log=(E/'analysis/zksbom-cli-cases-v0'/(r['case']+'.log')).read_text();ck('zkSBOM log '+r['case'],('Proof is valid.' in log)==r['proof_valid_message'])
labels=re.findall(r'\\label\{([^}]+)\}',s);refs=re.findall(r'\\ref\{([^}]+)\}',s)
ck('unique labels',len(labels)==len(set(labels)));ck('references resolve',set(refs)<=set(labels))
bib=set(re.findall(r'\\bibitem\{([^}]+)\}',s));cites={v for c in re.findall(r'\\cite\{([^}]+)\}',s) for v in c.split(',')};ck('citations resolve',cites<=bib)
ck('two figure descriptions',s.count('\\Description{')==2 and s.count('\\begin{figure}')==2)
ck('three tables',s.count('\\begin{table}')+s.count('\\begin{table*}')==3)
ck('author',all(v in s for v in ['Ezekiel Ologunde','Independent Researcher','ologunde@bu.edu','\\country{USA}']))
ck('no em dash','\u2014' not in s and '---' not in s)
ck('ACM format','\\documentclass[sigconf,nonacm]{acmart}' in s)
result=dict(status='passed',check_count=len(checks),checks=checks,scope='Independent presentation and evidence consistency checks; not fresh proof reproduction or novelty verification')
(P/'verification/check-results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
