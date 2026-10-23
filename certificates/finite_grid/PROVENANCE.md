# Provenance, source mapping and preservation

Ariel M. Williams directed the construction, acceptance criteria, software,
exact independent verification and preservation. Work used AI-assisted
computation, drafting and review. No affiliation, endorsement or external
refereeing by the cited authors is implied.

## Analytic dependencies

- Jianfeng Hou and Hongbin Zhao, [version3 Theorem2.1](https://arxiv.org/abs/2607.01169v3): original finite symmetric smoothing model, normalized nonnegative symmetric kernels and weights, real boundary coordinates, exact unit tails and fixed-certificate asymptotic transfer.
- John Akwei, [pinned manuscript](https://github.com/johnakwei/Science/blob/7934a1b1193307b09326c8cb3638f50552603388/The_limit_of_vector-valued_smoothing_for_Sidon_sets.pdf): continuum ramp/renewal analysis, reported approximate finite-grid behavior, Proposition5.2 quantitative construction and AppendixB localized repair. These ideas and the smoothing floor are credited dependencies.
- Haoyu Chen, [version3 capacity/physical note](https://zenodo.org/records/23273526): distinct continuum/physical statements. The finite coefficient here remains above2sqrt(2)/3 and is not claimed to improve the strongest external physical coefficient.
- Classical renewal, lossless-filter factorization, coefficient root exclusion and finite inverse/repair arguments are used explicitly. No new generic version of that machinery is claimed.

The original finite model uses M=2n, kernels1/(2k) on bins n-k,...,n+k-1,
lambda_k=4k^3/n^4 for k<n, and lambda_n=(2n-1)/n^2. Every cover q=0,...,ML
is checked. The constants are a=M sum lambda_k sum p_ki^2 and
b=1+(2/M)sum lambda_k sum_(j<ML)(v_kj^2-1). Boundary signs are unrestricted.
For fixed certificate data, the cited theorem supplies the usual coefficient
sqrt(ab) in the Sidon bound. No uniform remainder for data varying with the
ambient interval is asserted.

## Construction and exact identities

The new witness uses the positive discrete renewal recurrence with128
fractional interval bits and80-bit dyadic proposals. Its exact widest-component
repair makes every cover equal one. No floating solver, optimizer, alternative
kernel, mixture or boundary profile is an input. With n2048,M4096 fixed, an
explicit rational error bound selected L30 for the initial Pell benchmark
1121/1189 before full construction. The earlier v1.4.0 multiplier
and asymmetric two-sided boundary are not inputs to this certificate.

The public declaration is11785113371/12500000000. The research construction's
initial declaration was1121/1189; exact verification of its actual a,b,ab
supports the stronger public declaration without changing any kernel, weight
or boundary value. WITNESS.json records SHA-256 identities of the retained
research core, repair and original gzip. These are provenance identities,
not substitutes for reconstruction, and no private file is required to check
the public witness.

The compact and actual-array checkers use separate verification arithmetic.
The optional original JSON gzip is exported from the same exact data. Its
release copy changes only the declaration in the header; the component array
members are preserved byte for byte. Exact public results and asset hashes
are frozen in the accompanying manifests and release checksums.

Each component contains J=122880 finite boundary coordinates; the complete
array contains 251658240 finite entries. Invisible prefixes are fixed zero,
so that total is not a count of freely variable coordinates. Boundary entries
from J onward are the exact unit tail specified by the original schema.

## Replay state and trust scope

Defaults keep state in the repository-local tmp tree. An explicit `--state-dir`
may select another dedicated directory you control, including another controlled
checkout. Resume only private state produced by your own replay. Atomic
snapshots, checksums and input/code identities detect damage and accidental
mismatch; a checksum is not a signature authenticating an externally supplied
checkpoint. A fresh directory or `--no-checkpoint` provides fresh arithmetic
without relying on saved work. Completed prior runs start fresh arithmetic.

## Novelty and chronology

The useful application is the explicit fixed-grid analysis, prospective finite
error allowance and solver-free rational realization with exact checking.
Substantial content is inherited from Hou--Zhao, Akwei and classical methods.
The bounded source audit does not support a broad first-discovery or
standalone-manuscript recommendation. Four advertised Akwei implementation
artifacts were inaccessible during that audit; failed retrieval is not
novelty evidence and limits implementation-priority comparisons.

The earlier dated R9 development and communication remain recorded in the
root development history. Those specific records predate the inspected
August27 q2 commit; they do not identify the starting date of all external
work or establish first public availability. No claim is made that another
group used private materials. Historical R9, R16, two-sided and v1.4.0
symmetric bytes, tags, assets and Zenodo versions remain preserved.

Third-party papers are cited rather than bundled or relicensed. Our own new
code, certificate data and documentation use the repository's MIT license.
