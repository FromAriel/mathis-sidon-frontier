# 1. Renewal, cancellation and the finite moment model

Candidate proof; independent reconstruction and final disposition required.
The construction and the all-lag renewal inequality are attributed to Akwei.
This section includes the dependencies explicitly rather than treating an
earlier review verdict as a mathematical premise.

## 1.1 Renewal bounds with explicit constants

Let U be uniform density on [0,1), and let
M=delta_0+sum_{m>=1}U^{*m}=delta_0+r(t)dt. Local convergence follows from
U^{*m}(t)<=t^{m-1}/(m-1)!. Use right values at all jumps. Then

\[
 r(t)=e^t\ (0\le t<1),\quad
 r(t)=e^t-te^{t-1}\ (1\le t<2),\quad
 r(t)=\int_{t-1}^t r(s)ds\ (t\ge1).
\]

The only value jump on the positive half-line is -1 at t=1. Comparison in
the Volterra equation, followed block by block, gives 1<=r<=e. For completeness,
if f(z)=r(m-z), the next block has the averaging representation

\[
 r(m+y)=\int_0^1 q_y(z)f(z)dz,\quad
 q_y(z)=\mathbf1_{y+z\le1}+
 \int_{\max(0,y+z-1)}^y e^s ds,\quad 0\le y\le1.
\]

Indeed write B(y)=int_0^{1-y}f and solve the scalar Volterra equation
r(m+y)=B(y)+int_0^y r(m+s)ds. Interchanging its bounded integrals gives q.
Its mass is one and q_y>=1/2 on [0,1/2]. Subtract that common mass 1/4:
successive closed block ranges are nested and their oscillations contract
by 3/4. The invariant int_{t-1}^t(s-t+1)r(s)ds=1, obtained by differentiation,
identifies the common limit as 2. Consequently

\[
 |r(t)-2|\le(e-1)(3/4)^{\lfloor t\rfloor}.
\]

Define b(t)=(r(t)-2)/2 for t>=0 and zero for t<0, and
sigma(t)=r(t)/2 for t>=0 and zero otherwise. The bounds we use are

\[
 \|b\|_\infty\le\tfrac12,\quad \|b\|_1\le4,\quad
 \operatorname{TV}(b)\le10,\quad
 |b(t)|\le\tfrac43 e^{-t/4}\ (t\ge0),\quad
 \int_v^\infty|b(t)|dt\le6e^{-v/4}.
\tag{R1}
\]

For total variation, jumps at zero and one contribute 1 in total, regular
variation on (0,1) is (e-1)/2<1, and b'=b(t)-b(t-1) on (1,infinity) gives
remaining variation at most 2||b||1<=8. The exponential estimate uses e<3,
log(4/3)>1/4 and (3/4)^floor(t)<=(4/3)e^{-t log(4/3)}.

## 1.2 Mass and complete all-lag cancellation

Put g=2b on [0,infinity), G(t)=int_0^t g, and
A_g(s)=int_0^infinity g(t)g(t+s)dt. The following source identities are
reconstructed as follows. The Laplace transform

\[
 \widehat r(z)=\frac{1-e^{-z}}{z-1+e^{-z}}
             =\frac2z-\frac13+O(z)
\]

and exponential integrability of g imply int g=-1/3, hence int b=-1/6.
Differentiating A_g while retaining the moving jump at t+s=1 gives, for
0<s<1,

\[
 A_g'(s)=A_g(s)-A_g(1-s)+e^{1-s}+4s-4.
\]

Subtract the equation at 1-s to obtain
A_g(s)-A_g(1-s)=e^s-e^{1-s}-4s+2. Thus A_g'=e^s-2 and
A_g(s)=e^s-2s+C. On s>1 the same split-jump differentiation gives
A_g'=A_g(s)-A_g(s-1). Its decaying solution has
int_0^1 s A_g(s)ds=0: the derivatives of
A_g(t)-int_{t-1}^t A_g and int_{t-1}^t(s-t+1)A_g(s)ds are respectively
zero and the former invariant, and decay makes both invariants zero.
Therefore C=-2/3 and A_g(0)=1/3. In particular ||b||2^2=1/12.

Also G(t)>=-1. If T is the first uniform-increment sum exceeding t, its
finite mean follows by comparison with the waiting time for sufficiently
many increments >=1/2. Nonnegative Fubini gives E(sum_{j<=T}U_j)=E(T)/2>t;
the renewal function is E(T)-1. This proves the claimed bound on G.

Define

\[
 h(s)=2s+2+2G(s)-g(s)-A_g(s).
\]

The explicit formulas above give h=8/3 on 0<s<1. For s>=1, the renewal
equation gives g(s)=G(s)-G(s-1), so
h=2s+2+G(s)+G(s-1)-A_g(s). Cauchy-Schwarz gives A_g(s)<=1/3. If s>=3/2,
G>=-1 proves h>=8/3. On 1<=s<=3/2, r is increasing, g>=e-3,
G(s)>=3(e-3)/2, and G(s-1)>=sqrt(e)-2. Hence
h>=3e/2+sqrt(e)-17/6>8/3, using e>8/3 and sqrt(e)>3/2. Right values
at s=1 obey this inequality.

Writing A_b(s)=int_0^infinity b(t)b(t+s)dt, this is exactly

\[
 \mathcal B(s)=\frac16-\int_0^s b(t)dt+rac12b(s)+A_b(s)
 \le\frac s2\qquad(s>0).
\tag{R2}
\]

It is essential to retain the whole inequality (R2) through the value jump.
Furthermore translation of a BV function gives Lip(A_b)<=||b||infty TV(b)<=5.
For every U define

\[
 C_U(s)=U-s-\frac23-2\int_0^s b(t)dt+2A_b(s).
\]

It has Lipschitz constant at most 12 on s>0 and, by (R2),

\[
 C_U(s)+\sigma(s)=U-s+2\mathcal B(s)\le U.
\tag{R3}
\]

## 1.3 Finite construction and PSD

Let x=N^(1/4), ell=ceil(x^2)+514, delta=1/ell,
H=floor(sqrt(2)x^3), beta=1-1026/x and c=(ell-1)/2. For j=0,...,N-1,
put u_j=(j-c)/H, v_j=(N-1-j-c)/H and

\[
 \psi_j=\delta[\sigma(u_j)+\sigma(v_j)-1]_+,\quad
 \alpha_j=\frac{\beta\delta H}{2\ell}
 \mathbf1_{j<\ell\ \mathrm{or}\ j\ge N-\ell},\quad f_j=\psi_j+\alpha_j.
\]

Use the exact square-root cap

\[
 \widetilde\psi_j=\min\left\{\psi_j,
 \sqrt{\frac{\delta(f_j-f_j^2)}{1-\delta}}\right\},\qquad
 \epsilon_j=f_j-f_j^2-\frac{1-\delta}{\delta}\widetilde\psi_j^2.
\]

For x>=32768,
0<delta<1, 1/2<=beta<=1, N>=8ell and H>=ell. The profile satisfies
psi<=2delta, alpha<=1/x, so f<=2/x^2+1/x<1/2.
The cap is well-defined, nonnegative, <=psi<=f, and epsilon>=0.

The triangular Toeplitz matrix Phi_ell has Fejer symbol
ell^{-1}|sum_{a=0}^{ell-1}exp(ia theta)|^2 in [0,ell]. Thus
0<=Phi_ell<=ell I and I-delta Phi_ell>=0 exactly. Setting
D_jj=tildepsi_j/sqrt(delta) yields
Gamma=ff^T+D(I-delta Phi_ell)D+diag(epsilon). Its Schur complement is PSD,
its diagonal is f, and off-diagonal entries are nonnegative because
tildepsi<=f and 0<=Phi_ell<=1 entrywise. Hence every SDP condition except
the separate difference budgets is already proved. Those budgets are
established in ALL_DISTANCE_ESTIMATE.md.
