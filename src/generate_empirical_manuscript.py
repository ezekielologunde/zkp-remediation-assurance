import pathlib,json,hashlib,shutil
R=pathlib.Path(__file__).resolve().parents[1];P=R/'paper';E=P/'verification/evidence';E.mkdir(parents=True,exist_ok=True)
paths=['analysis/repair-verification.json','analysis/verisbom-acceptance-v0/cases.json','analysis/verisbom-repair-v0/cases.json','analysis/zksbom-cli-cases-v0/cases.json','analysis/verisbom-verification.json','analysis/zksbom-verification.json','data/corpus-ledger-v0.json']
paths += ['analysis/root-binding-verification.json','analysis/backend-comparison-verification.json','analysis/trustbom-receipt-verification.json','analysis/contract-controls-verification.json','analysis/zra-verification.json','analysis/circomspect-verification.json']
paths += ['analysis/repair-v1/original-inspect.log','analysis/repair-v1/repair-inspect.log']
for d in ['verisbom-acceptance-v0','verisbom-repair-v0','zksbom-cli-cases-v0']:
 paths += [str(x.relative_to(R)).replace('\\','/') for x in (R/'analysis'/d).glob('*.log')]
for f in paths:
 dst=E/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/f,dst)
(P/'verification/input-manifest.json').write_text(json.dumps({f:hashlib.sha256((E/f).read_bytes()).hexdigest() for f in paths},indent=2))
s=(P/'manuscript.template.tex').read_text();d=json.loads((E/paths[0]).read_text());a=d['constraints']['original'];b=d['constraints']['repair']
fig=r'''\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{axis}[ybar,bar width=20pt,width=\columnwidth,height=4.2cm,ymin=0,ymax=22000,ylabel={R1CS constraints},symbolic x coords={Original,Alternative},xtick=data,nodes near coords,nodes near coords style={font=\scriptsize},tick label style={font=\scriptsize},label style={font=\small},scaled y ticks=false,ytick={0,5000,10000,15000,20000},ymajorgrids=true]
\addplot[fill=blue!35,draw=blue!70] coordinates {(Original,%d) (Alternative,%d)};
\end{axis}
\end{tikzpicture}
\caption{Local Circom size comparison: %s versus %s constraints, an increase of %s (%.2f\%%). The alternative changes the relation; this is not runtime overhead.}
\Description{Two bars show %d original constraints and %d alternative constraints.}
\label{fig:size}
\end{figure}'''%(a,b,f'{a:,}',f'{b:,}',f'{b-a:,}',100*(b-a)/a,a,b)
s=s.replace('% GENERATED_SIZE_FIGURE',fig)
x=json.loads((E/paths[1]).read_text());y=json.loads((E/paths[2]).read_text());yes=lambda b:'Accept' if b else 'Reject'
rows=[]
for i,(u,v) in enumerate(zip(x,y)):
 rows.append(('Original' if i<2 else 'Changed')+' & '+('Original' if i%2==0 else 'Changed')+' & '+yes(u['application_accepted'])+' & '+yes(v['application_accepted'])+r' \\')
table=r'''\begin{table}[t]
\caption{VeriSBOM decisions. All rows use a mathematically valid proof. The diagnostic comparator uses authenticated outputs.}
\label{tab:veri}
\centering\small
\begin{tabular}{@{}llll@{}}
\toprule Metadata & Expected root & Archived & Diagnostic \\
\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule
\end{tabular}
\end{table}'''
s=s.replace('% GENERATED_VERI_TABLE',table)
z=json.loads((E/paths[3]).read_text());labels=['Honest member','Honest nonmember','Wrong label','Missing label','Changed commitment','Empty file'];rows=[]
for label,r in zip(labels,z):rows.append(label+' & '+('Valid' if r['proof_valid_message'] else 'Invalid')+' & '+str(r['exit_code'])+r' \\')
table=r'''\begin{table}[t]
\caption{zkSBOM CLI output. A valid message is not sufficient to establish an answer to a caller-specified nonempty query.}
\label{tab:zksbom}
\centering\small
\begin{tabular}{@{}lll@{}}
\toprule Case & Validity message & Exit code \\
\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule
\end{tabular}
\end{table}'''
s=s.replace('% GENERATED_ZKSBOM_TABLE',table)
(P/'main.tex').write_text(s,encoding='utf-8');print('Generated manuscript and frozen presentation evidence')
