# Bounded artifact feasibility plan

This is an artifact-selection and protocol design plan. No cryptographic experiment has run, and it is not a preregistration of a novel method's superiority.

## First decision

Within one artifact-feasibility stage, establish whether the intended semantic claim can be tested with real public proof outputs. Begin with the pinned zkSBOM source; assess PIRANHAS and one independent SBOM proof system for usable source, license, statement, and build instructions. Do not download all submodules indiscriminately. Do not conflate the zkSBOM Merkle-tree modes with its ordered zero-knowledge-set mode.

Use minimal official examples to reproduce each backend before adapting an application wrapper. Record build failures, unimplemented relations, supported platforms, versions, and deviations. If fewer than two independent applicable implementations are reproducible, do not claim a cross-system empirical result; reassess scope before large implementation work.

## Candidate hypotheses, pending executable adapters

- H1: Given authentic proof evidence, accepting a prover-selected root or version in place of an independently authorized expected value can change the relying party's all-assets/current-policy conclusion. This is a known composition risk; observing it in a toy implementation does not establish novelty.
- H2: For systems with an explicit fleet-wide operational contract, a reproducible mismatch between the contract and actual acceptance behavior persists under fair recommended configurations. This is the possible empirical contribution and is currently untested.
- H3: A private scope-bound implementation provides the same intended acceptance semantics as a disclosed authenticated manifest, with a measured privacy/cost tradeoff. A simple wrapper achieving this may be engineering, not a novel protocol.

## Required baselines

1. Disclosed authenticated scope plus measurement manifest with exact identity/incarnation matching, current policy/feed checks, nonce/domain binding, and anti-rollback state.
2. Each upstream proof system under its actual documented statement and assumptions. Label unsupported fleet semantics as unsupported, not false acceptance.
3. The same backend with a standard application wrapper implementing all applicable checks. This is the strong composition baseline.
4. Only if separately justified, a proposed private design with identical trust, leakage accounting, and acceptance predicate. No advantage from weaker information or authority assumptions for competitors.

## Adversarial cases and positive controls

Omit a required asset; replace it with a different authorized device so counts still match; duplicate a device; reuse a device ID after replacement with a new incarnation; mix measurement epochs; use old scope with current nonce; use old policy or feed with current scope; transplant evidence to another verifier; reuse a consumed challenge; perform an unauthorized rollback; provide a fresh proof of an old measurement. Positive controls include unchanged valid scope, authorized join/leave, authorized rollback satisfying current policy, and evidence near window boundaries. Test trusted-authority incompleteness separately as an excluded-assumption control.

Each case needs an independent expected-result oracle derived from an authority/event ledger and each system's *own* supported contract. Freeze adapters, case definitions, exact inputs and seeds before collection. Include missing-evidence outcomes rather than collapsing them into compromise. Avoid independence claims for many mutations of the same source artifact.

## Public data and execution

The pinned zkSBOM repository includes public CycloneDX fixtures. They are suitable for parsing/build smoke tests, not independent fleet histories or ground truth of live deployments. Preserve provenance and audit their schema before use. Acquire separate public release/version inputs and a hashed, licensed vulnerability-feed snapshot only after defining the predicate. An openly generated lifecycle ledger can supply controlled joins/leaves and rollback ground truth; mark it synthetic and retain its generator.

Local CPU: source audit, formal statement checks, minimal proof generation, and parser tests. ASA-X: only after a representative proof has run, dependencies and CPU/GPU support are verified, and a prespecified scaling question requires larger resources. Current cluster access, queue limits, and memory availability have not been verified for this project. No HPC job is submitted by this plan.

Measure application-level incorrect acceptance/rejection, unsupported/insufficient-evidence results, prover/verifier time, peak memory, proof bytes, and exposed information. Cryptographic soundness is inherited only under the backend's stated assumptions and correct relation implementation; finite tests are not a soundness proof.

## Stop or advance

Stop the new-protocol route if standard binding checks suffice without a distinct result. Advance an empirical paper only if actual artifact evidence establishes a nontrivial, reproducible finding beyond acknowledged assumptions and existing collective-attestation analyses. Otherwise preserve the audit as engineering documentation and move on. A final manuscript is not a substitute for passing this decision.
