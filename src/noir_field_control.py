import hashlib,json,pathlib,subprocess,time,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
BOX=ROOT/'data/proof-sandbox/noir-runtime'
OUT=ROOT/'analysis/noir-field-control-v0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=False)
    original=BOX/'original/target/proof'
    fields=json.loads((BOX/'original/target/proof_fields.json').read_text())
    data=bytearray(original.read_bytes())
    assert len(data)==4+32*len(fields)
    assert int.from_bytes(data[:4],'big')==len(fields)
    assert all(int.from_bytes(data[4+i*32:4+(i+1)*32],'big')==int(f,16) for i,f in enumerate(fields))
    abi=json.loads((BOX/'original/target/attest.json').read_text())['abi']['parameters']
    assert [p['name'] for p in abi if p['visibility']=='public']==['t','pk_x','pk_y']
    text=(BOX/'original/Prover.toml').read_text()
    assert int(re.search(r'pk_x\s*=\s*"([^"]+)"',text)[1],0)==int(fields[1],16)
    data[36:68]=(int(fields[1],16)+1).to_bytes(32,'big')
    changed=BOX/'changed-field-proof';changed.write_bytes(data)
    image=json.loads((ROOT/'analysis/noir-proof-complete-v0/freeze.json').read_text())['image']
    freeze={p.relative_to(ROOT).as_posix():sha(p) for p in [original,BOX/'original/target/vk',BOX/'original/target/attest.json',BOX/'original/target/proof_fields.json',changed,pathlib.Path(__file__),ROOT/'protocol/noir-field-control-v0.md']}
    (OUT/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    cmd=['docker','run','--rm','--network','none','--cpus','4','--memory','4g','--env','HOME=/work/home','--mount',f'type=bind,source={BOX},target=/work','-w','/work',image,'/work/bin/bb','verify','-s','ultra_honk','-k','/work/original/target/vk','-p','/work/changed-field-proof']
    start=time.perf_counter();r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
    log=r.stdout+'\n'+r.stderr;(OUT/'verify.log').write_text(log)
    result=dict(exit_code=r.returncode,seconds=time.perf_counter()-start,command=cmd,serialization_fields=len(fields),same_length=len(data)==len(original.read_bytes()),log=log)
    (OUT/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in OUT.iterdir() if p.is_file()},indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
