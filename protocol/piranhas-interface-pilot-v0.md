# PIRANHAS example interface pilot

Frozen before compiling or executing the example. Scope: pinned artifact 62bd2af3b7501ab7458a682d8849206537a86d9e, circom/attest.circom. This is a single-device example, not swarm reproduction or a claim about the paper's security proof.

Static review shows the Circom example declares enabled, pubX, and pubY as public; challenge is private. The Noir single-device main also declares chall private, while exposing a tag. These facts motivate checking the boundary between proof validity and a relying party's expected challenge. They do not establish an exploit of a deployed integration.

Use unchanged Circom source and supplied input in an ignored local sandbox. Use pinned npm circom2 0.2.23, snarkjs 0.7.6, circomlib 2.0.5, with Node 24.15.0. This differs from the artifact's native compiler and unpinned npm installer. Record the actual Circom compiler version; no timing comparison to the paper is valid. Do not run broad installer scripts or fetch unrelated dependencies.

First compile R1CS, symbols and witness generator. Inspect the public signal layout and check the supplied witness against constraints. If either fails, retain the error and do not claim proof reproduction. If these succeed, create a local test-only Groth16 setup, generate a proof, and verify it. Test setup is not production-secure or a ceremony result.

Then verify the identical proof/public vector again under a changed *external request label*, with no altered cryptographic input. This is intentionally a boundary demonstration: unchanged mathematical inputs must give the same verifier answer. It cannot alone show a vulnerability in a system that binds or checks the request elsewhere. Include tampering with one actual public field as a rejection control. Do not attempt credential theft, remote endpoints, or any third-party deployment.

Retain source hashes, compiler/runtime versions, dependency lock, command exit codes, logs and hashes of generated artifacts. Do not redistribute upstream source or fixtures: no repository-wide PIRANHAS license was found in the inspected checkout, although vendored libraries have their own licenses. A future release of derived materials requires checking applicable permissions. Report compilation, witness satisfaction, proof verification, and application-level acceptance as distinct facts.
