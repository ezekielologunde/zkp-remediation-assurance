"""Independent public fixture reconstruction; not a zkVM execution."""
import hashlib,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'data/proof-sandbox/trustbom-source'
def digest(x):return hashlib.sha256(x).digest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=SRC,text=True).strip()
    assert rev=='ea90058af5b137e0cdf6a4aa663bcc77040a928f'
    files=subprocess.check_output(['git','ls-files','-z'],cwd=SRC).decode().split('\0')
    hashes={p:sha(SRC/p) for p in files if p and (SRC/p).is_file()}
    defaults=[digest(bytes(32))]
    for _ in range(255):defaults.append(digest(defaults[-1]*2))
    rows=[];unique=set()
    for p in sorted((SRC/'proving-service/benchmark/data/merkleproofs').glob('*.json')):
        doc=json.loads(p.read_text());assert doc['depth']==256
        for proof in doc['merkle_proofs']:
            assert proof['value']=='0'
            index=bytes.fromhex(proof['leaf_index'].removeprefix('0x'))
            assert index==digest(proof['purl'].encode())
            bitmap=bytes.fromhex(proof['bitmap'].removeprefix('0x'));assert len(bitmap)==32
            siblings=[bytes.fromhex(s.removeprefix('0x')) for s in proof['siblings']]
            assert all(len(s)==32 for s in siblings)
            assert sum(bin(b).count('1') for b in bitmap)==len(siblings)
            current=defaults[0];pos=0;idx=int.from_bytes(index,'big')
            for d in range(256):
                if (bitmap[d//8]>>(d%8))&1:sib=siblings[pos];pos+=1
                else:sib=defaults[d]
                current=digest((sib+current) if (idx>>d)&1 else (current+sib))
            assert current.hex()==doc['root'],p.name
            unique.add(json.dumps(proof,sort_keys=True))
        rows.append(dict(file=p.relative_to(SRC).as_posix(),sha256=sha(p),proofs=len(doc['merkle_proofs']),all_roots_match=True))
    result=dict(source='https://github.com/tuberlin-blockchain-prototyping/sharing-sbom-system',revision=rev,license='Apache-2.0 root license',source_sha256=hashes,fixtures=rows,proof_records=sum(r['proofs'] for r in rows),unique_proof_records=len(unique),zkvm_executed=False,driver_sha256=sha(pathlib.Path(__file__)),plan_sha256=sha(ROOT/'protocol/trustbom-selection-v0.md'))
    (ROOT/'data/trustbom-fixture-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','fixtures']}))
if __name__=='__main__':main()
