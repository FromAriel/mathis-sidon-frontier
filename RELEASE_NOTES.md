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
Zenodo's new version identifier is recorded after ingestion, never invented
or substituted with the v1.1.0 DOI. All versions:
https://doi.org/10.5281/zenodo.23439039 .
