Overview
This repository contains a complete SQL + Python + GenAI pipeline for auditing Mamaearth’s 2026 order data, generating verified metrics, producing visualizations, and creating a Situation–Complication–Resolution (SCR) business narrative using Gemini — with a fully offline fallback path so the project is gradable without network access or API spend.

The project is divided into three parts:

SQL Reports

Python Cleaning + EDA + Visualizations

GenAI‑Powered Insight Narrator (SCR)

Everything is reproducible end‑to‑end.

🧱 Directory Structure
Code
.
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
│
├── analysis/
│   ├── clean_and_eda.py
│   ├── visualize.py
│   └── artifacts/
│       └── merged_clean.csv
│
├── narrator/
│   ├── findings.json
│   ├── generate_narrative.py
│   ├── check_accuracy.py
│   └── sample_output.txt
│
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
│
├── customers.csv
├── orders.csv
├── products.csv
└── README.md
🧩 Part 1 — SQL Pipeline
1. Load schema
bash
psql -f sql/schema.sql
2. Load seed data
bash
psql -f sql/seed_data.sql
3. Run analytical SQL reports
bash
psql -f sql/reports.sql
This produces the raw totals used later for reconciliation.

🧪 Part 2 — Python Cleaning + EDA
1. Run the cleaning + EDA pipeline
bash
python analysis/clean_and_eda.py
This script:

Loads all three CSVs

Standardizes payment methods

Removes 5 duplicate orders

Imputes missing discount_pct and rating

Merges customers + orders + products

Detects outliers

Computes monthly revenue (with and without outliers)

Writes narrator/findings.json automatically

Saves analysis/artifacts/merged_clean.csv

🔐 findings.json contains exactly:
Cleaned revenue: ₹97,358.30

Raw revenue: ₹99,860.20

Duplicate delta: ₹2,501.90

COD return rate: 44.4%

Highest‑risk segment: COD + Tier‑2 at 54.5%

True peak month: March 2026 — ₹20,318.90

Outlier‑inflated month: January 2026 — ₹29,582.10 → corrected ₹11,637.10

These values are never hand‑typed — they are computed directly from the raw CSVs.

2. Generate visualizations
bash
python analysis/visualize.py
This produces two PNGs in visualizations/:

return_rate_by_payment.png

monthly_revenue_trend.png (outlier‑corrected)

🤖 Part 3 — GenAI‑Powered Insight Narrator
This part converts verified metrics into a business narrative using Gemini, with a fully offline fallback path.

🔑 Free‑path statement (required)
Google AI Studio provides a free Gemini API key with a free usage tier.
Use that — never a paid‑only key.

The narrator also includes a fully offline fallback path, so the pipeline is gradable with zero API spend and zero network access.

1. Set Gemini API key (optional)
If you want to use the online path:

bash
export GOOGLE_API_KEY="your_free_key_here"
If you do not set a key, the narrator automatically switches to the offline deterministic path.

2. Generate the SCR narrative
bash
python narrator/generate_narrative.py
This:

Loads narrator/findings.json

Calls Gemini with:

temperature=0.0 (deterministic factual reporting)

max_output_tokens=300

timeout=15

Wraps the call in full try/except

Falls back to offline deterministic narrative if:

No API key is set

API call fails

Returns a dict:

status

narrative

tokens

The offline path produces the same three SCR sections using an f‑string template.

3. Accuracy checker (required)
The narrative must contain these five numbers:

97,358.30 (cleaned revenue)

44.4 (COD return rate)

54.5 (Tier‑2 COD return rate)

2,501.90 (duplicate delta)

March + 20,318.90 (true peak month)

Run the checker:

bash
python narrator/check_accuracy.py narrator/sample_output.txt
For the online path:

Run the narrator once

Paste the output into narrator/sample_output.txt

Run the checker

Grader verifies the saved sample, not a live API call
