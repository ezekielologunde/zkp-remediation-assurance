# Private remediation assurance with ZKP

**Status: literature and artifact feasibility assessment in progress.** The [primary-source review](protocol/literature-audit-v0.md) rejects the generic claim that combining ZKP, inventory commitments, and freshness is novel. A narrower empirical composition audit remains conditional, with a [threat model](protocol/threat-model-v0.md) and [bounded artifact plan](protocol/artifact-audit-plan-v0.md). No new protocol, fleet-wide assurance result, or publishable novelty has been demonstrated.

**Local proof milestone:** an unchanged PIRANHAS single-device Circom example compiled and produced a verifying proof. The initial test setup failed a public-key mutation control; an explicitly amended setup passed it. Both runs are preserved. [Feasibility results](analysis/feasibility-report-v0.md) and [independent receipt checks](analysis/interface-verification.json) report the three public inputs, dependency deviations, and limits. This does not reproduce the full swarm protocol or establish an application vulnerability.

**Backend comparison milestone:** real Circom and Noir proofs now verify locally. A fixed response/root mutation is accepted by the Circom benchmark with an unchanged signature, while the Noir response mutation fails at signature verification. [Comparison report](analysis/backend-comparison-v0.md) preserves environment failures, an abnormal malformed-proof termination, and the subsequent clean public-key rejection control. This is one artifact with two executed backends, not a cross-system result or novelty clearance.

The public zkSBOM source is pinned and 246 file hashes recorded. Three public CycloneDX fixtures were parsed, containing 522, 2,308, and 4 top-level component records. They are build/parser inputs, not fleet ground truth. [Reproduction instructions](REPRODUCE.md) and [source/data audit](data/public-fixture-audit.json) distinguish these checks from proof-system execution. The historical proposal below is retained for context.

[Research protocol and prior-art leads](protocol/research-plan.md). This plan comes from the October 4, 2026 independent research portfolio. Its literature assessment must be refreshed before implementation and submission.

**Second independent reproduction:** [TrustBOM real-receipt results](analysis/trustbom-receipt-report.md) now include a verified non-Fake RISC Zero receipt, two rejected negative controls and 49 successful evidence-hash checks. This clears a feasibility gate, not novelty or production validation.

[Statement-contract assessment](analysis/contribution-gate-v1.md): six TrustBOM adapter controls passed; cross-backend workload differences documented. No matched performance or new-method claim.

[Candidate repair and analyzer results](analysis/repair-report-v0.md): a repaired local statement passes its positive proof and rejects the specified controls. Circomspect and compiler inspection results are preserved. This is a bounded empirical pilot, not a new protocol or security certification.

[Five-paper corpus screening](analysis/corpus-expansion-v0.md) adds a zRA proof reproduction with passing selected controls and a newly located VeriSBOM archive. All five systems now have selected executed controls; coverage differs by system. No prevalence or novelty claim.

**VeriSBOM local binding result:** [Report](analysis/verisbom-output-binding-report.md). A metadata-only mutation makes the unchanged archived CLI accept an expected root different from the authenticated proof output. A comparator using authenticated outputs rejects it. Eight cases and 465 recorded hash checks passed. This is a local artifact finding, not a Nova break, hosted exploit or novelty clearance.

[zkSBOM verifier results](analysis/zksbom-execution-report.md): genuine native proofs and six Rust CLI cases reproduced. No new supported vulnerability claim. [Closest-work reassessment](analysis/closest-work-reassessment-v1.md) rejects a broad novelty claim for application-binding audits; a bounded empirical contribution remains under assessment.

## Research identity and publication route

Author: **Ezekiel Ologunde**. Affiliation: **Independent Researcher**, Boston, MA, USA, with no institutional affiliation. Author email: ologunde@bu.edu. No corresponding-author designation. Intended route: a suitable ACM journal, selected after assessing the completed contribution. No journal has accepted this work and no publisher metadata or DOI is assigned.

## Repository workflow

Keep research questions and hypotheses in `protocol/`; put code in `src/`, tests in `tests/`, and analyses in `analysis/`. Store redistributable datasets with provenance in `data/`, including source URL, retrieval date, version, license, SHA-256, schema, and role in the study. For restricted or large data, publish an acquisition script and manifest instead of copying files. Never commit credentials, private participant records, or copyrighted downloaded papers.

Freeze each experimental plan and code revision before collection. Retain failed and excluded runs with reasons. Publish analysis and result artifacts as work progresses. Keep manuscript drafts in `paper/`, clearly versioned; deposit the author-permitted final paper after journal-policy review. A planned experiment is not a result, and public code is not peer-reviewed acceptance.

Original work is intentionally unlicensed pending an author decision. Preserve applicable third-party notices. No dataset or final paper is claimed to exist merely because its directory is present.
