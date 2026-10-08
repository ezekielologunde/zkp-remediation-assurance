import pathlib,json,hashlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1];B=R/'data/proof-sandbox';D=B/'repair-proof-v0';O=R/'analysis/repair-proof-control-v1';O.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[pathlib.Path(__file__),D/'public.json',D/'proof.json',D/'vk.json',B/'repair-v1/original.json',B/'repair-v1/build/attest.sym']
(O/'freeze.json').write_text(json.dumps({str(p.relative_to(R)):sha(p) for p in files},indent=2))
public=json.loads((D/'public.json').read_text());original=json.loads((B/'repair-v1/original.json').read_text());sym=(B/'repair-v1/build/attest.sym').read_text().splitlines()
names={int(x.split(',')[1]):x.split(',')[3].removeprefix('main.') for x in sym if 1<=int(x.split(',')[1])<=5}
assert set(names.values())=={'challenge','t','enabled','pubX','pubY'}
def num(s):return int(s,16) if s.startswith('0x') else int(s)
assert public==[str(num(original[names[i]])) for i in range(1,6)]
changed=public[:];idx=[names[i] for i in range(1,6)].index('challenge');changed[idx]=str(int(changed[idx])+1)
(D/'changed-public-v1.json').write_text(json.dumps(changed))
cmd=['node','node_modules/snarkjs/build/cli.cjs','groth16','verify','repair-proof-v0/vk.json','repair-proof-v0/changed-public-v1.json','repair-proof-v0/proof.json']
p=subprocess.run(cmd,cwd=B,capture_output=True,text=True,timeout=60);log=p.stdout+'\n'+p.stderr;(O/'verify.log').write_text(log)
assert p.returncode!=0 and 'Invalid proof' in log
(O/'receipt.json').write_text(json.dumps(dict(status='complete',command=cmd,exit_code=p.returncode,public_order=names,changed_index=idx,changed_public_sha256=sha(D/'changed-public-v1.json'),note='Previous driver parsed hex challenge as decimal after positive proof verification; proof unchanged.'),indent=2))
(O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2));print('challenge rejected')
