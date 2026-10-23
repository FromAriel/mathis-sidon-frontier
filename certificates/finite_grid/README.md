# Exact finite-grid symmetric certificate

Version 1.5.0 adds one fixed rational certificate with

    sqrt(ab) < 11785113371/12500000000 = 0.942809069680.

It has n=K=2048 centered uniform boxes, kernel length M=4096, boundary depth
L=30 and J=122880 finite boundary coordinates per component, for 251658240
finite entries across the complete original array. Every original covering row
q=0,...,J equals one exactly. Kernels and mixing weights are nonnegative and
normalized; each kernel is reflected, unused boundary prefixes are zero and
boundary tails are exactly one. Invisible prefixes are fixed zero; the remaining
free boundary coordinates are real rationals.

The exact coefficient is bracketed by

    0.942809069679958604 < sqrt(ab) < 0.942809069679958605.

The initial Pell benchmark1121/1189 is also strictly beaten. It is an exact
benchmark, not an asserted extremal constant or a new Pell-equation result.

## Verify offline

Python3.10 or newer; standard library only. From the extracted repository:

```text
python -I -S certificates/finite_grid/verify.py
python -I -S tests/test_finite_grid_public.py
python -I -S tests/test_finite_grid_arrays_public.py
```

The compact witness is lossless: it stores the exact dyadic renewal proposal
and rational widest-box repair needed to reconstruct every original array.
The checker independently replays the directed recurrence, factor identities,
every finite cover and exact a,b,ab. No optimizer, private input, network or
external package is needed. Saved reference results never substitute for
mathematical reconstruction.

The original symmetric JSON can also be exported directly into a gzip
container and verified through a separate actual-array implementation:

```text
python -I -S certificates/finite_grid/verify.py --export-gzip tmp/finite_grid.json.gz --state-dir tmp/finite_grid_export
python -I -S certificates/finite_grid/verify.py --check-array tmp/finite_grid.json.gz --state-dir tmp/finite_grid_array
```

The dense representation is large. It is an optional GitHub release asset;
the Zenodo GitHub source archive contains this compact certificate, complete
reconstruction/export tools and independent exact-array checker. The compressed
asset does not need to be downloaded for the ordinary compact replay.
The gzip changes storage only; decompression yields the original symmetric
JSON schema, not a replacement production certificate format.

Use a separate controlled state directory for each operation. Defaults stay
under the repository-local `tmp/finite_grid_replay` tree; an explicit
`--state-dir` may select another directory you control, including another
controlled checkout. Checkpoints use atomic latest/previous snapshots,
input/code identities, OS exclusivity and ten-second heartbeats. Interrupted
component arithmetic can resume; a completed prior run starts fresh arithmetic.
Resume only private state created by your own replay. Checksums detect damage
and input/code mismatch; they do not authenticate checkpoint contents supplied
by someone else. Use a fresh state directory or `--no-checkpoint` for fresh
arithmetic without trusted saved work. Streaming parser state is not represented
as restorable solver state.

## Exact grid and boundary interpretation

For these fixed kernels and original mixture weights, the accompanying
analysis gives

    a_n = 4/3 - 1/(3n^2),
    beta_infinity,n = 2/3 + 1/(3n^2),
    a_n beta_infinity,n = 8/9 + 2/(9n^2) - 1/(9n^4).

Finite equality and inequality minima are treated separately. Both converge
nonincreasingly to the half-line value as depth increases; each finite-depth
minimum is strictly larger when n>=2. At n=1 all these values are one.
For the prescribed n1024 family, the limiting product already exceeds the
Pell target squared, so increasing depth alone cannot reach it. With n2048
fixed, an explicit rational error bound selects L30 for that initial Pell
benchmark before construction. Exact finite verification supports the stronger
public decimal bound.

The actual finite correction b-2796203/4194304 is positive, approximately
6.6727480930988364e-46. Exact values are in WITNESS.json and EXPECTED_RESULTS.json.
The special-family proof and prospective error calculation are in
[PROOF.md](PROOF.md) and PREDICTION.json. No global optimality over other kernels
or mixtures follows from the fixed-family calculation.

## Attribution and scope

Hou--Zhao provides the original finite symmetric framework and its fixed-data
Sidon consequence. Akwei's ramp/renewal analysis, approximate finite-grid
formula and quantitative/localized repair motivate this effective
specialization. Renewal, spectral factorization, coefficient root exclusion
and finite filter repair are established methods. See [PROVENANCE.md](PROVENANCE.md).

This is an attributed software, certificate-data and verification release.
Internal proof reconstructions and exact software checks are distinct from
external peer review or formal proof verification. The release claims no new
universal floor, worldwide record, exponent improvement or solution of
Erdos Problem30. A standalone-manuscript significance recommendation has not
been established. AI-assisted computation, software, drafting and review are
disclosed. All earlier certificate packages and releases remain preserved.
