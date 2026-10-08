# Noir environment amendment

Original Noir witness and two negative witness controls completed. The documented bb write_vk command failed before proving because curl was absent. Preserve analysis/noir-proof-controls-v0 unchanged. Install curl and CA certificates in a derived image using the same pinned Python base, record image ID, Dockerfile, package versions, commands and CRS hashes. One attempted Dockerfile used an image digest without the repository name and failed; the corrected build uses python@sha256. Both build logs are retained.

Resume key generation, proving, original verification, and one-byte proof corruption control with unchanged circuit/witness and documented flags. Network is allowed only for backend parameter acquisition in these commands. A rejected corrupted serialization is not a signature-binding test; the two earlier witness controls provide that narrower comparison. No production security claim follows from this local experiment.
