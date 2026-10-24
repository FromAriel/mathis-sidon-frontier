# Independent primary-source novelty audit

Date: 2026-10-23. Status: source baseline and final candidate comparison complete;
novelty assessment conditional on independent mathematical correctness.
This audit is separate from mathematical correctness review and publication
authorization. No earlier approval report is treated as evidence.

The proposed contribution is a uniform proof for Akwei's exact Definition 7.2
SDP, with explicit absolute losses, for every sufficiently large integer N.
The complete renewal/endpoint/Fejer construction is inherited. Completing the
named conjecture could be a useful specialized theorem, but inventing that
construction or discovering its coefficient would be inaccurate claims.

## Primary sources and exact locators

The machine-readable [source ledger](SOURCE_LEDGER.json) contains paths,
SHA-256 hashes, current Git blob identities, retrieval receipts and limitations.
The [search record](SEARCH_LOG.md) lists searches and access failures. Raw
head/tree responses and fresh HTTP receipts remain in `sources/`.

| Original | Pinned version and locator | Role in this audit |
| --- | --- | --- |
| [Hou-Zhao](https://arxiv.org/abs/2607.01169v3) | v3, 4 September 2026; Theorem 2.1, PDF p. 3; equation(12), PDF p. 7 | Finite covering/energy framework and master inequality. |
| [Akwei limit manuscript](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/Sidon_smoothing_limit.pdf) | Current Git revision 7934a1b; Definition 7.2, PDF p. 10; Proposition 7.3, pp. 10-11; Lemmas 7.4-7.5, pp. 11-12; equations(7.7)-(7.9), pp. 12-13; Conjecture 7.7, p. 14; Corollary C.2, p. 22 | Exact target and construction ancestry. |
| [Akwei V5](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/A_Data_Science_Analysis_of_Erdos_Problem_30_V5.pdf) | Current blobe3d684e6; computational Theorem 6.5 and Conjecture 6.6 | Earlier numbering of the target. |
| [Chen](https://doi.org/10.5281/zenodo.23273526) | v3, 10 October 2026; Theorem 2.1, PDF p. 2; Lemma 3.1, p. 3; Lemma 4.4, p. 7; Lemma 5.1, pp. 7-8; Section 6, pp. 8-9; Theorems 8.1-8.2, p. 11 | Physical +1 theorem, positive-measure capacity bound, explicit tail and absorption. |
| [HZ original code](https://github.com/HbZhao1/sidon-vector-smoothing/blob/ef044564300e546f8832b31f5fba133fd192cc3a/sidon_numerical_search.py) | Current head; `solve_boundary_qp`, lines154-239; continuation, lines318-350 | Component boundaries are already jointly optimized. |
| [Chen original proof text](https://github.com/chy4pro/automath/blob/5542184180d014b68637851941109dd5e584e920/problems/erdos30/SIDON_BOUND_PROOF.md) | Current head; Sections 2-6; cached original matches Git blob 03ec5395 | Exact proof text inspected instead of third-party summaries. |

Akwei's p. 14 was also rendered and visually read; see
`extracted/akwei_conjecture_page14.png`. Its printed conjecture and uncompleted
error-analysis statement agree with the text extraction. The current Git
revision has not replaced that conjecture with a proof.

## Claim-by-claim ancestry

| Claim or ingredient | Primary-source comparison | Proper attribution/status |
| --- | --- | --- |
| Definition 7.2 model, noncyclic difference budgets | Akwei Definition 7.2 | Existing exact model. |
| Transfer of covering bounds to real moment mass | Akwei Proposition 7.3 | Existing SDP transfer principle. |
| Half-line renewal profile and short-lag cancellation | Akwei Lemma 7.4 | Existing identity. |
| Fejer triangular covariance, diagonal completion, Schur complement | Akwei Lemma 7.5 | Existing construction and proof. |
| Centered additive ends, uniform atom strips, square-root cap | Akwei equation(7.9) | Existing ansatz. |
| Optimal leading scale and boundary excess | Akwei Section 7.3 | Existing leading-order analysis. |
| All-N bounded-loss conjecture | Akwei Conjecture 7.7; V5 Conjecture 6.6 | Explicitly announced target. |
| Full analytic renewal rather than numerical cutoff13.9 | Removes an implementation approximation from the existing ansatz | A proof obligation and implementation choice; not a new underlying profile. |
| Positive-part repair of overlapping endpoint tails | Must be compared on the actual finite interval | An analytical repair requiring mass and all-lag accounting; no novelty inferred merely from changing a formula. |
| Uniform error A*N^(-1/4)*(1-d/ell)+ + B*N^(-1/2) with explicit constants | Stronger than fixed-lag leading-order cancellation | Potential substantive contribution only if proved for every integer lag. |
| SDP upper +1 at an explicit onset | Chen's positive-measure capacity plus the existing SDP energy transfer | Attributed corollary/extension; does not improve Chen's physical theorem. |
| Additive4/9 scalar limit | Akwei Appendix C already gives ab/2 | Existing algebraic specialization. |

The current original HZ code solves one combined convex boundary problem and
recovers all component blocks. Re-describing that operation as a new joint
boundary optimization would conflict with the code. No code from the missing
Akwei helper suite was available for line-by-line comparison.

## Classical covariance and realizability lineage

These original cached PDFs were independently extracted and read. Their
title-page identifiers and hashes appear in the ledger.

- [Lasserre, 2001](https://doi.org/10.1137/S1052623400366802), pp. 796-798,
  introduces the moment/LMI approach, includes0/1 problems, and defines moment
  matrices in Section 2. This is the general relaxation machinery.
- [Torquato-Stillinger, 2003](https://doi.org/10.1103/PhysRevE.68.041113),
  SectionII, especially p. 041113-5 and equations(28)-(30), distinguishes spectral
  covariance positivity from point-process realizability and explains
  hyperuniform number-variance behavior.
- [Kuna-Lebowitz-Speer, 2007](https://arxiv.org/abs/math-ph/0612075v2),
  Section 2, pp. 5-7, equations(2.1)-(2.9), treats correlation nonnegativity,
  covariance PSD, and additional constraints such as Yamada's condition.
- [Kuna-Lebowitz-Speer, 2011](https://doi.org/10.1214/10-AAP703),
  Section 3.1, Theorem 3.2, pp. 1260-1261, requires nonnegativity against every
  admissible quadratic configuration polynomial. Section 3.2, Theorem 3.4,
  pp. 1261-1262, gives a sufficiency result under hard-core conditions.

Consequently a feasible pair in this particular SDP does not thereby produce
a probability distribution on Sidon sets. Nor would sharpness of this SDP
prove that all possible arguments using pair information have the same floor.
Additional valid quadratic inequalities can restrict pair data. Higher
moments are one possible strengthening, rather than a logically necessary
exclusive next step.

## Search result and significance boundary

Current head, current tree, arXiv version and Chen latest-record checks were
successful. No later proof of the exact conjecture was located in the bounded
web/code search. General indexing was poor and one code search failed.
Missing helper files and empty/irrelevant results cannot establish priority.

A complete lower proof would turn an explicitly motivated but unproved
claim into a theorem. The significance would be a precise limitation of an
important, explicitly defined relaxation. The construction, coefficient,
renewal mechanism and covariance mechanism should remain prominently
attributed. The result would not be a Sidon-set construction, a physical
bound below Chen's coefficient, a universal pair-information barrier, or a
resolution of Erdős 30.

## Final execution comparison

The final candidate was inspected directly, without using proof-review
verdicts as evidence. The separate [final comparison](FINAL_CLAIM_COMPARISON.md)
binds the exact effective statement to the existing sources and assesses its
usefulness, significance and private-manuscript gate. The compared proof-file
hashes are in [the candidate binding](CANDIDATE_BINDING.json).

Conditional on correctness, the substantive contribution is the uniform
bounded-loss lower theorem completing the announced conjecture, particularly
the structured all-lag estimate with its global N^(-1/2) remainder. The upper
companion is an attributed transfer of known material. This source audit
does not itself accept the mathematics.

If execution yields only an upper transfer, retain an attributed corollary.
If the frozen ansatz fails a lag, retain a precise obstruction; this would
not disprove the SDP conjecture. If a weaker o(N^(1/4)) lower loss is all that
is proved, label coefficient sharpness separately. Mathematical correctness,
novel contribution, significance and publication readiness remain separate
decisions. External circulation or publication is not authorized here.
