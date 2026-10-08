# Five-paper corpus expansion: current evidence

## Decision and study limits

The extension adds a useful no-mismatch case, zRA. It does not yet establish a recurring failure pattern or a novel detector. There are five screened papers, four previously located source repositories and one newly located archive candidate. Three systems have selected real-proof controls: PIRANHAS, TrustBOM and zRA. Only PIRANHAS currently has the observed benchmark-statement mismatch. The other two are not certified secure; they passed their limited tests. zkSBOM and VeriSBOM require further execution before they can enter an executable denominator.

Selection was frozen before this extension, after the earlier pilot results were known. This is a purposive exploratory sample, not a systematic review, independent random sample, or estimate of defect prevalence. zRA and PIRANHAS share explicit intellectual lineage; VeriSBOM also shares an author with that line. Multiple backends and mutations are not independent systems.

## zRA: selected controls pass

The official paper links https://github.com/zero-savvy/zk-remote-attestation. Revision 4a0416c614061753dcdfe7fc7494a4ba0d020afd is recorded with 162 file hashes. The shipped depth-40 WASM and key generated a fresh witness and proof. The proof verified. Each one-field mutation of root, devAddr and challenge rejected; changing response while retaining the root and path failed witness generation. Independent verification checks 9 manifest, 12 frozen, 7 generated and 162 source hashes (190 entries).

The visible circuit makes root, device address and challenge public. Source inspection of PublicAttestor shows owner-controlled root/challenge updates, root authorization, sender/address comparison and latest-challenge comparison before proof verification. This is an example of application checks complementing proof verification. Solidity was not deployed or executed. The public test-key provenance and source-to-shipped-binary correspondence were not independently established; no production trust or performance claim follows.

Pinned Circomspect analyzed the top-level zRA source and reported two informational field-arithmetic/comparison findings, the same categories seen in the PIRANHAS top-level analysis. This illustrates why warning count alone is not an application-contract oracle. It does not establish accuracy rates for the analyzer.

## zkSBOM: contract source assessed, execution pending

The pinned verifier distinguishes valid membership, valid non-membership and invalid proof. Its C++ wrapper uses QueryResult.verify(commitment) and extracts the query key. The Rust wrapper compares that key with the dependency-label hash when a label is present. Commitment authority remains a caller responsibility. Missing labels explicitly skip that label check; this is a source observation, not a demonstrated false acceptance.

The verifier's oZKS submodule was initialized at its recorded gitlink, 5a7d43d82742ca9917bc63ebd278476e239fb10e. The native stack requires Microsoft GSL, Flatbuffers, Poco and other dependencies plus a proof-producing example. This turn has not built it, generated an application proof, or run its cryptographic verifier. No build failure is claimed. Ordinary Merkle modes are excluded as substitutes for the oZKS claim. Static review also exposes edge cases worth testing, but they are not counted as findings without the applicable consumer contract and execution.

## VeriSBOM: acquisition correction

A targeted search located https://zenodo.org/records/21372814, titled VeriSBOM Artifact, with a 507,364,572-byte archive. The depositor is named VeriSBOM and the description matches the paper; individual author identity has not been independently authenticated. This corrects the earlier limited-search status. The public hosted service is not used for testing. Archive source inspection and local execution are separate gates.

## Contribution consequence

A promising question is whether a contract ledger detects implementation-to-paper mismatches that ordinary circuit checks do not express. The present evidence does not establish a new method, general superiority, or broad prevalence. It supports a reproducible pilot containing both a discrepancy and successful selected controls. Further work must execute the two pending artifact adapters and compare against specification-aware methods, not just linters. The corpus ledger retains exclusions and incomplete executions, so difficulty or a clean result cannot silently remove an artifact from the study.

Primary sources: [zRA paper](https://www.ndss-symposium.org/wp-content/uploads/2024-815-paper.pdf), [zkSBOM repository](https://github.com/chains-project/zkSBOM), [VeriSBOM paper](https://arxiv.org/html/2602.13682v1), and [VeriSBOM archive](https://zenodo.org/records/21372814). Detailed source/output provenance is in data/corpus-ledger-v0.json and the linked audit files. No paper acceptance, journal readiness or deployed vulnerability is claimed.

## Archive inspection update

VeriSBOM's archive checksum matched its Zenodo record. SHA-256 and hashes of selectively extracted source/text files are now recorded in data/verisbom-artifact-audit.json. User-study material was not analyzed. The source contains a Nova verifier with explicit expected package-manager root, auditor root and SBOM-hash parameters. An unresolved source-level question is whether the values compared with those expectations come from the cryptographic verifier's authenticated output or separately deserialized bundle metadata. This is a testable lead, not a verified vulnerability. No proof bundle has been generated or mutated here.

This changes the research priority: implement an honest local VeriSBOM example and trace the proof-output binding before spending resources on corpus-wide timing. Keep the source/archive identity caveat. The present expansion is complete as a five-paper screening pass, but executable coverage is still three systems and the generalization question remains open.
