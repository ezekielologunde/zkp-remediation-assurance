# TrustBOM real-receipt reproduction

## Result and limits

A real RISC Zero receipt was generated and verified locally for the public two-entry TrustBOM fixture. Developer mode was disabled and the probe explicitly rejected Fake receipts. This establishes executable feasibility for a second independent artifact. It does not establish a vulnerability, a novel method, production assurance, or journal readiness.

Source: https://github.com/tuberlin-blockchain-prototyping/sharing-sbom-system at ea90058af5b137e0cdf6a4aa663bcc77040a928f. The upstream guest was unchanged; an added CLI probe supplied the fixture and checked the receipt. No live service, blockchain, or HPC job was used.

| Check | Observed outcome |
|---|---|
| Real receipt verifies against compiled expected program ID | Pass |
| Journal root equals fixture root | Pass |
| Journal policy digest equals independently computed ordered purl-list digest | Pass |
| Compliance result for supplied fixture | True |
| Wrong program ID | Rejected |
| Altered journal | Rejected |
| Independent evidence hashes | 49 passed: 6 manifest, 40 frozen inputs, 3 generated files |

The Python verifier checks provenance and recorded assertions independently of the runner. Cryptographic verification is performed by the frozen Rust probe using RISC Zero, not by an independently implemented proof verifier. The single positive fixture does not establish general correctness.

## Preserved failures and resource amendments

The Windows bind-mounted build was manually stopped for poor build throughput. Two Linux-volume attempts failed compiler discovery before proving. The successful attempt used a regular versioned compiler directory because rzup excludes symlink directories. These failures remain under analysis/trustbom-receipt-v0 and analysis/trustbom-receipt-linux-v1/v2.

The final run exited 0 after 636.53 seconds including compilation. It began at four CPUs and 6 GiB, then changed to 12 GiB and eight CPUs during execution. Therefore this duration is a run record, not a performance estimate. The container was removed on completion. The proof receipt is 725293 bytes with SHA-256 71be596f93f04ec16f120eb6d52e79c013557e55409d2ff46440769522582fbb. Generated proof and downloaded dependencies remain in the ignored sandbox; hashes and reproduction code are tracked.

## Research decision

Proceed with a bounded statement-contract comparison, not a new cryptographic protocol claim. PIRANHAS and TrustBOM support different statements and must not be ranked as interchangeable proof systems. Define artifact-specific expected program, root, policy and caller responsibilities before evaluating any mismatch. Compare an ordinary signed-manifest/application wrapper with equivalent trust assumptions. The observed Circom/Noir difference remains a benchmark-specific finding until its intended contract is established.

The next study gate is evidence that a contract-aware audit reveals a meaningful issue not already covered by known constraint and mutation testing. A successful second reproduction clears the execution gate only. Retain the option to conclude that the candidate contribution is insufficient.

Evidence: trustbom-receipt-linux-v3/{freeze,receipt,manifest}.json, execution.log, resource-amendment.json, cpu-amendment.json, and trustbom-receipt-verification.json. Reproduce with src/run_trustbom_registered_copy.py and verify with src/verify_trustbom_receipt.py following REPRODUCE.md.
