"""Replay only the archived success expression over retained CLI logs."""
import ast,hashlib,json,pathlib,types
R=pathlib.Path(__file__).resolve().parents[1]
source=R/'data/proof-sandbox/verisbom-run-v0/app.py'
raw=source.read_bytes(); tree=ast.parse(raw)
assign=[n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='is_success' for t in n.targets)]
assert len(assign)==1
expr=assign[0].value
# Restrict this extracted expression to simple comparisons, names and attributes.
allowed=(ast.BoolOp,ast.And,ast.Compare,ast.Eq,ast.NotIn,ast.Attribute,ast.Name,ast.Load,ast.Constant)
assert all(isinstance(n,allowed) for n in ast.walk(expr))
code=compile(ast.Expression(expr),str(source),'eval')
branches=[n for n in ast.walk(tree) if isinstance(n,ast.If) and isinstance(n.test,ast.Name) and n.test.id=='is_success']
assert len(branches)==1
b=branches[0]
assert len(b.body)==1 and isinstance(b.body[0],ast.Expr)
call=b.body[0].value
assert isinstance(call,ast.Call) and isinstance(call.func,ast.Attribute) and call.func.attr=='success'
assert any(isinstance(n,ast.Name) and n.id=='wit_pm_root' for s in b.orelse for n in ast.walk(s))
results=[]
for name in ['original','bound']:
 folder=R/'analysis/verisbom-replay-2026-10-14'/name
 for row in json.loads((folder/'cases.json').read_text()):
  log=(folder/(row['case']+'.log')).read_text()
  outcome=eval(code,{'__builtins__':{}},{'res':types.SimpleNamespace(returncode=row['exit_code']),'out_text':log.lower()})
  assert outcome==row['application_accepted']
  results.append(dict(verifier=name,case=row['case'],client_success=outcome,exit_code=row['exit_code']))
result=dict(status='passed',source_sha256=hashlib.sha256(raw).hexdigest(),line=assign[0].lineno,
 expression=ast.unparse(expr),case_count=len(results),cases=results,
 scope='Exact success-expression replay over recorded CLI output, plus branch structure inspection. Not full web-app execution, root acquisition, upload handling or deployed exploit validation.')
(R/'analysis/verisbom-client-predicate-check.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
