"""Pin acquired source without copying third-party code into the release."""
import hashlib
import json
import pathlib
import subprocess

root=pathlib.Path(__file__).resolve().parents[1]
source=root/'data/piranhas-source'
revision=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
assert revision=='62bd2af3b7501ab7458a682d8849206537a86d9e'
files=subprocess.check_output(['git','-C',str(source),'ls-files'],text=True).splitlines()
hashes={f:hashlib.sha256((source/f).read_bytes()).hexdigest() for f in files}
result=dict(source_url='https://github.com/AppliedCryptoGroup/piranhas',revision=revision,
            source_file_sha256=hashes,
            license_status='No repository-wide LICENSE found in reviewed root; vendored libraries have separate license files. Source and fixtures not redistributed.',
            scope='Static source inspection and separate local Circom interface pilot; no full swarm or Noir reproduction',
            public_interface_observations=dict(circom_attest=['enabled','pubX','pubY'],noir_single_device=['t','pk_x','pk_y']),
            limitation='Input declarations alone do not establish a flaw in a complete protocol or application wrapper')
(root/'data/piranhas-source-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(revision=revision,files_hashed=len(hashes),license=result['license_status'])))
