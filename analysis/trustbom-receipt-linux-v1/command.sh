set -eu
cp -a /source/. /work/
mkdir -p /work/examples
cp /probe.rs /work/examples/audit_probe.rs
cd /work
cargo run --locked --release --example audit_probe -- benchmark/data/merkleproofs/batch_proof_2.json
cp audit-receipt.json /evidence/
cp Cargo.lock /evidence/host-Cargo.lock
cp methods/guest/Cargo.lock /evidence/guest-Cargo.lock
