# Independent operator and measure reconstruction

Reviewer: fresh execution-stage operator reviewer. Date: 2026-10-23.
Status: independent lemmas established below; whole lower construction is
pending review of the frozen candidate proof. No numerical feasibility test,
optimizer, FFT, sampled renewal table, or earlier approval report was used.

Primary sources inspected directly: `akwei_limit.txt`, Sections 4 and 7, and
`chen_proof.md`, Sections 2--6, in the preceding finite-grid packet's
`novelty/sources/` directory. These are attributed source ingredients.

## 1. Renewal representatives and usable absolute constants

Write `r` for the uniform-[0,1) renewal density, with the right-continuous
representative, and put

\[
 s_c(t)=\tfrac12r(t)\quad(t\ge0),\qquad s_c(t)=0\quad(t<0),
 \qquad b(t)=s_c(t)-\mathbf1_{[0,\infty)}(t).
\]

The primary source Chen, Lemma 4, gives the following elementary proof rather
than a numerical root location. On successive unit intervals the renewal
recurrence is a probability kernel

\[
 r(n+x)=\int_0^1K_x(y)r(n-1+y)\,dy,\quad
 K_x(y)=e^x-\mathbf1_{y\le x}e^{x-y}.
\]

Its integral is one, it is nonnegative, and it dominates
`(1/2)1_[1/2,1](y)dy`, of mass 1/4. Thus essential ranges are nested and
their lengths contract by 3/4. Initially the range is [1,e]. The exact
potential `h*(r dt/2+delta_0/2)=1_[0,infinity)` identifies the common limit
as 2. Consequently

\[
 |b(t)|\le (3/4)^{\lfloor t\rfloor}\quad(t\ge0),\qquad
 \|b\|_\infty\le\tfrac12,\quad \|b\|_1\le4,
 \quad\int_0^\infty t|b(t)|dt\le16.
\]

The sup bound uses the nested range [1,e] and e<3. The estimates extend to
the specified right-continuous values by continuity away from the known jump.
For L>=1,

\[
 \int_L^\infty |b(t)|dt\le6e^{-\alpha L},\qquad
 |b(t)|\le\tfrac43e^{-\alpha t},\qquad\alpha=\log(4/3).
\]

The atom in `b` is absent: it is a function. Its jumps have magnitudes 1/2
at 0 and 1. On (0,1), `b'=e^t/2`, whose integral is `(e-1)/2<1`.
On (1,infinity), `b'=b(t)-b(t-1)` almost everywhere, whose absolute
integral is at most `2||b||_1<=8`. Hence

\[
 \operatorname{TV}(b)<10,\qquad \operatorname{TV}(s_c)\le11.
\]

The signed measure `tau=delta_0/2+b(t)dt` has total mass 1/3. This follows
independently by the Laplace-transform calculation in Chen, Lemma 5, with
dominated convergence justified by the just-proved L1 bound; in particular
`integral b=-1/6`.

## 2. Whole-identity averaging handles the renewal jump

Set

\[
 A_b(s)=\int_0^\infty b(u)b(u+s)du,\qquad
 C_U(s)=U-s-\tfrac23-2\int_0^s b(u)du+2A_b(s)\quad(s>0).
\]

Translation of a BV function gives
`||b(.+h)-b||_1<=TV(b)|h|`. Therefore `A_b` is Lipschitz with constant
at most `(1/2)*10=5`, and `C_U` is Lipschitz with constant at most
`1+2*(1/2)+2*5=12`, uniformly in U. A proof by integrating the derivative
of `s_c` alone must include its jump at 1; the BV argument includes it.

Akwei, Lemma 7.4, reconstructed algebraically with `tau` above, states

\[
 \mathcal B(s)=\tfrac16-\int_0^s b(u)du+\tfrac12b(s)+A_b(s)
 \le s/2\quad(s>0).
\]

At s=1 the right-continuous value is used, consistent with the negative
jump and the stated inequality. Since `s_c(s)=1+b(s)` for s>0,

\[
 C_U(s)+s_c(s)=U-s+2\mathcal B(s)\le U.
\]

Let Z be any finite mean-zero distribution with `s+Z>0` pointwise. Averaging
the complete inequality and then using the Lipschitz bound gives

\[
 C_U(s)+\mathbb E s_c(s+Z)
 \le U+12\mathbb E|Z|.
\]

For an atom uniformly distributed over the first ell integer sites, its
center is `(ell-1)/2` and its exact normalized shifts are

\[
 Z_j=(j-(\ell-1)/2)/H\quad(0\le j<\ell).
\]

They have mean zero and absolute value strictly less than `ell/(2H)`.
For integer d>=ell/2, `s=d/H` gives `s+Z_j>0`. Thus the averaging error
is at most `6ell/H`. After multiplying by `delta^2 H`, this is
`6delta^2 ell=O(N^-1/2)`, which has the required constant-loss scale.
This proof never Taylor expands through the jump.

This identity by itself does not establish feasibility. It still requires
an exact comparison of discrete continuous/continuous and atom/continuous
sums with `C_U` and the displayed atom average, truncation errors, clipping,
and the opposite-end atom strip. Those obligations belong to the candidate
proof under review.

## 3. Fejer covariance reconstruction

For integer ell, extending a finite vector z by zero and writing B for
convolution with `1_{0,...,ell-1}`, one has

\[
 z^{\mathsf T}\Phi_\ell z=\|Bz\|_2^2/\ell\ge0,
 \qquad \|Bz\|_2\le\ell\|z\|_2.
\]

Thus `0<=Phi_ell<=ell I` on every finite interval. With `delta ell=1`,
`I-delta Phi_ell` is PSD exactly. If `0<=tildepsi<=f<=1` and
`(1-delta)tildepsi^2<=delta(f-f^2)`, the diagonal completion epsilon is
nonnegative and the covariance is PSD. Its diagonal is f. Its off-diagonal
entry is

\[
 f_i f_j-\tilde\psi_i\tilde\psi_j(1-|i-j|/\ell)_+\ge0.
\]

The augmented moment matrix follows by the Schur complement at the positive
upper-left entry 1. None of these arguments assumes a representing
probability measure for the moments.

## 4. Chen upper bound transfers to the precise SDP

Let `(f,Gamma)` be feasible, `kappa=sum f`, and let

\[
 \phi(t)=\begin{cases}4/3-2|t|+(2/3)|t|^3,&|t|\le1,\\0,&|t|>1.
 \end{cases}
\]

For real T>0, `Phi_T(i,j)=phi((i-j)/T)` is the Gram matrix of translates
of the scaled linear kernel, hence PSD, and its entries are nonnegative.
Schur complementation gives `Gamma-ff^T>=0`. Since the trace product of
two PSD matrices is nonnegative,

\[
 f^{\mathsf T}\Phi_T f\le\operatorname{tr}(\Phi_T\Gamma)
 \le\tfrac43\kappa+2\sum_{d\ge1}\phi(d/T)
 \le\tfrac43\kappa+T.
\]

The middle inequality uses the actual noncyclic difference capacities and
the diagonal equations. The last is the monotone right-endpoint integral
estimate; no integer scale or integer mass is required.

For 0<T<=N put `L=N/T>=1` and apply Chen, Lemma 6, to the positive finite
measure `mu=sum_j f_j delta_(j/T)` supported in [0,L]. Its mass is the
real number kappa. The lemma gives

\[
 f^{\mathsf T}\Phi_Tf\ge
 \frac{\kappa^2}{N/T+2/3+200e^{-\alpha N/T}}.
\]

For completeness, its reference measure is the finite signed measure
`nu_L=1_[0,L]dt+tau+reflection_L(tau)`, with mass `L+2/3` and exact
potential `phi*nu_L=1` on the closed interval. Its outside total variation
is at most `12e^{-alpha L}`. Since `||tau||TV<=9/2`, the full potential
has magnitude at most 13, so its energy is at most
`L+2/3+168e^{-alpha L}`. Cauchy in the autocorrelation energy gives the
displayed (slightly weaker) denominator. Signedness of the reference measure
is permitted; positivity is required only for mu, to identify its mass on
the interval. Zero kappa is included without division by kappa.

Therefore, for every real mass and every admissible T,

\[
 \kappa^2\le(N/T+2/3+200e^{-\alpha N/T})(T+4\kappa/3).
\]

This is precisely Chen's scalar inequality. Set `x=N^(1/4)`,
`T=sqrt(2)x^3`, `g=2sqrt(2)/3`, and `epsilon=200exp(-alpha x/sqrt(2))`.
For `N>=4,600,000`, Chen Section 6 establishes, using rational exponential
bounds, that the quadratic

\[
 P_e(z)=z^2-(gx+8/9+4e/3)z-x^4-gx^3-\sqrt2 e x^3
\]

is positive at `y=x^2+gx+1`: specifically
`P_e(y)>(4/1089)x^2>0`. Its constant term is negative, so it has precisely
one positive root. As `P_e(kappa)<=0` and `kappa>=0`, one obtains

\[
 H_2(N)<\sqrt N+gN^{1/4}+1\quad(N\ge4,600,000).
\]

The source's endpoint calculation uses `x>463/10`,
`alpha>719/2500`, `sqrt(2)<99/70`,
`200exp(-alpha(463/10)/sqrt(2))<2/121`, and normalized error
`F(x)<134/121<10/9`. All comparisons are exact rational ones, and the
root argument holds for arbitrary nonnegative real kappa. This is a valid
upper companion for the SDP, independently of the lower ansatz.

For positive integer T the sharper finite sum, reconstructed from sums of
powers through T-1, is

\[
 2\sum_{d\ge1}\phi(d/T)=T-4/3+1/(3T).
\]

This refinement is unnecessary for the +1 upper theorem.

## 5. Current independent disposition

The renewal/BV constants, complete-identity averaging lemma, Fejer PSD
argument, and SDP upper theorem above are established. The lower all-lag
construction and its explicit constants/onset are not yet passed by this
review: the full discrete comparison and parameter receipt remain pending.
No proof-status statement here relies on model agreement.
