# **MathIS** - Mathematical Integrity System 
### Sidon Frontier

[![Exact certificate verification](https://github.com/FromAriel/mathis-sidon-frontier/actions/workflows/verify.yml/badge.svg)](https://github.com/FromAriel/mathis-sidon-frontier/actions/workflows/verify.yml)

An exact rational certificate improving the finite Sidon-set
\(N^{1/4}\) upper-bound coefficient.

Let

\[
F(N)=\max\left\{|A|:A\subseteq\{0,1,\ldots,N-1\}
\text{ is a Sidon set}\right\}.
\]

The certificate in this repository verifies

\[
F(N)
\le
N^{1/2}
+0.9432424249899389\ldots N^{1/4}
+O(1).
\]

This improves the Hou–Zhao v2 certified coefficient

\[
0.9434925907135450\ldots.
\]

The decisive comparison is performed on exact rational values of
\(ab=\gamma^2\). Floating-point arithmetic is used only to print readable
decimal approximations. It is not used to accept the certificate or establish
the improvement.

> This result improves a quantitative frontier associated with Erdős Problem
> #30. It does **not** resolve Erdős Problem #30 or improve the exponent
> \(1/4\).

**Research and project direction:** Ariel M. Williams<br>
**Verification framework:** MathIS — Mathematical Integrity System<br>
**Analytic foundation:** Hou–Zhao, Lemma 2.1,
[arXiv:2607.01169v2](https://arxiv.org/abs/2607.01169v2)

## Verify in seconds

Python 3.9 or newer is required. No third-party packages, network connection,
optimizer, MathIS installation, or original research repository is needed.

```bash
python verify.py CERTIFICATE.json
```

On Windows, double-click:

```text
VERIFY_WINDOWS.cmd
```

A successful run ends with:

```text
ALL EXACT CHECKS PASSED
```

For the complete exact fractions and all 129 covering slacks:

```bash
python verify.py CERTIFICATE.json --verbose
```

The default successful output is frozen in `EXPECTED_OUTPUT.txt`.

## What is checked

Using only Python's standard-library `fractions.Fraction`, the verifier:

1. Checks the frozen certificate SHA-256 and strict JSON structure.
2. Checks that all nine mixing weights are nonnegative and sum exactly to one.
3. Checks that every kernel is nonnegative, normalized, and exactly symmetric.
4. Recomputes all 129 Hou–Zhao covering inequalities.
5. Recomputes the exact energy constant
   \[
   a=m\sum_r\lambda_r\sum_i(p_i^{(r)})^2.
   \]
6. Recomputes the exact boundary constant
   \[
   b=1+2\left(\frac1m\sum_r\lambda_r\sum_j(w_j^{(r)})^2-L\right)
   \]
   and checks \(b>0\).
7. Recomputes \(ab=\gamma^2\), checks the declared bound, and compares the
   candidate with the exact Hou–Zhao v2 \(ab\).

The frozen certificate is 177,454 bytes and has SHA-256:

```text
85e9e878cf3d129fdccbd74d54fbb88c1a6a0c0e6f6b50f6c7064826046b0e75
```

## Mathematical source and attribution

The analytic implication is Lemma 2.1 of:

> Jianfeng Hou and Hongbin Zhao, *Vector-valued smoothing for finite Sidon
> sets*, arXiv:2607.01169v2.

Their lemma permits an arbitrary finite number of symmetric probability
kernels, nonnegative mixing weights summing to one, real boundary vectors
satisfying the covering inequalities, and a positive boundary constant
\(b\). Their published certificate uses eight kernels. The certificate here
uses \(R=9\), \(m=32\), and \(L=4\) within the same published hypothesis
class.

This repository is not affiliated with or endorsed by Hou and Zhao.

## Scope of the result

This repository establishes an improved explicit coefficient in an upper
bound of the form

\[
F(N)\le N^{1/2}+\gamma N^{1/4}+O(1).
\]

It does not:

- resolve Erdős Problem #30;
- prove an error term \(O_\varepsilon(N^\varepsilon)\);
- improve the exponent \(1/4\);
- prove that this nine-kernel certificate is globally optimal;
- prove that the Hou–Zhao framework can drive \(\gamma\) to zero; or
- claim peer review or endorsement by the authors of the underlying lemma.

## About MathIS

**MathIS — Mathematical Integrity System** is a research and verification
framework developed by Ariel M. Williams for computer-assisted mathematics.
It separates numerical discovery from proof-bearing evidence, checks exact
certificates independently, preserves provenance and artifact identities, and
enforces explicit boundaries on what a computation does and does not
establish.

MathIS was used to organize, audit, rationalize, and independently replay the
research that produced this certificate. The verifier published here is
deliberately standalone: users do not need MathIS or the original research
environment to verify the result.

## About Ariel Williams

Ariel M. Williams is an independent researcher and software developer
exploring how exact computation, transparent certificates, and carefully
supervised AI systems can contribute to serious mathematical research. She
developed MathIS and directed the search and verification program that
produced this certificate.

## Computational assistance

The research program, acceptance criteria, claim boundaries, and final
disclosure are directed by Ariel M. Williams. Numerical optimization and
software development used AI-assisted workflows, including independent review
and debugging passes.

The numerical optimizer is not part of the proof. The public mathematical
evidence consists of the Hou–Zhao analytic lemma and the exact rational
certificate checked by the standalone verifier in this repository.

## Files

- `CERTIFICATE.json` — frozen exact rational certificate.
- `verify.py` — standalone standard-library exact verifier.
- `VERIFY_WINDOWS.cmd` — double-click Windows launcher.
- `EXPECTED_OUTPUT.txt` — deterministic successful reference output.
- `CITATION.cff` — citation metadata.
- `LICENSE` — MIT license.

## License

Copyright © 2026 Ariel M. Williams. This repository is released under the
MIT License. See `LICENSE`.
