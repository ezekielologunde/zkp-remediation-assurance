# Common statement-to-verifier audit protocol v1

Date: 2026-10-08. Exploratory protocol written after observing PIRANHAS and VeriSBOM results. It is not a preregistration of those discoveries. No held-out accuracy or superiority claim is allowed from this development corpus.

## Research question

In the five selected software-attestation/SBOM artifacts, which application expectations are actually connected to authenticated proof statements, and which observed discrepancies survive explicit consumer-side binding controls?

For each obligation record: expected value and trusted origin; witness computation; authenticated public input/output; consumer comparison; acceptance decision; evidence path; execution coverage. Missing support is unknown, not a vulnerability. Separate cryptographic verification, statement matching, and application authorization.

## Common outcomes

- Verified match: cryptographic verification passes and authenticated statement matches the independent expected context.
- Verified mismatch: cryptographic verification passes, application accepts, but authenticated statement fails a documented required expectation.
- Correct rejection: changed expected context or bound field is rejected.
- Unsupported: application does not promise the proposed expectation, or execution was not performed.
- Invalid experiment: honest case or setup integrity fails. Preserve and exclude from substantive finding counts.

## Required paired controls

1. Honest positive case.
2. Alter only caller expectation, retaining proof.
3. Alter only unauthenticated metadata, retaining proof-core bytes where available.
4. Alter metadata and expectation together.
5. Compare with a minimal consumer using authenticated outputs or explicitly bound public inputs.
6. Include a correctly bound implementation. Never count harmless ignored metadata as a false acceptance.

These are a reusable experiment design, not a new cryptographic construction. Circuit relations may need different witness mutations; do not imply the same byte mutation applies to all systems.

## Baseline policy

Ordinary specification-guided manual review and an explicit authenticated-output equality check are mandatory strong baselines. Circomspect, Picus and zkFuzz address different circuit-level properties. Inapplicable Rust consumer code must be marked out of scope, not counted as an analyzer miss. No tool superiority claim without execution on supported inputs and equivalent specification access. A discovered consumer binding error that the ordinary comparator fixes is not evidence that a new detection algorithm is required.

## Publication gate

Current evidence can support bounded artifact reproduction and a documented audit dataset. Novel methodology requires demonstrable additional capability or rigor beyond known application-binding review. Five purposively selected systems, with shared author lineage, cannot estimate vulnerability prevalence. A fresh held-out corpus or independent evaluation would be needed for generalization claims. Report all exclusions, setup failures, unchanged proof identity, and diagnostic repair limitations.
