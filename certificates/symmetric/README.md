# Compact exact symmetric certificate

This package reconstructs and verifies one finite original-symmetric Sidon
smoothing certificate, using Python 3.10+ and the standard library only.
The stronger strict declaration is

```
sqrt(ab) < 471404576987/500000000000 = 0.942809153974.
```

The actual diagnostic value is approximately
`0.9428091539736006311548630428264`. Exact rational comparisons determine
acceptance. The kernels are 1024 nonnegative centered boxes on 2048 bins;
the mixture is positive and normalized, depth is 8, and all 16385 covers
are exactly one. Finite boundary entries may be signed; the tails are
exactly one. [Proof and mathematical scope](PROOF.md).

From the repository root:

```
python -I -S certificates/symmetric/verify.py
python -I -S tests/test_symmetric_public.py
```

The default replay reads only `WITNESS.json` and the standard-library
modules in this package. It does not run an optimizer, need the archived
asymmetric profile, load its common core, or trust saved acceptance flags.
It reconstructs the finite multiplier repair, then independently sums
ordinary centered-box windows of the actual resulting arrays and their
squared entries. All covers, normalization, reflection, unused-prefix
zeros, exact unit tails, positive b and the stronger strict bound are
checked. `EXPECTED_RESULTS.json` is an additional exact reference check,
not the mathematical basis of acceptance.

The compact witness is a lossless mathematical representation of the
large explicit certificate; it contains only dimensions, an exact dyadic
multiplier and provenance hashes. The dense JSON is not needed for replay.
Generate it on demand and independently check the actual file:

```
python -I -S certificates/symmetric/verify.py --export tmp/symmetric_certificate.json --state-dir tmp/symmetric_export
python -I -S certificates/symmetric/verify.py --check-array tmp/symmetric_certificate.json --state-dir tmp/symmetric_actual_array
```

The canonical export has 682492622 bytes and SHA-256
`6fe10ab401d66c1f3e71ec930338374b6c86ba3b4f16d43ffba74c96176c2f3c`.
It has the original symmetric JSON schema and the stronger declaration.
No boundary entry is rounded. Export refuses to replace an existing file
with different bytes. The separate streaming actual-array path uses only
direct box prefixes and exact squared norms; it imports no multiplier or
C-operator helper. It accepts arbitrary root-key ordering and rejects
unknown/duplicate fields, malformed exact values and rational values beyond
the original 4096-bit limit. Its supported model is this centered-box family
with zero unused prefixes, n<=1024 and L<=8.

Long checks emit a JSON heartbeat to stderr at least every ten seconds of
component work. Exact completed-component accumulators persist atomically
under repository-local `tmp/symmetric_replay/` by default; use a dedicated
`--state-dir` for another operation. Latest and previous snapshots are
separate atomic files with input/code identity and checksum validation.
An incomplete check resumes persisted components; a completed prior run
starts a fresh arithmetic replay. An unfinished component or final export
assembly restarts. LAPACK or solver state is neither required nor restored.
`--no-checkpoint` is available for a fresh check without persisted state;
export requires a state directory for its component chunks.

The mathematical result is a new accepted own finite certificate, not a
worldwide record, new smoothing theorem or exact global optimizer. The
separate archived-cover barrier and tight ordinary-dual comparison are
research results discussed in the release notes; this compact replay
verifies the self-contained winning witness. HZ/Akwei/Wu attribution,
AI assistance and the distinction from the older asymmetric result are
recorded in [PROVENANCE.md](PROVENANCE.md). Historical releases are preserved.
