# Independent finite reconstruction

Date: 2026-10-23. Reviewer: fresh finite/error execution reviewer.
Scope: analytical reconstruction only; no campaign, sampling, FFT, optimizer,
renewal table, application, or Git mutation was used.

This is an independent derivation, not an acceptance of a packet not yet
received. Its remaining input is the operator-side renewal package stated
below. Once that package is independently proved, the constants in this note
are absolute. Earlier approval reports were not consulted.

## 1. Renewal input and conventions

Write b(t)=r(t)/2 for t>=0, b(t)=0 for t<0, and h=b-1 on [0,infinity).
Use the right-continuous renewal density corresponding to U=1_[0,1).
The required input is

- 1<=r<=e; integral h=-1/6; ||h||infinity<=1/2;
- |h(t)|<=4 exp(-t/3), J=||h||1<=12, Vh=TV(h)<26;
- A(s)=integral_0^infinity h(u)h(u+s)du;
- F0(s)=-s-2/3-2 integral_0^s h+2A(s)+b(s)<=0, s>=0.

The last identity is exactly the source's Lemma 7.4, with its value at zero
understood as the right limit. At s=0 it also follows from integral h^2=1/12
and b(0)=1/2. The renewal density has a downward jump of size 1 at t=1.
Consequently b(v)<=b(u)+(e/2)(v-u) for 0<=u<=v: derivatives are bounded above
by e/2 and its only positive-argument jump is downward. This one-sided
estimate, rather than a Taylor expansion through t=1, is essential.

A possible elementary proof of the explicit tail is the residual-life
Doeblin argument. Its transition after time 2, from any initial residual
z in [0,1], has density at least 1-y=(1/2)pi(y), where pi(y)=2(1-y).
Indeed a fresh process after u>=1 has residual density
integral_(u+y-1)^u r(s)ds >=1-y. Invariance of pi and contraction give total
variation at most 2^(-floor(t/2)). The expected renewal count in the next
unit, conditional on residual y, is exp(1-y); its pi-mean is 2 and its range
is [1,e]. Since r(t+1) is that expected count, the asserted tail follows.
This argument still requires a formal operator-side audit of the residual
process and its invariant law; it is not numerical renewal evidence.

## 2. Frozen finite objects

Let x=N^(1/4), ell=ceil(sqrt(N))+D0, delta=1/ell,
H=floor(sqrt(2)N^(3/4)), c=(ell-1)/2, and beta=1-B0/x. Put

q_j=[b((j-c)/H)+b((N-1-j-c)/H)-1]_+,
psi_j=delta q_j,
alpha_j=a 1_{j<ell or j>=N-ell}, a=beta delta H/(2ell), f=psi+alpha.

The source cap is psiTilde=min(psi,sqrt(delta(f-f^2)/(1-delta))).
All statements below use this actual repaired profile.

For intermediate calculations put v_j=b((j-c)/H)-1, j>=0, and define the
continuous v_a(u)=b(u-a0)-1 on u>=0, a0=c/H. Its total variation Vv satisfies
Vv<=1/2+Vh<27, its supremum in absolute value is at most 1, and

K=sum_(j>=0)|v_j| <= c+1+HJ+Vv.

For the explicit onset below, H>=ell, H>=28, and K<=14H.

At least one boundary argument is far from zero. The tail estimates in
section 5 imply q_j<=M=7/5 everywhere, and the only possible changes caused
by positivity repair occur where j<c or N-1-j<c. Each such change has
absolute size at most T=4 exp(-x/48), and their total is at most ell T.
Interior positivity follows from b>=1/2 and the far-end tail <=T<1/25.

## 3. Exact atom supports

For every integer 1<=d<N, assuming N>=2ell,

sum_j alpha_j alpha_(j+d)
 =a^2 {2(ell-d)_+ + [ell-|N-d-ell|]_+}.

The second term vanishes for d<=N-2ell and has maximum a^2 ell at
d=N-ell. It is the entire opposite-end atom contribution. All atom/bulk
terms are bounded above by 2 beta M delta^2 H, without any assumption on d.

For d<=N/2, the atom/bulk contribution is exactly

2a delta {sum_(j=0)^(ell-1) q_(j+d)
          +1_(d<ell) sum_(j=0)^(ell-d-1)q_j}.

The second term is at most M beta delta^2 H w, where w=(1-d/ell)_+.
The first term is beta delta^2 H times the average of the indicated q's.

## 4. Cancellation through the renewal jump

For s=d/H>=a0, direct splitting at u=a0 gives

E_a(s)=4 integral v_a-2 integral_0^s v_a
       +2 integral_0^infinity v_a(u)v_a(u+s)du
      =-2/3-2a0-2 integral_0^s h+2A(s).

In particular translating the continuous profile is charged explicitly;
there is no Taylor expansion through either the atom or the renewal jump.
Let t=s-a0>=0. Since ||h||infinity<=1/2 and
|A(s)-A(t)|<=Vh |s-t|/2,

-s+E_a(s)+b(t) <=F0(t)+(Vh-2)a0 <=(Vh-2)a0.

For the primary atom/bulk average, all its arguments are nonnegative and
the downward-jump inequality gives

(1/ell)sum_(j<ell)b((d+j-c)/H) <= b(t)+(e/2)a0.

Thus the combined continuous error is at most (Vh+2)c, in unscaled pair
units. This is O(ell), hence delta^2 times it is O(x^-2), uniformly through
d near H. An absolute two-sided approximation to the ideal atom term would
have an O(delta^2 H) error at this jump; that stronger approximation is not
used or claimed.

For any integrable BV function p, the left-grid quadrature error is at most
TV(p). Applying this to v_a, its partial integral, and
v_a(u)v_a(u+s), whose variation is at most 2Vv, bounds the error in
4 mass -2 cumulative +2 autocorrelation by 10Vv. This includes integer and
half-integer c, right-continuous jump samples, and d immediately adjacent to
ell. Finite-interval tails and positivity repair are charged in section 5.

It follows for c<=d<=N/2, away from opposite-end atoms, that

sum_j f_j f_(j+d) <= S+AA+M delta^2 H w+300 delta^2 ell+tail,

where S=delta^2 N and AA=w beta^2 delta^2 H^2/(2ell).
Here 300 safely exceeds (Vh+2)/2+10Vv<284.

For 1<=d<c one has w>=1/2. Since
sum_j |q_j-1|<=2K, the generic product bound gives

|sum_j q_j q_(j+d)-(N-d)| <=2(M+1)K.

It follows that the same raw bound holds with M replaced by 144. This
charges the origin transition to w instead of asserting cancellation there.

## 5. Finite tails

The expansion of the unrepaired two-end product differs from

N-d+4 sum_(j>=0)v_j-2 sum_(j<d)v_j
     +2 sum_(j>=0)v_jv_(j+d)

only by omitted linear/same-end tails and two opposite-end products.
For d<=N/2, every opposite product has one index at least N/4-1.
At x>=2^16, N/4-c-1>=N/8 and N/H>=x/2, so those entries have size at most
T=4exp(-x/48). Geometric summation bounds each omitted tail norm by 4HT.
The linear tails, omitted same-end term, and opposite products together
cost at most 100HT. Positivity repair costs at most 4HT in pair units; the
far-end part of the primary atom/bulk term costs at most HT after scaling
by delta^2. Thus a safe total pair-sum remainder is

tail <=105 delta^2 H T <=840 exp(-x/48)/x <=x^-2.

The last inequality follows without numerical exponent evaluation from
exp(x/48)>=(x/48)^3/6 and
(2^16)^2>840*6*48^3. The same geometric bound at index N gives objective
tail loss at most 16xT=64x exp(-x/48)<=1 at this onset.

## 6. Source cap and covariance lower bound

At the declared onset f<=1/2 and delta(M+1)<=1. Monotonicity of f-f^2 on
[0,1/2] shows psiTilde>=min(psi,delta). Hence

0<=psi-psiTilde<=delta(q-1)_+,
sum(q-1)_+<=2(HJ+Vh).

It follows at every lag that

0<=R_psi(d)-R_psiTilde(d)<=4M delta^2(HJ+Vh)<=73 delta^2 H.

For d<ell, the direct product bound of section 4 gives
R_psi(d)>=S-69 delta^2 H. Therefore

R_psiTilde(d)>=S-142 delta^2 H.

No differentiability of the square-root cap is assumed. Combining with the
raw lag bound and delta^2 H<=sqrt(2)/x proves, for every d<=N/2,

P_N(d)<=S+w[beta^2 delta^2 H^2/(2ell)-S+512/x]+301/x^2.

The source Fejer lemma then supplies the PSD, diagonal and entrywise
conditions. The source cap was used unchanged, following the frozen
positivity repair.

## 7. Exhaustive long-lag partition

For floor(N/2)<d<=N-2ell, w=0 and opposite atoms are absent. Then

P_N(d)<=sum f_jf_(j+d)
       <=(49/50)S+2M sqrt(2)/x <=S,

because S>=1/4 and x>=2^16. This handles overlapping boundary layers by a
fixed margin and does not extend the separated-end expansion beyond its
domain.

For N-2ell<d<N, the overlap has fewer than 2ell sites, and

P_N(d)<=2M^2/ell+2M sqrt(2)/x+1/2 <1.

Thus the integer partition is: 1<=d<c; c<=d<ell;
ell<=d<=floor(N/2); floor(N/2)<d<=N-2ell;
N-2ell<d<N. Empty real/integer endpoint subintervals are simply omitted.
The cases around d=ell and d=H are included in their exact formulas.

## 8. Explicit conservative receipt and objective

The constants B0=513, D0=604, N0=2^64 are candidate admissible choices.
For x>=2^16, all elementary smallness conditions above hold, beta>=0,
ell<=2x^2, and

1-S>=(D0)/(2x^2)>=301/x^2,
beta^2 H^2/(2ell^3)+512/x<=1-301/x^2.

The convex combination in section 6 is consequently at most 1.

Mass quadrature and positivity repair give

sum f >=delta N+delta H(beta-1/3)-2delta c-2delta Vv-tailMass.

Here delta N>=sqrt(N)-D0-1; x>=D0+1 implies
delta H>=sqrt(2)x-(sqrt(2)+1); the atom reduction costs at most sqrt(2)B0;
2delta c<=1; 2delta Vv<=1; and tailMass<=1. Therefore

sum f >=sqrt(N)+(2sqrt(2)/3)N^(1/4)-1636.

This is a finite/error reconstruction conditional on the complete renewal
package in section 1. It does not itself prove the uniform upper companion,
novelty, publication readiness, or the source's full conjecture. Final review
must inspect the actual proof packet, reconcile every convention, and record
the operator package's explicit proof before granting acceptance.
