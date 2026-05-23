# Master Transactions CSV — Column Schema

The single source of truth file. All GIFI schedules, HST returns, and balance sheets derive from this one file.

---

## Required Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `date` | YYYY-MM-DD | Transaction date | `2024-03-15` |
| `source` | string | Which institution/file this came from | `TD Visa`, `Amex`, `Costco MC`, `Wise` |
| `description` | string | Merchant/payee description as it appears on statement | `CURSOR AI IDE 415-935-5` |
| `amount` | float | Transaction amount in original currency (positive = debit/expense) | `28.80` |
| `category` | string | Spend category from statement (if available) or assigned | `Software` |
| `gifi` | string | GIFI code or special account code | `9180`, `PERSONAL`, `SHAREHOLDER` |
| `category_name` | string | Human-readable name matching the GIFI code | `Computer software and supplies` |
| `deductible_pct` | int | Percentage deductible (100 or 50) | `100` |
| `deductible_amount` | float | amount × deductible_pct / 100 | `28.80` |
| `notes` | string | Additional context or flags | `50% deductible — business meal` |
| `rationale` | string | Why this categorization was chosen | `AI IDE subscription — dev tool` |
| `hst_charged` | yes/no | Was Canadian HST/GST actually charged on this transaction? | `yes` |
| `debit` | string | Account debited in double-entry | `9180` (or `SKIP` for non-GIFI) |
| `credit` | string | Account credited in double-entry | `DUE_TO_SH` (or `SKIP` for non-GIFI) |

## Special Values

- `gifi = PERSONAL` → Non-deductible personal expense. Excluded from GIFI totals.
- `gifi = SHAREHOLDER` → Share purchase/loan transaction. Not deductible.
- `debit = SKIP` / `credit = SKIP` → Transaction does not participate in double-entry (personal, payments, transfers).
- `hst_charged = no` → No ITC claimable on this transaction.

## Double-Entry Patterns

Every business transaction follows one of these patterns:

| Transaction Type | Debit | Credit |
|-----------------|-------|--------|
| Business expense | GIFI code (e.g., 9180) | DUE_TO_SH |
| Revenue | CASH or receivable | 8000 (revenue) |
| Shareholder contribution | CASH | DUE_TO_SH |
| Shareholder drawdown | DUE_TO_SH | CASH |
| Personal expense (on mixed card) | SKIP | SKIP |

## Validation Rules

1. **Trial balance must balance**: Sum of all debits (non-SKIP) = Sum of all credits (non-SKIP)
2. **No orphan entries**: Every transaction must have both a debit and credit, or both SKIP
3. **Revenue is positive, expenses are positive**: The sign convention is that all amounts are positive. Revenue and expenses are distinguished by the GIFI code and debit/credit columns, not by sign.
4. **Date within fiscal year**: Every transaction's date must fall within the fiscal year being processed
5. **hst_charged is explicit**: Never infer HST from the description. The column must be set explicitly.
