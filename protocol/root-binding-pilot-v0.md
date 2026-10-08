# Root binding control, frozen before execution

Use the existing unchanged PIRANHAS Circom circuit and contributed local test key. No production system or remote verifier is involved. Evaluate four fixed cases: original; response plus one with old root; response plus one with recomputed Poseidon Merkle root and unchanged signature/message; signature S plus one with otherwise original input. Expected source-derived outcomes: accept, reject witness, accept, reject witness. These expectations are hypotheses, not results.

First independently recompute the original root with circomlibjs 0.1.7. Abort on mismatch. For each successful witness, check the unchanged R1CS, generate a real Groth16 proof, and verify. Require the same three public inputs for the two anticipated accepted cases. Preserve logs, commands, hashes, dependency lock, and failures. The witness generator rejecting an assertion is a different outcome from proof verification rejecting a proof.

This tests whether the benchmark relation authenticates its private root via the signature. It does not establish an attack on the complete published protocol, deployed fleet, Noir backend, or Plonky2 backend. Finite controls do not prove cryptographic soundness. Local test setup is not a production ceremony.
