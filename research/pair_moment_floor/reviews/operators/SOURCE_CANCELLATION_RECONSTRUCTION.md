# Independent reconstruction of the attributed cancellation

Date: 2026-10-23. Source: Akwei, `akwei_limit.txt`, Lemmas 4.1--4.3 and 7.4.
This is an independent analytical reconstruction of the source identity,
not a novelty claim. Let r be the right-continuous uniform renewal density,
g=r-2, and G(t)=integral_0^t g.

The elementary contraction proof recorded in `INDEPENDENT_OPERATOR_LEMMAS.md`
establishes exponential decay and all integrations below. On [0,1),
`r(t)=e^t`; at 1 the density jumps from e to e-1; for t>=1,
`r(t)=integral_(t-1)^t r`. Consequently, distributionally on (0,infinity),

\[
 g'=g-g(\cdot-1)\mathbf1_{[1,\infty)}
      +2\mathbf1_{(0,1)}-\delta_1.
\]

Let `A(t)=integral_0^infinity g(u)g(u+t)du`. For 0<t<1, differentiation
including the displayed atom gives

\[
 A'(t)=A(t)-A(1-t)+2G(1-t)-g(1-t)
       =A(t)-A(1-t)+e^{1-t}+4t-4.
\]

For `D(t)=A(t)-A(1-t)` this implies

\[
 D'(t)=e^t+e^{1-t}-4,
 \quad D(1/2)=0,
 \quad D(t)=e^t-e^{1-t}-4t+2.
\]

It follows that `A'(t)=e^t-2` and `A(t)=e^t-2t+C` on [0,1]. For t>1,
the same differentiation gives `A'(t)=A(t)-A(t-1)`. Define

\[
 F(t)=A(t)-\int_{t-1}^tA(s)ds,
 \qquad J(t)=\int_{t-1}^t(s-t+1)A(s)ds.
\]

Then `F'=0`, `J'=F`. Decay gives first F=0 and then J=0. At t=1,

\[
 0=J(1)=\int_0^1s(e^s-2s+C)ds=1/3+C/2,
\]

so `C=-2/3`, in particular `A(0)=1/3`.

For the cumulative bound `G(t)>=-1`, no numerical renewal theorem is needed.
Let independent uniform-[0,1) increments have partial sums S_n and let
`tau=min{n>=1:S_n>t}`. The local factorial bound for the renewal series
gives `E tau=1+sum_(n>=1)Pr(S_n<=t)<infinity`. Nonnegative summation and
independence of the n-th increment from `{tau>=n}` give
`E S_tau=(1/2)E tau`. Since S_tau>t almost surely, the renewal count
`H(t)=sum_(n>=1)Pr(S_n<=t)` satisfies `H(t)>2t-1`. As H(t)=integral_0^t r,
one has `G(t)>-1`, which is more than the required weak inequality.

Put

\[
 h(s)=2s+2+2G(s)-g(s)-A(s).
\]

For 0<s<1 the formulas above give h(s)=8/3 exactly. At and beyond 1,
`g(s)=G(s)-G(s-1)` with the right-continuous representative, hence

\[
 h(s)=2s+2+G(s)+G(s-1)-A(s).
\]

Since A(s)<=A(0)=1/3 by Cauchy, s>=3/2 gives h(s)>=2s-1/3>=8/3.
For 1<=s<=3/2, one has `r(s)=e^(s-1)(e-s)`, which increases there, so
`g(s)>=e-3` and `G(s)>=3(e-3)/2`. Also G decreases on [0,1/2], giving
`G(s-1)>=e^(1/2)-2`. Therefore

\[
 h(s)\ge4+\tfrac32(e-3)+e^{1/2}-2-\tfrac13>\tfrac83.
\]

The last strict inequality is exact: it is equivalent to
`(3/2)e+sqrt(e)>11/2`; the positive-term exponential series give
`e>8/3` and `sqrt(e)>3/2`, whose sum already gives strictness.
Thus h(s)>=8/3 for every s>=1, including the downward jump of r at 1.

Now `b=g/2` and `tau=delta_0/2+b dt` has mass 1/3. Its one-sided
boundary autocorrelation correction is

\[
 \mathcal B(s)=2/3-[1/2+G(s)/2]+[g(s)+A(s)]/4
              =s/2+(8/3-h(s))/4.
\]

Hence `B(s)=s/2` for 0<s<1 and `B(s)<=s/2` for every s>=1.
The point s=1 uses r(1)=e-1, not its left limit. This completes the
whole-continuum cancellation inequality needed by the discrete centered
averaging argument.
