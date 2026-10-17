# Verification guide

Run from the extracted repository root with Python3.10 or newer:

```text
python -I -S verify.py CERTIFICATE.json
python -I -S certificates/r16/verify.py
```

Both commands are verification-only, use the standard library and require
no external data, network, solver or installed MathIS package. The R9 checker
alone retains Python3.9 compatibility. The R16 checker uses zip(strict=True)
and therefore requires Python3.10 or newer.

## Expected decisions and output

R9 exits0 and ends with `ALL EXACT CHECKS PASSED`. Its complete default
output matches [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt), apart from
platform newline translation. Use `--verbose` for full fractions and slacks.

R16 exits0 and prints the full JSON in
[EXPECTED_OUTPUT.json](certificates/r16/EXPECTED_OUTPUT.json). Its status is
`exact-improvement-certified`, with checks_passed=true and covering_count=129.
The material=false field is expected: the last exact product improvement
over its preceding R16 baseline is below the historical1e-12 materiality
threshold. It does not negate exact acceptance. Decimals are diagnostic;
the exact fractions control comparisons.

A nonzero exit means a check failed. Preserve the error output and compare
file hashes; do not interpret a partial printed report as success.
R9's original Windows launcher verifies R9 only. No combined launcher or new
mathematical checker is introduced by this release.

## Manifest and integrity scope

The new public-subset [R16 manifest](certificates/r16/MANIFEST.json) binds all
four imported files, including the checker and expected output. Its file
inventory differs deliberately from the unchanged historical research archive.
The existing checker accepts this manifest and reconstructs the baseline and
candidate values. Original paper HTML and campaign files are unnecessary.

The prepared release ZIP also carries RELEASE_MANIFEST.json, containing each
other payload member's byte count and SHA-256. It does not list itself.
The neighboring ZIP SHA-256 identifies that archive. These hashes
establish byte identity, not mathematical novelty or a discovery timestamp.

## CI and reproduction limits

The GitHub Actions matrix runs Ubuntu/Python3.10 and3.13,
Windows/Python3.12 and macOS/Python3.12. It executes both checkers and compares
both expected outputs. The workflow defines these platform checks; consult
the actual GitHub Actions run for their execution status. Local preparation
also replayed both certificates and all four workflow commands on Python3.12.

The finite checkers do not replace Hou--Zhao's analytic theorem, external
mathematical review or formal proof verification. See the
[theorem mapping](DEVELOPMENT_AND_THEOREM.md) for that boundary.
