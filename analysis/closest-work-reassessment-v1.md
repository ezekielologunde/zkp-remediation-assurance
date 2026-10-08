# Closest-work reassessment, 2026-10-08

This is a targeted primary-source screen, not a systematic full-text review or novelty clearance.

| Source | Established scope | Implication for this study |
|---|---|---|
| Tang et al., Zero-Knowledge Proof Vulnerability Analysis and Security Auditing, ePrint 2024/514, https://eprint.iacr.org/2024/514 | Abstract explicitly covers layered auditing, application design flaws and primitive integration errors | Layered application-to-proof auditing is not itself a new idea. Full-text comparison remains necessary. |
| zkFuzz, IEEE S&P 2026, author publication page https://www.cs.columbia.edu/~junfeng/papers/zkfuzz/ | Trace-Constraint Consistency Test and mutation-guided circuit testing; author page reports 452 circuits | Do not claim circuit mutation or semantic inconsistency testing is new. Rust consumer metadata checks are outside the stated circuit target; this is scope, not a measured miss. Earlier preprint counts differ, so versions must not be mixed. |
| Picus official repository https://github.com/Veridise/Picus | Uniqueness/underconstraint checking for Circom, R1CS and gnark | No inference that it detects arbitrary consumer-side metadata use. No execution result claimed here. |
| Circomspect official repository https://github.com/trailofbits/circomspect | Circom static analysis | Earlier local runs are reported separately. No explicit diagnosis in those runs does not establish general inferiority. |
| ERC-8262 draft https://eips.ethereum.org/EIPS/eip-8262 | Explicit public-input and proof-result validation requirements, including external context | Current draft engineering guidance overlaps strongly with expected-context binding. Not an accepted standard or peer-reviewed efficacy study. |

## Decision

Reject the broad novelty claim that proofs must be linked to application expectations. Retain the narrower contribution candidate: reproducible statement-to-consumer discrepancy evidence across selected attestation/SBOM artifacts, with unchanged-proof controls and explicit repairs. Whether this is sufficient for a journal is unresolved. The ordinary authenticated-output comparator already detects the VeriSBOM discrepancy; presenting it as an advanced novel algorithm would be misleading.

## Next evidence requirement

Complete zkSBOM disposition, trace each claimed obligation to its source/paper, and compare any proposed automation with the ordinary manual/equality baseline under the same information. Do not write an affirmative novelty conclusion from search results alone.
