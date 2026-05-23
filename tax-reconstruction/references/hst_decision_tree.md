# HST/GST Decision Tree: Was Tax Actually Charged?

For each transaction where you need to determine if HST/GST was charged and ITC is claimable.

---

## The Core Question

**"Was Canadian HST/GST actually included in this charge?"**

Not "could it have been" or "is it eligible in theory" — was it *actually* charged. When in doubt, mark `hst_charged: no`.

---

## Decision Tree

```
Was the purchase from a Canadian merchant?
├── YES (merchant is in Canada, charges in CAD)
│   ├── Is it a financial service? (bank fees, insurance, interest)
│   │   └── YES → hst_charged: no (financial services are exempt)
│   │
│   ├── Is it a charitable donation?
│   │   └── YES → hst_charged: no (not a business expense)
│   │
│   ├── Is it a meal/restaurant?
│   │   └── YES → hst_charged: yes, but ITC at 50%
│   │     (matches the 50% meal deductibility limit)
│   │
│   ├── Is it a Canadian airline?
│   │   ├── Airline HQ in HST province (ON, NS, NB, NL, PE)?
│   │   │   └── YES → hst_charged: yes (13% HST)
│   │   └── Airline HQ in GST-only province (AB, BC, SK, MB, territories)?
│   │       └── YES → hst_charged: yes (5% GST only)
│   │         Extraction rate: 5/105 instead of 13/113
│   │
│   └── Everything else (SaaS, rent, supplies, phone, etc.)
│       └── hst_charged: yes (13% HST)
│
├── NO (merchant is foreign)
│   ├── Is it a foreign SaaS with Canadian GST registration?
│   │   (Netflix, Spotify, Google, Apple, Microsoft often are)
│   │   └── Check the receipt: does it show "HST" or "GST" on the line item?
│   │       ├── YES → hst_charged: yes
│   │       └── NO / can't tell → hst_charged: no
│   │
│   ├── Is it a freelancer platform (Upwork, Fiverr, etc.)?
│   │   ├── Is the contractor account registered in Canada?
│   │   │   ├── YES → hst_charged: yes (platform charges HST)
│   │   │   └── NO → hst_charged: no (no HST on non-Canadian accounts)
│   │   └── ASK THE USER: "Were your contractors on Canadian or non-Canadian accounts?"
│   │
│   ├── Is it a foreign hotel/rental in Canada?
│   │   └── hst_charged: yes (Airbnb, Booking.com charge HST for Canadian properties)
│   │
│   ├── Is it a foreign purchase for use abroad?
│   │   └── hst_charged: no (no Canadian tax on foreign consumption)
│   │
│   └── Everything else foreign
│       └── hst_charged: no
│
└── UNCLEAR
    └── hst_charged: no (default to no when uncertain)
      Flag for user: "I couldn't determine if HST was charged on [description]. Can you check the receipt?"
```

---

## Extraction Rates

| Tax Type | Rate | Extraction Formula |
|----------|------|--------------------|
| HST (Ontario) | 13% | `amount × 13/113` |
| GST (non-HST provinces) | 5% | `amount × 5/105` |
| No tax | 0% | Skip |

---

## Meals ITC Calculation

Meals are 50% deductible, so only 50% of the HST is recoverable:

```
meal_amount = $100 (tax-inclusive)
hst_portion = 100 × 13/113 = $11.50
recoverable_itc = 11.50 × 50% = $5.75
```

---

## Common Edge Cases

| Situation | HST Charged? | Why |
|-----------|-------------|-----|
| Canadian SaaS subscription (e.g., Shopify) | Yes | Canadian merchant |
| US SaaS with Canadian GST registration (e.g., Netflix) | Yes (5% GST) | Registered for Canadian digital services tax |
| US SaaS without Canadian registration | No | Not registered |
| Upwork with Canadian freelancer | Yes | Platform charges HST |
| Upwork with overseas freelancer | No | No HST on non-Canadian accounts |
| Airbnb for Canadian property | Yes | Airbnb collects HST for Canadian listings |
| Airbnb for foreign property | No | No Canadian tax |
| Hotel in Canada | Yes | Canadian merchant |
| Hotel abroad | No | Foreign consumption |
| Uber in Canada | Yes | Canadian merchant |
| Uber abroad | No | Foreign consumption |
| Bank fees, interest | No | Financial services are exempt |
| Car insurance | No | Insurance is exempt |
| Gas at Canadian station | Yes | HST embedded in price |
| Wire transfer fee | No | Financial service |
| Wise transfer fee | No | Financial service |
