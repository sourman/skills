---
name: canadian-t2-filing
description: Reconstruct years of unfiled corporate taxes from chaotic financial records. Use when the user has PDFs, CSVs, or bank statements they need turned into tax filings, or mentions overdue corporate taxes, expense categorization, GIFI schedules, or HST recovery.
---

# Tax Reconstruction Pipeline

You are helping a business owner reconstruct years of unfiled tax returns from chaotic financial records. This is a phased pipeline — do NOT skip phases or proceed past a gate condition.

**Core philosophy: Err on the side of inclusion.** The accountant will trim what's there, not add what's missing. Include borderline items and flag them rather than excluding upfront.

## Phase 1 — Archaeology: Sort the Chaos

**Trigger:** User dumps files (PDFs, CSVs) into a directory. Names are meaningless.

**DO NOT proceed to Phase 2 until:**
- [ ] Every file has been opened and inspected (headers, date ranges, column names)
- [ ] Files are grouped into directories by source institution
- [ ] Files are renamed to meaningful names based on their contents
- [ ] The user has confirmed the grouping is correct

**Steps:**
1. Read every file. Don't guess — inspect headers and sample rows
2. Identify distinct sources (bank, card, platform, account type)
3. Group by source into directories
4. Rename to content-based names (e.g., `amex_2023-04.csv` from the transactions inside)
5. Keep flat structures — users resist deep hierarchies

**Watch for:** numbered duplicates (`activity (1).csv`), format changes mid-year from issuer switches, Windows junk files, image-based PDFs needing OCR.

## Phase 2 — Extraction: PDFs to Structured Data

**Trigger:** Raw PDF statements need to become CSVs.

**Load:** `assets/extract_script_template.py`

**DO NOT proceed to Phase 3 until:**
- [ ] Every PDF has an extraction script
- [ ] Extracted transaction counts match visual inspection of at least 3 statements
- [ ] Balance verification passes for all statements (computed balance = stated balance)
- [ ] Cross-year date traps are handled (January statements contain December transactions)

**Steps:**
1. Use PyMuPDF (`fitz`) — preserves spaces better than alternatives
2. Build one script per institution (formats differ wildly)
3. Verify against stated balances after extraction
4. Print stats per file (transactions extracted, balance check pass/fail)

**Watch for:** issuer switches creating orphan format statements, negative balances with minus signs on separate lines, descriptions mashed together without spaces.

## Phase 3 — Categorization: Assign GIFI Codes

**Trigger:** Raw CSVs need to become categorized transactions with tax codes.

**Load:** `assets/categorize_script_template.py`, `references/categorization_decision_tree.md`, `references/gifi_code_reference.md`, `references/red_flags.md`

**DO NOT proceed to Phase 4 until:**
- [ ] Every transaction has a GIFI code or special account (PERSONAL/SHAREHOLDER/SKIP)
- [ ] All red flags from `references/red_flags.md` have been investigated with the user
- [ ] Currency conversions use Bank of Canada monthly average rates
- [ ] The user has reviewed a sample of categorizations and confirmed correctness
- [ ] Personal/business card classification is documented

**Steps:**
1. Build one script per tax year (keyword lists grow each year as edge cases emerge)
2. Follow `references/categorization_decision_tree.md` for every transaction
3. Apply `references/red_flags.md` checks — ask the user about any flagged items
4. Include an `hst_charged` column (yes/no) — use `references/hst_decision_tree.md`
5. Add `debit` and `credit` columns for double-entry accounting
6. Follow the column schema in `assets/csv_column_schema.md`

**Card types:**
- **Corporate cards**: 100% business. Trust everything.
- **Personal cards (mixed)**: Apply keyword filters. Default to inclusion for ambiguous items.
- **Payment platforms**: Check direction (in = revenue, out = contractor or shareholder).

## Phase 4 — Consolidation: Single Source of Truth

**Trigger:** Per-year categorized CSVs exist. Need one master file and GIFI schedules.

**DO NOT proceed to Phase 5 until:**
- [ ] All per-year CSVs are merged into one master `transactions_categorized.csv`
- [ ] Trial balance self-check passes: total debits = total credits for each year
- [ ] Shareholder loan schedule is traceable to actual transactions
- [ ] Pre-incorporation expenses are re-coded to proper GIFI codes (not a separate bucket)

**Steps:**
1. Merge all years into one CSV (generation scripts filter by date)
2. Verify double-entry integrity: sum(debits) = sum(credits) per year
3. Build shareholder loan schedule from actual contribution/withdrawal transactions
4. Handle pre-incorporation expenses: re-code to proper GIFI, add DUE_TO_SH credits

**Schema:** Follow `assets/csv_column_schema.md` exactly.

## Phase 5 — GIFI Generation: Official Tax Schedules

**Trigger:** Master CSV is clean and balanced.

**Load:** `assets/gifi_schedule_templates/`

**DO NOT proceed to Phase 6 until:**
- [ ] Schedule 125 (Income Statement) generated for each year
- [ ] Schedule 100 (Balance Sheet) balances: Assets = Liabilities + Equity
- [ ] Schedule 101 (Retained Earnings) flows correctly from year to year
- [ ] Schedule 8 (CCA) has $0 claimed in loss years
- [ ] Schedule 50 (Shareholders) lists all shareholders for each year
- [ ] Import files (.gfi, .csv) generated for tax software compatibility
- [ ] Summary stats printed: revenue, expenses, net loss per year

**Steps:**
1. Build one `generate_gifi.py` that reads the master CSV and produces all outputs for all years
2. Hardcode non-derivable data: CCA/asset records, cash balances
3. Use templates from `assets/gifi_schedule_templates/` for output format
4. Print per-year summary for sanity checking
5. Verify balance sheet equation for each year

## Phase 6 — HST/GST Recovery

**Trigger:** Categorized transactions exist with `hst_charged` column.

**Load:** `references/hst_decision_tree.md`

**DO NOT proceed to Phase 7 until:**
- [ ] ITC calculated only on transactions where `hst_charged = yes`
- [ ] Meals ITC at 50% (matching deductibility)
- [ ] Foreign transactions and financial services excluded
- [ ] Refund/reversal ITC reversed
- [ ] Per-period returns calculated (HST collected minus ITCs)

**Steps:**
1. The `hst_charged` column is the source of truth — no pattern matching
2. Apply extraction rates: HST 13/113, GST-only 5/105
3. Meals: ITC at 50% of the HST portion
4. Calculate net refund per period (if revenue is zero-rated, this is pure refund)
5. Output: `itc_detail.csv`, `hst_returns.csv`, `hst_excluded.csv`

## Phase 7 — Review and Fix

**Trigger:** All outputs generated. "Is this right?"

**Load:** `references/review_checklist.md`

**DO NOT declare the work done until:**
- [ ] All 6 checklists in `references/review_checklist.md` pass
- [ ] The user has reviewed the consolidated findings
- [ ] All fixes have been applied and outputs regenerated
- [ ] Trial balance still balances after fixes

**Steps:**
1. Launch 3-5 parallel review agents using checklists from `references/review_checklist.md`
2. For money flow tracing: launch 2-3 independent agents and compare results
3. Consolidate findings into numbered list with dollar impacts
4. Present to user for approval before making changes
5. After fixes: re-run generate_gifi.py and hst_prepare.py, verify balance

**Common fixes needed:**
- Misclassified transactions (personal ↔ business)
- Missing data discovered during review
- Shareholder complications (surprise co-founders, buyouts)
- HST edge cases (foreign merchants, platform account types)
- Refund reversals not netted against original categories

## Accumulated Knowledge Files

Build these as you work — they're living documents:

| File | Purpose | When to Update |
|------|---------|----------------|
| `TAX_GUIDELINES.md` | Tax rules, deadlines, deduction limits, CRA references | During research and whenever rules are clarified |
| `CLAUDE.md` | Project instructions, data sources, commands | When project structure changes |
| `share_transactions.md` | Share structure history and ownership changes | When shareholder info is discovered |
| `shareholder_loan_schedule.csv` | Running balance of contributions/withdrawals | After each categorization pass |
| Memory files | Key decisions and feedback ("store X is always personal") | Immediately when decisions are made |

## Key Principles

1. **Single source of truth**: One CSV, many derived outputs. Fix the source, regenerate everything.
2. **Self-validating**: Debits = credits. Balance sheet must balance. If it doesn't, stop and fix.
3. **Honesty over comfort**: Show reconciliation gaps clearly. Don't paper over with estimates.
4. **Name things for what they ARE**: `hst_charged` (was tax charged?) not `hst_eligible` (could it be?).
5. **The back-and-forth is the work**: Expect 5-10 review cycles. Each pass catches something the last missed.
6. **Check subagent work**: Subagents cut corners. Verify assumptions before accepting output.
7. **Accumulate decisions in writing**: Every ruling ("store X is personal", "person Y is a shareholder") goes into a memory file immediately.
