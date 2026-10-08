# Noir proof controls, frozen after successful baseline witness

The unchanged single-device Noir example compiled and solved its original witness. Proceed with its documented bb 0.82.0 UltraHonk options. A dedicated sandbox HOME permits backend CRS acquisition if needed; record its hashes and console output. Four CPU and 4 GiB container limits remain. No service ports are exposed.

Copy the original sandbox program into separate case directories. Change only rsp by plus one, then only the first signature byte by one modulo 256. Expected: both witness computations fail assertions. Verify the original real proof, and separately verify a proof copy with its first byte toggled; expected verification failure. A malformed-proof rejection is a transport negative control, not exhaustive soundness validation. Never overwrite original receipts. Compare the response mutation outcome to Circom while preserving that these are two implementations of one artifact, not two independent systems.
