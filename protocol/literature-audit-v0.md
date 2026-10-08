# Primary-source overlap audit

Reviewed 2026-10-07. Targeted search, not exhaustive novelty clearance. Preprints are identified as such; publication and author performance claims have not been independently reproduced.

| Source | Evidence inspected | Existing coverage and consequence |
|---|---|---|
| [TrustBOM, September 2026 preprint](https://arxiv.org/html/2609.21419v1) | Architecture; sections 7.1-7.2 | Private vulnerability/license checks; accurate SBOM input is assumed. Runtime attestation is explicitly suggested as future work. Neither private compliance nor adding runtime linkage is enough to claim novelty. |
| [VeriSBOM, February 2026 preprint](https://arxiv.org/html/2602.13682v1) | Trust assumptions; sections 7.4-7.5 | Committed package/policy evidence and proof aggregation. It explicitly discusses older commitment versions and assumes correct, complete SBOM input. Stale-root acceptance and SBOM incompleteness are already recognized issues, not newly discovered here. |
| [zkSBOM, May 2026 preprint](https://arxiv.org/html/2605.00076v1) | Sections 5.1-5.2; public verifier interface | Confidential set queries, leakage analysis, and an honest-SBOM supplier assumption. Query privacy does not establish inventory truth. Code acquisition and static inspection are separate from running its cryptographic backend. |
| [PIRANHAS, NDSS 2026](https://www.ndss-symposium.org/wp-content/uploads/2026-f526-paper.pdf) | Introduction; section IV, especially PDF p. 8 | Anonymous dynamic-swarm attestation, distinct-device tags, and aggregation are covered. It explicitly allows omitted honest reports to reduce the attested count. We must not claim duplicate prevention or dynamic anonymous fleets as new. An exact externally authorized scope is an application requirement requiring a careful comparison, not evidence that PIRANHAS is broken. |
| [On the Design and Security of Collective Remote Attestation Protocols, 2024 preprint](https://arxiv.org/html/2407.09203v1) | Sections 6.3-6.4 and appendix C.1 | Group semantics, synchronous versus asynchronous correctness, and absent contributor information are explicitly analyzed. We cannot present the distinction between a reported subset and intended group as a new conceptual discovery. |
| [RATS architecture, RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html) | Section 10 | Freshness must cover evidence and appraisal context; timestamps, challenges and epochs are established options. An unavoidable post-check race is acknowledged. A nonce alone does not prove a fresh underlying measurement. |
| [ZKASP, NIST-hosted author manuscript](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=932897) | Abstract and freshness discussion | Private software-possession attestation and fresh randomness already exist. Possession, deployed-state measurement, and continuous runtime integrity must not be conflated. |

Additional primary sources located for subsequent full-text assessment: [zRA, NDSS 2024](https://www.ndss-symposium.org/wp-content/uploads/2024-815-paper.pdf), [ZEKRO](https://ubitech.eu/wp-content/uploads/ZEKRO-Zero-Knowledge-Proof-of-Integrity-Conformance.pdf), and [ZKSA publisher abstract](https://www.sciencedirect.com/science/article/abs/pii/S0167404824004413). Their titles or abstracts are leads, not sufficient grounds for detailed exclusion claims.

## Decision at this stage

**No-go for the generic new-protocol claim. Conditional go for a bounded cross-artifact composition audit.** The entire area is not closed, but there is currently no defensible claim that an inventory root plus epoch, nonce, policy digest, and ZKP is novel. The possible empirical contribution is a reproducible account of how implemented verifier boundaries preserve or lose intended scope/version semantics, using actual proof backends and fair strengthened baselines.

We need independent artifacts and failures not already explained by their stated assumptions before elevating that possibility to a paper. A limitation acknowledged by its authors is not a newly discovered vulnerability. A toy mutation matrix alone is not a publishable finding. Do not claim any published system is vulnerable from CLI inspection.
