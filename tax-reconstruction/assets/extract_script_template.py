#!/usr/bin/env python3
"""Extract transactions from [INSTITUTION] PDF statements into CSVs.

Usage:
    python extract_<source>.py                     # all PDFs in source directory
    python extract_<source>.py statement1.pdf      # specific files only

Reads:  sources/<source>/pdf/*.pdf
Writes: sources/<source>/csv/*.csv (one per statement)
"""

import csv
import sys
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
PDF_DIR = Path("sources") / "<source>" / "pdf"
CSV_DIR = Path("sources") / "<source>" / "csv"

# CSV columns for output
CSV_COLUMNS = ["transaction_date", "posting_date", "description", "amount"]


def extract_transactions(pdf_path: Path) -> list[dict]:
    """Extract transactions from a single PDF statement.

    Returns list of dicts with keys matching CSV_COLUMNS.
    """
    import fitz  # PyMuPDF — preserves spaces better than alternatives

    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    transactions = []

    # ── Parse the text into transactions ────────────────────────────────
    # TODO: Implement parsing logic for this institution's statement format.
    #
    # Common patterns:
    #   1. Read all text, split by regex matching date patterns
    #   2. Extract: date, posting_date, description, amount per match
    #   3. Handle cross-year dates (Jan statement contains Dec transactions)
    #
    # Pitfalls to watch for:
    #   - Dates with no spaces ("MAR5" not "MAR 5")
    #   - Negative balances with minus on a separate line
    #   - Foreign currency amounts on a line below the CAD amount
    #   - Multiple pages with continuation of transactions
    #   - Statement period dates vs transaction dates

    return transactions


def verify_balance(transactions: list[dict], pdf_path: Path) -> bool:
    """Verify extracted transactions match stated balance on the statement.

    Returns True if balance checks out, False otherwise.
    """
    # TODO: Implement balance verification
    # 1. Find the stated balance on the PDF
    # 2. Calculate running balance from extracted transactions
    # 3. Compare — they should match
    return True


def process_pdf(pdf_path: Path) -> bool:
    """Process a single PDF and write CSV. Returns True on success."""
    transactions = extract_transactions(pdf_path)
    if not transactions:
        print(f"  WARNING: No transactions extracted from {pdf_path.name}")
        return False

    balance_ok = verify_balance(transactions, pdf_path)

    # Derive output filename from statement date range or PDF name
    csv_path = CSV_DIR / pdf_path.with_suffix(".csv").name
    CSV_DIR.mkdir(parents=True, exist_ok=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(transactions)

    status = "✓" if balance_ok else "✗ BALANCE MISMATCH"
    print(f"  {status} {pdf_path.name}: {len(transactions)} transactions → {csv_path.name}")
    return True


def main():
    if len(sys.argv) > 1:
        pdfs = [Path(a) for a in sys.argv[1:]]
    else:
        pdfs = sorted(PDF_DIR.glob("*.pdf"))

    if not pdfs:
        print(f"No PDFs found in {PDF_DIR}")
        sys.exit(1)

    print(f"Processing {len(pdfs)} PDFs from {PDF_DIR}...")
    successes = sum(process_pdf(p) for p in pdfs)
    print(f"\nDone: {successes}/{len(pdfs)} extracted successfully")


if __name__ == "__main__":
    main()
