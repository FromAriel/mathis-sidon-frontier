# Independent exact replay of the uniform SDP upper bound

Date: 2026-10-23. Disposition: PASS for the upper theorem stated here.
This transfers Chen's positive-measure argument, using Akwei's PSD trace
principle. It does not assume that a feasible pair is realized by a set.

The finite signed comparison-measure and Gram reconstruction are recorded
in `INDEPENDENT_OPERATOR_LEMMAS.md`, Section 4. They establish, for every
feasible SDP mass kappa>=0 and every real 0<T<=N,

\[
 \kappa^2\le(N/T+2/3+200e^{-\alpha N/T})(T+4\kappa/3),
 \qquad\alpha=\log(4/3).
\tag{1}
\]

Here `mu=sum f_j delta_(j/T)` is a finite positive measure supported on the
closed interval [0,N/T]. There is no division by kappa and no integrality
premise for it. The matrix argument is: `Gamma-ff^T` is PSD, the sampled
cubic matrix is PSD, their trace product is nonnegative, and the
nonnegative cubic weights multiply the noncyclic difference capacities.
This proves (1) with exactly the SDP in the frozen statement.

Let `x=N^(1/4)`, `s=sqrt(2)`, `g=2s/3`, `beta=alpha/s`, and
`epsilon=200exp(-beta x)`. For N>=4,600,000 set `T=s x^3`.
The rational number `u=463/10` obeys

\[
 463^4=45,954,068,161<46,000,000,000=10^4(4,600,000),
\]

so x>u>46>s. In particular 0<T<N and (1) applies. Its expansion is

\[
 P_\epsilon(\kappa)\le0,\quad
 P_\epsilon(z)=z^2-(gx+8/9+4\epsilon/3)z
               -x^4-gx^3-s\epsilon x^3.
\tag{2}
\]

At `y=x^2+gx+1`, direct multiplication, using `g^2=8/9`, gives

\[
 P_0(y)=\tfrac{10}{9}x^2+\tfrac g9x+\tfrac19
 \ge\tfrac{10}{9}x^2.
\tag{3}
\]

The following bounds reproduce the source's exact endpoint control rather
than replacing it by a decimal exponential estimate. The substitution
`alpha=2integral_0^(1/7)(1-t^2)^(-1)dt` gives

\[
 \alpha>2(1/7+1/(3\cdot7^3))=296/1029>719/2500.
\]

The last rational inequality is `740000>739851`. Since s<99/70
(`9800<9801`),

\[
 \beta u>\frac{719}{2500}\frac{463}{10}\frac{70}{99}
 >941/100>1.
\tag{4}
\]

The middle comparison is the integer inequality
`2,330,279,000>2,328,975,000`. Positive terms of the exponential series give

\[
 e^3>\sum_{j=0}^9 3^j/j!=22471/1120>1003/50,
\]
\[
 e^{41/100}>1+41/100+(41/100)^2/2+(41/100)^3/6
 =9033221/6000000>3/2.
\]

The rational comparisons are `1,123,550>1,123,360` and
`9,033,221>9,000,000`. Consequently

\[
 e^{\beta u}>e^{941/100}=(e^3)^3e^{41/100}
 >\frac{3\cdot1003^3}{2\cdot50^3}>12100,
 \qquad 200e^{-\beta u}<2/121.
\tag{5}
\]

The penultimate comparison is `3,027,081,081>3,025,000,000`.

Normalize the error term in (2) at y by x^2:

\[
 F(x)=\frac{\epsilon(4y/3+sx^3)}{x^2}
 =200e^{-\beta x}\left(sx+\tfrac43+
       \tfrac{4g}{3x}+\tfrac4{3x^2}\right).
\tag{6}
\]

This is a positive linear combination of `x exp(-beta x)`,
`exp(-beta x)`, `x^(-1)exp(-beta x)`, and `x^(-2)exp(-beta x)`.
All decrease for x>=u: the first derivative has sign `1-beta x<0` by
(4), and each of the other three derivatives is strictly negative.

Also 0<g<1, and exact rational comparisons give

\[
 su<\frac{99}{70}\frac{463}{10}=45837/700<131/2,
\]
\[
 \frac43(1+g/u+1/u^2)
 <\frac43(1+1/46+1/46^2)=721/529<3/2.
\]

Their final comparisons are `45837<45850` and `1442<1587`.
Together with (5), monotonicity of (6) yields

\[
 F(x)\le F(u)<(2/121)(131/2+3/2)=134/121.
\]

Thus (3) implies

\[
 P_\epsilon(y)>
 (10/9-134/121)x^2=(4/1089)x^2>0.
\]

The quadratic in (2) has negative constant term and positive leading
coefficient, hence precisely one positive root. Since kappa>=0 and
`P_epsilon(kappa)<=0`, kappa is at most that root. Since y>0 and
`P_epsilon(y)>0`, y is strictly larger than that root. Therefore

\[
 H_2(N)<\sqrt N+\frac{2\sqrt2}{3}N^{1/4}+1
 \qquad(N\ge4,600,000).
\]

All displayed comparisons are symbolic or integer comparisons. No sampled
scalar check or floating-point feasibility claim is used.
