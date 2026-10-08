# Initial ZKP assurance feasibility results

Date: 2026-10-07. Novelty remains unestablished. This report covers source review, public-data parsing, and a local single-device proof example, not a fleet-wide assurance system.

## Evidence obtained

The public zkSBOM checkout was pinned at 0bb63acc24f70e3480615696266963023b128275 and 246 files hashed. Three CycloneDX examples contain 522, 2308, and 4 top-level component records. The smallest lacks bom-ref fields; these fixtures cannot be assumed to supply identity-complete fleet ground truth. Its proof backend has not been built.

The PIRANHAS checkout was pinned at 62bd2af3b7501ab7458a682d8849206537a86d9e and 313 files hashed. Its unchanged single-device Circom example compiled to 16,743 constraints and three public inputs. The supplied witness satisfied the constraints. Compiler: Circom 2.2.3 from npm circom2 0.2.23, rather than a native 2.1.6-era compiler. Runtime: Node24.15.0, snarkjs0.7.6, circomlib2.0.5. These deviations preclude performance comparisons with the paper.

## Failed control and explicit amendment

The initial benchmark-style setup skipped contributions. Original verification and verification with a mutated public-key input both reported OK. The verification key contained four identity IC points. This run fails the basic negative control and supplies no usable evidence of public-input binding. Its logs and receipts are retained.

Before the second run, a written amendment added local Powers-of-Tau and zkey contributions using fresh entropy that was not stored. With that setup, the original proof verified, repeating identical proof/public inputs verified, and changing pubX caused rejection. The relevant verification-key points were nonidentity. This is still a local development setup, not a secure distributed ceremony or a cryptographic soundness proof. The contribution steps follow the [snarkjs setup guide](https://github.com/iden3/snarkjs#guide).

## Scope of the interface observation

The compiled public vector contains enabled, pubX, and pubY. The challenge is private in this example. The bare verifier is therefore not passed a verifier-selected challenge, scope root, policy version, or feed version. Changing an external request label while leaving every cryptographic input unchanged cannot change what it checks. This is an interface observation, not an attack on a complete implementation: an application might enforce additional bindings elsewhere, and its behavior has not been reproduced here.

The [PIRANHAS artifact](https://github.com/AppliedCryptoGroup/piranhas/tree/62bd2af3b7501ab7458a682d8849206537a86d9e) has several backends and aggregation variants. One Circom example is not a reproduction of its full anonymous swarm protocol. No cryptographic break, remote exploit, or new vulnerability is claimed. No author contact or disclosure message has been sent.

## Decision and next evidence

Continue only the bounded artifact audit. Reproduce a second relevant backend and trace expected-challenge/scope binding through the complete caller and verifier. Distinguish a documented benchmark simplification, a correctly handled application precondition, and an actual contract mismatch before treating this as a research finding. Any proposed remedy must beat or clarify a strong standard wrapper under the same trust assumptions. Do not begin an HPC sweep or manuscript on the strength of this pilot.

Public sources/fixtures and generated proof keys/witnesses stay in ignored local folders; release logs, hashes, protocols, original drivers, and dependency lock only. No repository-wide PIRANHAS license was found, so no source is repackaged. Original project work remains unlicensed. Repeating randomized setup yields different proof/key hashes; semantic outcomes, not identical random bytes, are the reproduction target.

## Receipt checks

Independently verified 27 archived manifest entries and 21 local generated-file hashes, source/driver inputs, public-signal order, and all positive/negative verification outcomes. These checks do not establish mathematical soundness.

| Run | Sum of recorded command seconds | Interpretation |
|---|---:|---|
| Initial | 49.161 | Negative control failed |
| Amended | 384.765 | Public-key rejection control passed |

These are one-off local timings including setup, not benchmark estimates or a backend comparison.
