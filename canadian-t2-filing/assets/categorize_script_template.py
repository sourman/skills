#!/usr/bin/env python3
"""Categorize [YEAR] transactions for [CORPORATION_NAME] T2 filing.

Produces:
  - output/[YEAR]/transactions_categorized.csv
"""
import csv
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ── Tax year boundaries ────────────────────────────────────────────────────
YEAR_START = datetime(YEAR, 1, 1)  # Replace YEAR with actual year
YEAR_END = datetime(YEAR, 12, 31)
# For short years (first year of incorporation):
# YEAR_START = datetime(2022, 4, 7)  # Incorporation date
# YEAR_END = datetime(2022, 12, 31)

# ── GIFI Codes ─────────────────────────────────────────────────────────────
# Load full reference from references/gifi_code_reference.md
GIFI_REVENUE = "8000"
GIFI_ADVERTISING = "8800"
GIFI_PROFESSIONAL = "8840"
GIFI_INTEREST = "8890"
GIFI_MEALS = "8910"
GIFI_OFFICE = "8920"
GIFI_RENT = "8940"
GIFI_SALARIES = "8960"
GIFI_SUBCONTRACT = "8970"
GIFI_TRAVEL = "8980"
GIFI_PHONE = "9110"
GIFI_SOFTWARE = "9180"
GIFI_FX_LOSS = "9220"
GIFI_OTHER = "9270"

# ── Monthly exchange rates ─────────────────────────────────────────────────
# Use Bank of Canada monthly average rates: https://www.bankofcanada.ca/valet/observations/
# Replace with actual rates for the tax year
USD_CAD_RATES = {
    1: 1.35, 2: 1.35, 3: 1.35, 4: 1.36, 5: 1.37, 6: 1.37,
    7: 1.37, 8: 1.37, 9: 1.36, 10: 1.37, 11: 1.39, 12: 1.42,
}


def to_cad(amount: float, currency: str, date_str: str) -> float:
    if currency == "CAD":
        return amount
    month = int(date_str[5:7]) if len(date_str) >= 7 else 1
    if currency == "USD":
        return amount * USD_CAD_RATES.get(month, 1.37)
    return amount


# ── Personal keywords (definitely NOT business) ────────────────────────────
# Add to this list as you discover edge cases. Each year should have more
# keywords than the last.
PERSONAL_KEYWORDS = [
    # Donations/charity
    "launchgood", "islamic relief", "canadahelps", "isna canada",
    # Personal expenses
    "insurance company", "freedom mobile",
    # Grocery/retail — depends on card type
    # (on corporate cards these might be business; on personal cards, personal)
]

# ── Business keywords (rescue from personal categories) ────────────────────
BUSINESS_IN_PERSONAL = [
    "staples", "google", "openphone", "namecheap", "canva",
    "paddle.net", "gsuite", "microsoft", "aws",
]

# ── Card classification ────────────────────────────────────────────────────
# Corporate cards: 100% business, include everything
CORPORATE_CARDS = ["TD Visa"]  # Replace with actual card sources
# Personal cards: mixed, needs filtering
PERSONAL_CARDS = ["Amex", "Costco MC"]  # Replace with actual card sources


def categorize(row: dict) -> dict:
    """Categorize a single transaction. Returns row with gifi, deductible_pct, etc."""
    description = row.get("description", "").lower()
    source = row.get("source", "")
    amount = abs(float(row.get("amount", 0)))
    category = row.get("category", "")

    # ── Skip payments/refunds ───────────────────────────────────────────
    for kw in ["payment received", "payment thank you", "cash back"]:
        if kw in description:
            return {**row, "gifi": "SKIP", "deductible_pct": 0, "deductible_amount": 0}

    # ── Personal card filtering ─────────────────────────────────────────
    if source in PERSONAL_CARDS:
        # Check personal keywords
        for kw in PERSONAL_KEYWORDS:
            if kw in description:
                return {**row, "gifi": "PERSONAL", "deductible_pct": 0, "deductible_amount": 0}

        # Check if business keywords rescue it
        business_match = any(kw in description for kw in BUSINESS_IN_PERSONAL)
        if not business_match and category in ["Personal and Household Expenses", "Retail and Grocery"]:
            return {**row, "gifi": "PERSONAL", "deductible_pct": 0, "deductible_amount": 0}

    # ── Business categorization ─────────────────────────────────────────
    # Follow the categorization decision tree from references/categorization_decision_tree.md
    gifi = GIFI_OTHER  # Default
    deductible_pct = 100

    # Software
    if any(kw in description for kw in ["cursor", "claude", "openphone", "google", "microsoft", "perplexity", "github", "aws", "domain"]):
        gifi = GIFI_SOFTWARE
    # Travel
    elif any(kw in description for kw in ["airbnb", "uber", "hotel", "airlines", "avis", "hertz", "booking.com"]):
        gifi = GIFI_TRAVEL
    # Meals
    elif any(kw in description for kw in ["tim hortons", "starbucks", "restaurant", "cafe"]):
        gifi = GIFI_MEALS
        deductible_pct = 50
    # Professional
    elif any(kw in description for kw in ["legal", "accounting", "consulting", "professional"]):
        gifi = GIFI_PROFESSIONAL
    # Subcontract
    elif any(kw in description for kw in ["upwork", "freelancer"]):
        gifi = GIFI_SUBCONTRACT
    # ... add more patterns as needed

    return {
        **row,
        "gifi": gifi,
        "deductible_pct": deductible_pct,
        "deductible_amount": round(amount * deductible_pct / 100, 2),
    }


def main():
    # Load transactions from all source CSVs
    # TODO: Implement loading from extract outputs
    # Filter to YEAR_START..YEAR_END
    # Run categorize() on each row
    # Write to output/YEAR/transactions_categorized.csv
    pass


if __name__ == "__main__":
    main()
