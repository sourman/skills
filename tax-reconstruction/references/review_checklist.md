# Review Checklist — Multi-Angle Audit

When categorization is "done," it isn't. Run this checklist before declaring the work complete.

---

## Checklist A: Transaction Completeness

Run these checks before proceeding to review:

- [ ] Count rows in each source CSV → total must match rows in categorized output (within expected exclusions)
- [ ] Every source directory has been processed (no leftover CSVs)
- [ ] Date ranges in categorized output match the fiscal year boundaries exactly
- [ ] No duplicate transactions (same date, amount, description appearing twice without explanation)
- [ ] All payment/refund transactions are excluded from expense totals

## Checklist B: GIFI Code Accuracy

Spot-check categorizations against transaction descriptions:

- [ ] Sample 20 random transactions from each year. Verify GIFI code matches description
- [ ] Check the "OTHER" (9270) bucket — if it's >15% of total expenses, create new categories
- [ ] Verify meals/entertainment (8910) is flagged as 50% deductible
- [ ] Verify travel (8980) is 100% deductible
- [ ] Check that SHAREHOLDER and PERSONAL transactions are excluded from GIFI totals

## Checklist C: HST ITC Accuracy

- [ ] ITC claimed only on transactions where `hst_charged = yes`
- [ ] Meals ITC calculated at 50% (not 100%)
- [ ] Foreign transactions excluded (no Canadian HST was charged)
- [ ] Financial services excluded (bank fees, insurance, transfer fees)
- [ ] Refund/reversal ITC reversed to match the original expense reduction
- [ ] Airlines in GST-only provinces use 5/105 extraction (not 13/113)

## Checklist D: Excluded Transaction Audit

Review transactions labeled PERSONAL to catch business expenses that were excluded:

- [ ] Sample 20 PERSONAL transactions. Could any plausibly be business?
- [ ] Check for business software tools hiding in personal categories
- [ ] Check for professional services (legal, accounting) that were on personal cards
- [ ] Verify the user's blanket rulings ("store X is always personal") are consistently applied

## Checklist E: Cross-Year Consistency

- [ ] Same merchant categorized the same way across all years
- [ ] Same expense type gets the same GIFI code across all years
- [ ] Personal/business classification is consistent across years
- [ ] Exchange rate methodology is consistent (monthly averages, not spot rates)

## Checklist F: Balance Sheet Integrity

- [ ] Trial balance: total debits = total credits for each year
- [ ] Balance sheet: Assets = Liabilities + Equity for each year
- [ ] Retained earnings flow: current year RE = prior year RE + net income/loss
- [ ] Shareholder loan balance is traceable to actual transactions
- [ ] CCA Schedule 8: opening UCC + additions - dispositions - CCA = closing UCC

## Running the Review

For maximum coverage, launch 3-5 parallel review agents, each assigned one checklist. Compare results. Where agents disagree, the discrepancy itself is the finding.

Consolidate into a numbered list:
```
Finding #N: [description]
  Impact: $X in [expense/ITC/balance sheet]
  Fix: [what to change]
  Affected years: [which years]
```

Present the consolidated list to the user before making changes.
