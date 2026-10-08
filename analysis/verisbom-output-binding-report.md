# VeriSBOM local authenticated-output binding result

## Finding and scope

The archived VeriSBOM CLI accepts a package-manager root that differs from the root authenticated by its valid Nova proof when the bundle's separate `zi_primary[1]` metadata is changed to match that expected root. The serialized cryptographic proof bytes are unchanged. This is an application output-binding discrepancy in the pinned local CLI, not a Nova forgery, a hosted-service exploit, or proof of publishable novelty.

Artifact: Zenodo record https://zenodo.org/records/21372814, associated paper https://arxiv.org/html/2602.13682v1. Archive provenance and checksums are in `data/verisbom-artifact-audit.json`; the depositor uses the project alias VeriSBOM, so personal depositor identity is not independently authenticated. This study uses the archived source, not the current hosted application.

## Mechanism

`nova/src/main.rs` calls `bundle.proof.verify(...)` and checks success, but then compares the expected hash, PM root and auditor root with separately deserialized `bundle.zi_primary`. The successful verifier returns authenticated final outputs that are not used for these comparisons. Our probe verifies the original proof, confirms original metadata agrees with those outputs, increments only the auxiliary PM-root field by one, verifies again, and confirms identical authenticated outputs and identical serialized proof-core bytes.

An honest fixture contains one authorized package in the archived depth-10 circuit. Expected roots are computed before proof generation using the archived tree and hash helpers. This does not independently validate those helpers or real-world package authorization. The explicit one-package policy is synthetic. Archived circuit/public parameters are used; Rust code is built with the archived lockfile. No fresh circuit-to-binary or trusted-parameter derivation is claimed.

## Prespecified comparison

| Bundle metadata | Caller expected PM root | Archived CLI | Authenticated-output control |
|---|---|---|---|
| Original | Original | Accept | Accept |
| Original | Changed | Reject | Reject |
| Changed | Original | Reject | Accept |
| Changed | Changed | Accept | Reject |

The control uses the primary outputs returned by successful Nova verification for all three comparisons and output-length accesses. It ignores redundant auxiliary metadata. Therefore accepting metadata-only modification is correct: the proof still authenticates the original expected root. The two rows with changed expected root must reject. This is a diagnostic patch, not an upstream-supported or formally verified repair.

All cases use the same honest proof or its metadata-only serialization variant. No adversarial cryptographic proof is generated. The threat condition is an untrusted proof bundle supplied to this CLI; the caller's expected root remains an external trusted input for each test. Hosted routing, proof provenance restrictions, and other deployment preconditions were not exercised.

## Reproducibility and evidence

`analysis/verisbom-acceptance-v0/` preserves the unchanged CLI cases. `analysis/verisbom-repair-v0/` preserves the control's build, frozen inputs, binary hashes and cases. `analysis/verisbom-bundle-probe-v0/` records the direct Nova-output and proof-core comparison. `analysis/verisbom-verification.json` reports the independently parsed evidence checks. Raw proof bundles and third-party material remain ignored locally; generators, provenance and execution logs are tracked.

Environment history is retained: v0 lacked Python; v1 could not run the archived C++ helpers because of glibc/libstdc++ versions; Ubuntu 24.04 resolved those dependencies. Honest v2 generated and verified/compressed the proof but its driver requested the wrong output filename; v3 successfully verified the saved proof using the actual appended suffix. These failures are not negative cryptographic controls. The repaired comparator build has an unused-import warning. Runtime is not a benchmark.

## Contribution gate

Four of the five purposively selected systems now have executed proof controls; zkSBOM is still pending. PIRANHAS and VeriSBOM provide distinct local mismatch mechanisms, but share author lineage and cannot justify prevalence estimates. TrustBOM and zRA passed their selected controls, which is not comprehensive security assurance.

The empirical evidence is stronger than a source-only lead. It does not establish a new cryptographic method or a novel class of vulnerability. Before a manuscript is called publishable, the study still needs a defensible specification-aware audit contribution, closest-work comparison, explicit control coverage and the remaining corpus disposition. No hosted testing, author contact, public issue filing or journal submission occurred.
