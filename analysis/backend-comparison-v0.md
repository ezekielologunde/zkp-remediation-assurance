# Local backend comparison: evidence and research decision

## Result and limits

Two PIRANHAS single-device implementations now have verified local proofs. The Circom benchmark accepts a changed response and a recomputed Merkle root while retaining the original signature, signature message, and public input vector. The Noir implementation rejects its response mutation at signature verification. This is an observed difference in relation enforcement, not a break of Groth16 or UltraHonk, and not proof of an attack on the complete PIRANHAS protocol or a deployed system.

The two implementations belong to one research artifact. We have not met the earlier gate of two independent applicable research systems. No novel cryptographic protocol, fleet-remediation result, or journal-ready contribution is claimed.

## Controlled results

| Implementation and case | Witness outcome | Proof outcome | Interpretation |
|---|---|---|---|
| Circom, original input | R1CS check passed | Verified | Positive control |
| Circom, response increased by one, original root | Assertion failed | Not attempted | Merkle relation enforced |
| Circom, changed response, recomputed root, original signature/message | R1CS check passed | Verified | Signature relation does not authenticate this private root |
| Circom, signature S increased by one | Assertion failed | Not attempted | Signature equation enforced separately |
| Noir, original input | Solved | Verified | Positive control |
| Noir, response increased by one | Signature assertion failed | Not attempted | Response/root/signature connection enforced for this case |
| Noir, first signature byte changed | Signature assertion failed | Not attempted | Signature negative control |
| Noir, valid serialization with public pk_x increased by one | Unchanged original witness | Explicit rejection, exit 1 | Public-input mutation control |
| Noir, first serialized byte toggled | Unchanged original witness | Abnormal termination, exit 139 | Not a clean cryptographic rejection; no broader availability claim |

These are fixed cases, not independent random samples. No acceptance-rate estimate or statistical significance is calculated. A witness rejection is not counted as a verifier rejection. No missing execution is treated as a pass.

## Why the comparison is meaningful, and where it stops

At pinned source revision `62bd2af3b7501ab7458a682d8849206537a86d9e`, `circom/attest.circom` supplies `root` to the Merkle component and an independent `message` to the Schnorr component. Its public vector contains enabled, pubX and pubY. The test independently reconstructed the original Poseidon root before making a controlled mutation, then checked the resulting witness against the unchanged R1CS and generated a real proof using the previously contributed local key. No signature was forged or regenerated. The independent verification script confirms that only response/root changed in the accepted mutation and both public vectors are identical.

In `noir/1-attest-(Pi-zkRA)/src/attest.nr`, the derived root and key are hashed into the message checked by the signature verifier. Both negative witness controls stop at `assert(valid_signature)` on line 81. The Noir ABI exposes t, pk_x and pk_y; challenge remains private. The public tag relation alone does not establish how a complete caller authenticates a current verifier challenge. That application-level question is still open.

Static review of the Plonky2 benchmark selected by `examples/benchmarks.sh` found an explicit unfinished-verification comment after computing `_e_v` in `examples/piranhas.rs`. This is a source-level lead only. Plonky2 was not executed, and its potential consequences are not included as an observed failure. The visible incompleteness also argues against describing every benchmark as a production implementation.

An outer wrapper checking an unbound JSON root is insufficient. Conversely, no claim is made that a correct circuit or a separately authenticated measurement statement would accept the mutation. We have not built or evaluated a repaired implementation, so there is no measured repair cost.

## Environment and retained failures

Circom used the existing compiler 2.2.3 build, snarkjs 0.7.6, circomlib 2.0.5, and circomlibjs 0.1.7 for independent root recomputation. This differs from the circuit's 2.1.6 pragma-era toolchain. The compiled relation and key were frozen by hash. The local trusted setup is not a production ceremony.

Noir used the documented nargo 1.0.0-beta.3 and bb 0.82.0 release binaries. The tagged schnorr dependency was pinned at `07ab027a52ea75a93f20bb849b6a1da93791d0a3`; only the dependency location was changed to a local path. Circuit source and original inputs were preserved. Linux containers were limited to four CPUs and 4 GiB on this PC. No ASA-X job ran and no service was exposed.

The first Noir proof attempt failed because curl was missing. The next failed because jq was missing. A derived container with curl, CA certificates, jq and gzip completed proof generation and verification. Both failures and both build attempts remain in the evidence. A first-byte corruption produced exit 139, prompting a separate frozen field-mutation control that preserved serialization and yielded explicit rejection. Do not interpret a receipt's `status: complete` as a claim that all malformed inputs were handled cleanly.

The valid serialized proof has 459 field elements and 14,692 bytes. Before modifying the public key, the driver checked every field against the exported field vector, the four-byte count, the ABI public order, and the original input key. Parameter files acquired by the backend were hashed. These are local measurements, not a comparative performance benchmark.

## Evidence

- `root-binding-v0/`: frozen plan and driver hashes, real proof logs, and case receipts.
- `root-binding-verification.json`: independent check of 14 manifest entries, 9 frozen inputs, and 10 generated-file hashes, plus changed-field isolation and public-vector equality.
- `noir-comparison-v0/`: original compilation and witness reproduction.
- `noir-proof-controls-v0/`: signature/response controls and initial missing-curl failure.
- `noir-proof-amended-v0/`: missing-jq failure.
- `noir-proof-complete-v0/`: verified original proof and abnormal malformed-proof termination.
- `noir-field-control-v0/`: explicit rejection of validly serialized public-key mutation.
- `backend-comparison-verification.json`: independent manifest, frozen-input, generated-file, and outcome checks across the five Noir runs.

Third-party source, inputs, binaries, proofs, and keys remain in the ignored sandbox; acquisition and hashes support reproduction without redistributing unlicensed source. No authors were contacted and no external issue or vulnerability report was submitted.

## Novelty and decision

Detecting missing circuit constraints is established work. Wen et al.'s [USENIX Security 2024 study](https://www.usenix.org/conference/usenixsecurity24/presentation/wen) describes circuit-dependence-based semantic detectors. [zkFuzz v3](https://arxiv.org/abs/2504.11961v3), revised May 2026, studies computation/constraint consistency and mutation-based testing. [Circuzz](https://arxiv.org/abs/2411.02077) uses metamorphic tests across ZK processing pipelines. These abstract-level comparisons are a screening step, not an exhaustive full-paper novelty review. We cannot claim novelty for mutation testing, differential testing, or finding an unbound relation in general.

The supported research lead is narrower: whether benchmark implementations advertised for the same application preserve the same authenticated statement, and how semantic differences affect the validity of performance comparisons. Our one-artifact observation motivates that question but does not answer its prevalence or establish a new method. Next evidence must include a prespecified cross-artifact selection rule, an independent statement oracle, stronger tool baselines, and reproducible artifacts from another research system. Do not inflate the sample by counting multiple backends of this repository as independent systems.

Decision: retain this as a substantive reproducible pilot; continue artifact selection and semantic-contract analysis. Do not launch an HPC scaling study or write a final journal manuscript yet. Correctness and novelty, rather than compute capacity, remain the gates.
