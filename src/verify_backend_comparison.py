"""Verify saved receipts independently, including abnormal termination classification."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    counts={};results={}
    for run in ['noir-comparison-v0','noir-proof-controls-v0','noir-proof-amended-v0','noir-proof-complete-v0','noir-field-control-v0']:
        folder=ROOT/'analysis'/run
        manifest=json.loads((folder/'manifest.json').read_text())
        for p,h in manifest.items():assert sha(folder/p)==h,(run,p)
        frozen=json.loads((folder/'freeze.json').read_text());frozen=frozen.get('sha256',frozen)
        for p,h in frozen.items():assert sha(ROOT/p)==h,(run,p)
        receipt=json.loads((folder/'receipt.json').read_text())
        for p,h in receipt.get('generated_sha256',{}).items():assert sha(ROOT/p)==h,(run,p)
        counts[run]=dict(manifest=len(manifest),frozen=len(frozen),generated=len(receipt.get('generated_sha256',{})))
    assert 'witness successfully solved' in (ROOT/'analysis/noir-comparison-v0/execute-original.log').read_text()
    for case in ['response','signature']:
        log=(ROOT/f'analysis/noir-proof-controls-v0/{case}-witness.log').read_text()
        assert 'assert(valid_signature)' in log and 'Cannot satisfy constraint' in log
    good=ROOT/'analysis/noir-proof-complete-v0'
    assert 'Proof verified successfully' in (good/'verify-original.log').read_text()
    malformed=json.loads((good/'receipt.json').read_text())['steps'][-1]
    assert malformed['name']=='verify-tampered' and malformed['exit_code']==139
    field=json.loads((ROOT/'analysis/noir-field-control-v0/receipt.json').read_text())
    assert field['exit_code']==1 and 'Proof verification failed' in field['log'] and field['same_length']
    results=dict(status='verified',hash_counts=counts,original_noir_proof_verified=True,response_signature_controls='failed at signature assertion as expected',malformed_proof='abnormal termination exit 139, not clean rejection',public_key_mutation='explicit rejection exit 1',independent_research_systems=1,executed_backends=2)
    (ROOT/'analysis/backend-comparison-verification.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results))
if __name__=='__main__':main()
