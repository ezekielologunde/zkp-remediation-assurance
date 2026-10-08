FROM zkp-zksbom-native:v0
COPY --from=zkp-trustbom-audit:local /usr/local/rustup /usr/local/rustup
COPY --from=zkp-trustbom-audit:local /usr/local/cargo /usr/local/cargo
ENV RUSTUP_HOME=/usr/local/rustup CARGO_HOME=/usr/local/cargo PATH=/usr/local/cargo/bin:$PATH
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends libclang-dev pkg-config ca-certificates
