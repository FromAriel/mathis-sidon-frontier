# MathIS - Mathematical Integrity System

## R9, R16 and exact two-sided Sidon certificates

**Version 1.2.0. Author: Ariel M. Williams.**

Exact rational certificates, standalone standard-library Python checkers, and
theorem/development mappings. The strongest included certificate proves
**sqrt(ab) < 0.942810721**, using Akwei's asymmetric ramp construction within
the Hou--Zhao smoothing lineage.

For the maximum size F(N) of an integer Sidon set in {0,...,N-1}, the cited
fixed-certificate theorem gives F(N) <= sqrt(N) + sqrt(ab) N^(1/4) + O(1).

| Certificate or comparison | Framework | Coefficient sqrt(ab), approximate |
| --- | --- | ---: |
| Original MathIS R9 | Symmetric, 9 kernels | 0.943242424989939 |
| Retained MathIS R16 | Symmetric, 16 kernels | 0.943242255546856 |
| External Wu/wustep q2 | Symmetric, 11 kernels | 0.943006169985179 |
| Included m=1024, L=8 certificate | Asymmetric two-sided, 1 ramp | 0.942810720298845 |
| Akwei's reported stronger certificate bound | Asymmetric two-sided | < 0.942809522 |
| Akwei's two-sided method floor | Continuum/infimum | 2 sqrt(2)/3 = 0.942809041582... |

The new finite certificate improves on the cited q2 coefficient, remains above
Akwei's reported certificate, and makes no current-record, novelty, optimality,
exponent-improvement or Erdos #30 solution claim. Certificate-dependent O(1)
terms are not compared here. This is not an exhaustive current-results catalogue.

## Verify independently

Python **3.10 or newer**; no dependencies, network, optimizer or MathIS install.
From the extracted repository root:

```text
python verify.py CERTIFICATE.json
python certificates/r16/verify.py
python -I -S certificates/two_sided/verify.py --all
python -I -S tests/test_two_sided_public.py
```

To check only the strongest new certificate:

```text
python -I -S certificates/two_sided/verify.py certificates/two_sided/two_sided_linear_m1024_L8_certificate.json
```

An explicit relative certificate path is relative to the current directory.
--all locates the seven bundled files beside the script and works from any
directory. Exit codes: 0 accepted, 1 mathematical rejection, 2 malformed input
or usage. R9 ends with `ALL EXACT CHECKS PASSED`; R16 reports `checks_passed: true`.
The historical Windows launcher checks R9 only. All R9/R16 proof-bearing files,
expected outputs and commands retain their historical bytes.

[Verification details](VERIFICATION.md), [new certificate inventory](certificates/two_sided/README.md),
and [theorem/development mapping](DEVELOPMENT_AND_THEOREM.md) explain the checks.

## Attribution and scope

**Jianfeng Hou and Hongbin Zhao** supplied the finite smoothing architecture:
[v2 Lemma 2.1](https://arxiv.org/abs/2607.01169v2) and
[v3 Theorem 2.1](https://arxiv.org/abs/2607.01169v3).

**John Akwei** supplied the nonnegative asymmetric two-sided extension
(Proposition 2.3 and Appendix C), ramp/renewal construction and sharp-floor
source theorem. See the [pinned manuscript](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/The_limit_of_vector-valued_smoothing_for_Sidon_sets.pdf).
These source results are attributed dependencies, not discoveries claimed here.

**Stephen Wu/wustep** supplied the external [q2 benchmark](https://github.com/wustep/maths/tree/da2440b68979b78d201182118d30ca418e3c2001/problems/sidon-second-term/compute/q2).
Its files are not bundled; q2 is not Akwei's one-ramp certificate.

Our contributions are finite certificate construction/recovery, checking
software, independent finite validation and reproducible preservation.
Generation used SciPy L-BFGS-B; verification is solver-independent. Numerical
generation and its dependencies are not bundled.

The new files do not prove continuum attainment, a convergence-rate theorem,
attainability within reflected signed C5, or a general physical forced-loss
inequality. Data are fixed before N tends to infinity; no varying-data uniform
remainder is asserted. Exact finite checking is not external peer review or
formal verification of the complete analytic source theorem.

## History, citation and license

Ariel M. Williams directed the research, acceptance criteria and claim scope.
Construction, software and review used AI-assisted workflows. No affiliation
with or endorsement by the cited authors is implied.

R9 was recorded August 23, 2026 and privately communicated August 24. The
repository and v1.1.0 became public October 17, 2026. Version 1.2.0 is dated
October 21, 2026; private development dates do not establish public priority.

- [Version 1.2.0 DOI](https://doi.org/10.5281/zenodo.23548458)
- [Version 1.1.0 DOI](https://doi.org/10.5281/zenodo.23439041)
- [All versions on Zenodo](https://doi.org/10.5281/zenodo.23439039)
- [Version 1.2.0 release](https://github.com/FromAriel/mathis-sidon-frontier/releases/tag/v1.2.0)
- [Citation metadata](CITATION.cff) and [release notes](RELEASE_NOTES.md)

Our code, data and documentation use the existing [MIT license](LICENSE).
Third-party papers are cited, not redistributed or relicensed here.
