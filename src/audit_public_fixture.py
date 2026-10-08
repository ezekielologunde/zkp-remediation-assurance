"""Read-only provenance/schema audit. Does not execute upstream code or proofs."""
import collections
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT/'data/zkSBOM-source'
REVISION = '0bb63acc24f70e3480615696266963023b128275'


def main():
    revision = subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD'],text=True).strip()
    if revision != REVISION:
        raise RuntimeError('Source revision differs from the reviewed version')
    hashes, submodules = {}, {}
    for row in subprocess.check_output(['git','-C',str(SOURCE),'ls-files','--stage'],text=True).splitlines():
        metadata, name = row.split('\t',1)
        mode, object_id, _ = metadata.split()
        if mode=='160000':
            submodules[name] = object_id
        else:
            hashes[name] = hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
    rows = []
    for file in sorted((SOURCE/'zksbom-operator/tests/sboms').glob('*.json')):
        value = json.loads(file.read_text(encoding='utf-8-sig'))
        components = value.get('components',[])
        refs = [c['bom-ref'] for c in components if c.get('bom-ref')]
        rows.append(dict(path=file.relative_to(SOURCE).as_posix(),bytes=file.stat().st_size,
                         bom_format=value.get('bomFormat'),spec_version=value.get('specVersion'),
                         top_level_component_count=len(components),
                         top_level_components_with_purl=sum(bool(c.get('purl')) for c in components),
                         top_level_components_without_bom_ref=len(components)-len(refs),
                         duplicate_top_level_bom_refs=[k for k,v in collections.Counter(refs).items() if v>1],
                         dependency_records=len(value.get('dependencies',[]))))
    result = dict(source='https://github.com/chains-project/zkSBOM',revision=revision,
                  retrieved='2026-10-07',license='MIT at repository root; no source/data redistributed',
                  attribution='CHAINS Research Project; repository CITATION.cff credits Tom Sorger, 2025 thesis',
                  source_file_sha256=hashes,uninitialized_submodule_revisions=submodules,fixtures=rows,
                  status='Parsed public JSON and inspected source only; no proof generated or verified',
                  limitations='Top-level schema inventory, not full CycloneDX validation, SBOM completeness, vulnerability status, or fleet ground truth')
    target = ROOT/'data/public-fixture-audit.json'
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(tracked_files_hashed=len(hashes),submodules_not_initialized=len(submodules),fixtures=rows),indent=2))


if __name__=='__main__':main()
