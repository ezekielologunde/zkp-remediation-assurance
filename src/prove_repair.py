import pathlib,hashlib,json,subprocess,secrets,time
R=pathlib.Path(__file__).resolve().parents[1];B=R/'data/proof-sandbox';D=B/'repair-proof-v0';O=R/'analysis/repair-proof-v0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
D.mkdir(exist_ok=False);O.mkdir(exist_ok=False)
files=[B/'repair-v1/build/attest.r1cs',B/'repair-v1/original.wtns',B/'control/final.ptau',R/'protocol/repair-pilot-v0.md',pathlib.Path(__file__)]
(O/'freeze.json').write_text(json.dumps({str(p.relative_to(R)):sha(p) for p in files},indent=2))
steps=[];status='incomplete'
def run(n,a,entropy=False):
 cmd=['node','node_modules/snarkjs/build/cli.cjs']+a;safe=cmd[:]
 if entropy:cmd+=['-e='+secrets.token_hex(32)];safe+=['-e=<not-recorded>']
 t=time.monotonic();p=subprocess.run(cmd,cwd=B,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=300);log=p.stdout+'\n'+p.stderr;(O/(n+'.log')).write_text(log);steps.append(dict(name=n,command=safe,code=p.returncode,seconds=time.monotonic()-t));print(n,p.returncode,flush=True);return p.returncode,log
try:
 assert run('setup',['groth16','setup','repair-v1/build/attest.r1cs','control/final.ptau','repair-proof-v0/initial.zkey'])[0]==0
 assert run('contribute',['zkey','contribute','repair-proof-v0/initial.zkey','repair-proof-v0/final.zkey','--name=local-repair-test'],True)[0]==0
 assert run('export',['zkey','export','verificationkey','repair-proof-v0/final.zkey','repair-proof-v0/vk.json'])[0]==0
 assert run('prove',['groth16','prove','repair-proof-v0/final.zkey','repair-v1/original.wtns','repair-proof-v0/proof.json','repair-proof-v0/public.json'])[0]==0
 a=['groth16','verify','repair-proof-v0/vk.json','repair-proof-v0/public.json','repair-proof-v0/proof.json']
 code,log=run('verify',a);assert code==0 and 'OK!' in log
 public=json.loads((D/'public.json').read_text());original=json.loads((B/'repair-v1/original.json').read_text())
 # Circom order follows declaration order, verified against the actual symbol file.
 sym=(B/'repair-v1/build/attest.sym').read_text().splitlines()
 names={int(x.split(',')[1]):x.split(',')[3].removeprefix('main.') for x in sym if 1<=int(x.split(',')[1])<=5}
 assert set(names.values())=={'challenge','t','enabled','pubX','pubY'}
 assert public==[str(int(original[names[i]])) for i in range(1,6)]
 changed=public[:];idx=[names[i] for i in range(1,6)].index('challenge');changed[idx]=str(int(changed[idx])+1)
 (D/'changed-public.json').write_text(json.dumps(changed));a[3]='repair-proof-v0/changed-public.json';code,log=run('changed-challenge',a);assert code!=0 and 'Invalid proof' in log
 (O/'public-order.json').write_text(json.dumps(names,indent=2));status='complete'
finally:
 (O/'receipt.json').write_text(json.dumps(dict(status=status,steps=steps,generated_sha256={str(p.relative_to(R)):sha(p) for p in D.iterdir() if p.is_file()}),indent=2))
 (O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2))
