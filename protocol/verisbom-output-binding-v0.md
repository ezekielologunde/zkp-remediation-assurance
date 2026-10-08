# Prospective VeriSBOM output-binding check

Source: Zenodo 21372814; acquisition and file hashes in data/verisbom-artifact-audit.json. Project-alias depositor identity caveat applies. Run locally only, no hosted-service requests, transactions or accounts. No finding claimed from source inspection alone.

First generate a valid small example using the archive's documented package-manager/auditor/vendor sequence and verify against independently captured expected roots and hash. Establish circuit, parameter and proof provenance. Failure to reproduce is inconclusive.

Separate authenticated outputs returned by the Nova verifier from the ProofData bundle's additional zi_primary field. On the saved honest proof, evaluate unchanged evidence, changed expected root/hash only, changed auxiliary metadata only, and paired changed auxiliary metadata/expectation. Keep proof bytes and mathematical verification inputs unchanged for metadata tests. Freeze concrete values and runner before collection. This tests a local consumer binding boundary, not Nova cryptographic soundness. A matched metadata edit cannot establish a deployed attack without the real caller contract.

Control: compare expectations against the cryptographic verifier's returned output, using identical proof and expectations. Require honest acceptance and altered-value rejection. Do not report superiority over circuit analyzers for a Rust consumer-layer issue they do not target. Source review and this prospective plan are not execution results.
