# Verification and reproduction

Python 3.10+; standard library only. No original MathIS checkout, generator,
optimizer, external Python packages or network is required.

```text
python -I -S verify.py CERTIFICATE.json
python -I -S certificates/r16/verify.py
python -I -S certificates/two_sided/verify.py --all
python -I -S tests/test_two_sided_public.py
```

Run these from the extracted root. --all finds files beside its script. An
explicit relative certificate path is relative to the invoking directory.
Absolute script/certificate paths work from an unrelated directory with -I -S.

## Exact checks

The new module checks normalized nonnegative kernels, normalized nonnegative
mixing, joint left covers against each kernel and joint right covers against
its reversal, every q=0,...,Lm row and fixed-one tails. Boundary coordinates
may be zero or negative. It reconstructs a,b,ab exactly, requires b>0 and a
positive declared coefficient, then checks ab < declared_bound^2 strictly.
Decimal square roots are diagnostic only.

Exit codes are 0 accepted, 1 mathematically rejected, 2 malformed input/usage.
The --all wrapper additionally checks its scoped manifest and expected exact
results. Original R9/R16 outputs and commands remain unchanged.

Tests exercise strictness, invalid declared bounds, malformed arrays, both
ends, tails, signed boundary coordinates, joint mixtures, old/new formula
equivalence and CLI exits. Finite tests do not verify an analytic theorem.

## Integrity and provenance

RELEASE_MANIFEST.json inventories all payload files except itself. R16's
manifest retains its historical four-member scope. The new two-sided manifest
binds its seven certificates, module/wrapper, expected results and guide,
excluding itself. The module is a byte-identical copy of the corrected research
checker; all seven certificate JSON files preserve their input bytes.

The original R9/R16 hashes remain in the development note. Git intentionally
exports VERIFY_WINDOWS.cmd with CRLF under .gitattributes. All proof-bearing
certificate and checker bytes must otherwise match manifests exactly.

[The theorem mapping](DEVELOPMENT_AND_THEOREM.md) distinguishes finite checking
from its Hou--Zhao/Akwei analytic dependency. The O(1) term depends on the fixed
certificate data. No novelty, record, exponent advance or full solution follows.
