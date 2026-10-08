import pathlib,subprocess,json,hashlib,time
R=pathlib.Path(__file__).resolve().parents[1];O=R/'analysis/zksbom-native-v2'
image=subprocess.check_output(['docker','image','inspect','zkp-zksbom-native:v0','--format','{{.Id}}'],text=True).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[pathlib.Path(__file__),R/'protocol/zksbom-native-v0.md',R/'data/zksbom-contract-audit.json']
(O/'freeze.json').write_text(json.dumps(dict(image=image,inputs={str(p.relative_to(R)):sha(p) for p in files}),indent=2))
cmd=['docker','run','--rm','--network','none','--cpus','4','--memory','8g','--mount',f'type=bind,source={R/"data/zkSBOM-source/zksbom-verifier/third_party/oZKS"},target=/source,readonly','--mount','type=volume,source=zkp-zksbom-native-v2,target=/work',image,'bash','-c','set -eu; cp -a /source/. /work/; cd /work; dpkg-query -W; mkdir -p /work/shim; printf \"include(/usr/lib/x86_64-linux-gnu/cmake/flatbuffers/FlatBuffersConfig.cmake)\\nset(Flatbuffers_FOUND TRUE)\\nset_target_properties(flatbuffers::flatc PROPERTIES IMPORTED_LOCATION_RELEASE /usr/bin/flatc)\\n\" > /work/shim/FlatbuffersConfig.cmake; cmake -S . -B build -DFlatbuffers_DIR=/work/shim -DOZKS_BUILD_EXAMPLES=ON -DOZKS_BUILD_TESTS=ON; cmake --build build -j4; build/bin/ozks-simple-unit-tests --gtest_list_tests']
t=time.monotonic()
with (O/'build.log').open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=900)
(O/'receipt.json').write_text(json.dumps(dict(command=cmd,exit_code=p.returncode,seconds=time.monotonic()-t),indent=2));print(p.returncode)
