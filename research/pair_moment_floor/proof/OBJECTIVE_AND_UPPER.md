# 3. Objective and upper companion

Candidate proof. The final complete review disposition is separate.

## 3.1 Constant-loss lower objective

Use the exact construction and chi_U from the preceding sections. Positive
part repair adds mass. The mesh quadrature bound and TV(chi_U)<=26 give

\[
 \sum_j\psi_j\ge\delta H
 \left(U-\frac13-2\int_U^\infty|b|\right)-26\delta.
\]

The atom mass is exactly beta delta H. As H U=N-ell, the actual objective
kappa satisfies

\[
 \kappa\ge\delta N-1+\frac23\delta H
 -\frac{1026\delta H}{x}-26\delta-12\delta H e^{-U/4}.
\tag{M1}
\]

Every constant loss is now uniform, without a recurrence table:

- ell<=x^2+515 implies delta N>=x^2-515.
- H>=sqrt(2)x^3-1 implies
  delta H>=sqrt(2)x-2(515)/x-1/x^2>=sqrt(2)x-1 at x>=32768.
  Hence (2/3)delta H>= (2sqrt(2)/3)x-1.
- 1026delta H/x<=1026sqrt(2)<2052.
- 26delta<1.
- 12delta H e^{-U/4}<=24/x<1.

For the last estimate, N>=8ell gives U>=(7/8)N/H>=x/2. Thus
e^{-U/4}<=e^{-x/8}<=24*8^4/x^4<=x^(-2), since x^2>=2^30>98304.
Together with delta H<=2x, this proves the displayed bound explicitly.

Together with the explicit centered-start loss 1 in (M1), these total
at most 515+1+2052+1+1+1=2571. Rounding the total allowance upward with
one unit of slack gives the declared K_minus=2572. Thus

\[
 \kappa\ge\sqrt N+\frac{2\sqrt2}{3}N^{1/4}-2572
 \quad(N\ge2^{60}).
\]

Square-root clipping changes Gamma only and has no direct objective loss.
The PSD construction and every separate pair budget have already been proved.
This supplies an explicit feasible moment pair for every integer above onset.

## 3.2 Upper companion: attributed positive-measure transfer

Let phi(t)=4/3-2|t|+(2/3)|t|^3 on |t|<=1 and zero outside. It is the
autocorrelation of the normalized rising ramp. For real 0<T<=N the sampled
matrix A_T(i,j)=phi((i-j)/T) is PSD and entrywise nonnegative. For every
feasible pair in the exact SDP, the Schur complement and the difference
budgets imply

\[
 f^{\mathsf T}A_Tf\le\operatorname{tr}(A_T\Gamma)
 \le\frac43\kappa+2\sum_{d\ge1}\phi(d/T)
 \le\frac43\kappa+T.
\tag{U1}
\]

The last step compares each value of the decreasing nonnegative phi with
the adjacent integral and uses int_R phi=1. This is valid for real T and
real kappa, with no cardinality or indicator assumption.

Chen's finite-positive-measure bound applies to
mu=sum f_j delta_{j/T}, supported on [0,N/T]. Its signed comparison measure
has exactly constant potential on that interval and energy at most
N/T+2/3+200exp[-log(4/3)N/T]. Positive-definite energy Cauchy-Schwarz gives

\[
 \kappa^2\le
 \left(\frac NT+\frac23+200e^{-\log(4/3)N/T}\right)
 \left(T+\frac43\kappa\right).
\tag{U2}
\]

The comparison measure need not be positive; the actual mu is positive.
There is no division by kappa, and kappa=0 is harmless. The independent
operator review reconstructs the comparison-potential construction and
Chen's exact root bounds, rather than citing a physical theorem for this SDP.

In particular Chen's section 6 scalar comparison with
T=sqrt(2)N^(3/4) gives

\[
 \kappa<\sqrt N+\frac{2\sqrt2}{3}N^{1/4}+1
 \quad(N\ge4600000).
\tag{U3}
\]

Its proof compares the unique positive root of the scalar quadratic (U2)
with the displayed test value and does not assume kappa is an integer.
The detailed independent algebra is included in
../reviews/operators/INDEPENDENT_OPERATOR_LEMMAS.md, section on the upper
companion. It is an inherited scalar result transferred to the SDP, not
the principal novelty claim.

Since 2^60>4600000, the same onset proves both halves of the declared
effective theorem. No original symmetric rational certificate is generated
by this moment construction, and no physical Sidon-set lower bound follows.
