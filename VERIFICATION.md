# Verification and reproduction

Python 3.10+; standard library only. No original MathIS checkout, generator,
optimizer, external Python packages or network is required.

```text
python -I -S certificates/finite_grid/verify.py
python -I -S tests/test_finite_grid_public.py
python -I -S tests/test_finite_grid_arrays_public.py
python -I -S certificates/symmetric/verify.py
python -I -S tests/test_symmetric_public.py
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

## Version 1.5.0: compact finite-grid witness

The strongest replay reads `certificates/finite_grid/WITNESS.json`. It
independently checks the directed renewal recurrence and exact reconstruction,
all 122,881 original covering rows, positive b, exact energy and the stronger
declared bound. It needs no numerical solver, earlier multiplier, private
research input, network or third-party Python package. The bundled exact
reference values are compared only after fresh mathematical reconstruction.

The component count is n=K=2048, kernel-array length M=4096 and boundary
depth L=30. Each component has J=M*L=122880 finite boundary coordinates;
the original full array therefore has 251,658,240 finite entries. Invisible
prefixes are fixed zero and every entry from J onward is exactly one. The
source theorem permits real finite boundary signs. Acceptance requires

```text
a = 5592405/4194304
b > 0
all joint covers q=0,...,122880 equal 1
ab < (11785113371/12500000000)^2
0 < 11785113371/12500000000 < 1121/1189.
```

The actual squared coefficient also satisfies the exact integer-square bracket

```text
(0.942809069679958604)^2 < ab < (0.942809069679958605)^2.
```

The decimal bound 0.942809069680 represents the exact rational
11785113371/12500000000. Rounded square-root displays never decide acceptance.
Kernel and mixture normalization, individual reflection, original finite
indices and the final structural cover are part of the checks.

The compact witness stores 80-bit dyadic proposals from a directly enclosed
renewal sequence and the exact widest-box repair. The independently checked
recurrence uses 128 fractional bits with exact integer accumulation and
directed endpoint division. This precision is not an unqualified floating-point
significand claim. A prospective bound including recurrence and proposal error
selected L=30 for the initial Pell benchmark 1121/1189 before constructing the
full point. Exact finite verification then supports the stronger public bound.
The proof and source mapping
are in [certificates/finite_grid/PROOF.md](certificates/finite_grid/PROOF.md).

The original symmetric JSON may be exported into gzip and checked from the
actual array through a separate standard-library streaming implementation:

```text
python -I -S certificates/finite_grid/verify.py --export-gzip tmp/finite_grid.json.gz --state-dir tmp/finite_grid_export
python -I -S certificates/finite_grid/verify.py --check-array tmp/finite_grid.json.gz --state-dir tmp/finite_grid_array
```

The dense representation is large. It is prepared as an optional separate
GitHub release asset; the source archive contains the lossless compact witness
and complete offline reconstruction/export/checking code. Gzip changes storage
only, and decompression yields the original symmetric certificate JSON schema.
The ordinary compact replay does not require downloading the dense asset.

Use a dedicated controlled state directory for each operation. The default
is repository-local `tmp/finite_grid_replay`; an explicit `--state-dir` may
select another directory you control, including another controlled checkout.
Checkpoints bind exact input and code
identities, use atomic latest/previous snapshots and OS exclusivity, and emit
ten-second heartbeats. Interrupted component arithmetic can resume; a completed
prior run starts fresh arithmetic. `--no-checkpoint` disables saved compact
replay state. Resume only private state created by your own replay. Checksums
detect corruption and input/code mismatch; they do not authenticate untrusted
checkpoint contents. Use a fresh state directory or `--no-checkpoint` when
checking inputs without trusted saved work. Streaming parser position is not advertised as a restorable
solver state. Package integrity, fresh arithmetic, optional array verification,
hosted CI and downloaded-archive replay remain separate checks.

The historical replay commands and descriptions below retain their original
version-specific scope. They do not imply v1.5.0 hosted or archive acceptance.

## Version 1.4.0: compact symmetric witness

The new default replay reads `certificates/symmetric/WITNESS.json`, constructs
the fixed centered boxes and exact weights, recovers each finite boundary
through rational full-box residual repair, and checks all 16,385 covers and
the exact energy constants. It does not use the historical two-sided boundary
or a numerical solver. The public witness has
format_version `mathis.sidon.symmetric_compact_witness.v1`, n=1024, L=8,
u_bits=80 and an exact integer multiplier vector. It fixes the stronger public
declaration 471404576987/500000000000. An explicit compact witness path may
be supplied as the positional argument to `verify.py`.

The kernel-array length is M=2048, the component count is R=1024 and each
finite boundary has J=M*L=16384 entries. The structural row q=J is included.
The exact checks require:

```text
a = 1398101/1048576
b > 0
all joint covers q=0,...,16384 equal 1
ab < (471404576987/500000000000)^2
471404576987/500000000000 < 188561854127/200000000000.
```

Kernel normalization, symmetry, nonnegativity, positive normalized weights,
zero unused prefixes and exact unit tails are checked as part of the fixed
representation. Boundary coordinates remain real rational values; they are
not required to be nonnegative by the source theorem. Decimal square roots
are diagnostic and do not decide acceptance.

The following optional commands expose and check the actual original-schema
array rather than only reconstructing it from the compact input:

```text
python -I -S certificates/symmetric/verify.py --export tmp/symmetric_certificate.json
python -I -S certificates/symmetric/verify.py --check-array tmp/symmetric_certificate.json
```

The export is hundreds of megabytes. The direct array route uses a separate
standard-library streaming reader and reconstructs covers and energy from
the actual array. The compact witness is sufficient for the normal replay;
the dense representation need not be stored in a Git checkout. Checkpoints
default to the repository's `tmp/symmetric_replay` directory. Use
`--state-dir PATH` to select a dedicated directory for a replay/export or
direct-array check, or `--no-checkpoint` to disable saved state. Keep the
exact input and configuration fixed on resume.

The compact witness is a lossless mathematical representation of the complete
finite point, with no private baseline input or solver dependency. The
optional dense gzip release asset is separate from Zenodo's compact GitHub
source ZIP. Its uncompressed JSON has 682,492,622 bytes and SHA-256
`6fe10ab401d66c1f3e71ec930338374b6c86ba3b4f16d43ffba74c96176c2f3c`.
The compact source archive remains sufficient to reconstruct and verify the
same mathematical data offline, without downloading the dense asset.

The symbolic argument and precise recovery map are in
[certificates/symmetric/PROOF.md](certificates/symmetric/PROOF.md).
The numerical proposal software is not an acceptance dependency. The default
public replay does not reconstruct the separate historical fixed-cover barrier
or original-QP near-optimality comparison retained in the research record.

The recovery wrapper locates its bundled winning certificate beside its script
when no path is supplied. It runs both the preserved general checker and a
separate direct standard-library checker. Both must accept and agree on exact
a,b,ab and the declared coefficient bound. The wrapper also checks its scoped
manifest and saved exact expected results. No saved acceptance flag replaces
reconstruction.

## Historical R9/R16 and two-sided checks

The preserved two-sided general module checks normalized nonnegative kernels, normalized nonnegative
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

The v1.3.0 recovery certificate has m=1024, L=8, right boundary identically one
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

The v1.4.0 symmetric subset has its own exact compact witness, replay tools,
expected results, proof/provenance guide and scoped integrity manifest. Its
public replay is a new standard-library implementation of the finite fixed
construction; the historical checkers and packages retain their bytes and
documented scope. No private correspondence, historical runtime database,
unpublished candidate collection or third-party manuscript copy is needed.

The additive v1.5.0 finite-grid subset has its own WITNESS.json, exact expected
results, proof, prediction receipt, separate compact/array checking code,
reproducible exporter and scoped manifest. It does not widen or replace the
preserved v1.4.0 checker's accepted envelope. Every older mathematical file,
expected output and subset manifest retains its historical bytes.

The original R9/R16 hashes remain in the development note. Git intentionally
exports VERIFY_WINDOWS.cmd with CRLF under .gitattributes. All proof-bearing
certificate and checker bytes must otherwise match manifests exactly.

[The theorem mapping](DEVELOPMENT_AND_THEOREM.md) distinguishes finite checking
from its Hou--Zhao/Akwei analytic dependency. The O(1) term depends on the fixed
certificate data. Finite checking does not establish external peer review,
significant generic-method novelty, a current record, exponent advance or a
full solution. Hosted CI and release/archive validation are separate checks.

Version 1.4.0 was published October 23, 2026, at
[DOI 10.5281/zenodo.23592514](https://doi.org/10.5281/zenodo.23592514), under
[concept DOI 10.5281/zenodo.23439039](https://doi.org/10.5281/zenodo.23439039).
The downloaded Zenodo source ZIP has 688,823 bytes, advertised MD5
`5a57d81b03a3c5d4e7779b7ecb9af723` and SHA-256
`7a6fe534ddcee0181b1352d3ba30e5951bbc258404d67b5cdef71e74d9a5606a`.
Its 52 source files match the actual tag's mathematical bytes; the historical
Windows launcher has the documented CRLF export transformation above.
The actual [main hosted run](https://github.com/FromAriel/mathis-sidon-frontier/actions/runs/39936375949)
and [tag hosted run](https://github.com/FromAriel/mathis-sidon-frontier/actions/runs/39936436894)
each passed all four jobs. All eight verification commands passed from the
downloaded Zenodo extraction: R9, R16, all seven historical two-sided
certificates, the recovered certificate, the symmetric witness, and the
three public test suites with 10, 9 and 13 tests respectively. The fresh
symmetric replay took approximately 303 seconds and verified all 16,385
covers exactly one, exact energy and the stronger strict coefficient bound.
These are completed archive replays in addition to the hosted checks.

Version 1.5.0 is prepared for publication on October 23, 2026. Its new version
DOI is pending; the existing concept DOI identifies the release series.
Fresh v1.5.0 hosted checks and actual downloaded-archive identity/replay will
be reported after completion. The v1.4.0 archive sizes, hashes and completed
checks above remain historical evidence for v1.4.0.
