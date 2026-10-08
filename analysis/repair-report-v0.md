# Candidate statement repair and baseline checks

## Outcome and limitations

A local candidate repair produces a verifying Groth16 proof. All six prespecified negative witness cases fail, and changing the public challenge invalidates the saved positive proof. This closes the tested acceptance discrepancy within a researcher-defined circuit. It is not a new cryptographic protocol, an upstream-approved patch, or a proof of privacy/security equivalence to PIRANHAS. Novelty remains unestablished.

The unmodified third-party checkout is preserved. Only a sandbox copy is transformed by src/generate_repair.cjs. Generated third-party-derived circuits, keys, proofs and fixtures remain ignored. The generator uses an explicitly public deterministic test signer and nonce, which are unsuitable for deployment.

## Implemented relation

The candidate retains the depth-20 Merkle and Schnorr components. It uses domain-separated Poseidon encodings for the challenge/response leaf, root/key signed message, and challenge/key tag. Challenge and tag are public, enabled is constrained to one, and the signed message is derived internally. Constants 101, 102 and 103 are local test encodings, not standardized parameter choices. The removed device-address leaf field and added key/tag relations mean this is a different intended relation, not an optimization preserving the original circuit's semantics.

The fixture generator independently checks the Schnorr group equation before circuit execution. This checks fixture consistency only. It does not certify the inherited signature implementation, subgroup handling, hiding/binding assumptions, side channels, or the full protocol.

| Case | Observed outcome |
|---|---|
| Honest candidate fixture | Witness and R1CS checks pass; real proof verifies |
| Changed response, stale root | Witness rejected |
| Changed response, recomputed root, old signature | Witness rejected |
| Changed secret key | Witness rejected |
| Changed public tag | Witness rejected |
| Changed challenge | Witness rejected |
| Changed signature scalar | Witness rejected |
| Original proof, changed public challenge | Verifier rejects |

Negative witness outcomes are not counted as proof-verifier rejections. The public-challenge test independently maps the actual symbol table to the five public values before editing exactly one field.

## Circuit size

Compiler 2.2.3 with the same default optimization reports 16,743 original constraints and 17,954 candidate constraints, an increase of 1,211 (7.23%). This is a circuit-size observation, not a runtime overhead estimate or a comparison with Noir. Public inputs increase from three to five. Local test setup reused the previously contributed phase-one parameters and made a fresh phase-two contribution. This is not a production ceremony.

## Existing compiler baseline

Both sources compiled using the existing --inspect pass. Logs include missing pragma and component-signal warnings, including an unused enabled input in the inherited Schnorr template. The pass did not explicitly diagnose the root-to-signature application contract. This does not establish a general detection failure or superiority over a semantic analyzer. Circomspect is evaluated separately; no zkFuzz or formal-verification baseline is claimed here.

## Retained execution history

The initial fixture-generator syntax error occurred before producing inputs and was corrected before the frozen experiment. The v0 repair compile failed to write its output path. v1 used the circuit directory as cwd and compiled successfully. The positive proof run completed verification, then its public-field checker failed because it parsed a hexadecimal challenge as decimal. A separate frozen control corrected numeric parsing and verified public order before observing rejection. All experimental logs are retained. An initial analysis regex matched linear constraints inside non-linear constraints; it was corrected to anchor at line start before reporting the size comparison.

The independent evidence script checks 106 manifest/frozen/generated hash entries across four run folders, plus the changed public-vector hash, expected witness outcomes, positive proof log, rejection log and compiler counts. Cryptographic checks use snarkjs; this is not an independent cryptographic verifier implementation.

Reproduce using the frozen protocol, generator, run_repair_pilot_v1.py, prove_repair.py, complete_repair_control.py and verify_repair_evidence.py. The historical drivers refuse to overwrite evidence; use a fresh workspace and follow REPRODUCE.md for the v0-to-v1 sandbox copy and tool dependencies.

## Circomspect result

Official Trail of Bits source at 50010b623ed4f3bff9d1b0363cfe952385b47af3 built with its lockfile. Package metadata identifies version 0.9.0. Both top-level Attest files were analyzed with INFO reporting and the circomlib library path. Each returned two informational findings about field arithmetic/comparison in the tree loop (exit 1 because findings were reported). Neither output explicitly identifies the missing root/signature contract. Identical warning categories do not establish semantic equivalence. Included libraries inform analysis but are not separately selected as report targets in this run.

The initial build succeeded but the unsupported --version flag stopped the driver before analysis. The amended run reused the compiled binary, recorded its SHA-256, and completed both analyses. SARIF, logs, exit codes and hash checks are retained in circomspect-v0/v1 and circomspect-verification.json. This is one pinned static analyzer and a compiler inspection pass, not a zkFuzz comparison or a general false-negative rate. The official tool describes its supported passes at https://github.com/trailofbits/circomspect.

Decision: the candidate now has an observed counterexample, a tested bounded repair and limited baseline evidence. Do not infer novelty from this alone. A broader corpus and explicit application-statement specification are still needed; the control suite is a reproducibility artifact, not a new detector.
