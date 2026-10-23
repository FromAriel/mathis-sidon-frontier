# Version 1.5.0 - October 23, 2026

Title: **MathIS Sidon Frontier: Exact Symmetric and Two-Sided Certificates.**

Adds one compact exact finite-grid certificate with 2,048 centered box kernels,
M=4096, L=30 and J=122880 finite boundary coordinates per component. It proves
the project's strongest strict declaration

```text
sqrt(ab) < 11785113371/12500000000 = 0.942809069680.
```

The actual coefficient has the exact strict bracket
`0.942809069679958604 < sqrt(ab) < 0.942809069679958605`. Every one of the
122,881 original covers equals one exactly, including the structural unit-tail
row. Kernel and mixture normalization, reflection, unused zero prefixes,
positive b and the strict squared-rational comparison are checked. The
original Hou--Zhao finite symmetric theorem supplies the Sidon consequence
for this fixed certificate.

The compact WITNESS.json stores exact dyadic renewal proposals and a rational
widest-box repair. Its default standard-library replay independently checks
the directed recurrence, every original cover and exact energy without an
optimizer, older certificate, private input or network. A separate streaming
implementation checks actual original-schema gzip arrays. The new commands are

```text
python -I -S certificates/finite_grid/verify.py
python -I -S tests/test_finite_grid_public.py
python -I -S tests/test_finite_grid_arrays_public.py
python -I -S certificates/finite_grid/verify.py --export-gzip tmp/finite_grid.json.gz --state-dir tmp/finite_grid_export
python -I -S certificates/finite_grid/verify.py --check-array tmp/finite_grid.json.gz --state-dir tmp/finite_grid_array
```

The source archive contains the lossless compact witness, proof, prospective
error calculation and complete offline reconstruction/export/checking tools.
The dense gzip is published as an optional separate
[GitHub release asset](https://github.com/FromAriel/mathis-sidon-frontier/releases/download/v1.5.0/FINITE_GRID_CERTIFICATE.json.gz)
with its [checksum](https://github.com/FromAriel/mathis-sidon-frontier/releases/download/v1.5.0/FINITE_GRID_CERTIFICATE.json.gz.sha256).
Gzip changes storage only: decompression yields the original symmetric JSON
certificate schema. The public declaration is stronger than the research
construction's initial Pell benchmark 1121/1189, with identical mathematical
kernel, weight and boundary data. The new declaration has its own byte hashes;
the sealed research artifact is preserved.

For the prescribed boxes and weights, the proof establishes the exact
half-line optimum and a strictly positive correction at every finite depth
when n>=2. An explicit rational realization bound selected L=30 for the
initial Pell benchmark before construction. The finite equality and inequality minima remain distinct
objects; no optimization over arbitrary kernels or mixtures is claimed.

Hou--Zhao supply the analytic framework. Akwei's ramp/renewal analysis,
approximate finite-grid formulas, quantitative construction and localized
repair are credited dependencies, alongside classical spectral-factor and
finite-filter arguments. Chen's distinct limiting physical coefficient remains
stronger than this finite coefficient. Wu/wustep's q2 remains an attributed
historical comparison. The August 23 R9 record and August 24 private
communication predate the inspected August 27 q2 artifact; this does not date
all external work, establish public priority or allege use of private material.

This is an attributed software, certificate-data and verification release.
It claims no worldwide record, new universal floor, significant generic-method
priority, global optimality over other kernels/weights, exponent advance or
solution of Erdos Problem 30. Internal proof reviews and exact finite checks
are distinct from external peer review and formal proof verification.
AI-assisted computation, software, drafting and review are disclosed.

All earlier proof-bearing certificate/checker packages, expected results,
commands, tags, release assets and issued Zenodo versions remain preserved.
Version 1.4.0 remains at https://doi.org/10.5281/zenodo.23592514 . Version 1.5.0
was published October 23, 2026, at
[DOI 10.5281/zenodo.23600836](https://doi.org/10.5281/zenodo.23600836); the existing
all-versions concept DOI remains https://doi.org/10.5281/zenodo.23439039 .
The actual Zenodo ZIP checksum and tagged source payload passed inspection,
with only the documented historical Windows-launcher CRLF export. Its
mathematical bytes match the clean source package from which all eleven
verification commands passed, including the compact replay of all 122,881 covers.
Archive acceptance uses that exact payload identity; no additional arithmetic
replay from the Zenodo extraction was run. Both main/tag hosted runs passed
all eight jobs in total. Actual downloaded GitHub assets match their frozen
hashes. Dense-array verification transfers from the completed independent
original-array check through unchanged compressed component members and the
exact stronger-bound comparison; the additional incomplete public streaming
replay is not counted as completed. All four earlier releases and Zenodo
versions passed the separate post-publication preservation audit. Historical
release notes below retain their original scope and completed verification
records; the frozen v1.5.0 tag and assets are unchanged by this DOI follow-up.

# Version 1.4.0 - October 23, 2026

Title: **MathIS Sidon Frontier: Exact Symmetric and Two-Sided Certificates.**

Adds a compact exact witness for 1,024 centered box kernels at n=K=1024,
M=2048, L=8. It proves the project's strongest exact declaration

```text
sqrt(ab) < 471404576987/500000000000 = 0.942809153974.
```

The diagnostic coefficient is approximately 0.942809153973600631. All 16,385
finite covers are exactly one, with normalized nonnegative symmetric kernels,
normalized positive mixing weights, real finite boundary coordinates, zero
unused prefixes and exact unit tails. The original Hou--Zhao finite symmetric
theorem supplies the cardinality consequence for fixed data.

The compact witness records an exact 80-bit multiplier. Standard-library replay
reconstructs the fixed operators, every repaired boundary and every cover and
energy value. It requires no older boundary, optimizer, network, third-party
Python package or private MathIS checkout. Optional export writes the original
dense JSON schema, and a separate direct streaming route checks that array.

```text
python -I -S certificates/symmetric/verify.py
python -I -S tests/test_symmetric_public.py
python -I -S certificates/symmetric/verify.py --export tmp/symmetric_certificate.json
python -I -S certificates/symmetric/verify.py --check-array tmp/symmetric_certificate.json
```

The accepted flat-cover construction depends only on the chosen kernels,
weights and multiplier, not the historical asymmetric boundary. Separate
research comparisons establish a fixed-cover redistribution obstruction and
a very tight nonnegative-dual comparison for these fixed operators/weights.
Those comparisons are not inputs to the default public replay and are not a
claim of exact global optimality or a universal conversion theorem.

Hou and Zhao supply the original finite analytic model. John Akwei's
ramp/renewal work and approximate finite linear-kernel formulas motivate the
comparison; those formulas and the smoothing floor are not new claims here.
Haoyu Chen separately gives the limiting physical coefficient in his stated
model. Weighted least-norm projection, quadratic-program duality and finite
filter cancellation are classical ingredients. Ariel M. Williams directed the
finite construction, exact acceptance, software and preservation, with
AI-assisted computation, drafting and review. Full attribution and limitations
are in the theorem mapping and new proof note.

This is an archival software/certificate-data milestone and a stronger
fixed-certificate consequence than this project's earlier releases. No
significant new generic theorem, finite-rate law, worldwide record, improvement
over the strongest external physical result, exponent improvement or Erdos
#30 solution is claimed. A
journal-significance recommendation has not been established by this release.

The historical R9/R16 and two-sided proof-bearing files, checkers, expected
outputs, tags, release assets and issued Zenodo records remain preserved.
Version 1.3.0 remains at https://doi.org/10.5281/zenodo.23555594 . The existing
all-versions concept DOI remains https://doi.org/10.5281/zenodo.23439039 .
Version 1.4.0 was published October 23, 2026, at
[DOI 10.5281/zenodo.23592514](https://doi.org/10.5281/zenodo.23592514), with its
[GitHub release](https://github.com/FromAriel/mathis-sidon-frontier/releases/tag/v1.4.0).
The issued Zenodo record, source ZIP checksum and mathematical payload
identities were inspected. Actual main and tag hosted runs each passed all
four jobs. All eight verification commands passed from the downloaded Zenodo
archive, covering every historical certificate, the new symmetric witness
and all 32 public tests. The fresh symmetric replay verified all 16,385 covers
exactly one and the stronger strict coefficient bound. The existing MIT
license covers our own new
software, certificate data and documentation; third-party papers are cited
without redistribution or relicensing.

# Version 1.3.0 - October 22, 2026

Title: **MathIS Sidon Frontier: R9, R16 and Exact Two-Sided Certificates.**

Adds one independently checked exact rational certificate proving
sqrt(ab) < 188561854127/200000000000 = 0.942809270635. It uses m=1024,
L=8, Akwei's asymmetric linear ramp, a right boundary identically one and
fixed tails. The strict declaration is below the fixed reported Akwei bound
0.942809522 by exactly 0.000000251365, and below the cited Wu/wustep q2
coefficient. No current-record, novelty, global-optimality, exponent-improvement
or Erdos #30 solution claim is made.

All 16,386 original left/right covers, dimensions, fixed tails and exact a,b,ab
are reconstructed by the preserved general verifier and a separately implemented
standard-library direct checker. The new scoped package includes the certificate,
both checking routes, expected exact results, provenance and a manifest. Checking
works with isolated Python and no optimizer, network or MathIS installation.

The winning numerical point came from SciPy sparse lifted primal trust-constr
optimization, followed by exact rational direction-and-lift recovery. The
trajectory was deliberately stopped after its saved best point stopped improving;
solver convergence is not claimed. A partial active-row KKT point was a weaker
comparison. Neither the numerical campaign nor private runtime state is bundled.
The seven preserved v1.2.0 files used L-BFGS-B generation; their bytes and checker
behavior remain unchanged.

John Akwei supplies the asymmetric construction and finite theorem in
Proposition 2.3 and Appendix C, within Jianfeng Hou and Hongbin Zhao's smoothing
lineage. Stephen Wu/wustep is credited for the external q2 comparison. Ariel M.
Williams directed construction, recovery, acceptance and preservation, with
AI-assisted software and review. The new finite certificate does not establish
an attainment theorem, convergence law or signed-C5 upper attainment.

This is an additive release. R9, R16, all seven v1.2.0 certificates, historical
verifiers, expected outputs, tags, assets and existing Zenodo records remain
preserved. The v1.3.0 DOI is https://doi.org/10.5281/zenodo.23555594 . Its issued
record and downloaded source archive were inspected, and every historical and
new verification command passed from that extraction. The preserved v1.2.0 DOI
is https://doi.org/10.5281/zenodo.23548458 and the all-versions DOI remains
https://doi.org/10.5281/zenodo.23439039 .

# Version 1.2.0 - October 21, 2026

Title: **MathIS Sidon Frontier: R9, R16 and Exact Two-Sided Certificates.**

Adds seven exact rational two-sided linear-ramp certificates and a portable
standard-library verifier. The strongest proves sqrt(ab) < 0.942810721.
Every finite covering row and exact energy constant was independently checked.
The earlier R9/R16 proof-bearing files, commands and expected outputs remain
unchanged. Version 1.1.0 remains archived at
https://doi.org/10.5281/zenodo.23439041 .

The new coefficient improves on Stephen Wu/wustep's cited q2 coefficient
0.943006169985179, but remains above John Akwei's reported 0.942809522.
No current-record, novelty, optimality, exponent improvement or Erdos #30
solution claim is made. The fixed-certificate consequence relies on Akwei's
Proposition 2.3 and Appendix C, extending the Hou--Zhao framework.

This release corrects research-checker handling of nonpositive declared
coefficient bounds, malformed array shapes, nonpositive-energy diagnostics
and certificate-verification exit codes. It preserves legitimate real boundary
coordinates and joint mixture covers. Public tests include rejection and
compatibility controls. Verification is solver-independent; numerical
generation used SciPy L-BFGS-B and is not bundled.

An erroneous private draft's continuum profile and finite proof were withdrawn.
This release maps to the inspected source theorem and does not present that
draft as a new proof. Akwei's ramp/renewal attainment and sharp floor are
attributed source results. The seven finite files do not prove an asymptotic
convergence rate or attainability within reflected signed C5.

Ariel M. Williams directed the research and artifact acceptance. Software,
construction and review used AI-assisted workflows. Hou--Zhao, Akwei and
Wu/wustep are credited without implying endorsement or coauthorship.

The repository first became public October 17, 2026. This release uses its
actual October 21 date; earlier private development is not public priority.
Version 1.2.0 is archived at https://doi.org/10.5281/zenodo.23548458 .
The immutable v1.2.0 tag and release assets precede this DOI metadata update;
their certificate and verifier bytes remain unchanged. All versions:
https://doi.org/10.5281/zenodo.23439039 .
