# Recovered m=1024, L=8 exact certificate

This additive v1.3.0 package contains one finite rational certificate proving

\[
\sqrt{ab}<188561854127/200000000000=0.942809270635<0.942809522.
\]

The last number is the fixed reported Akwei comparison, not a claim about an
exhaustive current-results catalogue. The earlier seven-certificate directory
and its checker remain unchanged.

## Verify

Python 3.10 or newer, standard library only. From the repository root:

```text
python -I -S certificates/two_sided_recovery/verify.py
python -I -S tests/test_two_sided_recovery_public.py
```

The replay wrapper locates its bundled certificate, two checkers, manifest and
exact expected results beside the script. It works from an unrelated working
directory when invoked with an absolute script path. No MathIS installation,
network, numerical solver or generation checkpoint is needed.

An optional certificate path is relative to the current working directory.
It runs both checkers and the same fixed comparison, after checking package
integrity. Only the bundled winner is compared with its bundled reference
results. A mathematically feasible alternative that does not strictly beat
0.942809522 is reported separately as a benchmark failure.

Exit codes: 0 accepted and beats the fixed comparison; 1 mathematical rejection,
benchmark failure or disagreement; 2 malformed input or package-integrity
failure. Normative results are exact rational strings, without a floating-point
square-root diagnostic.

## Two existing checking implementations

`smoothing_verify.py` is the unchanged general research checker, also preserved
in the v1.2.0 package. `independent.py` is the unchanged independent primal
checker, not the dual-bound checker used in the research campaign. Their source
hashes are recorded in PROVENANCE.md and MANIFEST.json.

The independent checker's advertised domain is one exact asymmetric linear
ramp, mixing weight one and right boundary `"ones"`. It reconstructs all 8193
original left covering conditions, including the structural final row. It
verifies all 8193 right conditions through the exact reversed-kernel and
normalized all-ones identity. These are 16386 covering obligations; the right
side is not claimed to be individually enumerated. Boundary coordinates may
be real rationals of either sign.

Both implementations reconstruct exact a,b,ab, require a positive declared
bound and strict ab<C^2, and the wrapper compares their results. The independent
checker separately reports whether C<942809522/10^9; the release wrapper
requires that comparison to pass. Saved success flags and solver status cannot
substitute for these checks.

## Provenance and limits

Akwei supplied the asymmetric extension, ramp/renewal construction and cited
finite theorem; Hou--Zhao supplied the smoothing lineage. Ariel M. Williams
directed this AI-assisted finite construction, recovery, implementation and
review. The winning numerical point came from sparse lifted primal
`trust-constr` refinement and exact direction/uniform-lift recovery. Its saved
best point was selected after a deliberate early stop, not a claim of solver
convergence. No numerical producer is bundled.

The [theorem mapping](../../DEVELOPMENT_AND_THEOREM.md) states the analytic
dependency and fixed-data asymptotic scope. Exact finite checking does not
formally verify that analytic theorem and is not external peer review. This
package claims neither a worldwide record, optimality, a new analytic theorem,
continuum or signed-C5 attainment, nor an exponent improvement or solution of
Erdos Problem 30. Our artifacts retain the repository's MIT license.
