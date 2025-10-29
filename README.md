# eCommerce Price & Stock Monitor

A tiny Python tool to check a list of product pages for **price** and **stock** changes and produce a CSV report you can paste into Slack/Email/Sheets.

> Built to demonstrate practical automation skills for eCommerce/ops roles.

---

## What it does
- Fetches product pages (with a polite user‑agent and delay)
- Extracts **price** and **availability** via CSS selectors or regex
- Compares with your last known values (optional)
- Outputs a timestamped **CSV report** listing deltas

## Quick start
```bash
# 1) Create a virtual env (optional)
python -m venv .venv && .venv/Scripts/activate  # Windows
# . .venv/bin/activate  # macOS/Linux

# 2) Install deps
pip install -r requirements.txt

# 3) Configure targets
#   Edit sites.json with your product URLs and selectors

# 4) Run
python monitor.py

# 5) See report in ./reports/report_YYYYMMDD_HHMMSS.csv
```

## Configure targets (sites.json)
Each entry lets you choose **css** or **regex** parsing strategies.

```json
[
  {
    "name": "Sample Hoodie",
    "url": "https://example.com/product/hoodie",
    "price": {"css": ".price", "regex": null},
    "in_stock": {"css": ".availability", "regex": "In Stock|Available"},
    "currency": "€"
  }
]
```

> To avoid TOS issues, respect robots.txt, add delays, and only monitor products you are allowed to check.

## Notes
- This project is intentionally **minimal and readable**
- Extend `parsers.py` to support JSON APIs or specific CMS patterns
- Hook `emit_row()` to send to Slack/Email instead of CSV
