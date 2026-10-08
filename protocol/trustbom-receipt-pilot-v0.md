# TrustBOM real receipt pilot

Use the smallest supplied batch (two records), unchanged guest and common code, and pinned source ea90058af5b137e0cdf6a4aa663bcc77040a928f. Add a CLI example only in a sandbox copy to exercise the same ExecutorEnv writes, default_prover, expected embedded image ID, and journal decoding as the original handler. Do not start an HTTP service or blockchain. Use locked dependencies, Rust 1.88, cargo-risczero/r0vm 3.0.3, and RISC Zero Rust r0.1.88.0. Record actual image ID and archive hashes.

Disable developer mode explicitly. Refuse Fake receipts. Positive control must verify against the independently built embedded guest ID. Decoded root and ordered banned-list digest must match the fixture-derived expected values. A copied receipt with altered journal byte and the same receipt under a changed image ID must both fail verification. No performance comparison from one run. Run within local container CPU/memory limits, retaining failed builds and dependency deviations.

This gate reproduces a statement, not a full-system exploit. Input-coverage and image-trust mutations come only after a successful positive control. Lack of a compiler or network resource is not a cryptographic failure and does not justify enabling developer mode.
