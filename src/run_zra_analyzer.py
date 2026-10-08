import pathlib,json,hashlib,subprocess,time
R=pathlib.Path(__file__).resolve().parents[1];B=R/'data/proof-sandbox';O=R/'analysis/zra-circomspect-v0';O.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
image=subprocess.check_output(['docker','image','inspect','zkp-trustbom-audit:local','--format','{{.Id}}'],text=True).strip()
files=[R/'protocol/analyzer-baseline-v0.md',pathlib.Path(__file__),B/'circomspect-source/Cargo.lock',B/'zra-source/circom/zRA.circom',R/'protocol/zra-controls-v0.md']
(O/'freeze.json').write_text(json.dumps(dict(image=image,revision='50010b623ed4f3bff9d1b0363cfe952385b47af3',sha256={str(p.relative_to(R)):sha(p) for p in files}),indent=2))
shell='set -eu; cd /work; sha256sum target/release/circomspect; set +e; target/release/circomspect /box/zra-source/circom/zRA.circom -L /box/zra-source/circom --level INFO --sarif-file /out/original.sarif > /out/original.log 2>&1; echo $? > /out/original.exit'
cmd=['docker','run','--rm','--name','zkp-circomspect-v0','--cpus','4','--memory','6g','--env','CARGO_BUILD_JOBS=4','--mount',f'type=bind,source={B/"circomspect-source"},target=/source,readonly','--mount',f'type=bind,source={B},target=/box,readonly','--mount',f'type=bind,source={O},target=/out','--mount','type=volume,source=zkp-circomspect-work-v0,target=/work',image,'bash','-c',shell]
t=time.monotonic()
try:
 with (O/'build.log').open('w') as f:x=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=600)
 code=x.returncode
except subprocess.TimeoutExpired:
 subprocess.run(['docker','stop','zkp-circomspect-v0'],capture_output=True);code=-1
(O/'receipt.json').write_text(json.dumps(dict(exit_code=code,seconds=time.monotonic()-t,command=cmd),indent=2))
(O/'manifest.json').write_text(json.dumps({p.name:sha(p) for p in O.iterdir() if p.is_file()},indent=2));print(code)
