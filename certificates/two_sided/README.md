# Seven exact two-sided linear-ramp certificates

These are unchanged finite rational research artifacts constructed under Ariel
M. Williams's direction with AI assistance. Akwei supplied the ramp construction
and two-sided framework; Hou--Zhao supplied the smoothing lineage.

| m | L | Exact strict coefficient upper bound |
| ---: | ---: | ---: |
| 32 | 8 | 0.942924807 |
| 64 | 8 | 0.942838305 |
| 128 | 8 | 0.942817031 |
| 256 | 8 | 0.942811945 |
| 512 | 8 | 0.942810791 |
| 1024 | 8 | **0.942810721** |
| 512 | 10 | 0.942811719 |

Every displayed bound is an exact rational decimal, with strictness checked by
comparing ab with its square. EXPECTED_RESULTS.json stores exact a,b,ab and
covering-slack results for all seven files. m=16 and other ledger-only levels
are not packaged as certificates because no corresponding file was preserved.

```text
python -I -S verify.py --all
python -I -S verify.py two_sided_linear_m1024_L8_certificate.json
```

Invoke these here, or use absolute script and certificate paths from elsewhere.
Without arguments the script checks the strongest bundled certificate.
--all checks the manifest and exact expected results as well. Mathematical
rejection exits 1; malformed input/usage exits 2. Verification needs only Python
3.10+ and the standard library. No generator or solver is used.

The copied smoothing_verify.py is byte-identical to the corrected research
module. MANIFEST.json binds every member except itself, with input hashes and
the research-module source hash. Certificate source bytes are unchanged.

The [main theorem mapping](../../DEVELOPMENT_AND_THEOREM.md) supplies the analytic
dependency. This package does not claim a new smoothing theorem, new method
floor, continuum attainment proof, current record, optimality, signed-C5
attainment, exponent improvement or Erdos #30 solution.
