# Development history and theorem mapping

Prepared for version 1.1.0; tagged-release date and Zenodo DOI pending.

## Dated development

| Date | Event | Evidence scope |
| --- | --- | --- |
| August23,2026 | Exact R9 result recorded, coefficient approximately0.943242424989938949 | Local result report and MathIS commit `db06b2da9da9120b6773ee8463b0a8d6ce808b5b`; Git dates are metadata, not an independent public timestamp. |
| August24 | This compact repository created; R9 result and reproduction packet privately communicated | Historical commit `aa4cf54f41f31ce69c3b8d14c58bf81cd81a6ab2`, hosting metadata and private correspondence retained separately. Private history is not public availability. |
| August24 | R12 coefficient approximately0.94324232243495565761 privately communicated | Historical certificate hash and dated communication. R12 is not bundled here. |
| August27 | Inspected external q2 commit records the stronger0.943006169985179 coefficient | [Wu/wustep commit](https://github.com/wustep/maths/commit/da2440b68979b78d201182118d30ca418e3c2001). Commit date and first public availability are separate questions. |
| September20 | Present retained R16 certificate preserved after exact verification | B3-triple-prime lineage, certificate SHA-256 below; MathIS commit `784fc88dc7825709fe79d35ef48f4f7ebfbe7473`. |
| October17,2026 | Repository made public with both certificate packets | Public commit `9202cd74070ae1d915b04012da1bb93f58e456fb`; anonymous certificate access and all four hosted CI jobs verified. This is the first established public-availability date in this record. |
| Tagged release | Pending | Repository availability and a tagged software release are separate events. Final release metadata must use the actual public date, not an August development date. |

This is a development record, not a claim of worldwide first discovery,
the first rational Sidon certificate, current record status, or peer review.
No claim is made that another group used our private materials.
Historical correspondence and the larger private research history are not
part of the public package.

## Analytic dependency

Hou and Zhao's [v2 Lemma2.1](https://arxiv.org/abs/2607.01169v2) and
[v3 Theorem2.1](https://arxiv.org/abs/2607.01169v3) supply the finite smoothing
inequality. Our finite certificate class has:

- Fixed positive integers R,m,L; rational data are a subset of the allowed
  real data. Both included certificates use m=32,L=4.
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
Wu/wustep supplied the stronger external q2 result. Neither external result
is presented as ours. No author endorsement or institutional affiliation is
implied. The included results do not resolve Erdős#30, improve its exponent,
prove global optimality or establish a universal physical fluctuation law.
