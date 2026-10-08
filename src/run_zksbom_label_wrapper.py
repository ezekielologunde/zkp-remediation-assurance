import pathlib,subprocess,json,hashlib,time
R=pathlib.Path(__file__).resolve().parents[1];O=R/'analysis/zksbom-label-wrapper-v1';O.mkdir(exist_ok=False);E=R/'data/proof-sandbox/zksbom-label-wrapper-v1';E.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
image=subprocess.check_output(['docker','image','inspect','zkp-zksbom-native:v0','--format','{{.Id}}'],text=True).strip()
files=[pathlib.Path(__file__),R/'data/proof-sandbox/zksbom-label-fixture-v0/probe.cpp',R/'data/zkSBOM-source/zksbom-verifier/cpp/verify_wrapper.cpp',R/'protocol/zksbom-cli-v0.md']
(O/'freeze.json').write_text(json.dumps(dict(image=image,inputs={str(p.relative_to(R)):sha(p) for p in files}),indent=2))
shell='set -eu; cd /work; cmake --build build --target ozks-simple -j4; gcc -O2 -c oZKS/hash/blake2b.c -o /work/blake2b.o; g++ -std=c++17 -O2 -I/work -I/work/build -I/wrapper /probe.cpp /wrapper/verify_wrapper.cpp build/lib/libozks-simple.a build/lib/libozks-1.6.a /work/blake2b.o -lPocoFoundation -lflatbuffers -lpthread -o /work/wrapper-probe; sha256sum /work/wrapper-probe; /work/wrapper-probe'
cmd=['docker','run','--rm','--network','none','--cpus','4','--memory','8g','--mount','type=volume,source=zkp-zksbom-native-v2,target=/work','--mount',f'type=bind,source={R/"data/proof-sandbox/zksbom-label-fixture-v0/probe.cpp"},target=/probe.cpp,readonly','--mount',f'type=bind,source={R/"data/zkSBOM-source/zksbom-verifier/cpp"},target=/wrapper,readonly','--mount',f'type=bind,source={E},target=/out',image,'bash','-c',shell]
t=time.monotonic()
with (O/'execution.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=600)
(O/'receipt.json').write_text(json.dumps(dict(command=cmd,exit_code=p.returncode,seconds=time.monotonic()-t,generated={str(p.relative_to(R)):sha(p) for p in E.iterdir()}),indent=2));print(p.returncode)
