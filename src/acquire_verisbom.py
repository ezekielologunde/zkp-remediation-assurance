import urllib.request,json,pathlib,hashlib,zipfile
R=pathlib.Path(__file__).resolve().parents[1];D=R/'data/proof-sandbox/verisbom-source';D.mkdir(exist_ok=True)
x=json.load(urllib.request.urlopen('https://zenodo.org/api/records/21372814',timeout=60));f=x['files'][0]
assert f['key']=='ase-artifact_new.zip' and f['checksum']=='md5:0cd5499573cb8877dac29bbbd9030a8d'
p=D/f['key']
if not p.exists():
 with urllib.request.urlopen(f['links']['self'],timeout=60) as a,p.open('wb') as b:
  while True:
   data=a.read(1024*1024)
   if not data:break
   b.write(data)
assert p.stat().st_size==f['size'] and hashlib.md5(p.read_bytes()).hexdigest()==f['checksum'].split(':')[1]
with zipfile.ZipFile(p) as z:
 for n in z.namelist():
  if not ('/Empirical/' in n or n.startswith('Empirical/') or n.lower().endswith('readme.md')):continue
  if pathlib.PurePosixPath(n).suffix.lower() not in ['.md','.py','.rs','.toml','.json','.circom','.txt','.sh','.lock']:continue
  if any(v in pathlib.PurePosixPath(n).parts for v in ['target','node_modules','.git','venv','.venv']):continue
  if z.getinfo(n).file_size>2000000:continue
  root=(D/'extracted').resolve();dest=(root/n).resolve();assert dest.is_relative_to(root)
  dest.parent.mkdir(parents=True,exist_ok=True);data=z.read(n)
  if dest.exists():assert dest.read_bytes()==data
  else:dest.write_bytes(data)
print('Archive checksum verified; selected source extracted without overwriting different files')
