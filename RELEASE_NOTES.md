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
all-versions concept DOI remains https://doi.org/10.5281/zenodo.23439039 . A
v1.4.0 version DOI and hosted/archive acceptance will be reported only after
they are issued and verified. The existing MIT license covers our own new
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
