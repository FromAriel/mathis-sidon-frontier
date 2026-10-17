# MathIS — Mathematical Integrity System

## Sidon Frontier: Exact R9 and R16 Certificates

**Version 1.1.0 preparation — tagged GitHub release and Zenodo DOI pending.**

Exact rational Sidon smoothing certificates, standalone verification tools,
and a dated development record by **Ariel M. Williams**. The certificates
improve the cited Hou–Zhao baseline. Stronger coefficients subsequently
appeared, including Stephen Wu/wustep's q2 certificate; these are historical
improvements, not a claim to the current record.

For
\[
F(N)=\max\{|A|:A\subseteq\{0,\ldots,N-1\}\text{ is an integer Sidon set}\},
\]
the cited finite smoothing theorem turns a valid fixed certificate into
\[
F(N)\le N^{1/2}+\sqrt{ab}\,N^{1/4}+O(1).
\]

| Certificate | R | m | L | Coefficient \(\sqrt{ab}\), diagnostic decimal |
| --- | ---: | ---: | ---: | --- |
| Original MathIS R9 | 9 | 32 | 4 | 0.943242424989938949… |
| Retained MathIS R16 | 16 | 32 | 4 | 0.943242255546856199… |
| Hou–Zhao v2 baseline | 8 | 32 | 4 | 0.9434925907135450… |
| External Wu/wustep q2 | 11 | 48 | 6 | 0.943006169985179… |

The proof-bearing quantities are exact rational values of \(a,b,ab\), not
the displayed square roots. The q2 data are an attributed external benchmark,
not a certificate produced by this project. This release does not attempt
an exhaustive best-known-result catalogue.

## Verify both certificates

**Python 3.10 or newer** is required to run both existing checkers. Python
3.12 is the locally checked environment for this release preparation.
No third-party package, network access, optimizer or MathIS installation
is needed for certificate verification.

Run from this repository's root:

```text
python verify.py CERTIFICATE.json
python certificates/r16/verify.py
```

The unchanged R9 command ends with `ALL EXACT CHECKS PASSED`.
The R16 command prints JSON with `"checks_passed": true` and
`"status": "exact-improvement-certified"`. A nonzero process exit
means verification failed. R16 also checks the preceding R16 baseline;
its final gain is positive but below the historical \(10^{-12}\)
product-gain materiality threshold. It establishes no optimality claim.

Expected outputs:
[original R9](EXPECTED_OUTPUT.txt) and
[retained R16](certificates/r16/EXPECTED_OUTPUT.json).
For R9's full exact fractions and every slack, add `--verbose`.
The original [Windows launcher](VERIFY_WINDOWS.cmd) checks **R9 only**;
use the second command above for R16. R9 alone retains its original
Python 3.9 requirement; R16's unchanged checker requires Python 3.10.

[Verification details](VERIFICATION.md) explain output comparison,
manifest scope and the analytic boundary of these checks.

## What the checkers reconstruct

Both checkers use standard-library rational arithmetic for kernel and mixing
normalization, nonnegativity, actual kernel reflection, all 129 covering
inequalities, fixed boundary tails, \(a,b,ab\), and \(b>0\).
R9 checks its frozen hash and exact improvement over the cited Hou–Zhao
baseline. R16 checks its public-subset manifest, its required baseline
identity, both certificates' obligations and their exact product comparison.

The root R9 certificate SHA-256 is
`85e9e878cf3d129fdccbd74d54fbb88c1a6a0c0e6f6b50f6c7064826046b0e75`.
The retained R16 certificate SHA-256 is
`bfdd1de9fced9e32010ccefb853803b6154980584ea71335d42572a4d4cc66d8`.

The R16 [manifest](certificates/r16/MANIFEST.json) is newly assembled for
this public subset. The certificate, baseline, checker and expected output
are byte-identical to their historical research-packet members.
The original research archive and its inventory remain unchanged.

## Analytic foundation and attribution

The finite smoothing architecture and analytic implication are due to
**Jianfeng Hou and Hongbin Zhao**:
[arXiv:2607.01169v2](https://arxiv.org/abs/2607.01169v2), Lemma 2.1, and
[v3](https://arxiv.org/abs/2607.01169v3), Theorem 2.1.
The R9 packet preserves its original v2 comparison. The retained R16
certificate has a separately reviewed v3 hypothesis mapping.

Our contributions represented here are certificate search and construction,
exact rationalization, standalone checking software and reproducible
artifact preservation within that existing framework. We do not claim
invention of the smoothing theorem or the first rational Sidon certificate.

Credit **Stephen Wu/wustep** for the stronger
[q2 certificate](https://github.com/wustep/maths/tree/da2440b68979b78d201182118d30ca418e3c2001/problems/sidon-second-term/compute/q2).
No q2 source or certificate is bundled in this release.

The [theorem and development note](DEVELOPMENT_AND_THEOREM.md) records
hypotheses, dates, comparison scope and remaining limitations.

## Scope

These certificates do not solve Erdős #30, improve the exponent \(1/4\),
establish a globally optimal coefficient or prove a physical forced-loss
theorem. The asymptotic consequence fixes certificate data before
\(N\to\infty\); no varying-grid uniform remainder is asserted.
Finite certificate checking is distinct from external peer review or a
formal proof of the complete analytic theorem.

Historical development, private communication and public release are
different dates. R9 was recorded August 23, 2026 and privately communicated
August 24. The repository became public on October 17, 2026. The version
1.1.0 GitHub release and Zenodo DOI are pending; citation metadata records
October 17 as the software's first public-availability date.
The earlier private repository history does not establish public priority.

## Authorship, assistance and citation

**Ariel M. Williams**, independent researcher and software developer,
directed the research, acceptance criteria and claim boundaries and
developed MathIS. Numerical search and software development used
AI-assisted workflows, including review and debugging.
The numerical optimizer is not part of the proof-bearing certificate.

Use [CITATION.cff](CITATION.cff) for author and version metadata. The DOI
will be added once issued. The citation
date records public availability on October 17, 2026.
The repository is not affiliated with or endorsed by Hou–Zhao or Wu/wustep.

## Files and license

The root certificate, verifier, expected output and Windows launcher retain
the original R9 bytes. The R16 files are in `certificates/r16/`.
[Release notes](RELEASE_NOTES.md) describe this candidate.

Our software, certificate data and accompanying documentation use the
existing [MIT license](LICENSE), copyright © 2026 Ariel M. Williams.
Third-party source papers are cited rather than redistributed here.
