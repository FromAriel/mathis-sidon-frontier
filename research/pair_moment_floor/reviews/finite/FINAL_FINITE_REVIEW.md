# Fresh finite/error review of the frozen execution proof

Date: 2026-10-23. Disposition: **PASS for the submitted mathematical theorem
and its finite/error obligations**, with the two explanatory extensions in
section 8 recorded explicitly here. This is not a novelty or publication
approval.

Reviewed statement: for every integer N>=2^60, in exactly Akwei Definition
7.2,

sqrt(N)+(2sqrt(2)/3)N^(1/4)-2572 <= H2(N)
 < sqrt(N)+(2sqrt(2)/3)N^(1/4)+1.

The reviewed construction has ell=ceil(sqrt(N))+514,
H=floor(sqrt(2)N^(3/4)), delta=1/ell, beta=1-1026/N^(1/4), the full
right-continuous renewal profile, the specified positive-part repair,
uniform centered endpoint atoms, and the original source square-root cap.

Inputs inspected: AGENTS.md, PLAN_SIDON_FLOOR_CLOSURE.md, frozen STATEMENT.md,
FULL_PROOF.md, proof/RENEWAL_AND_MODEL.md, proof/ALL_DISTANCE_ESTIMATE.md,
proof/OBJECTIVE_AND_UPPER.md, Akwei's source Sections 4 and 7, and Chen's
source Lemma 6 and scalar Section 6. The separate operator reconstruction was
used as a derivation to inspect, not as a verdict to inherit. Earlier planning
or approval reports were not used as evidence. No sampled feasibility,
renewal table, FFT, optimizer, numerical campaign, application run, or Git
mutation was used.

## 1. Independent reconstruction and exact model

The source Definition 7.2 and frozen statement agree: real f, symmetric Gamma,
the augmented PSD block, Gamma_jj=f_j, 0<=f<=1, entrywise nonnegative Gamma,
and each noncyclic positive-difference budget separately. No indicator or
integrality assumption enters the proof.

Before receiving the complete candidate I independently derived the atom
overlap formula, clipping estimate, shifted half-line cancellation, long-lag
fixed margins, and constant objective loss. That preliminary note is retained
as INDEPENDENT_FINITE_RECONSTRUCTION.md. Its deliberately weaker alternative
constants are not the accepted frozen receipt. This final review checks the
actual constants 512,256,1026,514,2572,1,2^60.

The initial suspected obstruction at d near H was investigated explicitly.
The renewal density jumps downward at 1, so a two-sided O(x^-2) approximation
to an individually smeared atom term would fail. The submitted proof does
not assert that approximation. It averages the complete source inequality
and applies Lipschitz continuity only to the continuous part C_U. This
resolves the jump without changing the construction.

## 2. Renewal dependencies and elementary bounds

The block averaging representation in the candidate follows by solving
R(y)=B(y)+integral_0^y R, where B(y)=integral_0^(1-y)r(m-z)dz. Interchanging
the integrals gives exactly the displayed q_y. The kernel has mass one and
dominates (1/2)1_[0,1/2], so its common mass is 1/4 and block oscillations
contract by 3/4. The weighted invariant has value 1 at t=1 because
integral_0^1 s exp(s)ds=1; it identifies the common limit as 2. This proves
the explicit decay without complex-root estimates or numerical recurrence.

With b=(r-2)/2, extended by zero to negative arguments, the reviewed bounds
are ||b||infinity<=1/2, ||b||1<=4, TV(b)<=10,
|b(t)|<=(4/3)exp(-t/4), and integral_v^infinity|b|<=6exp(-v/4).
The variation includes both half-unit jumps at 0 and 1. On later intervals
b'=b-b(.-1), so the regular variation there is at most twice its L1 norm.

The mass integral b=-1/6 follows from the displayed Laplace expansion and
the already established exponential domination. The moving-jump term is
retained when differentiating A_g. The two delay-equation invariants give
the integration constant -2/3, hence integral b^2=1/12. The source proof's
three ranges 0<s<1, 1<=s<=3/2, and s>=3/2 prove the complete cancellation
inequality for all positive real s, including its right value at 1.

Consequently C_U is Lipschitz with constant at most
1+2||b||infinity+2||b||infinity TV(b)<=12. This bound remains valid through
the renewal jump because the autocorrelation is Lipschitz by BV translation.

## 3. Every finite support and altered endpoint

Put c=(ell-1)/2 and U=(N-ell)/H. The identity
N-1-2c=N-ell is exact; it gives reflection symmetry of the sampled chi_U.
The support of chi_U maps to indices from ceil(c) to floor(N-1-c), all
within the original grid. Its endpoint values agree with the right renewal
representative. The only difference between the actual repaired profile and
delta chi_U is a nonnegative correction on the two exterior half-atom
strips. Together they contain at most ell grid points. Each correction is
at most delta*(4/3)exp(-U/4), so their total is at most
(4/3)exp(-U/4), using delta ell=1 exactly.

For atom amplitude a=beta delta H/(2ell), direct integer interval
intersection gives

AA(d)=a^2{2(ell-d)_+ +(ell-|d-(N-ell)|)_+}.

In particular the opposite strip begins at N-2ell+1, vanishes exactly at
N-2ell, and peaks at d=N-ell. There is one opposite-end term at positive
lags, not two. Its maximum is a^2 ell<=1/2.

For d>=ceil(ell/2), there are no outward atom/chi terms. Indeed a nonzero
chi index is at least ceil(c), and ceil(c)+ceil(ell/2)=ell for either
parity of ell. The two remaining inward terms are exactly the source's
average over j=0,...,ell-1, with shifts (j-c)/H. They have exact mean zero.
Their smallest rescaled argument is (d-c)/H>0 at both parities, so no
undefined value at the cancellation identity's s=0 is needed.

The positivity correction is included before forming this comparison. Its
cross terms with both chi and alpha are charged by
2||delta chi+alpha||infinity E+E^2. Thus the proof does not omit outward
interactions newly introduced by repair.

## 4. Quadrature and the complete finite tail ledger

The sampled-product variation estimate is valid:
TV(chi_U)<=26, ||chi_U||infinity<=2, hence
TV(chi_U(.)chi_U(.+s))<=104. The variation bounds account for both endpoint
cuts and all jumps. Shifted lattice quadrature therefore costs at most
104delta^2 in the continuous/continuous sum.

For ell/2<=d<=N/2, put s=d/H and V=U-s>=N/(4H). Expanding the finite
integral on [0,V] gives the asserted C_U(s) plus exactly these errors:

- The four linear-tail replacements cost at most
  4 integral_V^infinity |b|.
- The two omitted same-end products together cost at most
  integral_V^infinity |b|, because ||b||infinity<=1/2.
- The first cross-end product is at most (16/9)V exp(-V/4).
- The second is at most (16/9)V exp(-(U+s)/4).

Their sum is bounded by (30+4U)exp(-V/4). The remote part of the inward
atom average has argument at least N/(4H). Averaging the whole inequality
C_U(t)+sigma(t)<=U, then using Lip(C_U)<=12, costs at most 6ell/H.
Since HU=N-ell, this leaves exactly 5delta^2 ell, plus 104delta^2 and tails.
Both are bounded by 109/x^2 because ell>=x^2>=1.

For z=N/H, all residual terms are bounded by
[delta^2H(32+4z)+8]exp(-z/16). The frozen parameter inequalities give
delta^2H<=2/x, x/sqrt(2)<=z<=x, and the bracket is at most 32 for x>=4.
Also z/16>=x/24, so the common allowance 64exp(-x/24) is sufficient.
This is an analytical bound, not an inferred exponential cutoff.

## 5. Cap, exhaustive lag partition, and structured estimate

Because f<=1/2 and delta<=1/2, monotonicity of t(1-t) on [0,1/2] proves
tildepsi>=min(psi,delta). Thus the cap has no objective cost, its sum of
pointwise losses is at most D1, and its correlation loss is at most
4delta D1<=40delta^2H. The profile L1 defect bound D1<=10delta H includes
the exact missing step sites and the full sampled b tails. The product
estimate costs at most 3delta D1, yielding S-CT(d)<=71delta^2H for d<ell.

The exact identity P=CC+AB+AA-w CT then gives the submitted structured
estimate with A=512 and B=256. In the very short range w>=1/2 absorbs the
coarse 136w/x raw error; the cap/covariance term adds at most 142w/x.
Their sum is 278w/x<512w/x. In the remaining separated-end range the raw
error is at most 109/x^2 plus the common tail, with no free O(x^-1) error.

The exhaustive integer partition is:

1. 1<=d<ell/2: the short w>=1/2 argument.
2. ell/2<=d<ell: the complete-identity average plus tapered covariance.
3. ell<=d<=floor(N/2): the same average, with w=0 exactly.
4. floor(N/2)<d<=N-2ell: no atom/atom term; D4 gives
   P<=S/2+34delta^2H<=S/2+68/x.
5. N-2ell+1<=d<N: overlap shorter than 2ell; the complete opposite
   atom term is at most 1/2, CC<=8/ell, and AB<=8/x.

These cases include every integer d and all transitions at ell, H, N/2,
N-2ell, and N-ell. In range 4 one also has P<=S at the frozen onset,
because S>=1/2 and 68/x<=S/2. Thus the structured bound extends to all
non-opposite lags, even though D13 itself is stated only through N/2.

## 6. Exact quantifiers, onset, and objective

For every real x=N^(1/4)>=32768, ell<=5x^2/4, H>=x^3, N>=8ell,
beta>=1/2, and all square roots are in their proved domains. No argument
requires x to be an integer or sqrt(N) to be integral.

Put q=(ell-x^2)/x^2<=1/4. Then
1-S=1-(1+q)^(-2)>=q>=514/x^2 and S>=1/2. Also
H^2/(2ell)<=N and 1-beta^2>=1026/x. Therefore the structured bracket is
at most -1026/(2x)+512/x=-1/x. The exact integer comparison
64*24^5=509607936<1073741824=2^30 shows that
64exp(-x/24)<=x^-2 for every x>=32768. The main lag bound is consequently
at most 1-257/x^2-w/x<1, and both remaining lag ranges have fixed positive
margin below 1.

For the mass, exact HU=N-ell gives the explicit centered-start loss 1.
Quadrature of chi_U and the full tail integral give precisely M1. The
separate loss bounds are 515 for delta N, 1 for the boundary coefficient,
2052 for atom reduction, 1 for the centered start, 1 for quadrature, and
1 for the tail. Their sum is 2571<2572. The cap changes Gamma only.

The declaration N>=2^60 is exactly x>=2^15=32768; there is no hidden real
onset, finite exception list, cutoff, or unproved admissibility condition.

## 7. Upper companion and final assessment

I checked the upper transfer against Chen's actual finite-positive-measure
lemma and real-variable scalar argument. The cubic phi is the
autocorrelation of 2t 1_[0,1]; its sampled matrix is PSD and entrywise
nonnegative. PSD trace comparison and the actual noncyclic difference
capacities give f^T A_T f<=4kappa/3+T for every real T>0. Chen's reference
measure is allowed to be signed, has exact potential 1 on the closed
interval, and has the stated finite energy bound. The actual atomic measure
sum f_j delta_(j/T) is positive and fits [0,N/T]. Zero mass is harmless.

The scalar quadratic at y=x^2+(2sqrt(2)/3)x+1 has positive value for every
real x>=4600000^(1/4), by Chen's displayed exact rational exponential
comparisons. Its constant term is negative, so it has exactly one positive
root. No integer-mass argument is used. The same +1 upper theorem therefore
applies to this SDP, and its onset is smaller than 2^60.

The finite construction, all-distance estimate, clipping, full tail budget,
integer support accounting, explicit objective, upper transfer, and onset
are accepted. This establishes the stated mathematical theorem, subject to
ordinary further scrutiny of a research proof. It does not establish novelty,
manuscript readiness, publication permission, physical Sidon-set construction,
or any claim about stronger relaxations.

## 8. Explanatory extensions recommended in the main proof

The two recommendations are already justified in this review and are not
mathematical gaps:

- State D1 also for integrable BV functions, by truncation and passage to the
  limit. Its application to the noncompact b in D3 uses this immediate
  extension; the exponential bound ensures the sampled and integral tails
  converge.
- State explicitly that D14<=S at the frozen onset, using S>=1/2 and
  68/x<=S/2. This spells out the uniform structured target for every
  non-opposite lag rather than leaving the implication to the reader.
