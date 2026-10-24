# Manuscript transcription and scope review

Date: 2026-10-23. Disposition: **PASS for source-to-proof mathematical
transcription and stated scope**, for the exact source and PDF hashes below.
This is a plain internal AI mathematical review, not external human
refereeing or proof-kernel formal verification.

The four TeX sources were read against the accepted proof and frozen
statement. The model, noncyclic lag capacities, full renewal density with
right values, positive-part profile, centered atoms, cap, Fejer covariance,
all finite constants, objective loss, onset, and conclusion retain their
accepted mathematical meaning. The principal statement remains

\[
 \sqrt N+(2\sqrt2/3)N^{1/4}-2572
 \le H_2(N)<\sqrt N+(2\sqrt2/3)N^{1/4}+1
 \quad(N\ge2^{60}).
\]

No mathematical datum essential to the accepted construction or proof was
dropped in the TeX transcription. Shortened derivations retain their
dependencies and the accompanying packet contains the full audited detail.

## Upper-section change checked independently

The manuscript replaces the detailed lower-onset rational absorption with
a simpler direct comparison at the theorem's onset. This is valid.
With x>=32768, `T=sqrt(2)x^3` satisfies 0<T<N and L=N/T>=1.
Chen's finite-positive-measure hypothesis therefore applies to the measure
`sum_j f_j delta_(j/T)` of arbitrary nonnegative real mass kappa.
The PSD trace step, signed reference measure, constant potential on the
closed interval, and absence of an integrality substitution agree with the
accepted source proof. The original Chen v3 text identifies this comparison
as Lemma 4.4, as cited in the manuscript.

Set `a=log(4/3)`, `g=2sqrt(2)/3`,
`eta=200exp(-ax/sqrt(2))`, and `y=x^2+gx+1`.
Since `a>1/4` and `sqrt(2)<3/2`,

\[
 \eta\le200e^{-x/6}\le
 \frac{200\cdot24\cdot6^4}{x^4}\le x^{-2},
 \qquad200\cdot24\cdot6^4=6,220,800<2^{30}\le x^2.
\]

Using 0<g<1 and x>=1 gives y/x^2<=3. Hence the error at y is

\[
 \eta[(4/3)y+\sqrt2x^3]\le4+2x<\tfrac{10}{9}x^2.
\]

The exact positive part is
`P_0(y)=(10/9)x^2+(g/9)x+1/9`, so `P_eta(y)>0`.
The quadratic has negative constant term and exactly one positive root.
Thus `P_eta(kappa)<=0`, with kappa>=0, implies kappa<y.
This proves the manuscript's upper theorem without any mass integrality.
The broader upper onset N>=4,600,000 remains correctly credited to Chen
and the evidence packet's real-mass transfer; it is not claimed to follow
from this shortened large-onset calculation.

## Material transcription error found and repaired

The first manuscript snapshot omitted the backslash in
`operatorname{diag}(epsilon)` in the displayed covariance definition.
That was a material mathematical display error despite successful TeX
compilation. It was reported to the root agent. The final `finite.tex`
now contains `\operatorname{diag}(\epsilon)`, matching the accepted
covariance. The root agent recompiled the PDF after that repair.
No other material mathematical drift was identified.

## Attribution and limits

The text attributes the exact SDP, conjecture, renewal boundary profile,
centered atoms and capped covariance ansatz to Akwei, the finite-measure
comparison to Chen, and the original smoothing framework to Hou--Zhao.
It expressly separates PSD from realizability, the SDP theorem from a
Sidon-set lower construction, and the internal proof reviews from external
refereeing and formal verification. It retains the bounded priority audit
and private-draft/publication-readiness limits. These statements agree with
the accepted proof scope; no stronger physical theorem is introduced.

## Bound artifact identities

Paths are relative to the execution packet. SHA-256:

| Artifact | SHA-256 |
| --- | --- |
| `manuscript/main.tex` | `2DFEAFB41004258227475F86BA3BAC12DF4BB9437A5E6F1F49AC76E93B9E03A6` |
| `manuscript/renewal.tex` | `43DE26341F09ED17C6633B4E314EFBDFAAA9BE8D964484ECA19E5A7A77A347B0` |
| `manuscript/finite.tex` | `4D646D54E2C1CCC4936F2704E0F5F9E0D82A78A256530293BC0B71FBE78486A5` |
| `manuscript/completion.tex` | `DA4280EC4747542D4113E76E665C3C8936825DE11054495EB6DE2A7D9487887D` |
| `manuscript/main.pdf` | `BA4185058A20A4580F07A5B89B304DCA3E397CCA5AEE907C77F875F133EBCAF9` |

The PDF hash binds the root-recompiled artifact. This reviewer did not render
or visually inspect PDF pages, compile TeX, or modify any TeX/PDF file.
Compilation and page-layout inspection are separate root-agent evidence.
Only this new review document was written during the manuscript check.
