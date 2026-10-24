# MathIS Sidon Frontier: Exact Symmetric and Two-Sided Certificates

**Version 1.6.0. October 23, 2026. Author: Ariel M. Williams.**

## v1.6.0: pair-moment conjecture proof preprint

Archived version: [10.5281/zenodo.23607543](https://doi.org/10.5281/zenodo.23607543).

This release presents a proposed effective proof of Akwei's Conjecture 7.7
for exactly the noncyclic pair-moment relaxation in his Definition 7.2:

```text
sqrt(N) + (2 sqrt(2)/3) N^(1/4) - 2572
  <= h_hat_2(N)
  < sqrt(N) + (2 sqrt(2)/3) N^(1/4) + 1, for every integer N >= 2^60.
```

**External human verification and peer review are pending.** The proof and
manuscript received two separate internal AI-assisted mathematical reviews.
They have not been verified in Lean or another proof assistant.
Akwei is credited for the conjecture, model and construction; the upper
companion uses Chen's attributed energy inequality.

Read the [proof and audit guide](research/pair_moment_floor/README.md) or the
[manuscript PDF](research/pair_moment_floor/manuscript/main.pdf).
The package includes the full written argument, TeX sources, objection
resolutions and a bounded primary-source novelty comparison.
It concerns a relaxation, not a construction of Sidon sets, and does not
improve the published numerical coefficient. No worldwide-priority claim
or solution of Erdos Problem 30 is made.

All earlier certificates, checkers, release tags and assets are preserved.
Their data and verification commands below are unchanged. The large original
certificate remains available from v1.5.0; it is not attached again to v1.6.0.

## Preserved numerical certificates

Exact rational certificates, standalone standard-library Python checkers, and
theorem/development mappings. The project's strongest included certificate proves
**sqrt(ab) < 11785113371/12500000000 = 0.942809069680**, using 2,048 centered
box kernels in the original symmetric Hou--Zhao finite model. Its diagnostic
coefficient is approximately 0.9428090696799586049. The new compact exact
witness reconstructs every boundary value through a directed renewal recurrence
and exact repair, without an optimizer or an older boundary. All earlier
certificate packages and issued releases remain preserved.

For the maximum size F(N) of an integer Sidon set in {0,...,N-1}, the cited
fixed-certificate theorem gives F(N) <= sqrt(N) + sqrt(ab) N^(1/4) + O(1).

| Certificate or comparison | Framework | Coefficient sqrt(ab), approximate |
| --- | --- | ---: |
| Original MathIS R9 | Symmetric, 9 kernels | 0.943242424989939 |
| Retained MathIS R16 | Symmetric, 16 kernels | 0.943242255546856 |
| External Wu/wustep q2 | Symmetric, 11 kernels | 0.943006169985179 |
| Preserved v1.2.0 m=1024, L=8 certificate | Asymmetric two-sided, 1 ramp | 0.942810720298845 |
| Akwei's fixed reported certificate bound | Asymmetric two-sided | < 0.942809522 |
| Preserved v1.3.0 recovered certificate | Asymmetric two-sided, 1 ramp | < 0.942809270635 |
| Preserved v1.4.0 centered-box certificate | Symmetric, R=1024, M=2048, L=8 | < 0.942809153974 |
| New v1.5.0 finite-grid certificate | Symmetric, R=2048, M=4096, L=30 | < 0.942809069680 |
| Akwei's smoothing-method lower bound | Continuum/infimum | 2 sqrt(2)/3 = 0.942809041582... |

The new certificate gives the project's best strict coefficient, improving
its earlier certificates within the original symmetric model and preserving
the earlier two-sided results. This is a
software, certificate-data and verification milestone. It makes no current-
record, significant new generic theorem, global-optimality,
exponent-improvement or Erdos #30 solution claim. Akwei already reports the
approximate finite linear-kernel behavior credited in the
[v1.5.0 proof and source mapping](certificates/finite_grid/PROOF.md). The new
analysis gives an exact half-line optimum and an explicit finite realization
bound for the prescribed boxes and weights. It does not optimize over other
kernels or mixtures. Chen separately gives the limiting physical coefficient
in his stated model. Certificate-dependent O(1) terms
are not compared here, and this is not an exhaustive results catalogue.

## Verify independently

Python **3.10 or newer**; no dependencies, network, optimizer or MathIS install.
From the extracted repository root:

```text
python -I -S certificates/finite_grid/verify.py
python -I -S tests/test_finite_grid_public.py
python -I -S tests/test_finite_grid_arrays_public.py
python -I -S certificates/symmetric/verify.py
python -I -S tests/test_symmetric_public.py
python verify.py CERTIFICATE.json
python certificates/r16/verify.py
python -I -S certificates/two_sided/verify.py --all
python -I -S certificates/two_sided_recovery/verify.py
python -I -S tests/test_two_sided_public.py
python -I -S tests/test_two_sided_recovery_public.py
```

To check only the strongest new certificate, reconstructing every exact cover
and energy value from the compact witness:

```text
python -I -S certificates/finite_grid/verify.py
```

The v1.5.0 point has n=K=2048, kernel length M=4096 and boundary depth L=30.
Every one of its 122,881 original covers equals one exactly. Each component
has J=M*L=122880 finite boundary coordinates followed by an exact unit tail;
unused prefixes are fixed zero. The complete original array has 251,658,240
finite boundary entries. Boundary signs are unrestricted by the source theorem.

The compact `certificates/finite_grid/WITNESS.json` losslessly specifies that
array through exact dyadic renewal proposals and a rational widest-box repair.
The public replay independently reconstructs the recurrence, all covers and
exact energy. It uses only Python's standard library and runs offline.
The proof's prospective rational error bound selected L=30 for the initial
Pell benchmark 1121/1189 before construction. Exact verification then supports
the stronger decimal declaration. The historical v1.4.0 multiplier is not an input.

Optional original-schema export and a separate actual-array checker are available:

```text
python -I -S certificates/finite_grid/verify.py --export-gzip tmp/finite_grid.json.gz --state-dir tmp/finite_grid_export
python -I -S certificates/finite_grid/verify.py --check-array tmp/finite_grid.json.gz --state-dir tmp/finite_grid_array
```

The dense representation is published as the optional GitHub release asset
[FINITE_GRID_CERTIFICATE.json.gz](https://github.com/FromAriel/mathis-sidon-frontier/releases/download/v1.5.0/FINITE_GRID_CERTIFICATE.json.gz)
with its [checksum](https://github.com/FromAriel/mathis-sidon-frontier/releases/download/v1.5.0/FINITE_GRID_CERTIFICATE.json.gz.sha256).
The Zenodo GitHub source archive contains the compact witness and complete
offline reconstruction, export and checking tools; the dense gzip is separate.
Decompression yields the original symmetric JSON schema. Use a dedicated state
directory for each operation. Defaults stay under `tmp/finite_grid_replay` in
this repository; an explicit `--state-dir` may select another directory you
control, including one in another controlled checkout. Resume only private
state created by your own replay. Checksums detect corruption and input/code
mismatch; they do not authenticate state supplied by someone else. Use a fresh
state directory or `--no-checkpoint` for fresh arithmetic without saved state.
Interrupted component work can resume, while a completed prior run starts
fresh arithmetic. Full details are in the
[finite-grid guide](certificates/finite_grid/README.md).

### Preserved v1.4.0 replay and dense asset

The following description records the unchanged v1.4.0 package. Its commands,
declaration and asset identities remain valid independently of v1.5.0.

The new point has n=K=1024, kernel length M=2048 and boundary depth L=8.
Every one of its 16,385 covers is exactly one. The finite boundary has length
J=M*L=16384 in each component, with zero unused prefixes and exact unit tails.
The successful flat-cover construction depends on the fixed kernels and
weights; the older asymmetric boundary is not an input to this replay.

The original-schema array can be exported and checked separately:

```text
python -I -S certificates/symmetric/verify.py --export tmp/symmetric_certificate.json
python -I -S certificates/symmetric/verify.py --check-array tmp/symmetric_certificate.json
```

The dense JSON is 682,492,622 bytes. The compact witness is a lossless
mathematical representation and is the normal replay input. It reconstructs
the complete exact certificate offline; it is not a numerical approximation.
Checkpoint files default to `tmp/symmetric_replay` within this repository;
`--state-dir PATH` selects an explicit state directory and `--no-checkpoint`
disables saved replay state.

The optional GitHub release asset [SYMMETRIC_CERTIFICATE.json.gz](https://github.com/FromAriel/mathis-sidon-frontier/releases/download/v1.4.0/SYMMETRIC_CERTIFICATE.json.gz)
and its [checksum](https://github.com/FromAriel/mathis-sidon-frontier/releases/download/v1.4.0/SYMMETRIC_CERTIFICATE.json.gz.sha256)
are published separately from the compact source package. The gzip
is 155,162,896 bytes. Its uncompressed JSON SHA-256 is
`6fe10ab401d66c1f3e71ec930338374b6c86ba3b4f16d43ffba74c96176c2f3c`.
Zenodo's GitHub source archive contains the compact witness and self-contained
replay/export tools; the dense gzip is a separate release asset. The issued
archive identity, hosted checks and full arithmetic replay from the downloaded
archive all passed, as documented below.

An explicit relative certificate path is relative to the current directory.
--all in the historical two-sided checker locates its seven bundled files beside the script and works from any
directory. The historical two-sided checker exits 0 on acceptance, 1 on
mathematical rejection and 2 on malformed input or usage. The new recovery
wrapper also exits 1 for benchmark failure or checker disagreement, and 2 for
package-integrity failure. R9 ends with `ALL EXACT CHECKS PASSED`; R16 reports `checks_passed: true`.
The historical Windows launcher checks R9 only. All R9/R16 proof-bearing files,
expected outputs and commands retain their historical bytes.

[Verification details](VERIFICATION.md), [new finite-grid certificate](certificates/finite_grid/README.md),
[preserved v1.4.0 symmetric certificate](certificates/symmetric/README.md),
[preserved recovery certificate](certificates/two_sided_recovery/README.md),
[preserved seven-certificate inventory](certificates/two_sided/README.md),
and [theorem/development mapping](DEVELOPMENT_AND_THEOREM.md) explain the checks.

## Attribution and scope

**Jianfeng Hou and Hongbin Zhao** supplied the finite smoothing architecture:
[v2 Lemma 2.1](https://arxiv.org/abs/2607.01169v2) and
[v3 Theorem 2.1](https://arxiv.org/abs/2607.01169v3).

**John Akwei** supplied the nonnegative asymmetric two-sided extension
(Proposition 2.3 and Appendix C), ramp/renewal construction and sharp-floor
source theorem. See the [pinned manuscript](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/The_limit_of_vector-valued_smoothing_for_Sidon_sets.pdf).
These source results are attributed dependencies, not discoveries claimed here.

The new symmetric point uses Hou--Zhao's original finite theorem directly;
it does not require the asymmetric extension. Akwei's ramp/renewal work and
finite linear-kernel observations motivated the choice of fixed kernels and
the comparison. Standard weighted least-norm projection, quadratic-program
duality and finite geometric-sum filter algebra supply the recovery machinery.
The proof note identifies those dependencies and their sources.

The v1.5.0 construction uses a positive discrete renewal recurrence with 128
fractional interval bits, 80-bit dyadic proposals and exact finite repair.
Akwei's quantitative finite construction and localized repair are also credited
in its [provenance note](certificates/finite_grid/PROVENANCE.md), alongside
classical renewal, spectral factorization and finite-filter arguments. The
new fixed-family analysis and finite certificate do not establish a new
universal floor or broad implementation priority.

**Haoyu Chen** gives a distinct physical cardinality theorem with coefficient
2 sqrt(2)/3 and explicit onset in his [version 3 note](https://zenodo.org/records/23273526).
The present finite coefficient remains above that value. It gives a stronger
fixed-certificate consequence than this project's earlier releases, with an
exact symmetric representation and replay. No improvement over the strongest
external physical result is claimed.

**Stephen Wu/wustep** supplied the external [q2 benchmark](https://github.com/wustep/maths/tree/da2440b68979b78d201182118d30ca418e3c2001/problems/sidon-second-term/compute/q2).
Its files are not bundled; q2 is not Akwei's one-ramp certificate.

Our contributions are finite certificate construction/recovery, checking
software, independent finite validation and reproducible preservation. For
v1.4.0, a floating banded solve proposed an 80-bit rational multiplier; exact
full-box residual repair produced the accepted point. The public replay
uses the rational multiplier and fixed operators, not that numerical solver.
The seven v1.2.0 certificates used SciPy L-BFGS-B generation. The v1.3.0 recovery
used SciPy sparse trust-constr on a lifted primal problem, followed by exact
rational direction-and-lift recovery. The numerical trajectory was deliberately
stopped after its saved best point stopped improving; solver convergence is
not claimed. A partial active-row KKT result was a comparator, not the winning
certificate. Verification is solver-independent. Numerical generation and its
dependencies are not bundled.

The finite certificates do not attain the limiting coefficient or establish
a universal physical forced-loss inequality. The v1.5.0 proof gives a
fixed-family finite-depth limit and an explicit error bound; it does not give
a general convergence-rate theorem over other kernels and mixtures.
Data are fixed before N tends to infinity; no varying-data uniform
remainder is asserted. Exact finite checking is not external peer review or
formal verification of the complete analytic source theorem.

## History, citation and license

Ariel M. Williams directed the research, acceptance criteria and claim scope.
Construction, software and review used AI-assisted workflows. No affiliation
with or endorsement by the cited authors is implied.

R9 was recorded August 23, 2026 and privately communicated August 24. Those
specific records predate the inspected August 27 Wu/wustep q2 certificate
commit. They do not identify when all of Wu's work began, establish public
priority, or imply that another group used private materials. The
repository and v1.1.0 became public October 17, 2026. Version 1.2.0 is dated
October 21, 2026; private development dates do not establish public priority.
Version 1.3.0 was published October 22, 2026. Its Zenodo record and downloaded
source archive were inspected, and every certificate replay passed from that
archive, including both exact checking implementations for the recovered result.
Version 1.4.0 was published October 23, 2026, at DOI
[10.5281/zenodo.23592514](https://doi.org/10.5281/zenodo.23592514), under the
existing release-series concept DOI. The downloaded Zenodo source archive's
advertised checksum and mathematical payload identities were inspected.
The actual [main run](https://github.com/FromAriel/mathis-sidon-frontier/actions/runs/39936375949)
and [tag run](https://github.com/FromAriel/mathis-sidon-frontier/actions/runs/39936436894)
each passed all four hosted jobs. All eight verification commands also passed
from the downloaded Zenodo archive: R9, R16, all seven historical two-sided
certificates, the recovered certificate, the new symmetric witness and all
32 public tests. The fresh symmetric replay verified all 16,385 covers exactly
one and the stronger strict coefficient bound.

Version 1.5.0 was published October 23, 2026, at
[DOI 10.5281/zenodo.23600836](https://doi.org/10.5281/zenodo.23600836), under the
unchanged release-series concept DOI. The actual Zenodo source ZIP checksum
and all 66 source members match the frozen tagged payload, allowing the
documented CRLF export of the historical Windows launcher. All mathematical
files are byte-identical to the freshly replayed source package, from which
all eleven verification commands passed. The Zenodo archive is accepted by
that payload identity; no additional arithmetic replay was run from its
extraction. The actual [main run](https://github.com/FromAriel/mathis-sidon-frontier/actions/runs/39981382618)
and [tag run](https://github.com/FromAriel/mathis-sidon-frontier/actions/runs/39981383126)
each passed all four hosted jobs. All four prior releases and their assets
and Zenodo records passed the separate post-publication preservation audit.
The documentation follow-up does not alter the frozen v1.5.0 tag or assets.

- [Version 1.5.0 DOI](https://doi.org/10.5281/zenodo.23600836)
- [Version 1.6.0 DOI](https://doi.org/10.5281/zenodo.23607543)
- [Version 1.6.0 release](https://github.com/FromAriel/mathis-sidon-frontier/releases/tag/v1.6.0)
- [Version 1.5.0 release](https://github.com/FromAriel/mathis-sidon-frontier/releases/tag/v1.5.0)
- [Version 1.4.0 DOI](https://doi.org/10.5281/zenodo.23592514)
- [Version 1.4.0 release](https://github.com/FromAriel/mathis-sidon-frontier/releases/tag/v1.4.0)
- [Version 1.3.0 DOI](https://doi.org/10.5281/zenodo.23555594)
- [Version 1.3.0 release](https://github.com/FromAriel/mathis-sidon-frontier/releases/tag/v1.3.0)
- [Version 1.2.0 DOI](https://doi.org/10.5281/zenodo.23548458)
- [Version 1.1.0 DOI](https://doi.org/10.5281/zenodo.23439041)
- [All versions on Zenodo](https://doi.org/10.5281/zenodo.23439039)
- [Version 1.2.0 release](https://github.com/FromAriel/mathis-sidon-frontier/releases/tag/v1.2.0)
- [Citation metadata](CITATION.cff) and [release notes](RELEASE_NOTES.md)

Our code, data and documentation use the existing [MIT license](LICENSE).
Third-party papers are cited, not redistributed or relicensed here.
