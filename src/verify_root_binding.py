"""Independently check frozen inputs, logs, output hashes, and case isolation."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/root-binding-v0'
BOX=ROOT/'data/proof-sandbox/root-binding'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    counts={}
    for name,base in [('manifest',OUT),('freeze',ROOT)]:
        manifest=json.loads((OUT/(name+'.json')).read_text())
        for p,h in manifest.items():assert sha(base/p)==h,p
        counts[name]=len(manifest)
    receipt=json.loads((OUT/'receipt.json').read_text());assert receipt['status']=='complete'
    for p,h in receipt['generated_sha256'].items():assert sha(ROOT/p)==h,p
    counts['generated']=len(receipt['generated_sha256'])
    cases={n:json.loads((BOX/(n+'.json')).read_text()) for n in ['original','stale_root','recomputed_root','invalid_signature']}
    original=cases['original']
    diffs={n:sorted(k for k in original if original[k]!=v[k]) for n,v in cases.items()}
    assert diffs=={'original':[],'stale_root':['response'],'recomputed_root':['response','root'],'invalid_signature':['S']}
    for n in ['original','recomputed_root']:
        assert 'OK!' in (OUT/(n+'-verify.log')).read_text()
        assert 'WITNESS IS CORRECT' in (OUT/(n+'-check.log')).read_text()
    for n in ['stale_root','invalid_signature']:
        assert 'assert failed' in (OUT/(n+'-witness.log')).read_text().lower()
    a=json.loads((BOX/'original-public.json').read_text());b=json.loads((BOX/'recomputed_root-public.json').read_text())
    assert a==b==[str(int(original[k],0)) for k in ['enabled','pubX','pubY']]
    result=dict(status='verified',hash_counts=counts,changed_fields=diffs,accepted_public_vectors_identical=True,scope='Local benchmark circuit only')
    (ROOT/'analysis/root-binding-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
