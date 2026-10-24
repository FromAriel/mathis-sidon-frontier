# Effective sharpness of the specified pair-moment relaxation

Candidate submitted for independent execution-stage review, 2026-10-23.
Read FINAL_ASSESSMENT.md when present for acceptance and scope.

The frozen theorem and exact model are in [STATEMENT.md](STATEMENT.md).
The proof is composed, in dependency order, of:

1. [Renewal, complete cancellation and finite PSD model](proof/RENEWAL_AND_MODEL.md).
2. [Structured all-distance estimate and exact parameter absorption](proof/ALL_DISTANCE_ESTIMATE.md).
3. [Constant-loss objective and attributed uniform upper companion](proof/OBJECTIVE_AND_UPPER.md).

The candidate constants are A=512, B=256, B0=1026, D0=514,
K_minus=2572, K_plus=1 and N0=2^60. The construction is implicit and analytic,
using the full renewal density, not a sampled recurrence table. No numerical
campaign, solver, FFT or flagship verification is part of this proof.

Source attribution: Akwei Definition 7.2, Lemmas 7.4-7.5 and Conjecture 7.7
provide the model, cancellation, covariance ansatz and target. Chen provides
the finite-positive-measure comparison and explicit scalar upper bound.
The specific new proof obligation is the uniform lower construction and
its finite, all-distance, constant-loss accounting. Correctness, novelty
and publication significance have separate final decisions.
