# Development history and theorem mapping

Version 1.4.0 was published October 23, 2026. It adds a compact exact symmetric
certificate and standard-library replay in the original Hou--Zhao finite
model. Its version DOI is [10.5281/zenodo.23592514](https://doi.org/10.5281/zenodo.23592514);
the existing concept DOI is https://doi.org/10.5281/zenodo.23439039 . The issued
record, source ZIP checksum and mathematical payload identities were inspected.
Main and tag hosted runs each passed all four jobs. All eight verification
commands passed from the downloaded Zenodo archive, including every historical
certificate, the new symmetric witness and all 32 public tests. The fresh
symmetric replay verified all 16,385 covers exactly one and the stronger
strict coefficient bound.

Version 1.3.0, October 22, 2026, is archived at
https://doi.org/10.5281/zenodo.23555594 . The preserved v1.2.0 release
is archived at https://doi.org/10.5281/zenodo.23548458 . Version 1.1.0 was
published October 17, 2026 and is archived at
https://doi.org/10.5281/zenodo.23439041 .

## Dated development

| Date | Event | Evidence scope |
| --- | --- | --- |
| August23,2026 | Exact R9 result recorded, coefficient approximately 0.943242424989938949 | Local result report and MathIS commit `db06b2da9da9120b6773ee8463b0a8d6ce808b5b`; Git dates are metadata, not an independent public timestamp. |
| August24 | This compact repository created; R9 result and reproduction packet privately communicated | Historical commit `aa4cf54f41f31ce69c3b8d14c58bf81cd81a6ab2`, hosting metadata and private correspondence retained separately. Private history is not public availability. |
| August24 | R12 coefficient approximately 0.94324232243495565761 privately communicated | Historical certificate hash and dated communication. R12 is not bundled here. |
| August27 | Inspected external q2 commit records the stronger0.943006169985179 coefficient | [Wu/wustep commit](https://github.com/wustep/maths/commit/da2440b68979b78d201182118d30ca418e3c2001). Commit date and first public availability are separate questions. |
| September20 | Present retained R16 certificate preserved after exact verification | B3-triple-prime lineage, certificate SHA-256 below; MathIS commit `784fc88dc7825709fe79d35ef48f4f7ebfbe7473`. |
| October17,2026 | Repository made public with both certificate packets | Public commit `9202cd74070ae1d915b04012da1bb93f58e456fb`; anonymous certificate access and all four hosted CI jobs verified. This is the first established public-availability date in this record. |
| October17,2026 | Tagged v1.1.0 published and independently replayed from Zenodo | DOI 10.5281/zenodo.23439041; original record and assets remain unchanged. |
| October21,2026 | Seven two-sided finite certificates independently checked for v1.2.0 | Best exact declared coefficient bound 942810721/1000000000; actual publication is the tagged release event, not a backdated private-development claim. |
| October21,2026 | Fixed m=1024, L=8 recovery experiment produced a stronger finite certificate | Exact declaration 188561854127/200000000000, independently checked against all 16,386 left/right covers; private acceptance is separate from public availability. |
| October22,2026 | Additive v1.3.0 release and inspected Zenodo archive | DOI 10.5281/zenodo.23555594; every historical and new certificate replay passed from the downloaded source archive. Previous release artifacts remain preserved. |
| October 23, 2026 | Exact symmetric centered-box certificate independently accepted and v1.4.0 published | DOI 10.5281/zenodo.23592514; stronger exact declaration 471404576987/500000000000, all 16,385 covers exactly one. Issued archive identity, eight main/tag hosted jobs, and all eight verification commands including 32 public tests passed from the downloaded Zenodo archive. |

This is a development record, not a claim of worldwide first discovery,
the first rational Sidon certificate, current record status, or peer review.
No claim is made that another group used our private materials.
Historical correspondence and the larger private research history are not
part of the public package.

## Historical R9/R16 analytic dependency

Hou and Zhao's [v2 Lemma2.1](https://arxiv.org/abs/2607.01169v2) and
[v3 Theorem 2.1](https://arxiv.org/abs/2607.01169v3) supply the finite smoothing
inequality. The historical R9/R16 certificate class has:

- Fixed positive integers R,m,L; rational data are a subset of the allowed
  real data. Both historical R9/R16 certificates use m=32,L=4.
- Symmetric nonnegative probability kernels, nonnegative mixing weights
  summing to one, and real finite boundary coordinates.
- Boundary tail equal to one at indices j>=Lm, and every covering row
  q=0,...,Lm. The q=Lm row is structural and remains checked.
- Exact energy a and boundary constant b with b>0, using the conventions
  reconstructed by the included checkers.

For the source's admissible scales H=mh, with integer h>=1 and N>=2LH,
the finite bound yields the displayed asymptotic coefficient sqrt(ab).
Certificate data are fixed before taking N to infinity. This package claims
no uniform remainder for data varying with N.

The standalone programs check the finite certificate obligations. They do
not formally verify the full analytic source proof. R9 retains its historical
v2 exact-baseline comparison. The R16 obligation mapping was separately
reviewed against v3, with all129 covers, symmetry, positivity, tail and energy
conventions retained. That review is internal analytic acceptance, distinct
from external refereeing.

## Identities and public-subset provenance

R9 CERTIFICATE.json SHA-256:
`85e9e878cf3d129fdccbd74d54fbb88c1a6a0c0e6f6b50f6c7064826046b0e75`.

Retained R16 CERTIFICATE.json SHA-256:
`bfdd1de9fced9e32010ccefb853803b6154980584ea71335d42572a4d4cc66d8`.

R16 BASELINE.json SHA-256:
`5c441ae04ec2ad404832d9ffa77a2d0c61b07648202aed2805829363e883da77`.
This baseline is the preceding R16 certificate needed by the existing
checker, not the original Hou--Zhao certificate.

The public R16 directory copies exactly four members from the original
retained research archive: CERTIFICATE.json, BASELINE.json, verify.py and
EXPECTED_OUTPUT.json. Original archive SHA-256:
`5a707c4716b90c943613e3cb2a2f4b48548f55c2cae6afe1019ebfcfde8bc2c6`.
Its full archive and historical manifest are preserved separately unchanged.
The public-subset MANIFEST.json is new and explicitly identifies its scope.

The public subset omits internal configuration/provenance and the saved
source-paper HTML. The source paper is referenced by URL; it is not relicensed
or redistributed under our MIT license. Historical input paths in the private
archive are not required to run these self-contained public checks.

## Contributions and limits

Ariel M. Williams directed the certificate search, verification criteria,
claim scope and artifact preservation through MathIS. Development used
AI-assisted computation, software work and review. The included independent
checking implementations reconstruct exact obligations rather than trust
numerical search objectives or saved success flags.

Hou--Zhao supplied the analytic framework and earlier exact certificate.
Wu/wustep supplied the external q2 result, stronger than the historical R9/R16
certificates but weaker in coefficient than the v1.3.0 two-sided certificate.
Neither external result is presented as ours. No author endorsement or institutional affiliation is
implied. The included results do not resolve Erdős#30, improve its exponent,
prove global optimality or establish a universal physical fluctuation law.

## Two-sided certificates: source mapping and exact new result

John Akwei's [pinned October 5 manuscript](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/The_limit_of_vector-valued_smoothing_for_Sidon_sets.pdf),
Section 2.2, equations (2.3), Proposition 2.3 and Appendix C, extends the Hou--Zhao framework
to nonnegative asymmetric kernels. The checker verifies precisely these
finite conditions:

- m,L positive; each kernel p is a nonnegative probability vector; normalized
  nonnegative mixture weights; arbitrary real left/right boundary vectors.
- Every joint left cover uses p_i; every joint right cover uses p_(m-1-i),
  for q=0,...,Lm. Both tails equal one. No boundary-positivity restriction.
- a=m sum_r lambda_r sum_i p_(r,i)^2 and
  b=1+(1/m) sum_r lambda_r sum_(j<Lm)(u_(r,j)^2+v_(r,j)^2-2), with b>0.

For H=mh, the source block-replicates the kernel: K_r(t)=p_(r,i)/h on each
integer block ih<=t<(i+1)h. Thus its squared norm is a_r/H, not a_r/m.
For N>=2LH, weights are defined over every row 0,...,N+H-2 with two disjoint
LH boundary strips. The right strip reflects at N+H-2-x. Joint covers
interpolate between adjacent discrete rows; real boundary signs cause no
division because the argument uses inner products and squared norms.

The source energy and weight identities, followed by direct-sum
Cauchy--Schwarz, give Lemma C.1:

```text
k^2 <= (N-1+bH) (1+(k-1)a/H).
```

Source Corollary C.2 then yields sqrt(N)+sqrt(ab) N^(1/4)+O(1) for fixed
certificate data. Its threshold depends on a,b,m,L. The checkers do not
formally prove this source theorem, and no varying-grid uniform remainder
is claimed.

The preserved best v1.2.0 certificate, m=1024,L=8, has exactly

```text
a  = 1398101/1048576
b  = 682669260471443050366205717/1024000000000000000000000000
ab = 954440575734385000160042579143417/1073741824000000000000000000000000
sqrt(ab) < 942810721/1000000000.
```

That historical certificate improves the cited q2 coefficient but remains above Akwei's reported
sqrt(ab)<0.942809522. Construction used one ramp p_i=(2i+1)/m^2 and SciPy
L-BFGS-B boundary generation, followed by exact recovery and independent
finite reconstruction. Verification is solver-independent.

Akwei's source Theorem 5.1 supplies continuum sharpness, with boundary
omega(t)=exp(t)-1 for 0<=t<1 and omega(t)=integral_0^1 x r(t-x)dx for t>=1.
This is an attributed source result, not a fresh proof here. An erroneous
private draft used (1/2) integral_0^t r(s)ds; that profile fails the cover at
zero and grows instead of tending to one. That derivation was withdrawn.
The finite certificates do not depend on it. No convergence-rate theorem
or reflected signed-C5 attainment is established by the seven finite files.

## Version 1.3.0: exact feasibility recovery on the same grid

The added certificate retains m=1024, L=8, the same ramp, a right boundary
identically one and fixed tails. Its exact declaration is

```text
a = 1398101/1048576
sqrt(ab) < 188561854127/200000000000 = 0.942809270635.
```

The exact b and ab are reconstructed from the certificate by both included
checking routes and retained in its expected results. The certificate SHA-256 is
`42f85414452e5114f5ae25cee3b9b927698ae232f3f2483136d7f6957f8f1be2`.
Its declaration is below the fixed reported Akwei bound 0.942809522 by exactly
50273/200000000000. This is a comparison of the specified coefficient bounds,
not an independent replay of an unavailable exact Akwei certificate or a claim
of the current worldwide record.

Construction used sparse lifted primal trust-constr optimization and exact
rational direction-and-lift recovery. The numerical trajectory was deliberately
stopped after its saved best point stopped improving; this is not a solver
convergence claim. A partial active-row KKT refinement supplied a weaker
comparison certificate. The winning recovery optimizes its stated two-parameter
family, not all feasible boundary vectors. Exact finite verification, rather
than solver termination or a small floating-point residual, establishes the
published certificate obligations.

The existing general two-sided checker is preserved. A separate standard-library
checker directly reconstructs the one-ramp/right-ones covers, including the
reversed right kernel, fixed tails and both structural end rows. It imports no
producer arithmetic. Neither checker formally verifies the analytic source
theorem. The source mapping above is unchanged: Akwei supplies the asymmetric
construction and finite theorem within the Hou--Zhao lineage. Our contribution
is certificate construction, numerical implementation and exact recovery,
independent finite checking and reproducible preservation, with AI assistance.

The new file does not prove a convergence law, global boundary optimality,
continuum or signed-C5 attainment, a physical forced-loss theorem, or an
Erdos #30 exponent improvement. All older certificates, theorem dependencies
and immutable release identities retain their historical scope.

## Version 1.4.0: direct finite symmetric construction

The new point returns to Hou--Zhao's original symmetric finite model, using
R=n=1024 centered box kernels of length M=2048 and depth L=8. Each boundary
has J=ML=16384 finite entries followed by an exact unit tail. Every covering
row q=0,...,J is exactly one, including the structural last row. Kernel and
mixing normalization, symmetry, nonnegativity, unused zero prefixes, exact
energy, positive b and strict coefficient comparison are finite obligations.

The exact energy constant and stronger public declaration are

```text
a = 1398101/1048576
sqrt(ab) < 471404576987/500000000000 = 0.942809153974.
```

The diagnostic coefficient is approximately 0.942809153973600631. This is
below the preserved v1.3.0 declaration 0.942809270635 and remains above the
inherited limiting value 2 sqrt(2)/3. The exact rational inequality, not a
rounded square root, determines the declaration.

[The public proof note](certificates/symmetric/PROOF.md) defines every box and
weight and maps them directly to HZ v3 Theorem 2.1. The fixed-data consequence
is sqrt(N)+sqrt(ab)*N^(1/4)+O(1). The asymmetric extension is not needed for
this new point. No varying-grid uniform remainder or explicit numerical O(1)
constant is claimed.

Construction used one banded numerical proposal for an 80-bit rational
multiplier and an exact full-box residual repair. The successful flat-cover
point depends on the fixed operators and that multiplier, not the historical
asymmetric boundary. The public compact witness retains the exact multiplier;
standard-library replay reconstructs every boundary, cover and energy without
the solver or private research inputs. Optional original-schema export and
a separate streaming array check expose the full finite data. The compact
file is a lossless mathematical representation, not a rounded boundary table.

Separate retained research comparisons show why preserving a historical
aggregate cover is more restrictive than uniformly releasing its slack: the
exact fixed-cover endpoint cannot reach the stated target, while the flat-
cover endpoint does. A verified nonnegative dual also places the original
inequality problem's optimum within approximately 2.157380189016e-13 energy
of the new point for these frozen kernels and weights. The default public
replay checks the winning certificate; it does not reconstruct those separate
baseline-barrier or dual-comparison receipts. Neither statement is exact
global optimality or a universal conversion theorem.

Hou--Zhao Section 3 already develops joint boundary quadratic programming,
Gram duality, recovery and feasibility repair. Weighted least-norm projection
and finite box-filter cancellation are classical. Akwei's pinned limit
manuscript page 10/Section 5/Table 2 and V5 pages 22-23/Table 9 already describe
approximate finite linear-kernel behavior b approximately2/3+1/(3m^2) and
ab approximately8/9+2/(9m^2)-1/(9m^4). These are attributed unnumbered finite
diagnostics, not new formulas or rates established by this release. His m is
the linear-ramp grid and differs from this certificate's symmetric length M.

Haoyu Chen's [version3 note](https://zenodo.org/records/23273526) separately
gives a physical cardinality bound at coefficient 2 sqrt(2)/3 with explicit
onset in its stated scalar-capacity model. The new finite certificate does
not strengthen that physical coefficient. The unavailable advertised Akwei
certificate/code packages were not independently replayed, so comparisons
with that work retain their stated source and priority limits.

This is an additive archival software/certificate-data milestone. It preserves
the historical proof-bearing files and issued release identities and provides
a new independently checked finite artifact. It does not establish significant
new generic-method novelty, a convergence law, current record, exponent
improvement or Erdos #30 solution, and makes no journal-significance claim.
Ariel M. Williams directed construction, claim scope and acceptance;
computation, software, drafting and review used AI assistance. Internal
analytic review and exact finite checks are distinct from external peer
review or formal verification of the complete source theorem. Third-party
sources are cited without endorsement, redistribution or relicensing.
