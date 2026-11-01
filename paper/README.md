# Research note

`main.tex` is a self-contained LaTeX draft with an embedded bibliography and no
external figures. It has not been submitted to arXiv and makes no novelty or
open-problem-resolution claim. Author attribution remains for review; the draft
discloses AI assistance.

From the repository root:

```sh
python paper/verify_results.py
tectonic --keep-logs --outdir paper paper/main.tex
```

Alternatively run `pdflatex main.tex` twice from the `paper` directory.

The standard-library verifier independently checks the three prime tables,
certificate values, finite unit/atom-proof hypotheses, an explicit factorization,
boundary cases, and 848 eligible cases in a rational grid. General validity
comes from the written proofs. These checks do not prove atomicity or IDF.

The source is [CrowdMath Open Problem 2](https://artofproblemsolving.com/polymath/mitprimes2026/p/open-prob2),
consulted November 1, 2026. The linked prior chat had no accessible attachment;
the complete official online problem was recovered and used instead.

Before submission, a human author must review the mathematics, authorship,
literature priority, and attribution of shared CrowdMath contributions.
Compiling successfully is not evidence of arXiv acceptance.
