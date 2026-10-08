import pathlib,hashlib,json
R=pathlib.Path.cwd();E=R/'data/proof-sandbox/zksbom-label-fixture-v0';E.mkdir()
names=['pkg:generic/audit-present@1','pkg:generic/audit-absent@1'];vals=[]
for n in names:
 v=hashlib.blake2b(n.encode(),digest_size=32).digest();k=hashlib.blake2b(n.encode()+v,digest_size=32).digest();vals.append((k,v))
s=(R/'src/zksbom_wrapper_probe.cpp').read_text()
def b(x):return '{'+','.join('std::byte{'+str(i)+'}' for i in x)+'}'
s=s.replace('key_type key{std::byte{1},std::byte{1},std::byte{1}};',f'key_type key{b(vals[0][0])};').replace('key_type absent{std::byte{1},std::byte{1},std::byte{0}};',f'key_type absent{b(vals[1][0])};').replace('payload_type payload{std::byte{1},std::byte{2}};',f'payload_type payload{b(vals[0][1])};')
(E/'probe.cpp').write_text(s);(E/'labels.json').write_text(json.dumps(dict(names=names,keys=[k.hex() for k,v in vals],payloads=[v.hex() for k,v in vals]),indent=2))
