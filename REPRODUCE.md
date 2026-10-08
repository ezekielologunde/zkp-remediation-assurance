# Reproduce the initial source/data audit

Use Python 3.10 or later. The audit uses the standard library only. No ZKP backend has been executed.

```powershell
git clone https://github.com/chains-project/zkSBOM.git data/zkSBOM-source
git -C data/zkSBOM-source checkout --detach 0bb63acc24f70e3480615696266963023b128275
python src/audit_public_fixture.py
```

Compare the resulting data/public-fixture-audit.json with the committed version. File hashes describe acquired working-tree bytes; Git line-ending settings can affect source-text hashes across platforms. Pin the revision and preserve line-ending configuration when requiring exact byte reproduction. JSON counts refer to the top-level components array, not a semantic validation of every CycloneDX field. No submodule is needed for this audit.

Upstream code and fixtures remain in an ignored checkout and are not redistributed. The upstream root LICENSE is MIT; preserve it and any component-specific notices if a later release includes third-party material. SBOM-listed package licenses describe those packages and are not a blanket grant for arbitrary data redistribution.

See protocol/threat-model-v0.md for the actual intended claim and protocol/artifact-audit-plan-v0.md for the next gate. Reproducing a parser result does not reproduce a cryptographic proof or establish a novel research contribution.
