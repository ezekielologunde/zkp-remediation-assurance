# Second-system selection and fixture audit

Select TrustBOM because the paper links its public implementation and it has guest, orchestrator, and verifier boundaries plus public benchmark inputs. Pin sharing-sbom-system at ea90058af5b137e0cdf6a4aa663bcc77040a928f. Root license is Apache-2.0; preserve third-party notices if later redistribution occurs. Keep this checkout ignored.

Before running the zkVM, independently reconstruct all supplied benchmark Merkle paths with Python SHA-256 and compare the root. Check purl-to-path binding, zero non-membership values, path depth, and bitmap/sibling cardinality. These are fixture checks, not execution of the Rust guest, proof generation, or a deployment assessment. Repeated proofs across files must not be counted as independent samples.

Static leads require complete caller interpretation: the verifier takes image_id from its request and checks the journal against request fields; the orchestrator checks the requested banned-list hash and rejects empty returned proof lists. Therefore guest acceptance of an empty list alone is not an end-to-end failure. A consumer might independently authenticate expected image/root/policy values. Do not assume that trust boundary away.

Build gate: obtain a real local RISC Zero receipt with developer mode disabled, pin RISC Zero/compiler dependencies, and validate expected guest image ID plus journal fields. A mock receipt or Python reimplementation cannot satisfy the two-independent-system execution gate. No credentials, blockchain transactions, GitHub runner setup, or external service deployment is necessary for that local gate.
