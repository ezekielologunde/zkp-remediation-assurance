"""Evidence checks independent of the runner; backend verification is performed by the frozen Rust probe."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/trustbom-receipt-linux-v3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    for p,h in manifest.items():assert sha(OUT/p)==h,p
    frozen=json.loads((OUT/'freeze.json').read_text())['sha256']
    for p,h in frozen.items():assert sha(ROOT/p)==h,p
    receipt=json.loads((OUT/'receipt.json').read_text());assert receipt['status']=='complete' and receipt['exit_code']==0
    for p,h in receipt['generated_sha256'].items():assert sha(ROOT/p)==h,p
    lines=(OUT/'execution.log').read_text().splitlines()
    records=[json.loads(line) for line in lines if line.startswith('{') and 'real_receipt_verified' in line]
    assert len(records)==1
    record=records[0]
    for k in ['real_receipt_verified','wrong_image_rejected','altered_journal_rejected','root_matches','banned_list_matches','compliant']:assert record[k] is True,k
    saved=ROOT/'data/proof-sandbox/trustbom-linux-results-v3/audit-receipt.json'
    raw=json.loads(saved.read_text());assert 'Fake' not in raw['inner']
    result=dict(status='verified',manifest_entries=len(manifest),frozen_files=len(frozen),generated_files=len(receipt['generated_sha256']),backend_assertions=record,receipt_sha256=sha(saved),receipt_bytes=saved.stat().st_size,note='Frozen Rust probe performs cryptographic verification; this script independently checks provenance and recorded outcomes. Not a performance benchmark.')
    (ROOT/'analysis/trustbom-receipt-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
