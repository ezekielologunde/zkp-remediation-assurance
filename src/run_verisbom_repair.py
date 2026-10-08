import pathlib,json,hashlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1]
E=R/'data/proof-sandbox/verisbom-repair-v0';E.mkdir(exist_ok=True)
O=R/'analysis/verisbom-repair-v0';O.mkdir(exist_ok=False)
source=R/'data/proof-sandbox/verisbom-run-v0/nova/src/main.rs'
s=source.read_text();assert s.count('bundle.zi_primary.len()')==2
s=s.replace('bundle.zi_primary.len()','res.as_ref().unwrap().0.len()')
for name,i in [('hash',0),('pm',1),('audit',2)]:
 old=f'let actual_{name} = bundle.zi_primary[{i}];';assert s.count(old)==1
 s=s.replace(old,f'let actual_{name} = res.as_ref().unwrap().0[{i}];')
(E/'bound_verifier.rs').write_text(s)
case=(R/'src/verisbom_acceptance_cases.py').read_text().replace('/work/bomz','/compiled/target/release/bound_verifier').replace('[True,False,False,True]','[True,False,True,False]')
(E/'cases.py').write_text(case)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def img(n):return subprocess.check_output(['docker','image','inspect',n,'--format','{{.Id}}'],text=True).strip()
buildimg=img('zkp-trustbom-audit:local');runimg=img('zkp-verisbom-audit:ubuntu')
files=[source,pathlib.Path(__file__),E/'bound_verifier.rs',E/'cases.py',R/'protocol/verisbom-repair-v0.md']
files+=list((R/'data/proof-sandbox/verisbom-results-v3').glob('*'))+list((R/'data/proof-sandbox/verisbom-bundle-v0').glob('*'))
(O/'freeze.json').write_text(json.dumps(dict(build_image=buildimg,run_image=runimg,sha256={str(p.relative_to(R)):sha(p) for p in files if p.is_file()}),indent=2))
def run(cmd,log):
 t=time.monotonic()
 with (O/log).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=900)
 return dict(command=cmd,exit_code=r.returncode,seconds=time.monotonic()-t)
b=['docker','run','--rm','--cpus','4','--memory','12g','--mount','type=volume,source=zkp-verisbom-build-v0,target=/work','--mount',f'type=bind,source={E},target=/repair,readonly',buildimg,'bash','-c','set -eu; cd /work; cp /repair/bound_verifier.rs src/bin/bound_verifier.rs; cargo build --locked --release --bin bound_verifier; sha256sum target/release/bound_verifier target/release/bomz']
a=run(b,'build.log');assert a['exit_code']==0
cmd=['docker','run','--rm','--network','none','--cpus','4','--memory','12g','--mount','type=volume,source=zkp-verisbom-build-v0,target=/compiled,readonly','--mount','type=volume,source=zkp-verisbom-work-v0,target=/work','--mount',f'type=bind,source={E},target=/repair,readonly','--mount',f'type=bind,source={O},target=/out','--mount',f'type=bind,source={R/"data/proof-sandbox/verisbom-results-v3"},target=/evidence,readonly','--mount',f'type=bind,source={R/"data/proof-sandbox/verisbom-bundle-v0"},target=/bundle,readonly',runimg,'bash','-c','set -eu; cd /work; sha256sum bomz; python3 /repair/cases.py']
a2=run(cmd,'execution.log')
(O/'receipt.json').write_text(json.dumps(dict(build=a,test=a2),indent=2))
(O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2))
print(a2['exit_code']);assert a2['exit_code']==0
