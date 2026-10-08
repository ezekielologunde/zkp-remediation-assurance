# Reproduce the initial source/data audit

Use Python 3.10 or later. The source/data audits use the standard library only. A separate local Circom proof-interface pilot is described below; the zkSBOM backend itself has not been executed.

```powershell
git clone https://github.com/chains-project/zkSBOM.git data/zkSBOM-source
git -C data/zkSBOM-source checkout --detach 0bb63acc24f70e3480615696266963023b128275
python src/audit_public_fixture.py
```

Compare the resulting data/public-fixture-audit.json with the committed version. File hashes describe acquired working-tree bytes; Git line-ending settings can affect source-text hashes across platforms. Pin the revision and preserve line-ending configuration when requiring exact byte reproduction. JSON counts refer to the top-level components array, not a semantic validation of every CycloneDX field. No submodule is needed for this audit.

Upstream code and fixtures remain in an ignored checkout and are not redistributed. The upstream root LICENSE is MIT; preserve it and any component-specific notices if a later release includes third-party material. SBOM-listed package licenses describe those packages and are not a blanket grant for arbitrary data redistribution.

See protocol/threat-model-v0.md for the actual intended claim and protocol/artifact-audit-plan-v0.md for the next gate. Reproducing a parser result does not reproduce a cryptographic proof or establish a novel research contribution.

## Local PIRANHAS example

Use Node24.15.0. Acquire the pinned source separately; source and generated keys/witnesses are not shipped in this repository. In a separate reproduction checkout without archived output directories:

```powershell
git clone https://github.com/AppliedCryptoGroup/piranhas.git data/piranhas-source
git -C data/piranhas-source checkout --detach 62bd2af3b7501ab7458a682d8849206537a86d9e
python src/audit_piranhas_source.py
New-Item -ItemType Directory -Force data/proof-sandbox
Copy-Item data/proof-runtime-package.json data/proof-sandbox/package.json
Copy-Item analysis/piranhas-interface-pilot-v0/package-lock.json data/proof-sandbox/package-lock.json
npm ci --prefix data/proof-sandbox --ignore-scripts --no-audit --no-fund
```

The dependency lock above is part of the archived release. Preserve a copy before using a fresh reproduction checkout without run outputs. After installing, the two drivers are `python src/run_interface_pilot.py` and `python src/run_setup_control.py`. They refuse to overwrite their corresponding analysis output and sandbox build/control directories. The second requires the first's compiled circuit, witness, and initial setup. Use a separate checkout for recollection; do not delete the published evidence.

The first driver intentionally reproduces the setup sequence whose negative control failed. The second implements the documented amendment. Neither creates production-secure parameters. After both finish, run `python src/verify_interface_receipts.py` followed by `python src/report_interface_pilot.py`. The receipt verifier requires generated local binaries and will not fully run from the public logs alone. Random setup changes generated hashes on reproduction; each new manifest must verify its own bytes, while acceptance/control outcomes should agree.

Read analysis/feasibility-report-v0.md for the exact limits of this example. No swarm protocol, real device measurement, or deployed application vulnerability is reproduced.
