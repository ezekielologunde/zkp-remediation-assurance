"""Fresh offline saved-proof verification, without modifying original evidence."""
import hashlib
import json
import pathlib
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/verisbom-replay-2026-10-14'
OUT.mkdir(exist_ok=False)
image = subprocess.check_output(['docker', 'image', 'inspect', 'zkp-verisbom-audit:ubuntu', '--format', '{{.Id}}'], text=True).strip()
receipt = {'scope': 'Fresh execution of saved-proof controls; not fresh proof generation or independent cryptography', 'image': image, 'runs': []}
for name, script in [('original', ROOT / 'src/verisbom_acceptance_cases.py'), ('bound', ROOT / 'data/proof-sandbox/verisbom-repair-v0/cases.py')]:
    folder = OUT / name
    folder.mkdir()
    cmd = ['docker', 'run', '--rm', '--network', 'none', '--cpus', '4', '--memory', '12g',
        '--mount', 'type=volume,source=zkp-verisbom-work-v0,target=/work,readonly',
        '--mount', 'type=volume,source=zkp-verisbom-build-v0,target=/compiled,readonly']
    for source, target, readonly in [(script, '/probe.py', True), (folder, '/out', False),
        (ROOT / 'data/proof-sandbox/verisbom-results-v3', '/evidence', True),
        (ROOT / 'data/proof-sandbox/verisbom-bundle-v0', '/bundle', True)]:
        cmd += ['--mount', f'type=bind,source={source},target={target}' + (',readonly' if readonly else '')]
    cmd += [image, 'bash', '-c', 'set -eu; cd /work; sha256sum /work/bomz /compiled/target/release/bound_verifier; python3 /probe.py']
    started = time.monotonic()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    (folder / 'execution.log').write_text(result.stdout + '\n' + result.stderr)
    receipt['runs'].append({'name': name, 'command': cmd, 'exit_code': result.returncode, 'seconds': time.monotonic() - started,
        'script_sha256': hashlib.sha256(script.read_bytes()).hexdigest()})
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2))
    if result.returncode:
        raise RuntimeError(f'{name} failed; inspect preserved log')
    cases = json.loads((folder / 'cases.json').read_text())
    expected = [True, False, False, True] if name == 'original' else [True, False, True, False]
    assert len(cases) == 4 and [r['application_accepted'] for r in cases] == expected
    assert all(r['math_verified'] for r in cases)
    assert [r['exit_code'] for r in cases] == [0 if x else 1 for x in expected]
    print(name, expected, flush=True)
(OUT / 'manifest.json').write_text(json.dumps({str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file()}, indent=2))
