import pathlib,subprocess,json
E=pathlib.Path('/evidence');O=pathlib.Path('/out');F=pathlib.Path('/fixtures');F.mkdir(exist_ok=True)
labels=json.loads(pathlib.Path('/labels.json').read_text())['names'];member=(E/'member.bin').read_bytes().hex();nonmember=(E/'nonmember.bin').read_bytes().hex();root=(E/'commitment.bin').read_bytes().hex();newroot=(E/'new-commitment.bin').read_bytes().hex()
cases=[('member',member,labels[0],root,True),('nonmember',nonmember,labels[1],root,True),('wrong_label',member,labels[1],root,False),('missing_label',member,None,root,True),('wrong_commitment',member,labels[0],newroot,False),('empty',None,None,root,True)]
rows=[]
for name,proof,label,c,expected in cases:
 f=F/(name+'.txt');f.write_text(('Proof: '+proof+'\n' if proof else '')+('Dependency: '+label+'\n' if label else ''))
 cmd=['/work/target/release/zksbom-verifier','verify','--method','ozks','--commitment',c,'--proof_path',str(f)]
 r=subprocess.run(cmd,cwd='/work',text=True,capture_output=True,timeout=60);log=r.stdout+'\n'+r.stderr;(O/(name+'.log')).write_text(log)
 accepted='Proof is valid.' in r.stdout
 rows.append(dict(case=name,exit_code=r.returncode,proof_valid_message=accepted,expected_message=expected,member_message='Yes (member)' in r.stdout,nonmember_message='No (not in trie)' in r.stdout,command=cmd))
 assert accepted==expected,(name,log)
assert rows[0]['member_message'] and rows[1]['nonmember_message']
(O/'cases.json').write_text(json.dumps(rows,indent=2));print('SIX_CLI_CASES_COMPLETE')
