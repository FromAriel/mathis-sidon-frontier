# Exact fixed-grid optimum and effective finite boundary correction

2026-10-23. Attributed finite-grid proof supporting the v1.5.0 certificate.
Read with PROVENANCE.md for the inherited framework and scope of the contribution.

## 1. Definitions and theorem

Fix n>=1, M=2n, k=1,...,n. Kernel k is 1/(2k) on the bins n-k,...,n+k-1
and zero elsewhere. Let lambda_k=4k^3/n^4 for k<n and
lambda_n=(2n-1)/n^2. These are positive and sum one, by the sum-of-cubes
identity. Every kernel is normalized, nonnegative and individually reflected.
Its free coordinates below n-k are invisible to all future covers.

For integer L>=1 put J=2nL and extend each finite vector v_k by exactly one
for j>=J. Define B_q=sum_k lambda_k sum_i p_ki v_(k,q+i), q>=0, and

    b(v)=1+(1/n)sum_k lambda_k sum_(j<J)(v_kj^2-1).

The same definition on the half-line uses absolutely convergent sums, with
v_k-1 in l1 intersect l2. All covers there are required for q>=0. Denote
the finite minima under B>=1 or B=1 by beta_ge and beta_eq, and the half-line
infimum by beta_inf. Invisible coordinates are zero at any minimizer.

The assertions proved below are

    a_n=4/3-1/(3n^2), beta_inf(n)=b0_n=2/3+1/(3n^2),
    b0_n <= beta_ge(n,L) <= beta_eq(n,L).

Both finite minima decrease (nonstrictly) to b0_n as L grows. For n>=2 each
finite minimum strictly exceeds b0_n. For n=1 all these values are one.
The explicit construction below has every cover exactly one and a rational
total error bound E(n,L;s,p). It includes fixed-point interval and proposal
rounding error. No physical varying-data remainder is asserted.

## 2. Correlation, shift conventions and reduced stability

Let F be the future shift (Fx)_q=x_(q+1) on nonnegative indices. Its adjoint
is the causal zero-extended shift; generating functions describe this causal
action. Put

    D(z)=(1+z)/2,
    R_k(z)=z^(n-k)(1+z^2+...+z^(2k-2))/k,
    P_k(z)=D(z)R_k(z),
    r(z)=sum_(i=0)^(n-1)(2n-2i-1)z^i/n^2.

P_k is precisely the centered normalized box polynomial. The previously
audited finite-box correlation identity can be reconstructed by expanding
both sides, or matching the piecewise-linear autocorrelation knots of the
cell-average ramp. It gives the Laurent-polynomial identity

    sum_k lambda_k R_k(z)R_k(z^-1)=r(z^2)r(z^-2).       (2.1)

For completeness, the ramp knot at ell/n is
(4n^3-6n^2 ell+2ell^3-n+ell)/(3n^3); its internal slope jump is4ell/n^2,
matching lambda_ell/(ell/n)^2. The final slope is-(2n-1)/n^2 and both
extensions are zero beyond1. Refining each ramp cell twice contributes the
same D factor on both sides; cancel it as a polynomial identity, not as an
assertion of a bounded infinite inverse at z=-1. Evaluating kernel energies
directly gives a_n=sum lambda_k*n/k=4/3-1/(3n^2).

Here is an elementary quantitative stability proof, including explicit
constants used later. For n>=2 define

    t=31/32, rho=1+t/(2n), c=(2n-1)/(2n-3), R=rho^2,
    rprime=(n-1)(2n-1)/(6n), ell=1+(R-1)rprime.

Then 1<R<c. Indeed R<1+1/n+1/(4n^2), whereas
c>1+1/n+3/(2n^2). Write r(w)=sum a_i w^i. Since c is the minimum ratio
a_(i-1)/a_i, the polynomial (c-w)r(w) has a positive constant and all other
coefficients nonpositive. For |w|=R,

    |(c-w)r(w)| >= (c-R)r(R)>0,
    |r(w)| >= (c-R)r(R)/|c-w|.                         (2.2)

The same argument inside the circle proves zero-freeness there. Positive
coefficients give r(R)>=r(1)+(R-1)r'(1)=ell. In particular 1/r(z^2) is
analytic on a disk strictly larger than |z|<=rho; the removable point at1
in all step deviations is retained. There is no stability assertion for D^-1.

Set

    A = [(8/3)*(1+rho+(c-1)/(rho-1))]/[(c-R)*ell] + 1/(rho-1),
    B = sum_(j=0)^min(8,2n) binom(2n,j)*(t/(2n))^j.

These are positive explicit rational numbers. The inequality e^t<8/3 follows
from the rational upper bound sum_(j=0)^8 t^j/j! + [t^9/9!]/(1-t/10)<8/3.
Also rho^(2n-2)<e^t and rho^(2n)>=B>1. No large polynomial root calculation
is used to establish these estimates.

## 3. Renewal profiles and covers

With d=2n-1 and m=n^2/d, direct coefficient subtraction proves

    (1-z)r(z)=(1-Q(z))/m,
    Q(z)=[2sum_(i=1)^(n-1)z^i+z^n]/d.

Q is a positive probability law; at n>=2 it is aperiodic. Define

    Y(z)=1/[(1-z)r(z^2)]=m(1+z)/(1-Q(z^2)),
    V_k(z)=R_k(z)Y(z)=H_k(z)/(1-z), H_k=R_k/r(z^2).

Thus y_(2j)=y_(2j+1)>=0. Each H_k(1)=1. Stability above implies H_k has
absolutely summable coefficients with every polynomial moment finite;
v_k^inf-1 has the same exponential property. All ideal profiles are
nonnegative, and their invisible prefixes vanish.

On the half-line, F^i(F*)^j reduces to a future or causal shift; therefore
the Laurent identity(2.1) gives the exact Toeplitz factorization

    sum lambda_k R_k(F)R_k(F)^T=r(F^2)r(F^2)^T.

Since r(F^2)^T y=1 and r(F^2)1=1, the ideal profiles v_k^inf=R_k(F)^T y
satisfy sum lambda_k P_k(F)v_k^inf=D(F)1=1. This checks every q>=0.

Define the original-cover multiplier by its generating function

    mu(z)=4Y(z)/(1+z)=4m/(1-Q(z^2)).

It is nonnegative and bounded, with mu_(2j)=4y_(2j) and mu_(2j+1)=0.
The exact relation D(F)^T mu=2y proves P_k(F)^T mu=2v_k^inf. This is the
original-row normalization. It explicitly cancels the alternating factor;
the multiplier itself tends periodically to(4,0), not pointwise to2.

## 4. Absolute energy calculation and the gap identity

Write h_kj for the causal coefficients of H_k. Absolute summability with a
finite first moment justifies the following double sums. Since sum_j h_kj=1,
v_kj^inf=sum_(l<=j)h_kl and

    sum_(j>=0)[(v_kj^inf)^2-1]
      = -sum_(l,m>=0)max(l,m)h_kl h_km.

This is obtained by summing the absolutely convergent difference
1_(j>=max(l,m))-1, not by subtracting divergent squared norms. Use
max(l,m)=(l+m+|l-m|)/2. The full-line weighted filter autocorrelation from
(2.1) is sum_k lambda_k sum_l h_kl h_(k,l+d)=1_(d=0). Its |d|-weighted
contribution is therefore zero. The remaining first-moment contribution is

    sum_k lambda_k sum_j[(v_kj^inf)^2-1]
      = -sum_k lambda_k H_k'(1)
      = -(n-1-2r'(1))=-(n^2-1)/(3n).

The absolute domination is bounded by a constant times
sum_l l|h_kl| sum_m |h_km|, which is finite. Hence b(v^inf)=b0_n exactly.

For any half-line admissible v set e_k=v_k-v_k^inf. Then e_k is in l1 and
l2. Expanding only convergent differences and using P_k^T mu=2v_k^inf gives

    b(v)-b0_n = (1/n)sum_k lambda_k ||e_k||_2^2
              +(1/n)sum_q mu_q[B_q(v)-1].               (4.1)

Fubini in the cross term is valid because mu is bounded, each P_k has finite
support, and each e_k is in l1. Both terms are nonnegative on cover-feasible
profiles. For a finite unit-tail profile the slack sum has only q<J terms.
For exact-cover profiles it is zero, so the cost is exactly squared error.
This proves the half-line optimum, without using the attributed global floor.

Finite feasibility is nonempty: set active free entries to1 and invisible
entries to0. All covers equal1. The finite positive-weight quadratic is
coercive on its free variables, and the constraint sets are closed, so finite
minima exist. Appending another M free ones embeds depth L into L+1 without
changing b or covers. Thus both finite minima are nonincreasing.

If n>=2, v_1^inf cannot be eventually one. Otherwise
(1-z)V_1^inf=z^(n-1)/r(z^2) would be a polynomial. A nonconstant r with
nonzero constant term cannot divide a monomial. Consequently every finite
unit-tail profile has a strictly positive squared-error tail in (4.1), so
beta_ge(n,L)>b0_n. This applies to its attained finite minimum as well.
For n=1 the ideal is identically one, b0=1, and that finite profile attains1.

Finite positivity can also be reconstructed without this identity. Sum
Jensen's inequality over q<J; symmetry gives the total tail-bin contribution
n-1/2. Thus V=sum lambda sum_(j<J)v_kj^2 >=J-n+1/2 and
b=1+(V-J)/n>=1/(2n). Final witnesses must additionally check b directly.

## 5. Explicit tail estimate and exact terminal repair

Let Z_k(z)=(H_k(z)-1)/(1-z), whose coefficients are e_kj=v_kj^inf-1.
The point z=1 is removable. On |z|=rho, (2.2) and

    |c-z^2|/|1-z| <=1+rho+(c-1)/(rho-1),
    |R_k(z)|<=rho^(n+k-2)<=rho^(2n-2)<8/3

give |Z_k(z)|<=A. Cauchy's coefficient bound therefore proves

    |e_kj|<=A rho^(-j).

For J=2nL set tau=A B^(-L). Since rho^(2n)>=B,

    |e_kj|<=tau rho^(-(j-J)), j>=J,
    sum_k lambda_k sum_(j>=J)e_kj^2 <=tau^2/(1-rho^-2).  (5.1)

Truncate v^inf at J, attaching ones, and call its cover error f_q=B_q-1.
It vanishes for q<=J-M and for q>=J. The latter uses the weighted identity
B_q(v^inf)=1; individual component tail deviations need not have zero cover.
If h_kj=e_kj*1_(j>=J), endpoint subtraction of each box gives

    f_q-f_(q+1)
      = -sum_k lambda_k[h_(k,q+n-k)-h_(k,q+n+k)]/(2k).

Hence M|f_q-f_(q+1)|<=2a_n tau. Its support is contained in the M indices
J-M,...,J-1. The finite widest-box inverse, with zero extension, is

    T_n^-1=M(I-F)sum_(r=0)^(L-1)F^(rM).

Repair the widest component by x=-T_n^-1 f/lambda_n. This restores every
original cover exactly, including all partial overlaps; q=J is separately1
by normalization and the fixed unit tail. Each residue progression meets the
support of (I-F)f at most once, so

    |x_j|<=2a_n tau/lambda_n.                          (5.2)

The repaired profile has no free error except x in component n, and retains
the ideal discrepancy only in the forced tail. Applying (4.1) gives

    0<=b-b0_n<=tau^2*[8a_n^2 L/lambda_n
                         +1/(n(1-rho^-2))].           (5.3)

For each fixed n this tends to zero, since B>1 and the prefactor grows only
linearly in L. Together with the finite lower bound and embeddings, it proves
both finite convergence assertions. It makes no claim that their finite
optima agree or that the constructed profile is a finite optimizer.

## 6. Directed recurrence and a fully rational realization bound

The duplicated coarse sequence y_j has initial y_0=m and, with negative
indices zero, satisfies

    y_j=[2sum_(i=1)^(n-1)y_(j-i)+y_(j-n)]/(2n-1), j>=1.

Compute outward dyadic intervals with s FRACTIONAL bits. Initialize y_0 by
one floor/ceiling division. Maintain exact scaled-integer sliding sums and
perform exactly one floor/ceiling division per endpoint per recurrence.
The coefficients are nonnegative and total one. Induction bounds each endpoint's
absolute error by(j+1)2^-s: each update adds at most one fractional mesh.
There is no floating or repeatedly rounded accumulation. The initial rational
m must be enclosed directly; do not round unscaled renewal mass then multiply.

For j<nL, round the interval midpoint to the nearest p-fractional-bit dyadic,
ties to even, and duplicate it. Its total error is at most

    eta=(nL+1)2^-s+2^(-p-1).                           (6.1)

Each R_k is a nonnegative causal averaging polynomial, so all free component
profiles obtained from these exact dyadics have error at most eta and invisible
prefixes still zero. Attach exact unit tails; no independent final rounding
of component boundaries is performed.

Apply the same exact widest-box repair. Split its cover error into the
previous ideal-tail error and the free quantization error. For the latter,
endpoint subtraction gives M|Delta f|<=2a_n eta, and there are at most L
terms on a residue progression. Its repair amplitude is therefore at most
2a_n L eta/lambda_n. The final error in component n is bounded by

    (1+2a_n L/lambda_n)eta+2a_n tau/lambda_n.

Every other free component has error at most eta. The tail remains (5.1).
The exact gap identity proves the fully explicit rational upper bound

    E(n,L;s,p)=2L*[(1-lambda_n)eta^2
       +lambda_n*((1+2a_n L/lambda_n)eta
                    +2a_n tau/lambda_n)^2]
       +tau^2/[n(1-rho^-2)].                           (6.2)

All data of this finite construction are rational. Finite repair preserves
every cover exactly. Real free entries are permitted by the original model;
no boundary nonnegativity assumption is introduced. Stability and (6.2)
were proved without assuming the global floor or an infinite duality theorem.

For n=1 use the exact finite profile1 and E=0. For all n>=2, formulas(2.2)
and(6.1)-(6.2) specify every constant. The flagship prescription is s128,p80;
the approved arithmetic-only refinement is s256,p128.

## 7. Predictive Pell selection and scope

At n2048 let P=1121/1189. The exact scalar allowance is

    Delta=P^2/a_n-b0_n
         =637004018641/33160588486005227520>0.

Evaluate the rational expression(6.2) at s128,p80 for each integer8<=L<=32.
The first passing value is L30. All L8,...,29 fail E<=Delta/2; in particular

    E(2048,29;128,80)>47/10^9,
    E(2048,30;128,80)<71/10^10<96/10^10<Delta/2.

The exact fractions for every comparison are in PREDICTION.json;
independent acceptance must bind the assembled proof and repeat these scalar
comparisons. They require no large-grid recurrence coefficients or profiles.
The n2048,L30 construction, if executed faithfully with those rounding bounds,
therefore satisfies b<=b0+E<b0+Delta and a_n*b<P^2 before any numerical trial.

This chooses the smallest passing L for this explicit conservative bound,
not the smallest achievable certificate depth. It does not assert a new
universal floor, finite attainment of the global floor, or exact finite
equality/inequality optima. The conditional certificate has fixed data before
the ambient Sidon interval is introduced. Hou--Zhao's analytic transfer is a
separately reviewed cited dependency; no varying-data uniform remainder is
proved here. The Pell identity supplies an exact benchmark, not a new
Diophantine theorem or a reason that this rational must be an optimum.
