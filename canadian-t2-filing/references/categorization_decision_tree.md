# Categorization Decision Tree

For each transaction, follow this tree from top to bottom. Stop at the first match.

---

## Level 1: Skip Entirely

```
Is it a payment/refund/credit card payment?
├── YES → SKIP (not an expense — it's a transfer between accounts)
│   Keywords: "payment received", "payment thank you", "cash back credit",
│             "welcome bonus", "paiement merci"
└── NO → continue to Level 2
```

## Level 2: Personal or Business?

```
Which card was it on?
├── CORPORATE CARD (100% business) → continue to Level 3
│   Trust it. All transactions are business expenses.
│
├── PERSONAL CARD (mixed) → apply keyword filters
│   ├── Match PERSONAL_KEYWORDS? → PERSONAL (skip)
│   │   (donations, charities, personal insurance, groceries, personal health,
│   │    personal entertainment, personal vehicle, personal subscriptions)
│   │
│   ├── Spend category is personal? → PERSONAL (skip)
│   │   ("Personal and Household Expenses", "Health and Education",
│   │    "Retail and Grocery")
│   │
│   ├── Match BUSINESS_RESCUE keywords in personal category? → continue to Level 3
│   │   (software tools, professional services, travel on personal card)
│   │
│   └── No match → FLAG for user review
│       Ask: "Is [description] ($amount) a business expense?"
│       Default to inclusion if user doesn't respond.
│
└── PAYMENT PLATFORM (Wise, PayPal, etc.) → check direction
    ├── MONEY IN → could be revenue → continue to Level 3 (revenue)
    └── MONEY OUT → check recipient
        ├── Known contractor → SUBCONTRACT (8970)
        ├── Known shareholder → SHAREHOLDER (not deductible)
        └── Unknown → FLAG for user review
```

## Level 3: Which GIFI Code?

```
What type of business expense?
│
├── Software subscriptions, SaaS, dev tools → SOFTWARE (9180)
│   Keywords: "google", "microsoft", "cursor", "claude", "openphone",
│             "perplexity", "github", "aws", "domain", "hosting"
│
├── Flights, hotels, taxis, rental cars, transit → TRAVEL (8980)
│   Keywords: "airbnb", "uber", "lyft", "hotel", "airlines", "avis",
│             "hertz", "expedia", "booking.com", "transit"
│
├── Restaurants, coffee, food during work → MEALS (8910)
│   ⚠️ 50% deductible only
│   Keywords: "tim hortons", "starbucks", "restaurant", "cafe", "grill"
│   Exception: Team events/parties → 100% deductible (max 6/year)
│
├── Office rent, cowork space → RENT (8940)
│   Keywords: "edge", "cowork", "office", "workspace", "rent"
│
├── Consulting, legal, accounting, professional → PROFESSIONAL (8840)
│   Keywords: "legal", "accounting", "consulting", "wonsulting",
│             "professional", "incorporation"
│
├── Contractor payments for services → SUBCONTRACT (8970)
│   Must have: known contractor name, service agreement
│   NOT: shareholder payments (→ SHAREHOLDER, not deductible)
│
├── Phone, internet, communication → PHONE (9110)
│   Keywords: "rogers", "bell", "telus", "openphone", "voip"
│
├── Bank charges, interest, transfer fees → INTEREST (8890)
│   Keywords: "interest", "fee", "charge", "transfer fee"
│
├── Advertising, marketing, promotions → ADVERTISING (8800)
│   Keywords: "adwords", "facebook ads", "google ads", "linkedin",
│             "upwork connects", "promotion"
│
├── Office supplies, equipment → OFFICE (8920)
│   Keywords: "staples", "amazon" (if office supplies), "best buy"
│
├── Memberships, licences, business taxes → TAXES_LICENCES (9060)
│   Keywords: "nuans", "corporation canada", "licence", "membership"
│
├── Foreign exchange losses → FX_LOSS (9220)
│   When exchange rate causes a realized loss on conversion
│
└── Everything else → OTHER (9270)
    ⚠️ Review this bucket regularly. If it grows large, create new categories.
```

## Level 4: Special Accounts

```
Is this NOT a normal expense/revenue?
│
├── Shareholder contribution (owner's personal money funding the business)
│   → DUE_TO_SH credit (the corp owes the owner)
│
├── Shareholder drawdown (owner taking money from the corp)
│   → DUE_TO_SH debit (reduces what the corp owes the owner)
│   ⚠️ Must be repaid within 1 year of year-end or taxable
│
├── Share purchase/buyout payment
│   → SHAREHOLDER (not deductible, not GIFI-reportable)
│
├── Pre-incorporation business expense
│   → Re-code to proper GIFI code (claimable under s.69(1)(b))
│   → Also create DUE_TO_SH credit for the owner's contribution
│
├── Personal expense on business card
│   → PERSONAL (skip in GIFI totals)
│
└── Refund/reversal of previous expense
    → Same GIFI code as original, negative amount
    ⚠️ Also reverse any ITC claimed on the original
```
