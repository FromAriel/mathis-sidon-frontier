# Provenance of the recovered certificate

The certificate was constructed in the private MathIS research programme under
Ariel M. Williams's direction, with AI-assisted software, checking and review.
It was frozen on October 21, 2026 in America/Phoenix; v1.3.0 public availability
is recorded separately using its actual UTC release date. Private development
timestamps do not establish public priority.

The public filename differs from the research filename `B_line_certificate.json`.
Its bytes are unchanged. No original certificate or expected-output file in
the historical R9, R16 or seven-certificate two-sided packages is replaced.

| Artifact | SHA-256 |
|---|---|
| Winning certificate | `42f85414452e5114f5ae25cee3b9b927698ae232f3f2483136d7f6957f8f1be2` |
| General checker | `513b870fab25999b2f92467337ca8ace26519227c7eba76657dea2e4b6082213` |
| Independent primal checker | `7ad75263622788175b7276503e4cfa68393900e7d724d998753cac9ebd190eb9` |

The exact declaration is 188561854127/200000000000. The kernel constant is
a=1398101/1048576. EXPECTED_RESULTS.json preserves the exact b,ab, covering
results and strict comparisons reconstructed from the JSON, rather than
rounded display values. Minimum covering slack is exactly zero; a claim of
strict positivity of every cover is unnecessary.

The new point uses m=1024, L=8, the original asymmetric linear ramp, right
boundary one and fixed tails. Sparse primal refinement was deliberately ended
after its saved best point stopped improving. The exact recovery minimizes
energy in a two-parameter direction/uniform-lift family; it does not globally
optimize all boundary vectors. An earlier partial KKT point supplied a weaker
comparison, not the winning certificate. The seven historical two-sided files
used a different L-BFGS-B generation process.

## Attributed analytic dependencies

- Jianfeng Hou and Hongbin Zhao: finite smoothing framework, including
  [v3 Theorem 2.1](https://arxiv.org/abs/2607.01169v3).
- John Akwei: asymmetric two-sided extension, Section 2.2, Proposition 2.3 and
  Appendix C, ramp/renewal construction and sharp-floor source. The
  [pinned manuscript](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/The_limit_of_vector-valued_smoothing_for_Sidon_sets.pdf)
  is cited rather than redistributed.
- Stephen Wu/wustep: the separately attributed historical
  [q2 benchmark](https://github.com/wustep/maths/tree/da2440b68979b78d201182118d30ca418e3c2001/problems/sidon-second-term/compute/q2).

The present contribution is finite certificate construction/recovery,
implementation, independent exact validation and reproducible preservation.
The fixed reported comparison 0.942809522 is a strict coefficient bound, not
Akwei's unavailable original certificate or a certified current world record.
No inference about new analytic proofs or general physical forced loss follows.

Only this winning certificate is added publicly. Intermediate candidates,
numerical trajectories, internal reviews and operational recovery state remain
in the private research record. Verification is self-contained in this package.
