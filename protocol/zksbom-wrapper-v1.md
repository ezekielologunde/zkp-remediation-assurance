# Wrapper build amendment v1

v0 failed linking archived tests with unresolved blake2b. Compile the unchanged archived oZKS/hash/blake2b.c explicitly and link that object to the probe. Do not change hash algorithm, VRF mode or proof verifier. Skip upstream unit tests that did not link; report them unavailable. Execute only the three custom real-proof wrapper controls already specified. This is an environment/link adjustment, not successful reproduction of the complete upstream test suite.
