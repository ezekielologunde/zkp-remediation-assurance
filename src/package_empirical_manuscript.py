import pathlib,json,hashlib,shutil,zipfile,subprocess
R=pathlib.Path(__file__).resolve().parents[1];P=R/'paper';D=R/'deliverables/binding-audit-v0.1';D.mkdir(parents=True,exist_ok=True);name='statement_binding_audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=dict(status='draft_package_validation_in_progress',manuscript='Bounded empirical reproduction, no novel-method or publication claim',author='Ezekiel Ologunde, Independent Researcher, Boston, MA, USA, ologunde@bu.edu',compiler='Tectonic 0.17.0 (XeTeX)',builtin_compiler='Unavailable: Windows sandbox helper setup error before compilation',evidence_snapshot='70a6f01224c9bfd64cbca40d4049de82100414ba',source_sha256=sha(P/'main.tex'),pdf_sha256=sha(P/'build/main.pdf'),presentation_checks=json.loads((P/'verification/check-results.json').read_text())['check_count'],pages=6,tables=3,figures=2,visual_review='All six pages inspected; final diagram re-inspected at 150 dpi; no observed clipping or collisions',warnings=['Final-page overfull vbox 1.64198pt; visually inspected without clipped content','Underfull box diagnostics','Fontconfig default configuration warning and font-request diagnostics; Libertine and other used fonts embedded'],unverified=['Prior-art novelty and first-discovery status','Maintainer confirmation','Deployed-system exploitability','Fresh reproduction of all proof systems during packaging','Overleaf remote compiler'],clean_extraction='pending')
(P/'validation.json').write_text(json.dumps(v,indent=2))
shutil.copyfile(P/'main.tex',D/(name+'_acm.tex'));shutil.copyfile(P/'build/main.pdf',D/(name+'_acm.pdf'))
with zipfile.ZipFile(D/(name+'_overleaf.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for f in [P/'main.tex',P/'README.md',P/'validation.json']+sorted((P/'verification').rglob('*')):
  if f.is_file():z.write(f,f.relative_to(P).as_posix())
E=R/'data/proof-sandbox/paper-release-check-v1';E.mkdir(exist_ok=False)
with zipfile.ZipFile(D/(name+'_overleaf.zip')) as z:z.extractall(E)
print(E)
