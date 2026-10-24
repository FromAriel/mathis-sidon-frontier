# Effective pair-moment sharpness: v1.6.0 preprint

**External human verification and peer review are pending.** This package
presents a proposed effective proof of Akwei's Conjecture 7.7 for exactly
Definition 7.2's noncyclic pair-moment relaxation. Two separate internal
AI-assisted mathematical reviews accepted the written argument. No Lean or
other proof-assistant verification is claimed.

For every integer N >= 2^60, the proposed theorem states

```text
sqrt(N) + (2 sqrt(2)/3) N^(1/4) - 2572
  <= h_hat_2(N)
  < sqrt(N) + (2 sqrt(2)/3) N^(1/4) + 1.
```

## Read the argument

- [Public manuscript PDF](manuscript/main.pdf) and [TeX source](manuscript/main.tex).
- [Exact model and theorem](STATEMENT.md).
- [Full proof index](FULL_PROOF.md), followed by its three linked proof sections.
- [Objection resolutions](OBLIGATIONS_AND_OBJECTIONS.md) and [final assessment](FINAL_ASSESSMENT.md).
- [Operator review](reviews/operators/FINAL_OPERATOR_REVIEW.md) and [finite/error review](reviews/finite/FINAL_FINITE_REVIEW.md).
- [Claim-by-claim novelty assessment](novelty/FINAL_CLAIM_COMPARISON.md), [primary-source comparison](novelty/PRIMARY_SOURCE_NOVELTY_AUDIT.md) and [source/hash ledger](novelty/SOURCE_LEDGER.json).

Akwei receives credit for the conjecture, exact model, renewal profile,
atoms, covariance construction and cap. The upper companion uses Chen's
attributed positive-measure energy bound. The proposed contribution is the
uniform all-distance analysis and explicit constant-loss construction.

The theorem concerns a relaxation. It neither constructs Sidon sets nor
improves the previously published numerical coefficient. Bounded literature
searches do not establish worldwide priority. AI assistance in derivation,
drafting and internal review is disclosed in the manuscript.

## Provenance and review status

The proof sections, objections and review/audit reports retain their audited
bytes. Historical references to a private draft, withheld publication
readiness or no circulation describe the pre-release audit state. Public
archival release is now authorized; it does not change external verification
status. The public manuscript changes author/public-status wording only;
its mathematical sections are unchanged. [Publication status](PUBLICATION_STATUS.json)
and [file hashes](MANIFEST.json) distinguish this release copy from historical
review bindings to the private manuscript. [Compilation receipt](manuscript/COMPILE_RECEIPT.json)
binds the public PDF.

Third-party PDFs, extracted text, operational logs and local source caches
are omitted. Source-ledger cache paths identify historical audit inputs;
use their pinned source URLs and hashes, rather than treating those paths as
bundled files. No numerical campaign or repeated certificate replay was run
for this analytical release.

The manuscript uses four TeX files and standard packages, with an inline
bibliography. Compile `manuscript/main.tex` with a LaTeX engine or Tectonic.
Earlier certificate packages remain in the repository; large optional data
stay on their original releases. In particular, [v1.5.0](https://github.com/FromAriel/mathis-sidon-frontier/releases/tag/v1.5.0)
and [its Zenodo record](https://doi.org/10.5281/zenodo.23600836) preserve the
0.942809069680 certificate.
