# Frozen execution statement

Date: 2026-10-23. Initial status: candidate theorem under independent review.
The approved slice is analytical. No numerical campaign is included.

Let H2(N) be exactly Akwei Definition 7.2: maximize kappa=sum f_j on
0<=j<N subject to the PSD block [[1,f^T],[f,Gamma]], Gamma_jj=f_j,
0<=f_j<=1, Gamma_ij>=0, and sum_{j=0}^{N-1-d}Gamma_{j,j+d}<=1 for every
integer 1<=d<N. Indices are noncyclic. No additional pair inequalities are
imposed.

The submitted candidate effective theorem is

\[
 \sqrt N+\frac{2\sqrt2}{3}N^{1/4}-2572
 \le H2(N)<\sqrt N+\frac{2\sqrt2}{3}N^{1/4}+1
 \quad\text{for every integer }N\ge2^{60}.
\]

Constants in the structured proof are A=512, B=256, B0=1026, D0=514.
For x=N^(1/4), set ell=ceil(sqrt N)+514, delta=1/ell,
H=floor(sqrt(2)N^(3/4)), beta=1-1026/x. Use the full uniform-renewal
density, right values at its jump, the positive-part additive profile, the
centered uniform endpoint atoms, and Akwei's capped Fejer covariance.

The intended lower theorem proves an explicit feasible moment pair. It does
not construct a Sidon set or an original-format rational smoothing witness.
The upper theorem is an attributed extension of Chen's positive-measure
energy estimate by Akwei's PSD trace principle.

The full candidate proof is assembled in FULL_PROOF.md. A candidate statement
is not acceptance. Reviews, objections, final correctness and novelty decisions
must be read before quoting this theorem as a completed result.

Scope exclusions: no optimizer, sampled feasibility, FFT, renewal table,
flagship replay, new certificate, public release, Git write, contact,
circulation or submission. Exact symbolic arithmetic and source/metadata
checks are allowed. Production interfaces and earlier evidence stay fixed.
