import pathlib,json,hashlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1];B=R/'data/proof-sandbox';S=B/'zra-source/benchmarking/ra40';D=B/'zra-controls-v0';O=R/'analysis/zra-controls-v0'
D.mkdir(exist_ok=False);O.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=list(S.iterdir())+[pathlib.Path(__file__),R/'protocol/zra-controls-v0.md',B/'package-lock.json']
(O/'freeze.json').write_text(json.dumps({str(p.relative_to(R)):sha(p) for p in files if p.is_file()},indent=2))
steps=[];status='incomplete'
def run(n,args):
 t=time.monotonic();p=subprocess.run(['node']+args,cwd=B,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=900);log=p.stdout+'\n'+p.stderr;(O/(n+'.log')).write_text(log,encoding='utf-8');steps.append(dict(name=n,code=p.returncode,command=['node']+args,seconds=time.monotonic()-t));print(n,p.returncode,flush=True);return p.returncode,log
try:
 assert run('witness',[str(S/'generate_witness.js'),str(S/'zRA.wasm'),str(S/'good_input.json'),str(D/'witness.wtns')])[0]==0
 cli='node_modules/snarkjs/build/cli.cjs'
 assert run('prove',[cli,'groth16','prove',str(S/'zRA.zkey'),str(D/'witness.wtns'),str(D/'proof.json'),str(D/'public.json')])[0]==0
 c,log=run('verify',[cli,'groth16','verify',str(S/'verification_key.json'),str(D/'public.json'),str(D/'proof.json')]);assert c==0 and 'OK!' in log
 x=json.loads((S/'good_input.json').read_text());pub=json.loads((D/'public.json').read_text())
 def n(v):return int(v,16) if str(v).startswith('0x') else int(v)
 assert pub==[str(n(x[k])) for k in ['root','devAddr','challenge']]
 for i,k in enumerate(['root','devAddr','challenge']):
  changed=pub[:];changed[i]=str(int(changed[i])+1);f=D/(k+'.json');f.write_text(json.dumps(changed))
  c,log=run('changed-'+k,[cli,'groth16','verify',str(S/'verification_key.json'),str(f),str(D/'proof.json')]);assert c!=0 and 'Invalid proof' in log
 x['response']=str(n(x['response'])+1);f=D/'changed-response.json';f.write_text(json.dumps(x))
 c,log=run('changed-response',[str(S/'generate_witness.js'),str(S/'zRA.wasm'),str(f),str(D/'changed.wtns')]);assert c!=0 and 'assert' in log.lower()
 status='complete'
finally:
 (O/'receipt.json').write_text(json.dumps(dict(status=status,steps=steps,generated_sha256={str(p.relative_to(R)):sha(p) for p in D.iterdir() if p.is_file()}),indent=2))
 (O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2))
