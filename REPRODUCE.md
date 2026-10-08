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

## Root-binding and Noir comparison

Use a separate reproduction workspace; the drivers deliberately refuse existing output directories. After the Circom setup above, install circomlibjs 0.1.7 into `data/proof-sandbox/mutation-runtime` using the archived lock in `analysis/root-binding-v0/package-lock.json`. Run `src/run_root_binding.py` and `src/verify_root_binding.py`. The latter checks local generated witnesses/proofs, so archived logs alone are insufficient.

For Noir, acquire these official binaries into `data/proof-sandbox/noir-runtime` as `nargo.tar.gz` and `bb.tar.gz`:

- https://github.com/noir-lang/noir/releases/download/v1.0.0-beta.3/nargo-x86_64-unknown-linux-gnu.tar.gz
- https://github.com/AztecProtocol/aztec-packages/releases/download/v0.82.0/barretenberg-amd64-linux.tar.gz

Clone https://github.com/noir-lang/schnorr.git into that directory's `schnorr` child and checkout `07ab027a52ea75a93f20bb849b6a1da93791d0a3`. Archive hashes are in `analysis/noir-comparison-v0/freeze.json`. Run `src/run_noir_comparison.py`, then `src/run_noir_proof_controls.py`. The latter intentionally preserves the original missing-curl environment failure. Its response/signature witness controls should reject.

To reproduce the exact environment history, build `analysis/noir-proof-amended-v0/Dockerfile` as `zkp-noir-audit:local`, then run `src/resume_noir_proof.py`. This records the missing-jq failure. Build `analysis/noir-proof-complete-v0/Dockerfile` as `zkp-noir-audit:complete` using that local parent, then run `src/complete_noir_proof.py`, `src/noir_field_control.py`, and `src/verify_backend_comparison.py`. The Dockerfiles install packages via apt, so rebuilt image IDs may differ; each run freezes its actual image ID and package versions. Native proof binaries are not redistributed. The first malformed-proof control may terminate abnormally and must not be labeled clean rejection. The field control checks exact serialization and should explicitly reject.

Noir drivers use local Linux containers, four CPUs and 4 GiB, with no exposed ports. Backend parameter downloads are allowed during key/proof generation; files under the dedicated sandbox HOME are hashed. These are functional controls, not performance estimates or a production deployment. A fresh proof can differ bytewise while satisfying the same semantic controls.

## TrustBOM selection

Clone https://github.com/tuberlin-blockchain-prototyping/sharing-sbom-system.git into `data/proof-sandbox/trustbom-source` and checkout `ea90058af5b137e0cdf6a4aa663bcc77040a928f`. Run `src/audit_trustbom.py` with Python 3.9 or newer. All seven fixture files should reconstruct their recorded Merkle roots: 387 records, 200 distinct proof records. This is independent SHA-256 path validation, not a RISC Zero proof reproduction. See `protocol/trustbom-selection-v0.md` for the remaining build and trust-boundary gates.

### TrustBOM receipt environment

The receipt pilot uses a sandbox CLI example, `src/trustbom_receipt_probe.rs`, while leaving the upstream guest unchanged. It rejects Fake receipts and checks independently expected image ID, root and ordered policy-list digest. Do not enable `RISC0_DEV_MODE` to work around a proving failure.

Official archive inputs, kept in `data/proof-sandbox/risc0-runtime`:

- `cargo-risczero.tgz`: https://github.com/risc0/risc0/releases/download/v3.0.3/cargo-risczero-x86_64-unknown-linux-gnu.tgz
- `rust-toolchain.tar.gz`: https://github.com/risc0/rust/releases/download/r0.1.88.0/rust-toolchain-x86_64-unknown-linux-gnu.tar.gz

Extract the first archive to obtain cargo-risczero and r0vm. Build `analysis/trustbom-build-v0/Dockerfile.direct` from that directory as `zkp-trustbom-audit:local`. The original Dockerfile's `cargo risczero install` command is deprecated and its failure is retained. The build helper uses rzup's directory discovery, so a rustup registration alone is insufficient. Its discovery also excludes a symlinked version directory. The final local runner copies the compiler to its versioned rzup directory without altering compiler bytes.

`src/run_trustbom_registered_copy.py` uses dedicated Linux volumes `zkp-trustbom-work-v1` and `zkp-trustbom-registry-v1`, which retain build and registry caches. Run in a fresh output workspace and use fresh volumes for a clean reproduction; existing volumes in this research session preserve the failed attempts. The earlier runners and receipts document the Windows bind-mount stop and compiler-discovery failures. The functional run began with four CPUs and 6 GiB, then was explicitly amended to eight CPUs and 12 GiB. Timestamps and commands are recorded in its resource-amendment and cpu-amendment receipts. This amended run is unsuitable as an unqualified performance measurement. Actual completion and semantic controls must be established from the final receipt and independently verified logs, not from the existence of a runner.

The completed v3 run and its checks are summarized in `analysis/trustbom-receipt-report.md`. Run `src/verify_trustbom_receipt.py` after reproduction; the local recorded run passes 49 hash comparisons and all six backend assertions.

### Saved-receipt contract controls
Run `src/run_contract_controls_online.py` in a fresh output workspace with the existing TrustBOM image and Linux volumes, then `src/verify_contract_controls.py`. This reuses the v3 saved receipt and verifies six adapter outcomes; it does not regenerate a proof or run the HTTP service. The v0 offline attempt failed due to an uncached git dependency. v1 failed before container startup due to a driver protocol-path error. v2 preserves the successful locked dependency build.

### Candidate repair and analyzer pilot

Read `protocol/repair-pilot-v0.md` before interpreting the alternative hash instantiation. With the existing Node runtimes, run `node src/generate_repair.cjs` to create the ignored repair-v0 sandbox. For the successful path, create repair-v1 and copy only the generated .circom and .json files from repair-v0 into it, without the build directories. Run `src/run_repair_pilot_v1.py`, `src/prove_repair.py`, then `src/complete_repair_control.py`. The proof driver preserves a post-verification hex-parsing failure; the final control handles both hexadecimal and decimal input representations. The historical v0 compiler-path failure is recorded separately. Run `src/verify_repair_evidence.py` against the full recorded history; a reproduction that omits the failed v0 attempt will not satisfy this history-specific checker. None of these drivers overwrite existing outputs.

For the analyzer, clone https://github.com/trailofbits/circomspect.git under data/proof-sandbox/circomspect-source and checkout 50010b623ed4f3bff9d1b0363cfe952385b47af3. `src/run_circomspect.py` builds in its dedicated Docker volume and preserves the unsupported --version failure. `src/complete_circomspect.py` uses the cached binary and records the actual analysis results. The pinned metadata version is 0.9.0. Both top-level files produce two informational findings and exit 1, which is not a build failure. Sandbox material remains ignored and original work unlicensed.

### Corpus expansion
Clone https://github.com/zero-savvy/zk-remote-attestation.git under data/proof-sandbox/zra-source and checkout 4a0416c614061753dcdfe7fc7494a4ba0d020afd. Run src/run_zra_controls.py then src/verify_zra_controls.py in a fresh output workspace. The driver uses shipped ra40 WASM/keys without changing source; a source build is not reproduced. src/run_zra_analyzer.py reuses the pinned Circomspect binary volume.

In the pinned zkSBOM checkout, initialize only zksbom-verifier/third_party/oZKS at the committed gitlink. No proof test is yet claimed. Run src/acquire_verisbom.py to checksum and selectively extract the Zenodo archive; do not run the hosted service. src/verify_corpus_expansion.py verifies the local source/archive evidence and ledger. The archive is approximately 507 MB and remains ignored.


## VeriSBOM binding experiment

See analysis/verisbom-output-binding-report.md and protocol/verisbom-*.md. Archived runtime inputs are hashed in data/verisbom-runtime-inputs.json. Runs are immutable and refuse reused output directories. Preserve the failed v0/v1/v2 runs and amendments; successful saved-proof verification is v3. src/run_verisbom_bundle_probe.py builds the direct authenticated-output probe; src/run_verisbom_acceptance.py runs four unchanged-CLI cases; src/run_verisbom_repair.py generates the minimal comparator and repeats those cases. All require the locally prepared Docker images and volumes documented in their frozen commands, plus separately acquired third-party inputs. This is not a one-command clean-machine reproduction. src/verify_verisbom.py checks saved run hashes, archived input hashes, proof-core byte identity, expected output fields and all eight log/exit-code results without generating another proof. Verification passed 465 hash checks.
