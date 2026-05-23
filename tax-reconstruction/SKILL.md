---
name: tax-reconstruction
description: Reconstruct years of unfiled corporate taxes from chaotic financial records using iterative AI-assisted data extraction, categorization, and CRA form generation
---

# Tax Reconstruction: From Chaos to Filed Returns

This skill teaches AI agents how to help a business owner reconstruct years of unfiled tax returns from a mess of PDF statements, CSV exports, and scattered financial records. It distills a real project where Claude helped prepare 4 years of overdue Canadian corporate tax filings for a small CCPC.

## When to Use This Skill

- A business owner has years of unfiled tax returns and needs to reconstruct their financial history
- Financial records exist as PDFs, CSVs, and exports from multiple institutions in various states of organization
- You need to produce official tax forms/schedules from raw transaction data
- The work involves categorizing thousands of transactions into tax-relevant categories
- The project will involve iterative refinement — not a single pass

## Core Philosophy

**Err on the side of inclusion.** The work will be handed to a conservative accountant who will review and trim expenses, but will only look at what's included. If you exclude something doubtful upfront, it's gone. If you include it, the accountant can decide to remove it. Over-include and let the accountant filter down.

**Single source of truth.** Maintain one master transactions file that everything derives from. All GIFI schedules, HST returns, and balance sheets should be generated from this one file, not maintained separately.

**Self-validating outputs.** Use double-entry accounting (debits = credits) so trial balances self-check. If the numbers don't balance, something is wrong — don't proceed.

## The Process: 7 Phases

### Phase 1: Archaeology — Sorting the Chaos

**What happens:** The user dumps files — PDFs, CSVs, screenshots — from multiple financial institutions into a directory. Names are meaningless (`activity.csv`, `activity (1).csv`, statement PDFs with dates or cardholder names).

**What to do:**
1. Read every file. Don't guess — actually open and inspect headers, date ranges, and column names
2. Identify distinct sources (which bank, which account, which cardholder)
3. Group into directories by source institution
4. Rename files to meaningful names based on their contents (e.g., `amex_2023-04.csv` based on the transactions inside, not the filename)
5. Keep flat structures — the user will resist deep hierarchies

**What can go wrong:**
- Files that look identical but cover different date ranges (numbered duplicates like `activity (1).csv`)
- PDFs from the same institution but different time periods with completely different formats (e.g., a card issuer switch mid-year)
- Windows junk files (`Zone.Identifier`, `desktop.ini`)
- Image-based PDFs that need OCR, not text extraction

### Phase 2: Extraction — PDFs to Structured Data

**What happens:** Build Python scripts to parse PDF statements into CSVs. Each institution has a different format. Some use text layers; some are scanned images.

**What to do:**
1. **Start with PyMuPDF (`fitz`)** — it preserves spaces and layout better than alternatives. `pdfplumber` is a backup
2. **Expect format differences** — even within the same institution, statement formats change over time. Build flexible parsers
3. **Verify against stated balances** — after extracting, compare computed balances against what the statement says. This catches extraction bugs
4. **Watch for cross-year date traps** — a January statement contains December transactions. A naive parser assigns them to the wrong year
5. **Handle the orphans** — one Capital One statement sitting in the middle of a CIBC run because the card issuer switched. It has a completely different layout. Write a separate parser for it

**Script pattern:**
```
extract_<source>.py → sources/<source>/csv/ per-statement CSVs
```

Each script should:
- Accept optional filename args (for testing individual files)
- Output to a predictable CSV format
- Print verification stats (transactions extracted, balance checks)

### Phase 3: Categorization — Assigning Meaning to Transactions

**What happens:** Write per-year scripts that assign GIFI codes (or your jurisdiction's equivalent) to every transaction based on description pattern matching.

**What to do:**
1. **Start with keyword lists** — personal keywords (donations, groceries, personal insurance) and business keywords (software, travel, professional services)
2. **Build layered matching** — first exclude personal, then match business categories, then catch remaining as "other" for manual review
3. **Handle mixed cards** — some credit cards are 100% business (corporate cards); others are mixed personal/business. Treat them differently
4. **Track the ambiguous** — flag transactions that could be either personal or business rather than deciding. The inclusion philosophy means leaning toward business
5. **Currency conversion** — use Bank of Canada monthly average rates for foreign currency transactions. Don't use spot rates
6. **Grow the keyword lists** — each year's script will have more keywords than the last as you discover edge cases

**The categorization hierarchy:**
```
1. Skip payments/refunds (exclude from expense totals)
2. Match personal keywords → PERSONAL (non-deductible)
3. Match personal spend categories on personal cards → PERSONAL
4. Match business keywords → appropriate GIFI code
5. Everything else → review and decide
```

**Script pattern:**
```
categorize_YYYY.py → output/YYYY/transactions_categorized.csv
```

Each script contains:
- GIFI code constants for the jurisdiction
- Monthly exchange rate tables
- Personal keyword list (growing each year)
- Business keyword rescues (business items in personal categories)
- Currency conversion helper
- Deductibility percentages (e.g., meals at 50%)

### Phase 4: Consolidation — Single Source of Truth

**What happens:** Merge all years into one master file with double-entry accounting columns.

**What to do:**
1. **Add debit/credit columns** — every transaction hits two accounts (e.g., expense debit + Due to Shareholder credit)
2. **Self-check** — total debits must equal total credits. If they don't, find the rounding error or missing entry
3. **Track shareholder contributions** — when the owner funds the business from personal accounts, create "Due to Shareholder" entries
4. **Handle pre-incorporation expenses** — expenses before the company was founded are claimable under specific tax provisions (e.g., ITA s.69(1)(b) in Canada). Re-code them to proper expense categories, not a separate bucket

### Phase 5: GIFI Generation — Official Tax Schedules

**What happens:** Generate the official tax schedules from the categorized data.

**What to do:**
1. **One script, all years** — `generate_gifi.py` reads the master file and produces all schedules for all years
2. **Produce all required schedules** — Income Statement (Schedule 125), Balance Sheet (Schedule 100), Retained Earnings (Schedule 101), CCA (Schedule 8), Shareholder info (Schedule 50)
3. **Hardcode what can't be derived** — CCA data, cash balances, and equipment records are manually maintained, not derived from transactions
4. **Generate import files** — produce `.gfi` and `.csv` files compatible with tax preparation software (TaxTron, Profile, etc.)
5. **Print summary stats** — revenue, total expenses, net loss for each year. Sanity-check against expectations

**Key schedules (Canadian T2):**
| Schedule | What It Shows |
|----------|---------------|
| 125 | Income Statement (revenue, expenses by GIFI code, net income/loss) |
| 100 | Balance Sheet (assets, liabilities, shareholder equity) |
| 101 | Retained Earnings / Deficit |
| 8 | Capital Cost Allowance (CCA) — depreciation for tax purposes |
| 50 | Shareholder information |

### Phase 6: HST/GST Recovery — The Hidden Refund

**What happens:** If the business never registered for sales tax but was eligible, calculate the Input Tax Credits (ITCs) that can be recovered.

**What to do:**
1. **Determine if HST was charged** on each transaction — use explicit flags in the data, not pattern matching. Add an `hst_charged` column during categorization
2. **Apply the correct extraction rate** — HST-inclusive amounts need 13/113 extracted. GST-only (5%) needs 5/105
3. **Apply deductibility limits** — meals are only 50% deductible, so only 50% of HST is recoverable
4. **Exclude non-eligible items** — foreign transactions (no Canadian HST was paid), financial services, zero-rated items
5. **Group by filing period** — annual periods matching the tax years
6. **Calculate net refund** — HST collected on revenue minus ITCs on expenses. If revenue is zero-rated, this is pure refund

**Output:**
```
output/hst/itc_detail.csv       — Every transaction with HST calculation
output/hst/hst_returns.csv      — One row per filing period
output/hst/hst_excluded.csv     — Excluded transactions with reasons
```

### Phase 7: Review and Fix — The Back-and-Forth

**What happens:** Multiple review cycles where the user finds issues, you fix them, and the changes cascade through all outputs.

**Common issues that arise:**
- **Misclassified transactions** — something marked personal that was actually business (or vice versa)
- **Missing data** — payment platform transactions for early years not in the dataset; bank statements for closed accounts
- **Shareholder complications** — discovering another shareholder existed, their buyout terms, and that payments are share purchases (not deductible expenses)
- **Exchange rate corrections** — wrong rates for specific months
- **Refund reversals** — refunds that reduce expense totals need to be netted against their original category
- **HST edge cases** — foreign merchants that do charge GST, airlines in GST-only provinces, financial services ITC that must be excluded
- **Balance sheet items** — cash balances, equipment values that need manual research

**How to handle review:**
1. Fix the categorization in the master CSV or per-year script
2. Re-run `generate_gifi.py` for affected years
3. Re-run `hst_prepare.py` to update ITC calculations
4. Verify trial balance still balances
5. Print before/after comparison for the user to confirm

## Key Tools & Scripts

Build these scripts in roughly this order:

| Script | Purpose | When to Build |
|--------|---------|---------------|
| `extract_<source>.py` | PDF → CSV for each bank/card | Phase 2 (one per institution) |
| `categorize_YYYY.py` | Assign GIFI codes + personal/business flag | Phase 3 (one per tax year) |
| `add_debit_credit.py` | Add double-entry columns to master file | Phase 4 |
| `add_hst_charged.py` | Flag HST on each transaction | Phase 6 |
| `generate_gifi.py` | Produce all GIFI schedules from master file | Phase 5 |
| `hst_prepare.py` | Calculate ITC refunds | Phase 6 |

## Accumulated Knowledge Files

As the project progresses, build these reference documents:

| File | Purpose |
|------|---------|
| `TAX_GUIDELINES.md` | Domain-specific tax rules, deadlines, deduction limits, CRA references |
| `CLAUDE.md` | Project instructions, data source descriptions, command reference |
| `sources/share_transactions.md` | Share structure history and ownership changes |
| `output/shareholder_loan_schedule.csv` | Running balance of shareholder contributions/withdrawals |
| Memory files | Key decisions, feedback, discovered facts (e.g., "that store is always personal") |

## Canadian-Specific Tax Knowledge

### GIFI Codes (General Index of Financial Information)

Common expense codes for a software/services CCPC:
- `8000` — Revenue from sales of goods and services
- `8840` — Consulting and professional fees
- `8890` — Interest and bank charges
- `8910` — Meals and entertainment (50% deductible)
- `8920` — Office supplies and expenses
- `8940` — Rent
- `8970` — Subcontracting costs
- `8980` — Travel
- `9110` — Telephone and communication
- `9180` — Computer software and supplies
- `9270` — Other operating expenses

### Special Accounts (Non-GIFI)
- `DUE_TO_SH` — Due to Shareholder (liability). Credits when owner contributes, debits when owner is repaid
- `PERSONAL` — Non-deductible personal expenses (skip in GIFI totals)
- `SHAREHOLDER` — Share purchase transactions (not deductible)
- `PRE_INCORP` — Pre-incorporation expenses (re-code to proper GIFI under s.69(1)(b))

### Key Rules
- **Meals & entertainment**: 50% deductible (100% for team events, max 6/year)
- **Travel**: 100% deductible (flights, hotels, taxis, rental cars)
- **CCA**: Claim $0 in loss years to preserve UCC for profitable years
- **Non-capital losses**: Carry forward 20 years
- **Shareholder loans**: Must repay within 1 year of year-end or it's taxable income
- **Pre-incorporation expenses**: Claimable under s.69(1)(b) ITA election

## Research Strategy: Waves of Erosion

Tax knowledge is not acquired in one search. Use a deliberate **research-by-erosion** strategy:

1. **Wave 1** (broad): Basic filing obligations, loss treatment, pre-revenue situations
2. **Wave 2** (targeted): Entity classification risks (e.g., Personal Services Business), specific deduction categories
3. **Wave 3** (deep): Shareholder loans, owner compensation mechanisms, retroactive registration
4. **Wave 4** (specialized): Capital assets and depreciation, audit triggers and preparation
5. **Wave 5** (synthesis): Year-by-year filing strategy, practical roadmap with deadlines

Launch 2 subagents per wave, each probing from a different angle. Refine the prompts between waves based on what came back vague. The goal: by the end, every major tax question has been answered with CRA source references.

**Distill findings immediately.** Write them into a `TAX_GUIDELINES.md` as you go. Don't wait until the research is "done" — the document is a living reference that the categorization scripts will depend on.

## War Stories: What Went Wrong and What We Learned

### The .COR File Dream and Its Death
The user wanted to generate a `.COR` file — the machine-readable format the CRA accepts for electronic filing. The research revealed: `.COR` files are proprietary, generated only by CRA-certified tax preparation software. There is no public specification.

**Lesson:** Don't assume government filing formats are open. Sometimes the best you can do is prepare the *data* (GIFI schedules, financial statements) so that an accountant or tax software can complete the filing. The work is still enormously valuable — the accountant would have charged thousands more to reconstruct this from raw PDFs.

### The Surprise Shareholder / Co-Founder Buyout
While reviewing recurring payments to individuals, the user casually dismissed one: "that one's just a pass-through." Investigation revealed this person had been a **co-founder and 50% shareholder** who was bought out months earlier. ~$15,000 in recurring payments previously coded as "subcontractor expenses" were actually share purchase installments — not deductible business expenses at all.

The payment notes contained "eqty 1st installment" — a smoking gun. But even without explicit notes, the pattern was suspicious: same recipient every month, same approximate amount, no deliverables or invoices tied to the payments.

**Red flags that a "contractor" might actually be a shareholder:**
- Monthly payments with no corresponding deliverables or project descriptions
- Payment notes containing "equity", "shares", "buyout", "installment", or "agreement"
- The user describes the person as a "partner" or "co-founder" in passing
- Large irregular lump sums mixed with regular smaller payments
- The payments started around the time the person's name disappears from corporate records

**What to ask the user when you spot these patterns:**
- "What was [Name]'s role? Were they ever a shareholder?"
- "Are these payments for services rendered, or related to a share purchase?"
- "Did [Name] contribute capital to the business? Was it repaid?"

**Lesson:** When the user dismisses a recurring payment as "just a pass-through" or "personal," dig deeper. Share buyouts disguised as contractor payments are a common mistake in small corporations. The tax treatment is completely different: contractor fees are deductible operating expenses, share purchases are non-deductible capital transactions. Misclassifying ~$15K as operating expenses would artificially inflate deductions and could trigger audit issues.

### The Stolen Asset and the Tax Silver Lining
A laptop purchased before incorporation, later transferred to the business, then stolen. Personal property transferred to a corporation is deemed acquired at fair market value (Section 69 ITA in Canada). A stolen asset qualifies as a terminal loss deductible from the CCA class. But since the corporation was in a loss year, claiming the loss would be wasted — it only increases an already-unused loss carryforward.

**Lesson:** Even when you find a deduction, check whether it *matters*. In loss years, additional deductions are worthless. Defer CCA claims and terminal losses to profitable years.

### The Missing Revenue
After completing all four years of categorization, the user had an instinct: "wait, are you sure we had no revenue that year?" They were right. ~$7,000 was hiding in a personal payment account that had been used for business late that year. The amount had never been captured because it was received in a personal account and nobody thought to check there. This meant one year was no longer a zero-revenue year, and every downstream calculation (balance sheets, cumulative deficits, shareholder loans) had to be recalculated across all years.

**Lesson:** Always ask "are you sure?" about zero-revenue years. Check all accounts the user controls, including personal ones that might have been used for business. Revenue hiding in unexpected places is more common than you'd think. Specifically ask: "Did you receive any payments for work in a personal PayPal, Venmo, bank account, or other platform that year?"

### The HST That Wasn't
A freelancer platform charges HST on Canadian accounts. But when the user's contractors were on non-Canadian platform accounts (routed through an overseas agency), no HST was charged. ~$1,800 in ITC was initially claimed on platform spending, but most had to be reversed because the transactions went through non-Canadian accounts.

**Lesson:** HST depends on the *seller's* GST/HST registration, not the buyer's location. A Canadian business paying through a foreign intermediary may not have Canadian HST embedded in the charge. Verify the actual HST charge on each transaction, not just the buyer's address. Ask the user: "Were your contractors on Canadian or non-Canadian accounts on that platform?"

### The Architecture Pivot
Initially, HST eligibility was determined by 150 lines of fragile pattern matching in the HST script. The user suggested adding an `hst_charged` column directly to the transactions CSV. The script went from pattern-matching to a simple column read. The user also preferred "hst_charged" over "hst_eligible" — "eligible is a bit muddy." Name the column after what it *is*, not what it *could be*.

The same session saw merging per-year transaction CSVs into one large file. The user: "What if we make the transactions CSV one large file and not split it per year?" The generation script just filters by date.

**Lesson:** When the data model becomes a bottleneck (fragile pattern matching, scattered files), simplify. A single column in a single file beats 150 lines of regex. The user will often see the simpler architecture before you do.

### The Pass-Through Trap
Some money flows looked like shareholder drawdowns (business payment account → owner's personal bank account) but were actually pass-throughs. The owner received money from the business account, then immediately paid corporate credit cards from their personal bank account. The money never reached their pocket — it was just routed through a personal account because the corporate card was linked there.

If classified as drawdowns, these would be taxable shareholder loans. If classified as pass-throughs, they're neutral. Each flow had to be traced individually against the credit card payment records.

**Red flags for pass-throughs vs. real drawdowns:**
- An outgoing business transfer to a personal account is followed within 1-3 days by a credit card payment of approximately the same amount
- The credit card being paid is a corporate/business card
- The transfer amount closely matches the card payment (small difference = transfer fees)

**What to ask the user:**
- "When you transferred $X from the business account to your personal account on [date], where did that money go next?"
- "Was this to pay a corporate credit card, or did you keep the funds personally?"

**Lesson:** Follow the money to its final destination, not just its intermediate stop. A transfer from business → personal → corporate card is not a drawdown. The intermediate personal account is just a routing mechanism.

### The Orphan Statement
In the middle of 47 statements from one card issuer sat a single statement from a *different* issuer — a fossil from the month the card program switched processors. It had a completely different layout. The extraction script needed an entire separate parser for this single orphan.

**Lesson:** Real-world financial data is never uniform. Always check for format changes, especially around known issuer/processor switches. Build parsers that can detect and handle multiple formats.

## Review Protocol: Multi-Agent Parallel Audit

When the categorization is "done," it isn't. Launch parallel review agents, each examining a different angle:

**Recommended review agents (launch simultaneously):**

1. **Transaction Completeness** — verify raw source counts match categorized output. Are any source CSVs missing?
2. **GIFI Code Accuracy** — spot-check categorizations against transaction descriptions. Is the catch-all bucket too large?
3. **HST ITC Accuracy** — verify ITC claims are only on expenses where Canadian HST was actually charged. Check for foreign merchants, financial services exclusions, refund reversals
4. **Excluded Transaction Audit** — review PERSONAL-labeled transactions. Are any actually business expenses?
5. **Cross-Year Consistency** — verify consistent treatment across all years (same merchant categorized the same way in 2023 and 2024)

**For money flow tracing**, launch 2-3 independent trace agents on the same data and compare results. If Agent 1 finds 31 transfers classified as pass-through while Agent 2 classifies all 28 as personal, the discrepancy itself is the finding.

**Consolidate findings** into a numbered list with dollar impacts. Present the before/after to the user for approval before making changes.

## Iterative Trust and Communication

This kind of project involves deep trust-building between user and AI:

1. **Early sessions**: The user says "discuss before making changes" and "let me check the result." Honor this — show plans, wait for approval, verify after execution
2. **Middle sessions**: The user starts saying "go for it" and "looks reasonable." You've earned trust through accuracy
3. **Late sessions**: The user says "sniff the memories and figure out the answers." They trust you to autonomously research and answer complex questions

**Never break trust by being sloppy.** If you're unsure about a tax classification, flag it rather than guessing. The user would rather see 20 flagged items than discover one wrong classification at audit time.

## The Meta-Lessons

1. **Start messy, clean up iteratively** — don't try to design the perfect system upfront. Build extraction scripts, discover edge cases, fix them
2. **Build tools early** — scripts are force multipliers. A 30-line Python script saves hours of manual work and can be re-run when data changes
3. **Research domain knowledge in parallel** — while extracting data, simultaneously research tax rules. The knowledge informs categorization decisions. Use a "research-by-erosion" approach: waves of subagents, each wave refining based on gaps in the previous one
4. **Single source of truth** — one CSV file, many derived outputs. When something changes, fix the source and regenerate everything. The user will often see the simpler architecture before you do
5. **Self-validating outputs** — double-entry accounting means debits = credits is a built-in integrity check
6. **Accumulate decisions in writing** — "that store is always personal," "err on inclusion," "that person is a shareholder not a contractor." Write these down so you don't re-litigate them
7. **Expect the unexpected** — format changes mid-year, missing data, surprise shareholders, closed bank accounts. The data will surprise you
8. **The back-and-forth is the work** — the categorization isn't done once. It's done 5-10 times with corrections each round. Each pass catches something the previous one missed
9. **Prefer honesty over comfort** — "I would rather see a reconciliation gap at the end of the CSV than some feel-good 'everything balances'." Real data has gaps. Show them clearly rather than papering over with estimates
10. **Name things for what they ARE, not what they COULD be** — `hst_charged` (was HST actually charged?) beats `hst_eligible` (could HST theoretically apply?). The latter invites wishful thinking
11. **Check subagent work** — subagents cut corners. Verify their assumptions and eliminate shortcuts before accepting their output
12. **Ask "are you sure?"** about zero-revenue years, missing accounts, and "complete" data. Revenue hiding in unexpected places is more common than you'd think
13. **The project will consume context** — a 9-day, 7,827-line session with 25 context compactions is normal for this kind of work. Plan for long-running, iterative engagement. Write things down (CLAUDE.md, TAX_GUIDELINES.md, memory files) so context resets don't lose knowledge

## Project Scale Reference

The real project that distilled this skill:
- **9 days** of active work across 15 sessions
- **6,050 lines of Python** across 13 scripts
- **2,514 transactions** in the master file
- **4 tax years** (2022 short year through 2025)
- **5+ financial institutions** (corporate credit cards, personal cards, payment platforms, personal bank accounts)
- **68 subagents** spawned in the main session alone
- **108 web searches** for tax law research
- **37 context window overflows** requiring compaction
- **Final output**: Complete GIFI schedules, HST ITC calculations, shareholder loan reconciliation, and T2 form answers ready for accountant review
