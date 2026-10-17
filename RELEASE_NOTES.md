# Release 1.1.0 preparation

Title: **MathIS Sidon Frontier: Exact R9 and R16 Certificates**.
Status: content reviewed; tagged release and Zenodo DOI pending.

## Contents

- Preserves the original R9 certificate, checker, expected output and command.
- Adds the retained R16 certificate, required preceding baseline and existing
  checker/expected output, with a new explicitly scoped public manifest.
- Documents both coefficients, exact-check commands, dated development,
  Hou--Zhao theorem dependencies, attribution and limitations.
- Updates citation metadata and the proposed CI checks for both certificates.
  Both checkers together require Python3.10 or newer.
- Omits private correspondence, internal campaigns and full third-party papers.

The R9 and R16 coefficients improve the cited Hou--Zhao baseline and have
been surpassed by external results including Wu/wustep q2. This is a
reproducible research-artifact release, not an announcement of a current
record, an exponent improvement, global optimality or an Erdős#30 solution.

## Subsequent publication checklist

These are future actions; preparation does not execute them.

1. Ariel has reviewed the proposed public files, release notes and validation report.
2. Set the actual release date in citation/release metadata; retain August and
   September dates only in the development history. Recheck changed hashes
   and rebuild the final candidate after any approved edit.
3. Commit and push only the approved certificate-repository update, reconciling
   the existing August24 README-only commit. Preserve
   the historical commit and leave the larger private MathIS repository private.
4. Make this compact repository public and verify unauthenticated access.
5. Connect the public repository through Zenodo's GitHub integration before
   creating the GitHub release. Review any account authorization personally.
6. Publish the GitHub release tagged v1.1.0, then inspect its processed Zenodo
   record, author, title, version, license, files, DOI and archival status.
7. Add the real DOI/citation link and verify it resolves. Never invent a DOI
   or backdate the public release to a private-development event.

If integration fails, inspect the reported metadata/processing error rather
than assume a DOI exists. A separately approved direct Zenodo upload is an
alternative; avoid creating duplicate records for the same object by accident.

Zenodo [repository setup](https://help.zenodo.org/docs/github/enable-repository/)
and [release archiving](https://help.zenodo.org/docs/github/archive-software/github-upload/)
describe the account and ingestion steps. This release uses CITATION.cff
alone; no competing .zenodo.json or placeholder identifiers are included.
