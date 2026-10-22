# Verification and reproduction

Python 3.10+; standard library only. No original MathIS checkout, generator,
optimizer, external Python packages or network is required.

```text
python -I -S verify.py CERTIFICATE.json
python -I -S certificates/r16/verify.py
python -I -S certificates/two_sided/verify.py --all
python -I -S certificates/two_sided_recovery/verify.py
python -I -S tests/test_two_sided_public.py
python -I -S tests/test_two_sided_recovery_public.py
```

Run these from the extracted root. --all finds files beside its script. An
explicit relative certificate path is relative to the invoking directory.
Absolute script/certificate paths work from an unrelated directory with -I -S.

The recovery wrapper locates its bundled winning certificate beside its script
when no path is supplied. It runs both the preserved general checker and a
separate direct standard-library checker. Both must accept and agree on exact
a,b,ab and the declared coefficient bound. The wrapper also checks its scoped
manifest and saved exact expected results. No saved acceptance flag replaces
reconstruction.

## Exact checks

The preserved general module checks normalized nonnegative kernels, normalized nonnegative
mixing, joint left covers against each kernel and joint right covers against
its reversal, every q=0,...,Lm row and fixed-one tails. Boundary coordinates
may be zero or negative. It reconstructs a,b,ab exactly, requires b>0 and a
positive declared coefficient, then checks ab < declared_bound^2 strictly.
Decimal square roots are diagnostic only.

The historical general checker's exit codes are 0 accepted, 1 mathematically
rejected and 2 malformed input/usage. The new recovery wrapper exits 0 only
when accepted below the fixed benchmark; exit 1 also covers benchmark failure
or checker disagreement, while exit 2 includes malformed input, usage and
package-integrity failures. The historical wrapper checks its scoped manifest
and expected results with `--all`; the recovery wrapper checks them on every
invocation. Original R9/R16 outputs and commands remain unchanged.

Tests exercise strictness, invalid declared bounds, malformed arrays, both
ends, tails, signed boundary coordinates, joint mixtures, old/new formula
equivalence and CLI exits. Finite tests do not verify an analytic theorem.

The new recovery certificate has m=1024, L=8, right boundary identically one
and the unchanged asymmetric ramp. Expected acceptance requires all 8,193
left and 8,193 right covers, including the final structural rows, positive
a,b and declaration, and the strict rational comparisons

```text
ab < (188561854127/200000000000)^2
0 < 188561854127/200000000000 < 942809522/1000000000.
```

The independent checker is intentionally restricted to this one-ramp/right-ones
class. The preserved general checker continues to handle its documented joint
mixtures and signed real boundary coordinates. A restrictive independent
checker does not narrow the general source theorem or certificate schema.

## Integrity and provenance

RELEASE_MANIFEST.json inventories all payload files except itself. R16's
manifest retains its historical four-member scope. The new two-sided manifest
binds its seven certificates, module/wrapper, expected results and guide,
excluding itself. The module is a byte-identical copy of the corrected research
checker; all seven certificate JSON files preserve their input bytes.

The recovery subset has its own manifest and a byte-identical copy of the
previously inspected independent research checker. The new certificate preserves
its source bytes; the public wrapper adds invocation and consistency checks,
without introducing a new mathematical verifier. The full numerical campaign,
runtime checkpoints, private reviews and source-paper copies are not bundled.

The original R9/R16 hashes remain in the development note. Git intentionally
exports VERIFY_WINDOWS.cmd with CRLF under .gitattributes. All proof-bearing
certificate and checker bytes must otherwise match manifests exactly.

[The theorem mapping](DEVELOPMENT_AND_THEOREM.md) distinguishes finite checking
from its Hou--Zhao/Akwei analytic dependency. The O(1) term depends on the fixed
certificate data. No novelty, record, exponent advance or full solution follows.
