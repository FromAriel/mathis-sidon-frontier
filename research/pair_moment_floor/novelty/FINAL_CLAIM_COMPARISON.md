# Final claim comparison and significance judgment

Date: 2026-10-23. Independent novelty assessment, conditional on mathematical
correctness. No earlier approval report or current reviewer verdict is used
as evidence. The proof sections themselves and original sources were read.

## Compared statement

For exactly Akwei Definition 7.2, the submitted candidate asserts

\[
 \sqrt N+\frac{2\sqrt2}{3}N^{1/4}-2572\le H_2(N)
 <\sqrt N+\frac{2\sqrt2}{3}N^{1/4}+1
 \qquad(N\in\mathbb Z,\ N\ge2^{60}).
\]

The construction uses ell=ceil(sqrtN)+514, delta=1/ell,
H=floor(sqrt2*N^(3/4)), beta=1-1026/N^(1/4), the full renewal profile,
positive-part additive ends, centered uniform endpoint atoms and the capped
Fejer covariance. `CANDIDATE_BINDING.json` hashes the statement, combined
proof and three proof sections as inspected. Changes after that snapshot
require checking that this comparison still describes the actual claim.

The exact model and all-integer-N quantifiers agree with the announced target.
This is an effective version of
[Akwei's Conjecture 7.7](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/Sidon_smoothing_limit.pdf),
PDF p. 14. Neither a subsequence theorem nor a coefficient-limit assertion has
silently replaced the bounded remainder.

## Proof ingredient comparison

| Candidate item | Comparison with inspected primary sources | Contribution assessment |
| --- | --- | --- |
| Renewal definition, limiting mass and elementary tail contraction | Existing renewal machinery in Akwei and Chen; constants are deliberately weakened for uniform use | Attributed reconstruction and convenient bounds. |
| Full cancellation inequality R2 | Akwei Lemma 7.4 and its preceding renewal-correlation analysis | Existing key identity/inequality. |
| C_U+sigma<=U, R3 | Reorganizes the existing cancellation into a form suitable for averaging | Useful proof organization; not a new renewal mechanism. |
| PSD, nonnegative entries and diagonal completion | Akwei Lemma 7.5 | Existing Fejer construction. |
| Positive-part additive profile and outer-strip comparison D7 | Explicitly repairs the analytic-tail positivity problem | Part of the completed uniform finite-interval argument; its value lies in the charged error. |
| BV lattice quadrature D1 and elementary atom intersection D2 | Standard estimates and interval counting | Tools/bookkeeping, not standalone novelty. |
| Cap control D3-D6 | Quantifies the inherited covariance cap, retaining the exact triangular multiplier | Necessary uniform error accounting. |
| Finite overlap expansion D8, including cross-end tails | Strengthens the half-line heuristic to an explicit finite-interval estimate | Part of the candidate theorem's analytical completion. |
| Averaging the COMPLETE cancellation inequality in D9-D10 | Retains the renewal jump while using a Lipschitz bound only on C_U | The clearest specific step beyond the inspected heuristic: it avoids an unjustified smooth Taylor argument. |
| Structured estimate D13 and exhaustive long-lag/opposite-atom estimates D14-D15 | Uniformly separates triangular O(N^(-1/4)) error from global O(N^(-1/2)) error | Principal technical contribution if correct. |
| Explicit beta/ell choices, tail absorption and objective bound M1 | Converts uniform estimates into one effective feasible family | Completes the all-N bounded-loss lower theorem. Constants are not claimed optimal. |
| Upper U1-U3 with additive1 and onset 4,600,000 | Chen positive-measure energy bound, combined with Akwei's PSD trace principle | Attributed SDP corollary. Chen's physical +1 theorem and its real-root algebra already exist. |

This distinguishes a new proof of an announced statement from a new ansatz.
The inspected source already motivates atom reduction by O(N^(-1/4)) and
predicts bounded mass loss. The potential contribution here is proving all
required implications with explicit constants, including transition lags,
clipping and endpoint overlap. A general per-lag O(N^(-1/4)) estimate alone
would not be the same theorem: global density loss could then be unbounded.

## Conditional novelty determination

No prior all-integer-N proof of this exact conjecture was located in the
bounded search or current original manuscripts/code. Current source versions
and limitations are recorded in `PRIMARY_SOURCE_NOVELTY_AUDIT.md`,
`SEARCH_LOG.md` and `SOURCE_LEDGER.json`. This supports a candidate
contribution beyond the formulas already proved in those inspected sources.
It does not establish worldwide priority, and missing code is not evidence
in favor of novelty.

Conditional on correctness, the appropriate description is:

> An effective proof of Akwei's conjecture for the specified pair-moment
> Sidon relaxation, obtained by uniform analysis of the attributed renewal
> and Fejer construction.

This wording credits the originator of the statement and construction while
identifying the analytical work actually added. A title suggesting a new
Sidon-set construction, a new coefficient, a discovery of hyperuniform
covariance, or a general impossibility theorem for pair statistics would
overstate the result.

## Usefulness and significance

The result would replace four computational examples and an explicit
conjecture with a theorem covering every sufficiently large integer N. It
would establish the precise second-order power of this natural relaxation,
even when its feasible pairs need not be realizable by random sets. That is
a meaningful specialized contribution to understanding the method's limits.

The theorem would also give future work a concrete comparison family: a
proposed strengthening can be tested against the moment pair or against its
specific omitted constraints. It would clarify that retaining PSD covariance
and separate difference budgets in this exact model does not by itself
improve the leading second-order coefficient.

The printed constants and onset are conservative existence bounds. They
should not be presented as a practical optimum or an improvement of the
physical Sidon upper bound. The core value is the uniform theorem and the
handling of its error structure. Its ingredients are largely inherited,
and its scope is narrower than a theorem about all possible uses of pair
data. This is enough to justify serious private mathematical review if the
proof is accepted; it does not justify claims about Erdős 30, a prize, or a
general breakthrough in additive combinatorics.

## Private attributed manuscript gate

Assuming both fresh mathematical reviews accept the complete proof and
their objections are resolved, this novelty audit supports preparing a
private attributed manuscript or research note around the named conjecture.
That recommendation is conditional and is not external-publication approval.
The paper should lead with the exact relaxation, state the theorem and
constants, give the inherited ansatz full attribution, and isolate the
structured all-lag proof as its main contribution. It should include the
direct Chen-to-SDP upper transfer as a short attributed companion.

The bounded literature search leaves priority uncertainty. Before external
circulation, a separate final source/version check and mathematical review
of the manuscript are appropriate. No author contact, submission or public
posting was performed or authorized by this audit.

If mathematical review rejects a uniform estimate, the novelty headline is
withdrawn accordingly: an obstruction or a weaker limit theorem must be
described with its actual quantifiers. Source overlap and mathematical
correctness remain independent questions; neither a new-looking formula
nor agreement among reviewers establishes both.
