# zkSBOM wrapper controls v0

Native v0 failed dependency discovery. Native v1 shim duplicated a supplied target. Native v2 corrected the shim and built core/simple libraries, but the all-target build failed in distributed tests due to missing this_thread declaration. Preserve failures. Narrow target to ozks-simple and its unit tests without modifying cryptographic code. This excludes distributed tests, not a successful full build.

Use the archived C++ verifier wrapper unmodified, default oZKS configuration and real randomized native proofs. Insert key 010101 with payload 0102; query present key and absent key 010100. Expected wrapper codes 0 and 1 respectively, exact extracted key match. Insert absent key to change commitment; expect previous member proof invalid (code 2). Run existing QueryTest and InsertTest. Save proof bytes locally and hashes publicly. This is a native backend/wrapper reproduction, not Rust CLI or operator deployment.
