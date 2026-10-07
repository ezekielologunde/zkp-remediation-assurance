# Private remediation assurance with ZKP

Status: Proposed. Historical candidate design, not a preregistration or proven novelty claim. Source: independent research portfolio dated 2026-10-04.

**Research question:** Can a verifier check that every asset in an agreed, committed scope met a stated remediation policy at a specified epoch, without learning sensitive component details, and detect replay, omitted assets and rollback?

**Existing coverage:** [TrustBOM](https://arxiv.org/html/2609.21419v1) already proves selected vulnerability or license absence while hiding dependency details. Its section 7.2 explicitly proposes connecting commitments to runtime deployment, so that direction is already articulated. [zkSBOM](https://github.com/chains-project/zkSBOM) supplies a concrete related prototype. [ZKASP](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=932897) addresses private software-possession attestation, and [RATS, RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html) addresses attestation architecture and freshness. Freshness alone is not novel.

**Proposed difference:** Specify and evaluate inventory coverage across change epochs, with rollback and omission adversarial tests. This is an applied protocol and evidence-model candidate, not a claim to invent a cryptographic primitive.

**Build and experiment:** Public inputs should bind an inventory commitment, policy version, vulnerability-feed snapshot, measurement epoch and verifier challenge. Private inputs contain the asset measurements and authenticated membership paths. Define who authorizes the inventory root and why the collector is trusted. Compare a disclosed signed inventory, a private snapshot proof, and the proposed epoch-aware protocol. Use independently generated histories containing omissions, repeated assets, old measurements, policy changes and rollbacks.

**Metrics:** Invalid-statement acceptance, valid-statement rejection, prover time, peak memory, proof size, verifier time and information revealed. Unit tests do not establish cryptographic soundness; use established proof systems and review the statement and threat model.

**Critical boundary:** A proof over a committed inventory cannot establish that the inventory includes every real asset. Continuous compliance between observations is also not established by two passing snapshots. External enrollment and measurement trust are indispensable. Stop if the claimed advance is merely TrustBOM plus a timestamp.
