# Finite symmetric certificate: model, recovery and verification

Version 1.4.0, October 23, 2026. Ariel M. Williams.

This note maps the compact witness to the original finite symmetric theorem
of Jianfeng Hou and Hongbin Zhao. It explains the exact recovery used by the
public replay and attributes its standard ingredients. The certificate-data
and software release does not claim a new generic optimization theorem,
finite convergence law, physical record or solution of Erdos Problem 30.

## 1. Source theorem and fixed data

The analytic dependency is [Hou--Zhao v3, Theorem 2.1](https://arxiv.org/html/2607.01169v3#S2),
with its finite normalization, covering and energy conventions. Rational data
are a special case of the real data allowed by that theorem. The finite
checker does not formally verify the complete analytic source proof.

Set n=1024, M=2n=2048, L=8 and J=ML=16384. There are R=n kernels. For
k=1,...,n define the centered box probability vector of length M by

```text
p[k,i] = 1/(2k)  if n-k <= i < n+k,
         0       otherwise.

lambda[k] = 4*k^3/n^4  for k<n,
lambda[n] = (2n-1)/n^2.
```

Each kernel is nonnegative, symmetric and normalized. Every weight is
positive, and the weights sum to one. Each boundary f[k,j], j=0,...,J-1,
is real rational; its extension is exactly 1 at every j>=J. The unused
prefix j<n-k is zero in the exported point.

The finite covering obligations are

```text
sum[k] lambda[k] * sum[i=0,...,M-1] p[k,i] * f[k,q+i] >= 1
for q=0,...,J.
```

The q=J row is structural because it sees only unit tails. The public point
has equality in every row, including q=J. The exact constants are

```text
V = sum[k] lambda[k] * sum[j=0,...,J-1] f[k,j]^2
a = M * sum[k] lambda[k] * sum[i=0,...,M-1] p[k,i]^2
  = 4/3 - 1/(3*n^2) = 1398101/1048576
b = 1 + (2/M)*V - 2*L.
```

The replay reconstructs V and b, verifies b>0, and checks the exact strict
comparison

```text
a*b < (471404576987/500000000000)^2.
```

Thus the cited theorem gives, for these fixed data,

```text
F(N) <= sqrt(N) + sqrt(a*b)*N^(1/4) + O(1),
sqrt(a*b) < 471404576987/500000000000 = 0.942809153974.
```

The diagnostic coefficient is approximately 0.942809153973600631. The data
are fixed before N tends to infinity. No explicit numerical O(1) constant or
uniform remainder for data varying with N is supplied by this release.

## 2. Finite operators and unit-tail accounting

Let S act on a J-vector by (Sv)[q]=v[q+1], with zero extension beyond J-1.
Then S^J=0. The finite unknown-part operator for the kth box is

```text
T[k] = (1/(2k)) * sum[i=n-k,...,n+k-1] S^i.
```

This zero extension is an operator convention for the finite unknown vector;
the actual certificate's boundary extension is one. Write 1 for the finite
all-ones vector and h=sum[k]lambda[k]*T[k]*1. The actual full cover vector is

```text
1 + sum[k] lambda[k]*T[k]*(f[k]-1).
```

Therefore all full covers are one exactly when
sum[k]lambda[k]*T[k]*f[k]=h. This identity keeps every late overlap and fixed-
tail contribution; dropping those terms would change the finite problem.

The finite geometric sum factors as

```text
D = (I+S)/2
D^-1 = 2*sum[r=0,...,J-1] (-S)^r
R[k] = (1/k) * sum[r=0,...,k-1] S^(2r)
T[k] = S^(n-k)*D*R[k].
```

The widest box has an invertible finite operator:

```text
T[n]^-1 = 2*n*(I-S)*sum[r=0,...,L-1] S^(2*n*r).
C[k] = T[n]^-1*T[k]
     = (n/k)*S^(n-k)*(I-S^(2*k))*sum[r=0,...,L-1] S^(2*n*r)
C[n] = I.
```

These are exact polynomials in a nilpotent shift, not infinite-filter
approximations or inverses requiring an analytic stability hypothesis.
Finite box-filter cancellation and sliding recurrences are classical; see
[Claerbout, PVI Section 3.2.1](https://sepwww.stanford.edu/sep/prof/pvi/zp/paper_html/node6.html).
[Daubechies--Sweldens, 1998](https://sites.math.duke.edu/~ingrid/publications/J_Four_Anal_Appl_4_p247.pdf)
provides a broader finite-filter factorization setting. The present scalar
identity is not claimed as a new wavelet lifting theorem.

## 3. Exact recovery from the compact multiplier

Set

```text
d = T[n]^-1*h = sum[k]lambda[k]*C[k]*1
W = sum[k]lambda[k]*C[k]*C[k]^T.
```

W is positive definite because C[n]=I and lambda[n]>0. The equality fibers
are complete: arbitrary f[1],...,f[n-1] determine the remaining component by

```text
f[n] = (d - sum[k<n]lambda[k]*C[k]*f[k]) / lambda[n].
```

The witness stores an exact vector u=u0/2^80. It is an untrusted rational
proposal, not a saved assertion of success. Compute e=d-W*u and define

```text
f[k] = C[k]^T*u                 for k<n,
f[n] = u + e/lambda[n].
```

Then sum[k]lambda[k]*C[k]*f[k]=W*u+e=d. Applying T[n] proves all the full
cover equalities. The shift structure makes the unused prefixes zero. All
entries remain rational, with no subsequent boundary rounding or numerical
linear solve. The public program also reconstructs covers and energy from
the resulting rows rather than accepting this identity as a saved flag.

For any rational u, the weighted energy of that repaired point is exactly

```text
U = 2*u^T*d - u^T*W*u + ||d-W*u||^2/lambda[n].
```

Completing the square gives the lower bound
L=2*u^T*d-u^T*W*u on the equality-constrained minimum. The exact minimum is
d^T*W^-1*d; this is standard weighted least-norm projection, not a new
optimization principle. See [Boyd--Vandenberghe, Section 6.2](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf).
Hou--Zhao Section 3 already provides joint boundary quadratic programming,
the weighted Gram dual, recovery and rational feasibility repair.

The floating banded solve used during construction is absent from acceptance.
The exact compact vector, deterministic finite operators, recovered arrays
and strict rational comparisons determine the public result. The public point
depends on these fixed operators and u; it needs no older asymmetric boundary.

## 4. Separate research comparisons

The development record separately compares redistribution at an exact
historical aggregate cover with uniform release of its cover slack. Exact
lower/upper receipts exclude the stronger target while preserving that cover,
and accept the flat-cover endpoint. The historical boundary supplies that
comparison, not the successful point's construction. This is no general
lossless conversion theorem or exclusion of other kernels and weights.

A separately checked nonnegative dual of the original inequality problem
also places its optimum within approximately 2.157380189016e-13 in energy of
the point, for these frozen kernels and weights. This is a fixed-problem
proximity statement, not exact global optimality. Neither that dual comparison
nor the historical fixed-cover barrier is reconstructed by the default public
compact replay; they are not premises of its finite certificate acceptance.

## 5. Quantitative overlap and attribution

[John Akwei's pinned limit manuscript](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/The_limit_of_vector-valued_smoothing_for_Sidon_sets.pdf),
physical page 10, Section 5/Table 2, and his
[V5 report](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/A_Data_Science_Analysis_of_Erdos_Problem_30_V5.pdf),
physical pages 22-23/Table 9, already report approximate finite linear-kernel
behavior b approximately2/3+1/(3m^2) and ab approximately
8/9+2/(9m^2)-1/(9m^4) at L=8 in the scanned range. Those statements are not
exact all-m identities. This certificate's close single-point agreement
does not establish a new finite formula or convergence rate. Akwei's m is
the linear-kernel grid, distinct from the present symmetric kernel length M.

Akwei supplies the ramp/renewal inspiration, asymmetric extension and
smoothing-method lower-bound source result. The new symmetric certificate's
analytic application uses Hou--Zhao's original theorem directly.
[Haoyu Chen's version3](https://zenodo.org/records/23273526) separately gives a
physical cardinality theorem with coefficient 2 sqrt(2)/3 and explicit onset
in its scalar-capacity setting. The present finite coefficient is larger.
Stephen Wu/wustep supplies the separately credited historical q2 benchmark.

Our contribution is this finite certificate construction and recovery,
implementation, independent exact finite checking and reproducible archival
preservation. Ariel M. Williams directed the work, acceptance criteria and
claims. Computation, software, drafting and review used AI assistance.
Internal review is distinct from external refereeing and formal verification
of the analytic source theorem. No source-author endorsement, coauthorship
or institutional affiliation is implied.

Our own code, certificate data and documentation use the repository's MIT
license. External papers and software sources remain the work of their
authors; they are cited, not redistributed or relicensed by this package.
