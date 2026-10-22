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
