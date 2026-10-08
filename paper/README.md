# ACM/Overleaf manuscript package

This is a complete bounded empirical manuscript draft, not a submitted or accepted paper. Novelty priority, deployed exploitability, and maintainer confirmation remain unverified. Author: Ezekiel Ologunde, Independent Researcher, Boston, MA, USA; ologunde@bu.edu. No corresponding-author designation or institutional affiliation is implied.

Upload the ZIP to Overleaf and choose XeLaTeX with main.tex as the main document. The source is self-contained apart from standard TeX packages (acmart, TikZ and pgfplots). Local validation used Tectonic 0.17.0, which uses the XeTeX engine, with a cached bundle. A venue may require a different class option; no venue has been selected. The default is acmart sigconf,nonacm.

For a local build: `tectonic --keep-logs main.tex`. With a TeX Live installation: run `xelatex -interaction=nonstopmode -halt-on-error main.tex` until references stabilize. No BibTeX step is needed because references are embedded. XeLaTeX/Overleaf server compilation is not independently tested by this local package build.

Run `python verification/verify.py` from any directory to check the source presentation against the included evidence. The 69 checks cover snapshot hashes, raw compiler constraint totals, table cells, logged decisions, references, figure descriptions, format and author fields. They do not reproduce cryptographic proofs. Full proof reproduction requires the separately acquired sources, dependencies and instructions in the repository: https://github.com/ezekielologunde/zkp-remediation-assurance

The ZIP includes only the manuscript, this README, validation.json and verification/. The latter contains the independent checker, snapshot manifest, recorded results, and selected locally generated evidence. Third-party archives, keys, binary proofs and copyrighted papers are excluded. Original research remains unlicensed; no new reuse license is granted by packaging. AI-assisted preparation is disclosed in the manuscript and requires the author's final review.

The source is newly authored, not a formatting-only rewrite of an uploaded original. Tables and the constraint plot are generated from saved results; the flow diagram is a source-grounded conceptual description. Underfull-box/font request diagnostics and a small final-page vertical box warning are recorded in validation.json. Embedded fonts and page inspection distinguish these diagnostics from missing glyphs or visible clipping.
