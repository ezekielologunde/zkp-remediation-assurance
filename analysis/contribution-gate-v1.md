# Contribution gate: statement contracts

## Decision

Continue the bounded empirical audit. Do not claim a novel method or draft a final journal paper yet. A benchmark-to-statement mismatch is now a concrete case-study lead, while TrustBOM supplies a successful independent receipt and consumer-contract control. It is not a second failure and must not be counted as one.

## Fair-comparison matrix

| Dimension | PIRANHAS Circom | PIRANHAS Noir | TrustBOM |
|---|---|---|---|
| Executed scope | Single-device benchmark | Single-device benchmark | Two-entry nonmembership fixture |
| Tree depth | 20 | 10 | 256 in audited fixtures |
| Main hash | Poseidon | Pedersen | SHA-256 |
| Public statement | enabled, pubX, pubY | t, pk_x, pk_y | Receipt program ID plus root/policy/compliance journal |
| Authentication connection | Separate private message and Merkle root | Signature over hash of derived root and secret key | Guest execution bound to program ID; journal bound to receipt |
| Controlled observation | Changed response/recomputed root accepted with original signature | Changed response rejected by signature check | Original receipt accepted; expected-value and journal changes rejected by local adapter |
| Unresolved boundary | Intended benchmark simplification versus omitted relation | Full caller handling of current challenge | Authority for expected image/root/policy in actual consumer |

These relations are not interchangeable. Differences in workload and semantics preclude attributing runtime differences solely to proving backends. Neither one positive TrustBOM fixture nor two PIRANHAS backends establishes prevalence across independent projects. Fixed cases do not support acceptance-rate estimates.

## Evidence strengthening

The [PIRANHAS paper](https://www.ndss-symposium.org/wp-content/uploads/2026-f526-paper.pdf), Section V.D and artifact appendix D/E, connects the Groth16 benchmark to a single-device performance claim. Section V.D describes signing individual device roots. The pinned Circom source instead feeds independent private root and message values into separate components. The prior real-proof mutation demonstrates the missing connection for that fixture. This is a source/specification alignment concern, not evidence that the formal scheme or an external deployment is broken. The appendix distinguishes single-device and recursive experiments; do not present all timings as the same task.

The new TrustBOM experiment reuses the verified non-Fake receipt with developer mode disabled. A local Rust adapter checks an expected image and compares decoded journal fields to independently computed fixture root and ordered-list hash. Original acceptance and five negative outcomes all matched the frozen expectations. This demonstrates the explicit contract on saved evidence. It does not execute the HTTP handler, establish an upstream vulnerability, or introduce a new defense. Initial offline dependency failure and a driver preflight path error are preserved before the successful v2 run.

Source hashes and line anchors: contract-source-map.json. Run evidence: contract-controls-v0, v1 and v2. Independent check: contract-controls-verification.json. Frozen protocol: ../protocol/contract-controls-v0.md.

## Formal relation mapping

Section III.B, PDF pages 5-6, specifies public key, challenge and linkage tag as the statement, with a signature binding accumulator and PRF key. The circuit entrypoints provide this concrete mapping:

| Obligation | Circom entrypoint | Noir entrypoint |
|---|---|---|
| Current challenge in public statement | Private input | Private input |
| Public linkage tag with key/challenge relation | Absent | Present as t |
| Signature binds accumulator and key | Independent message, connection absent | Derived auth_root includes root and k |

This mapping is source evidence. It does not demonstrate an end-to-end replay or establish whether another application layer compensates. A correct repair requires more than setting message equal to root. The initial formal-relation mapping is complete; full scheme equivalence and caller behavior remain unverified.

## Prior-work boundary

[zkFuzz](https://arxiv.org/html/2504.11961v3), Sections III and VIII, compares program execution semantics with constraints and already supports a language-independent consistency formulation. Its preliminary Noir support is an acknowledged limitation, not an unclaimed research space. Our changed Circom input passes both the original witness computation and its constraints; a contract mismatch need not be a trace/constraint inconsistency. This is a conceptual distinction, not evidence that zkFuzz would miss the artifact: no tool baseline has been executed.

[Circuzz](https://arxiv.org/abs/2411.02077) already studies metamorphic pipeline testing. [zk-Harness](https://github.com/zkCollective/zk-Harness) already provides standardized functional benchmarking. Therefore neither cross-backend testing nor benchmarking is a novelty claim. The remaining candidate is an empirical account of application-contract preservation and the consequences for reported comparisons. Its originality still requires a broader full-paper and artifact review.

## Next executable gate

1. Resolve the remaining caller and recursive-variant boundaries using the formal relation mapping above.
2. Freeze a minimally repaired sandbox Circom relation only after defining the correct signed payload and regenerating an honest matching fixture. Validate positive and negative controls before measuring cost. Do not force message=root if the formal scheme specifies another encoding.
3. Evaluate applicable existing analyzers against the same frozen source and bounded budgets. Report unsupported targets and timeouts; do not count them as missed bugs.
4. Expand the corpus using a published selection rule, including clean cases. Use an ordinary authenticated-manifest baseline with explicit signer trust and disclosure differences. Do not label it privacy-equivalent to a ZKP.

Stopping rule: if results remain a single known class of implementation omission without a new empirical insight, deliver a reproducibility/technical report rather than inventing a journal contribution. HPC scaling follows a validated question; it cannot supply novelty by itself.
