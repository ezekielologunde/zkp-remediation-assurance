"""Independent receipt, byte-hash and acceptance-log audit; not soundness proof."""
import hashlib
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
BOX=ROOT/'data/proof-sandbox'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    count=0;generated=0
    for foldername in ['piranhas-interface-pilot-v0','piranhas-setup-control-v0']:
        folder=ROOT/'analysis'/foldername
        for file,expected in json.loads((folder/'manifest.json').read_text()).items():
            assert sha(folder/file)==expected
            count+=1
        receipt=json.loads((folder/'receipt.json').read_text())
        for file,expected in receipt['generated_sha256'].items():
            assert sha(BOX/file)==expected
            generated+=1
    initial=ROOT/'analysis/piranhas-interface-pilot-v0'
    corrected=ROOT/'analysis/piranhas-setup-control-v0'
    assert 'WITNESS IS CORRECT' in (initial/'witness-check.log').read_text()
    assert 'OK!' in (initial/'verify-tampered-public-key.log').read_text()
    assert all(x==['0','1','0'] for x in json.loads((BOX/'build/vk.json').read_text())['IC'])
    assert 'OK!' in (corrected/'verify-original.log').read_text()
    assert 'OK!' in (corrected/'verify-identical-inputs.log').read_text()
    assert 'Invalid proof' in (corrected/'verify-changed-key.log').read_text()
    public=json.loads((BOX/'control/public.json').read_text())
    changed=json.loads((BOX/'control/changed-public.json').read_text())
    assert len(public)==3 and public[0]==changed[0] and public[2]==changed[2] and int(changed[1])==int(public[1])+1
    lines=(BOX/'build/attest.sym').read_text().splitlines()
    assert [s.split(',')[-1] for s in lines[:3]]==['main.enabled','main.pubX','main.pubY']
    for i in [2,3]:assert json.loads((BOX/'control/vk.json').read_text())['IC'][i]!=['0','1','0']
    first=json.loads((initial/'freeze.json').read_text())
    assert first['driver_sha256']==sha(ROOT/'src/run_interface_pilot.py')
    assert first['protocol_sha256']==sha(ROOT/'protocol/piranhas-interface-pilot-v0.md')
    for f,h in first['source_hashes'].items():assert sha(BOX/f)==h
    second=json.loads((corrected/'freeze.json').read_text())
    assert second['driver_sha256']==sha(ROOT/'src/run_setup_control.py')
    assert second['amendment_sha256']==sha(ROOT/'protocol/piranhas-setup-control-amendment.md')
    for f,h in second['inputs'].items():assert sha(BOX/f)==h
    result=dict(manifest_files_verified=count,generated_files_verified=generated,
                original_negative_control_failed=True,amended_negative_control_passed=True,
                public_signal_names=['enabled','pubX','pubY'],
                scope='Single-device Circom example and local test setup only. No swarm reproduction, application exploit, or cryptographic soundness claim.')
    (ROOT/'analysis/interface-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
