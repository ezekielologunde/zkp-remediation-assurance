"""Run inside the isolated image. Extract archived client logic, not its UI runtime."""
import ast,base64,glob,hashlib,io,json,os,pathlib,shutil,subprocess,sys,time
from types import SimpleNamespace
out=pathlib.Path('/out'); work=pathlib.Path('/tmp/client-path');work.mkdir()
shutil.copy('/work/common.py',work/'common.py')
(work/'circuits').symlink_to('/work/circuits',target_is_directory=True)
sys.path.insert(0,str(work));os.chdir(work)
raw=pathlib.Path('/work/app.py').read_bytes();tree=ast.parse(raw)
helpers=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['get_root_hex','get_available_policies','hex_to_u64_arr_str']]
blocks=[n for n in tree.body if isinstance(n,ast.With) and any(isinstance(i.context_expr,ast.Name) and i.context_expr.id=='tab4' for i in n.items)]
assert len(helpers)==3 and len(blocks)==1
code=compile(ast.Module(body=helpers+blocks,type_ignores=[]),'/work/app.py','exec')
expected=json.loads(pathlib.Path('/evidence/expected.json').read_text())
probe=json.loads(pathlib.Path('/bundle/probe.json').read_text())
components=json.loads(pathlib.Path('/evidence/selected-sbom.json').read_text())
for c in components:c['type']='public'
class UI:
 def __init__(self,bundle):self.bundle=bundle;self.messages=[]
 def __enter__(self):return self
 def __exit__(self,*a):return False
 def file_uploader(self,*a,**k):return io.StringIO(json.dumps(self.bundle))
 def selectbox(self,label,options):return list(options)[0]
 def button(self,*a,**k):return True
 def status(self,*a,**k):return self
 def update(self,*a,**k):pass
 def __getattr__(self,name):
  assert name in ['header','info','success','write','error'],name
  return lambda message:self.messages.append(dict(kind=name,text=str(message)))
rows=[]
for variant,binary,pattern in [('original','/work/bomz',[True,False,False,True]),('bound','/compiled/target/release/bound_verifier',[True,False,True,False])]:
 for idx,name in enumerate(['original','expected_root_only','metadata_only','metadata_and_expected_root']):
  case=variant+'-'+name; commands=[]
  root=expected['root_pm'] if idx%2==0 else probe['changed_metadata'][1]
  (work/'tree_pm_test.json').write_text(json.dumps([[root]]))
  (work/'policy_audit_test.json').write_text(json.dumps([[expected['root_audit']]]))
  proof=pathlib.Path('/evidence/honest.proof.proof' if idx<2 else '/bundle/changed-metadata.proof').read_bytes()
  ui=UI(dict(components=components,zk_proofs={'audit':base64.b64encode(proof).decode()}))
  def run(cmd,**kwargs):
   r=subprocess.run(cmd,**kwargs)
   commands.append(dict(command=cmd,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr))
   return r
  env=dict(st=ui,tab4=ui,BASE_DIR=str(work),SESSION_ID='test',RUST_BIN=binary,
   os=os,json=json,glob=glob,time=time,subprocess=SimpleNamespace(run=run))
  exec(code,env)
  verdict=any(m['kind']=='success' and 'Verification Successful' in m['text'] for m in ui.messages)
  verified=[c for c in commands if c['command'][0]==binary]
  record=dict(variant=variant,case=name,success=verdict,expected_success=pattern[idx],
   computed_hash=env.get('expected_h_hex'),messages=ui.messages,commands=commands)
  (out/(case+'.json')).write_text(json.dumps(record,indent=2));rows.append(record)
  assert len(verified)==1 and 'ZK Proof Math Valid' in verified[0]['stdout']
  assert int(env['expected_h_hex'],16)==int(expected['expected_hash'],16)
  assert verdict==pattern[idx]
  if verdict:assert not any(m['kind']=='error' for m in ui.messages)
  print(case,verdict,flush=True)
(out/'result.json').write_text(json.dumps(dict(status='passed',cases=8,
 app_sha256=hashlib.sha256(raw).hexdigest(),block_lines=[blocks[0].lineno,blocks[0].end_lineno],
 scope='Unmodified extracted client block with test-double widgets, real hashing and proof verification; not full Streamlit/HTTP/browser execution'),indent=2))
