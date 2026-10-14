"""Package the reviewed October 14 revision without overwriting release v0.1."""
import hashlib,json,pathlib,shutil,subprocess,zipfile,sys
R=pathlib.Path(__file__).resolve().parents[1]; P=R/'paper'
revision=sys.argv[1] if len(sys.argv)>1 else 'v0.3'
assert revision in ['v0.2','v0.3']
D=R/('deliverables/binding-audit-'+revision); D.mkdir(exist_ok=False)
E=R/('data/proof-sandbox/paper-release-check-'+revision); E.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((P/'validation.json').read_text())
v.pop('clean_pdf_sha256',None)
v.update(status='release_validation_in_progress',source_sha256=sha(P/'main.tex'),
 pdf_sha256=sha(P/'build/main.pdf'),presentation_checks=93,
 visual_review='All six revised pages inspected on October 14; no observed clipping or collisions',
 warnings=['Underfull box diagnostics','Fontconfig default configuration and font-request diagnostics; visual rendering inspected'],
 clean_extraction='pending',replay='Eight fresh saved-proof verifications; original and bound patterns reproduced; not fresh proof generation',
 evidence_snapshot='Original evidence follows 70a6f01; additional dated replay identified by included manifest')
(P/'validation.json').write_text(json.dumps(v,indent=2))
name='statement_binding_audit'
shutil.copyfile(P/'main.tex',D/(name+'_acm.tex'))
shutil.copyfile(P/'build/main.pdf',D/(name+'_acm.pdf'))
def pack():
 with zipfile.ZipFile(D/(name+'_overleaf.zip'),'w',zipfile.ZIP_DEFLATED) as z:
  for f in [P/'main.tex',P/'README.md',P/'validation.json']+sorted((P/'verification').rglob('*')):
   if f.is_file(): z.write(f,f.relative_to(P).as_posix())
pack()
with zipfile.ZipFile(D/(name+'_overleaf.zip')) as z:z.extractall(E)
subprocess.run(['C:/Python314/python.exe',str(E/'verification/verify.py')],check=True)
subprocess.run(['C:/Python314/python.exe',str(R/'src/build_empirical_manuscript.py'),str(E)],check=True,stdout=subprocess.DEVNULL)
def text(p):
 return subprocess.check_output(['pdftotext','-layout',str(p),'-'],encoding='utf-8')
assert text(P/'build/main.pdf')==text(E/'build/main.pdf'),'Extracted PDF text mismatch'
v.update(status='passed_with_documented_limitations',clean_extraction='Passed: empty-directory build and exact pdftotext -layout comparison',
 extracted_pdf_sha256=sha(E/'build/main.pdf'))
(P/'validation.json').write_text(json.dumps(v,indent=2)); pack()
print(json.dumps(v,indent=2))
