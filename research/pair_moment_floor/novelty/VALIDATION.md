# Source-audit tooling validation

Date: 2026-10-23. Scope: provenance bookkeeping only.

- `python -m ruff check .../novelty/build_source_ledger.py`: PASS.
- `python -m ruff format --check .../novelty/build_source_ledger.py`: PASS.
- Python AST parse of the script: PASS.
- Ledger JSON parse, fifteen original-source entries, all nine current-Git
  blob comparisons true, all referenced original files present: PASS.
- Fresh latest Chen PDF metadata: MD5
  `471fb69a8d0045ad6d1a93301833a507`,493055 bytes, exactly matches cached PDF.
- Akwei current Conjecture 7.7 PDF p. 14 rendered and visually inspected: printed
  statement matches extraction.

The script's first formatting/lint checks found style issues, corrected with
native pre-edit backups; the final checks above passed. A Windows shell glob
read and two ad-hoc extraction display commands failed because of glob and
console-encoding behavior, respectively. They were corrected without changing
any original source. All network failures are retained separately in the
search record and HTTP/connector receipts.

No downloaded checker or optimization program was executed. No mathematical
numerical campaign, solver, FFT, sampled renewal sweep or application launch
was performed. These checks verify source bookkeeping, not the candidate
theorem. The acquisition script deliberately uses exclusive file creation;
rerunning it in the same packet is expected to fail rather than replace
recorded receipts.
