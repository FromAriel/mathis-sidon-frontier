# 2. Exact finite all-distance estimates

Candidate proof. Not a sampled or numerical feasibility test.
Notation and renewal bounds are from RENEWAL_AND_MODEL.md. Throughout
x>=32768, ell<=5x^2/4, N>=8ell, x^3<=H<=sqrt(2)x^3, 1/2<=beta<=1.
These inequalities follow immediately from the frozen constants.

## 2.1 Exact elementary controls

For an integrable BV function F and any shifted lattice of mesh a,

\[
 \left|a\sum_{j\in\mathbb Z}F(t_0+ja)-\int F\right|
 \le a\operatorname{TV}(F).
\tag{D1}
\]

To prove it, compare each sample with the integral on its adjacent cell; the
cell error is bounded by its variation times a, and sum. Endpoint values
are those of the specified function, including a point at a jump; its
variation accounts for those values. For noncompact F, finite cell sums
followed by a limit prove the same result; applying the bound first to |F|
also proves absolute convergence of the lattice sum. This covers b in (D3).

Let CC(d)=sum psi_j psi_{j+d}, AB(d)=sum(alpha_j psi_{j+d}+psi_j alpha_{j+d}),
and AA(d)=sum alpha_j alpha_{j+d}. All sums use zero extension. Put
a_atom=beta delta H/(2ell), w=(1-d/ell)_+ and S=delta^2 N. Exact interval
intersection gives

\[
 AA(d)=a_{\rm atom}^2
 \{2(\ell-d)_++(\ell-|d-(N-\ell)|)_+\}.
\tag{D2}
\]

Thus the opposite-end strip begins at N-2ell+1 and peaks at N-ell.
For d<=N/2 only the first term remains; it equals
w beta^2 delta^2 H^2/(2ell).

The one-profile L1 defect obeys

\[
 D_1:=\sum_{j=0}^{N-1}|\psi_j-\delta|
 \le\delta(\ell+8H+20)\le10\delta H.
\tag{D3}
\]

Indeed the two shifted step functions miss at most ell lattice sites in
total. Each sampled b contributes at most H||b||1+TV(b)<=4H+10 by (D1).
Taking the positive part contracts distance from the positive reference 1.
Since ||psi||infty<=2delta, expanding one factor at a time gives

\[
 |CC(d)-\delta^2(N-d)|\le3\delta D_1\le30\delta^2H,
 \qquad AB(d)\le4\delta^2H.
\tag{D4}
\]

The second inequality uses sum alpha=beta delta H and the two directions.

Write CT(d)=sum tildepsi_j tildepsi_{j+d}. Because f>=psi, f<=1/2 and
psi<=1/2, monotonicity of t(1-t) on [0,1/2] proves
tildepsi>=min(psi,delta). Therefore

\[
 \sum(\psi-\widetilde\psi)\le D_1,\quad
 0\le CC(d)-CT(d)\le40\delta^2H.
\]

For d<ell, (D4) then gives

\[
 S-CT(d)\le\delta^2d+70\delta^2H\le71\delta^2H.
\tag{D5}
\]

The exact pair budget is

\[
 P_N(d)=CC(d)+AB(d)+AA(d)-w CT(d).
\tag{D6}
\]

Thus clipping error is exactly multiplied by w. It vanishes for d>=ell.

## 2.2 Finite-to-half-line comparison including positive-part tails

Let U=(N-ell)/H and define on the real line

\[
 \chi_U(z)=[1+b(z)+b(U-z)]\mathbf1_{[0,U]}(z).
\]

On [0,U] it is nonnegative, since sigma>=1/2. Its supremum is <=2 and
TV(chi_U)<=26: two sigma variations contribute at most 22 and the endpoint
cuts at most 4. The product chi_U(z)chi_U(z+s) has variation <=104.

The actual profile psi_j differs from delta chi_U((j-c)/H) only at the
outer half-atom strips, where one sigma argument is negative. At most ell
sites are involved. Their correction e_j is nonnegative and, by (R1),

\[
 E:=\sum e_j\le\tfrac43e^{-U/4}.
\tag{D7}
\]

For any lag, replacing delta chi_U by psi changes the full un-capped
correlation of delta chi_U+alpha by at most 2||delta chi_U+alpha||infty E+E^2.
The supremum here is <=2/x^2+1/x<1. Thus a bound 8e^{-U/4} is sufficient.
This comparison charges all additional outward atom interactions as well.

Fix ell/2<=d<=N/2, s=d/H. Then V=U-s>=N/(4H). Direct expansion gives

\[
 I_U(s):=\int\chi_U(z)\chi_U(z+s)dz
         =C_U(s)+\mathrm{error},
\]
\[
 |\mathrm{error}|\le(30+4U)e^{-V/4}.
\tag{D8}
\]

Here are all terms in that bound. Replacing the two linear b integrals by
their half-line values costs at most 4 int_V^infinity|b|. Replacing the two
same-end b*b integrals costs at most int_V^infinity|b|. These total at most
30e^{-V/4}. The two cross-end integrals are bounded respectively by
(16/9)V e^{-V/4} and (16/9)V e^{-(U+s)/4}; their sum is <=4U e^{-V/4}.
No full-line correlation is identified with a finite Gram matrix.

By (D1), the discrete continuous/continuous sum differs from delta^2 H I_U(s)
by at most 104delta^2.

For the inward atom terms define h_j=(j-c)/H, 0<=j<ell. These have mean zero
and |h_j|<=ell/(2H), and s+h_j>0. Exactly two inward terms occur by reflection.
There are no outward atom/chi terms: a nonzero chi index must be >=ceil(c),
while d>=ceil(ell/2) makes that index plus d >=ell. Their normalization is

\[
 AB_{\chi}(d)=\beta\delta^2H\frac1\ell
 \sum_{j=0}^{\ell-1}\chi_U(s+h_j).
\tag{D9}
\]

All arguments lie inside [0,U]. The remote b term has argument at least
(N/2-ell-c)/H>=N/(4H). Since beta<=1 and sigma>=0, (D9) is bounded by
delta^2H times the average of sigma(s+h_j), plus
(4/3)delta^2H exp(-N/(16H)).

Now average the COMPLETE inequality (R3) at s+h_j. Lipschitz continuity of
C_U, not of sigma, gives

\[
 C_U(s)+\frac1\ell\sum_j\sigma(s+h_j)
 \le U+12\frac1\ell\sum_j|h_j|
 \le U+6\ell/H.
\tag{D10}
\]

This step is valid on either side of, and at, the renewal value jump. It uses
no Taylor expansion through that jump. Combining (D7)-(D10) yields

\[
 CC(d)+AB(d)\le S+5\delta^2\ell+104\delta^2+\mathcal T_N
 \le S+109/x^2+\mathcal T_N,
\tag{D11}
\]

where the common conservative tail allowance is

\[
 \mathcal T_N=64e^{-x/24}.
\tag{D12}
\]

To check its constant, put z=N/H, so x/sqrt(2)<=z<=x and U<=z. All finite
overlap, inward remote-end and positive-part terms above are at most
[delta^2H(32+4z)+8]e^{-z/16}. Since delta^2H<=2/x and x>=4, the bracket
is <=32. Also z/16>=x/24. The factor 64 leaves additional slack.

## 2.3 Structured short/medium estimate

If 1<=d<ell/2, (D4) and w>=1/2 imply
CC+AB<=S+136w/x. If ell/2<=d<ell, use (D11). In either case (D5) contributes
at most 142w/x when the hole term is written as -wS+w(S-CT).
For ell<=d<=floor(N/2), w=0 and (D11) applies directly.
Together with exact (D2), (D6), this proves uniformly for 1<=d<=floor(N/2)

\[
 P_N(d)\le S+w\left[
 \frac{\beta^2\delta^2H^2}{2\ell}-S+\frac{512}{x}
 \right]+\frac{256}{x^2}+\mathcal T_N.
\tag{D13}
\]

The constants 512 and 256 exceed respectively 278 and 109. They are uniform
for beta in [1/2,1], ell<=5x^2/4, N>=8ell, H between x^3 and sqrt(2)x^3.
They are not fitted to sampled profiles or chosen by an optimizer.

## 2.4 Long and opposite-end regimes

For floor(N/2)<d<=N-2ell there are no atom/atom terms and w=0. By (D4),

\[
 P_N(d)\le S/2+34\delta^2H\le\tfrac12+68/x<1.
\tag{D14}
\]

Indeed this regime even has P_N(d)<=S: S>=1/2 and 68/x<=S/2 at the
declared onset. The opposite-end atom strip still requires its own bound.

For N-2ell+1<=d<N, N-d<2ell, w=0, and the opposite atom term in (D2)
is <=ell a_atom^2<=1/2, since H^2<=2N^(3/2) and ell^3>=N^(3/2).
Using the actual profile bound psi<=2delta for the short overlap gives
CC<=8delta^2ell. Together with AB<=4delta^2H,

\[
 P_N(d)\le\tfrac12+8/x^2+8/x<1.
\tag{D15}
\]

These four regimes cover every integer 1<=d<N, including all transition
indices. Equation (D15) treats the opposite-end interaction explicitly.

## 2.5 Analytical parameter and tail absorption

The approved selection rule gives B0=ceil(2(512+1))=1026 and
D0=ceil(2(256+1))=514. For x>=32768, x>=2B0 and x^2>=4(D0+1).
Consequently S>=1/2 and S<=1-D0/x^2. For the latter put
q=(ell-x^2)/x^2<=1/4; then 1-(1+q)^(-2)>=q>=D0/x^2.
Furthermore H^2/(2ell)<=N and 1-beta^2>=B0/x. Thus the bracket in (D13)
is at most -B0/(2x)+512/x=-1/x.

Finally e^t>=t^4/24 gives

\[
 \mathcal T_N\le\frac{64\,24^5}{x^4}\le x^{-2},
 \qquad 64\,24^5<2^{30}\le x^2.
\]

Therefore (D13) is at most 1-257/x^2-w/x<1. Equations (D14)-(D15)
are also strictly below one. All difference budgets hold for every integer
N>=2^60. This onset is selected entirely by proved scalar inequalities.
