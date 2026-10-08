# Threat model and statement boundary, v0

Date: 2026-10-07. Status: design for feasibility assessment, not a novel protocol or security proof.

## Question

Can an independently authorized fleet scope and its changes be bound to private software-policy evidence so that a relying party distinguishes a valid proof about reported assets from evidence covering every required asset incarnation under its current policy and vulnerability-feed snapshot?

The potential research output is an empirical study of composition errors and their costs across public artifacts. The generic construction below uses established commitments, authenticated statements, and zero-knowledge proofs; it is not proposed as a new cryptographic primitive.

## Parties and trust

- The scope authority enrolls and removes assets and authorizes a canonical inventory commitment for each epoch. It is independent of the potentially dishonest prover. Its signatures, enrollment process, and non-equivocation are trusted in the initial model.
- The measurement authority obtains authenticated software measurements bound to asset identity, incarnation, and measurement time. Its completeness and connection to deployed software must be established separately. A trustworthy signature does not make an incomplete SBOM complete.
- The policy/feed authority authenticates exact policy bytes and a frozen vulnerability-feed snapshot. Authenticity does not establish feed accuracy, exhaustiveness, or exploitability.
- The prover/aggregator may omit or duplicate assets, substitute an equally sized scope, mix epochs, reuse old statements, or withhold results. It cannot forge authority signatures, break the commitment/proof system, or read another asset's trusted attestation secrets.
- The verifier uses authenticated expected inputs and maintains challenge-consumption and latest-accepted-epoch state. The relying party must interpret its result with these explicit assumptions. A malicious verifier and adaptive query leakage are separate privacy tests, not automatically protected by a zero-knowledge proof.

A compromised scope or measurement authority is outside the first protection claim and must be included as a negative control: the system may accept an incomplete real-world inventory when the trusted authority signs it. No claim of discovering unregistered machines is permitted.

## Public contract and private witness

Proposed public contract: protocol/circuit version, authorized scope root and epoch, expected cardinality, policy digest, feed digest, measurement-window bounds, verifier/domain identifier, and single-use challenge. These must be authenticated or supplied independently by the verifier, not accepted solely because the prover included them in its proof.

Private witness: canonical asset/incarnation records, committed software measurements, component-level facts, membership paths, measurement endorsements, and policy evaluation witnesses. A real ZK backend must constrain these relations. Ordinary Merkle membership verification is not itself a zero-knowledge proof. Public commitments to low-entropy values require a privacy analysis and appropriate randomization; hashing alone is not a confidentiality guarantee.

The acceptance relation requires an exact one-to-one match between authorized asset incarnations and measured entries, not just equality of counts. Every entry must meet the bound policy against the bound feed, and have authorized measurement evidence in the stated window. The verifier must independently validate the expected root, versions, challenge, and domain, then atomically consume the challenge. An outer JSON timestamp or root that is not cryptographically bound cannot supply these guarantees.

## What acceptance means

All required asset incarnations were measured as satisfying the specified predicate at their respective authenticated measurement times within the accepted interval. This is an asynchronous bounded-evidence statement. It does not imply a simultaneous clean fleet at a common instant, uninterrupted compliance, absence of unknown vulnerabilities, or safety after verification. A synchronized snapshot would require additional collection semantics, as recognized in collective-attestation literature.

Rollback means a violation of current authorized state/policy, not simply a decrease in a version string. An explicitly authorized rollback that satisfies current policy must remain acceptable. Missing evidence means insufficient evidence, not proven compromise.

## Privacy accounting

Record disclosed scope size, roots, epochs, timestamps, query predicates, aggregate result, proof length, and timing. Assess cross-epoch linkability and adaptive queries separately from the backend's witness-hiding property. Do not claim zero leakage or hide necessary policy outputs by definition.

## Contribution gate

Implementation beyond a small artifact-reproduction audit requires either a reproducible, nontrivial cross-layer failure within a system's stated deployment contract, or a precise new method/bound not equivalent to existing binding and attestation practice. An expected rejection of a deliberately unbound toy verifier does not pass. If a routine signed manifest plus proper verifier checks provides equivalent assurance with comparable privacy/cost, report that and reject the new-protocol claim.
