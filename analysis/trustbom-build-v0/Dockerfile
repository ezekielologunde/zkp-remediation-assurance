FROM rust@sha256:38bc5a86d998772d4aec2348656ed21438d20fcdce2795b56ca434cf21430d89
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libssl-dev pkg-config curl git ca-certificates cmake clang
COPY cargo-risczero r0vm /usr/local/bin/
RUN chmod +x /usr/local/bin/cargo-risczero /usr/local/bin/r0vm
RUN cargo risczero install --version r0.1.88.0
ENV RISC0_DEV_MODE=0
ENV RISC0_SERVER_PATH=/usr/local/bin/r0vm
ENV CARGO_BUILD_JOBS=2
