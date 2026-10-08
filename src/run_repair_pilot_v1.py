import pathlib,json,hashlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1];B=R/'data/proof-sandbox';D=B/'repair-v1';O=R/'analysis/repair-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
O.mkdir(exist_ok=False);(D/'build').mkdir();(D/'baseline-build').mkdir()
inputs=[R/'protocol/repair-pilot-v0.md',R/'src/generate_repair.cjs',pathlib.Path(__file__),B/'package-lock.json']+list(D.glob('*.circom'))+list(D.glob('*.json'))
(O/'freeze.json').write_text(json.dumps({str(p.relative_to(R)):sha(p) for p in inputs},indent=2))
steps=[];status='incomplete'
def run(name,args):
 t=time.monotonic();x=subprocess.run(['node']+[str(B/a) if a.startswith('node_modules/') else a for a in args],cwd=D,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180);log=x.stdout+'\n'+x.stderr;(O/(name+'.log')).write_text(log,encoding='utf-8');steps.append(dict(name=name,code=x.returncode,seconds=time.monotonic()-t,command=['node']+[str(B/a) if a.startswith('node_modules/') else a for a in args]));print(name,x.returncode,flush=True);return x.returncode,log
try:
 for name,source,dest in [('original-inspect',str(B/'attest.circom'),'baseline-build'),('repair-inspect','attest.circom','build')]:
  assert run(name,['node_modules/circom2/cli.js',source,'--r1cs','--wasm','--sym','--inspect','-l',str(B/'node_modules'),'-o',dest])[0]==0
 for n in ['original','stale_root','recomputed_root','changed_key','changed_tag','changed_challenge','invalid_signature']:
  code,log=run(n+'-witness',['build/attest_js/generate_witness.js','build/attest_js/attest.wasm',''+n+'.json',''+n+'.wtns'])
  assert (code==0)==(n=='original')
  if code:assert 'assert failed' in log.lower()
 assert run('r1cs-check',['node_modules/snarkjs/build/cli.cjs','wtns','check','build/attest.r1cs','original.wtns'])[0]==0
 status='complete'
finally:
 (O/'receipt.json').write_text(json.dumps(dict(status=status,steps=steps,generated_sha256={str(p.relative_to(R)):sha(p) for p in D.rglob('*') if p.is_file()}),indent=2))
 (O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2))
