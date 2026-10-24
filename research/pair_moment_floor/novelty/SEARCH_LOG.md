# Bounded novelty search, 2026-10-23

This is an execution-stage search record. Earlier approval or novelty reports
were not used as evidence. The mathematical baseline comes from the original
manuscripts, original code and classical papers pinned in `SOURCE_LEDGER.json`.
No author was contacted, no external text was posted, and no mathematical
numerical campaign or solver was run.

## Version and code checks

Live GitHub connector `GET /repos/{owner}/{repo}/commits/main` returned:

| Source | Current commit | Commit date UTC |
| --- | --- | --- |
| johnakwei/Science | 7934a1b1193307b09326c8cb3638f50552603388 | 2026-10-10 17:35:57 |
| HbZhao1/sidon-vector-smoothing | ef044564300e546f8832b31f5fba133fd192cc3a | 2026-07-04 08:01:54 |
| chy4pro/automath | 5542184180d014b68637851941109dd5e584e920 | 2026-10-12 05:25:05 |

The complete recursive Akwei and Chen trees were retrieved. The first HZ tree
request disconnected; one later request succeeded. Nine selected cached
GitHub files, including the three Akwei manuscript PDFs, HZ original search
and certificate code, and Chen proof/checker text, match their current Git
blob SHA-1 IDs exactly. Their separate SHA-256 hashes are in the ledger.
Source code was read, not executed.

The current [HZ arXiv abstract](https://arxiv.org/abs/2607.01169) still identifies
v3, revised 4 September 2026. The fresh
[Chen latest-version endpoint](https://zenodo.org/api/records/23273526/versions/latest)
returns record 23273526, version 3, DOI 10.5281/zenodo.23273526. Its PDF checksum is
consistent with the pinned v3 artifact. The unsuitable concept-record
`/api/records/23103979/versions` route returned 404; the successful concrete-record
latest route is the version evidence. Chen's GitHub `/releases/latest` also
returned 404. Neither404 implies absence of a newer mathematical result elsewhere.

Four advertised Akwei helper paths were independently checked against the
pinned current revision and returned 404: `sym512c.py`, `upsample.py`,
`verify_sym_certs.py`, `README_K2_certificates.md`. The complete current tree
contains no such helper files. A connector contents request for `sym512c.py`
also returned 404. This limits implementation comparison and provides no
affirmative novelty evidence.

## General web search queries

The search service was called in four bounded batches, with these literal
queries. Results were inspected for an exact model, named conjecture or
uniform theorem rather than mere keyword co-occurrence.

| Batch | Queries | Result relevant to the exact theorem |
| --- | --- | --- |
| 1 | `"Sidon" "Conjecture 7.7"`; `"Sidon" "pair-moment"`; `"The limit of vector-valued smoothing for Sidon sets"`; `"Sidon" "Akwei" "relaxation"` | No later proof located. A point-process moment extension lemma appeared in an adjacent automated-research wiki; it did not state this floor theorem. |
| 2 | `"Sidon" "semidefinite" "renewal"`; `"Sidon" "7.7" "Akwei"`; `"Sidon" "pair-level relaxation"`; `"Sidon" "hat h" "moment" "smoothing"` | No later proof located. Mostly unrelated papers or broad keyword matches. |
| 3 | `"Sidon" "2sqrt2/3" "relaxation"` with the square-root symbol in the actual query; `"Sidon" "Conjecture 6.6"`; `"Sidon" "Fejer" "moment"`; `"Sidon" "semidefinite program" "N" "renewal"` | No later proof located. An original Erdős 30 work thread described the physical problem and ruler computations rather than the exact SDP claim. |
| 4 | `"Akwei" "Sidon"` with 30-day recency; `"2sqrt2/3" "Sidon"`; `"Sidon" "H2(N)"`; `"Sidon" "all-N" "relaxation"` | No later proof located. The H2 notation also retrieves unrelated Hilbert-cube notation. |

For exact reproducibility, the batch3 first literal query used `2√2/3`, not the
ASCII rendering in the table. Search engines normalize this notation poorly.
The spelling alternatives `Fejer` and `pair-level` are included above; the
primary PDF itself uses Fejér and a hatted h2 notation.

GitHub code search for `Conjecture 7.7 Sidon` returned mostly irrelevant token
files and a mirror of Chen's already known paper; it located no new proof.
`pair-level relaxation Sidon` failed with an internal connector error. The raw
connector receipts are retained in `sources/`. The mirror was not used as
mathematical evidence; Chen's original manuscript was inspected instead.

## Meaning and limitations

No later proof of Akwei's exact all-integer-N conjecture was located by these
checks. This is a bounded search result, not an exhaustive bibliographic
priority determination. General search indexing of this material was weak;
one failed search was not silently converted into a negative result.

Classical covariance/realizability papers were read from the supplied cached
original PDFs and hashed, with fresh text extractions retained locally. Their
metadata were identified from the original title pages and DOI/arXiv labels.
The classical papers supply attribution and a scope warning, not an all-N
Sidon floor theorem. No claim of current revision search for those older
papers is made.
