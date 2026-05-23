# GIFI Code Reference — Canadian T2 Filing

The General Index of Financial Information (GIFI) is the standardized account code system the CRA requires on corporate tax returns. Every transaction must be assigned a GIFI code.

---

## Revenue Codes

| Code | Name | When to Use |
|------|------|-------------|
| 8000 | Revenue from sales of goods and services | All business revenue |
| 8299 | Other revenue | Investment income, foreign exchange gains |

## Expense Codes (most common for software/services CCPC)

| Code | Name | Deductibility | What Goes Here |
|------|------|---------------|----------------|
| 8800 | Advertising and promotion | 100% | Marketing, ads, promotional expenses |
| 8840 | Consulting and professional fees | 100% | Legal, accounting, consulting |
| 8871 | Management and administration fees | 100% | Management company fees |
| 8880 | Insurance | 100% | Business insurance premiums |
| 8890 | Interest and bank charges | 100% | Loan interest, bank fees, transfer fees |
| 8910 | Meals and entertainment | **50%** | Business meals, coffee, client dinners |
| 8920 | Office supplies and expenses | 100% | Stationery, small equipment, office items |
| 8940 | Rent | 100% | Office rent, cowork space |
| 8960 | Salaries, wages, and benefits | 100% | Employee compensation (T4) |
| 8970 | Subcontracting costs | 100% | Contractor payments for services |
| 8980 | Travel | 100% | Flights, hotels, taxis, rental cars |
| 9060 | Business taxes, licences, memberships | 100% | Incorporation fees, business licences |
| 9110 | Telephone and communication | 100% | Phone, internet, VoIP |
| 9180 | Computer software and supplies | 100% | SaaS subscriptions, dev tools, hosting |
| 9220 | Foreign exchange loss | 100% | Realized FX losses |
| 9270 | Other operating expenses | 100% | Catch-all for expenses that don't fit elsewhere |

## Non-GIFI Accounts (used in double-entry, not reported on Schedule 125)

| Account | Purpose | Direction |
|---------|---------|-----------|
| DUE_TO_SH | Due to Shareholder (liability) | Credit when owner contributes, debit when repaid |
| PERSONAL | Non-deductible personal expenses | Skip in GIFI totals entirely |
| SHAREHOLDER | Share purchase transactions | Not deductible, not GIFI-reportable |
| CASH | Cash/bank balances | Asset on balance sheet |
| RETAINED_EARNINGS | Accumulated profits/losses | Equity on balance sheet |

## CCA Classes (Schedule 8)

| Class | Rate | What Goes Here |
|-------|------|----------------|
| 50 | 55% | Computers, laptops, servers, monitors |
| 12 | 100% | One-time software purchases (not subscriptions) |
| 8 | 20% | Office furniture, smartphones |
| 14.1 | 5% | Incorporation costs over $3,000 threshold |

## Strategy: Claim $0 CCA in Loss Years

CCA is optional. In loss years, claiming CCA wastes the deduction — it increases the loss but generates no tax savings. Preserve full UCC balances and claim CCA only when the corporation becomes profitable.

---

## Canadian Tax Rules Quick Reference

| Rule | Detail |
|------|--------|
| Meals & entertainment | 50% deductible (100% for team events, max 6/year) |
| Travel | 100% deductible |
| Software subscriptions | 100% deductible |
| Pre-incorporation expenses | Claimable under s.69(1)(b) ITA |
| Incorporation costs | First $3,000 deductible under s.20(1)(b) ITA |
| Non-capital losses | Carry forward 20 years |
| Shareholder loans | Must repay within 1 year of year-end |
| Loss year CCA | Claim $0 — preserve UCC for profitable years |
| Small supplier threshold | Revenue < $30K = no mandatory HST registration |
| Zero-rated exports | 0% HST on revenue, but ITCs still recoverable |
