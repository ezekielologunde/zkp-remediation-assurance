# zkSBOM executed disposition and consumer boundary

Date: 2026-10-08. Pinned repository 0bb63acc24f70e3480615696266963023b128275; oZKS submodule 5a7d43d82742ca9917bc63ebd278476e239fb10e. This is a local verifier reproduction, not an operator deployment, end-to-end SBOM/advisory study, or new vulnerability claim.

## Executed results

The original native C++ wrapper accepted real member proofs (code 0), accepted real nonmember proofs (code 1), and rejected a previous member proof against a changed commitment (code 2). Extracted keys matched the requested keys. Three controls were repeated with dependency-hash keys, giving six native wrapper cases. Proofs used default VRF labels and committed payloads, not ordinary Merkle-mode substitution.

The Rust CLI was built using its archived Cargo.lock with unchanged Rust application source and C++ wrapper. A build.rs replacement links the same native library and distro Poco. Six cases used genuine generated proofs:

| Case | CLI validity message | CLI exit | Explicit expected-query consumer |
|---|---|---|---|
| Honest member | Valid, member | 0 | Accept member answer |
| Honest nonmember | Valid, nonmember | 0 | Accept nonmember answer |
| Wrong dependency label | Invalid | 0 | Reject |
| Missing dependency label | Valid, member | 0 | Reject missing query binding |
| Changed commitment | Invalid | 0 | Reject |
| Empty proof file | Valid, no details | 0 | Reject missing answer |

The output-level consumer baseline requires one nonempty dependency equal to the independently expected label, a valid message, and explicit membership status. This is ordinary validation, not a novel method or independent cryptographic implementation. A valid nonmember answer is accepted as an answer, not interpreted as membership. The wrong-label case also prints member status despite its overall invalid message, so callers must honor the aggregate validity result.

## Interpretation

The explicit dependency binding and commitment controls behaved correctly. Empty files pass the vacuous all_valid loop; missing labels skip binding; failure messages still exit 0. These are reproduced interface behaviors. Exploitability depends on a downstream contract, such as requiring at least one answer to an independently supplied dependency. That contract was not established or tested in a deployed caller. Do not count these as a third confirmed application vulnerability or a cryptographic break.

All five selected corpus systems now have executed controls, but coverage is unequal. This completes the pending verifier feasibility disposition, not complete security analysis of every system.

## Build history and limits

Native v0 failed Flatbuffers package discovery. v1 compatibility shim duplicated an existing flatc target. v2 corrected the package-name shim and built libraries, but the all-target build failed distributed tests with an undeclared this_thread. Wrapper v0 then failed upstream simple-test linking because blake2b was unresolved. Wrapper v1 explicitly compiled the unchanged bundled blake2b.c and passed the controls. The CLI linked through its existing Rust dependency graph. A missing GNU-stack assembly-note warning remains; no production-hardening claim. Upstream unit tests were not successfully executed.

The first image lookup ran before Docker finished exporting; no experiment ran. A label-wrapper preparation used a nonexistent protocol path and stopped before execution; corrected preparation was run separately. These scripting failures do not count as rejected proofs. The source, failure logs, frozen commands, exact image IDs, hashes and successful outputs are preserved. Fresh random native proofs mean reproduction should match decisions, not proof bytes or timing. No performance comparison is made.

`analysis/zksbom-verification.json`: 274 hash checks passed; six native cases and six CLI cases checked. It also recomputes the Blake2b-256 dependency key formula independently in Python and checks the explicit-query baseline. Proofs are retained locally under ignored data/proof-sandbox; source-derived files and third-party libraries are not redistributed here.

## Research consequence

No additional supported vulnerability claim from zkSBOM. The broad new-audit-method claim is not supported: conventional expected-query checks explain the observed boundaries. The surviving candidate is a bounded, reproducible empirical study of the previously observed PIRANHAS and VeriSBOM mismatches, with correctly binding controls and transparent source/build limitations. See analysis/closest-work-reassessment-v1.md and protocol/common-binding-audit-v1.md. A full manuscript must not promise a new class of attack, tool superiority, or representative prevalence.
