import pathlib,subprocess,json,hashlib,time
R=pathlib.Path(__file__).resolve().parents[1];O=R/'analysis/zksbom-cli-build-v0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
image=subprocess.check_output(['docker','image','inspect','zkp-zksbom-cli:v0','--format','{{.Id}}'],text=True).strip()
S=R/'data/zkSBOM-source/zksbom-verifier'; files=[pathlib.Path(__file__),R/'src/zksbom_system_build.rs',R/'protocol/zksbom-cli-v0.md']+list((S/'src').rglob('*.rs'))+[S/'Cargo.lock',S/'Cargo.toml',S/'build.rs']
(O/'freeze.json').write_text(json.dumps(dict(image=image,inputs={str(p.relative_to(R)):sha(p) for p in files}),indent=2))
cmd=['docker','run','--rm','--cpus','4','--memory','10g','--mount',f'type=bind,source={S},target=/source,readonly','--mount',f'type=bind,source={R/"src/zksbom_system_build.rs"},target=/build.rs,readonly','--mount','type=volume,source=zkp-zksbom-native-v2,target=/native,readonly','--mount','type=volume,source=zkp-zksbom-cli-v0,target=/work',image,'bash','-c','set -eu; cp -a /source/. /work/; cd /work; cp /build.rs build.rs; cp config/config_template.toml config/config.toml; CARGO_BUILD_JOBS=4 cargo build --locked --release; sha256sum target/release/zksbom-verifier']
t=time.monotonic()
with (O/'build.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=1200)
(O/'receipt.json').write_text(json.dumps(dict(command=cmd,exit_code=p.returncode,seconds=time.monotonic()-t),indent=2));print(p.returncode)
