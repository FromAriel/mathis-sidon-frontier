# Final independent operator/measure review

Date: 2026-10-23. Disposition: **PASS for mathematical correctness of the
frozen theorem and explicit construction**, with the scope described below.

The statement reviewed is

\[
 \sqrt N+\frac{2\sqrt2}{3}N^{1/4}-2572
 \le H_2(N)<\sqrt N+\frac{2\sqrt2}{3}N^{1/4}+1
 \quad\text{for every integer }N\ge2^{60},
\]

where H2 is exactly the noncyclic pair-moment SDP in `STATEMENT.md`.
The fixed parameters are A=512, B=256, B0=1026, D0=514,
`ell=ceil(sqrt(N))+514`, `delta=1/ell`,
`H=floor(sqrt(2)N^(3/4))`, and `beta=1-1026/N^(1/4)`.
The actual density uses the positive part of the full additive renewal
profile and the displayed square-root covariance cap.

I first reconstructed the source operator and measure arguments independently,
without reading earlier approval reports. I then audited all three sections
linked from `FULL_PROOF.md`, including their exact finite constants and lag
domains. No optimizer, FFT, renewal table, numerical feasibility sample,
floating eigenvalue, or earlier agent agreement was used as evidence.

The independent derivations are recorded in:

- `INDEPENDENT_OPERATOR_LEMMAS.md`: renewal/BV controls, complete-identity
  averaging, Fejer PSD, and the positive-measure-to-SDP upper transfer.
- `SOURCE_CANCELLATION_RECONSTRUCTION.md`: the source correlation identity,
  including its jump at 1 and the cumulative renewal estimate.
- `UPPER_BOUND_EXACT_REPLAY.md`: every rational exponential estimate and the
  real-mass quadratic-root argument for the upper bound.

## 1. Renewal and cancellation verdict

The block recurrence is a probability kernel with a common positive part of
mass 1/4. Its essential ranges contract by 3/4 and remain within [1,e].
The source's potential identity, or the explicitly constant weighted moving
integral, identifies the limit as 2. Right-continuous values at the jump
are essential and have been retained.

For `b=(r/2-1)1_[0,infinity)` the bounds
`||b||infinity<=1/2`, `||b||1<=4`, `TV(b)<=10`, and the stated exponential
tails follow analytically. The variation includes both the zero-extension
jump at 0 and the renewal jump at 1. The signed mass is `integral b=-1/6`.

The distributional derivative gives the source autocorrelation formula
`A_g(s)=e^s-2s-2/3` on [0,1] and `A_g(0)=1/3`. The moving jump contributes
the necessary atom during differentiation. The cumulative bound `G>=-1`
follows from nonnegative Fubini at the first uniform-increment passage time.
Those facts prove the whole inequality

\[
 C_U(s)+\sigma(s)=U-s+2\mathcal B(s)\le U\quad(s>0).
\]

`C_U` is Lipschitz with constant 12, by the BV translation estimate. At the
exact discrete shifts `h_j=(j-(ell-1)/2)/H`, the whole inequality can therefore
be averaged before comparing `C_U(s+h_j)` with `C_U(s)`. This gives an error
at most `6ell/H`. All arguments are strictly positive when integer
`d>=ell/2`; no undefined value at zero or Taylor expansion through the
renewal jump is needed. Multiplication by `delta^2 H` makes this an
`O(N^-1/2)` residual, as required.

## 2. Finite comparison, clipping and PSD verdict

`chi_U=[1+b(z)+b(U-z)]1_[0,U]` is nonnegative because both underlying
renewal half-densities are at least 1/2. Its supremum is at most 2 and its
pointwise total variation, including endpoint cuts, is at most 26. Thus
the product variation is at most 104 and the shifted-lattice quadrature
error is at most `104delta^2`.

The quadrature lemma also applies to integrable BV functions such as |b|,
despite its infinite tail: sum the same absolute cell error bound over
finite collections of adjacent cells, then use monotone convergence for
the nonnegative samples and the integrable absolute error. This proves
both convergence of the lattice sum and the same total-variation bound.
Consequently the use of quadrature in D3 is justified.

For `s=d/H`, expansion of the finite autocorrelation gives `C_U(s)` plus
four linear tails, two same-end product tails, and two cross-end products.
Their aggregate bounds are exactly

\[
 (30+4U)e^{-(U-s)/4}.
\]

No positive finite Gram object is replaced by a signed full-line kernel.
For the two atomic strips, at integer `d>=ell/2` the outward atom/chi
orientations vanish exactly. The inward terms have normalization
`beta delta^2 H` times the stated centered empirical average. Their remote
end term has the declared exponential bound. The positive-part repair
occurs only outside the centered core, on at most ell sites, with total
mass at most `(4/3)e^{-U/4}`. Its full uncapped product error is bounded
by the displayed `2||base||infinity E+E^2`, including outward interactions.

With `z=N/H`, the complete exponential errors are at most
`[delta^2 H(32+4z)+8]exp(-z/16)`. The bracket is at most 32 for x>=4,
and `z/16>=x/24`, so `64exp(-x/24)` is conservative.

The clipping argument is valid: on [0,1/2], monotonicity of t(1-t) implies
`tildepsi>=min(psi,delta)`. Thus the L1 loss is at most D1 and the product
loss at most `40delta^2 H`. It enters every pair budget multiplied by the
exact taper w; it is absent when d>=ell. The covariance does not alter f.

The triangular matrix is a normalized box Gram matrix, giving
`0<=Phi_ell<=ell I`. Since `delta ell=1` exactly, the covariance is PSD;
the cap gives a nonnegative diagonal completion. The moment block is PSD
by Schur complementation, its diagonal is f, and off-diagonal entries
are nonnegative. Also `0<=f<1/2`, so every square root is valid.

## 3. Exhaustive pair-budget and constant verdict

All integer lags are covered as follows:

1. `1<=d<ell/2`: coarse profile and atom/bulk errors are at most
   `136w/x`; the hole deficit adds at most `142w/x`.
2. `ell/2<=d<ell`: complete-identity averaging gives
   `S+109/x^2+tail`, and the hole deficit contributes at most `142w/x`.
3. `ell<=d<=floor(N/2)`: w=0 and the same complete-identity bound applies.
4. `floor(N/2)<d<=N-2ell`: there is no atom/atom term, and the budget is
   at most `1/2+68/x<1`.
5. `N-2ell+1<=d<N`: the opposite atom triangle is at most 1/2, the
   continuous overlap at most `8/x^2`, and the atom/bulk contribution
   at most `8/x`; their sum is strictly below 1.

The exact atomic intersection formula is correct, including the start of
the opposite strip and its peak. Cases 1--3 give D13 with A=512>278 and
B=256>109. For x>=32768, `S>=1/2`, `S<=1-514/x^2`,
`Q<=beta^2 S`, and `1-beta^2>=1026/x`. Hence the bracket in D13 is
at most `-1/x`. The elementary fourth-term exponential bound gives

\[
 64e^{-x/24}\le64\,24^5/x^4\le x^{-2},
 \qquad64\,24^5<2^{30}\le x^2.
\]

Thus D13 is at most `1-257/x^2-w/x<1`. All lag capacities hold exactly
for every integer N>=2^60, without sampling any N or d.

## 4. Objective and upper theorem verdict

The mass calculation includes the centered start loss exactly:

\[
 \kappa\ge\delta N-1+\tfrac23\delta H
 -1026\delta H/x-26\delta-12\delta H e^{-U/4}.
\]

At the stated onset the losses are bounded respectively by
515, 1, 1, 2052, 1, 1, totaling 2571. In particular
`U>=x/2` and `e^{-x/8}<=24*8^4/x^4<=x^-2` prove the last tail bound.
The declared Kminus=2572 has one additional unit of slack. Floors,
ceilings, the actual unreduced objective, and the positive-part repair
are included. No unbounded loss remains.

For the upper theorem, the sampled cubic autocorrelation matrix is PSD
and nonnegative. The Schur complement transfers the energy bound to
the trace of Gamma, where the noncyclic capacities apply. Chen's comparison
measure argument accepts any finite positive measure, so it applies to
`sum f_j delta_(j/T)`, of real mass kappa. Its signed comparison measure
is legitimate and has exactly constant potential on the closed support
interval. There is no cardinality or integrality substitution.

The independently replayed real quadratic comparison gives the upper
bound with additive 1 for N>=4,600,000. Every numerical-looking endpoint
in that replay is an exact rational/integer inequality. Since 2^60 is
larger, this supplies the upper half on the frozen onset.

## 5. Objections and final scope

Three presentation objections raised during review have been resolved in
the candidate: the square-root cap is now explicit; the final mass tail
inequality is justified; and the w=0 middle-lag interval is explicitly
listed. The integrable-BV quadrature extension is supplied above and does
not require a new assumption. No unresolved mathematical objection remains
within this operator/measure review.

The earlier lemma note's pending lower-review disposition was an interim
status. This final review supersedes it for the exact frozen statement.
The result is an effective near-extremizer theorem for the specified SDP;
it does not construct Sidon sets or assert realizability of its moments.
This correctness PASS does not decide novelty, priority, publication
readiness, or significance, and does not authorize numerical escalation.

The source construction, renewal identity and covariance ansatz remain
attributed to Akwei; the finite positive-measure upper estimate and the
scalar +1 calculation remain attributed to Chen. The uniform finite
all-lag and constant-loss audit is the claim actually reviewed here.
