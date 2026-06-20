# Retail Sales Performance Analysis

A data analysis project investigating profitability drivers in a 4-year retail
sales dataset — built to identify *why* a profitable-looking business was
losing money in specific segments, and what to do about it.

**[View the interactive dashboard](./dashboard.html)** ·
**[Read the insights summary](./INSIGHTS.md)**

---

## Project Overview

| | |
|---|---|
| **Dataset** | Sample Superstore — 9,994 orders, 2014–2017 |
| **Question** | Where is the business profitable vs. losing money, and why? |
| **Headline finding** | Discounts above ~20% turn profitable orders into losses |
| **Tools** | SQL (SQLite), Python (pandas, matplotlib, seaborn), HTML/Chart.js |

## What's in this repo

```
├── superstore_clean.csv     # Cleaned dataset (source for all analysis)
├── analysis.sql             # 10 business-question SQL queries
├── eda.py                   # Python EDA script (run to regenerate charts)
├── charts/                  # Output charts from eda.py
├── dashboard.html           # Interactive dashboard (open in any browser)
├── INSIGHTS.md               # Findings + recommendations write-up
└── README.md                 # This file
```

## How to explore this project

- **Just want the findings?** → Read [`INSIGHTS.md`](./INSIGHTS.md)
- **Want the visual dashboard?** → Open [`dashboard.html`](./dashboard.html) in a browser
- **Want to see the SQL?** → Open [`analysis.sql`](./analysis.sql)
- **Want to run the Python analysis yourself?**
  ```bash
  pip install pandas matplotlib seaborn
  python eda.py
  ```

## Process

1. **Data cleaning** — Source dates were inconsistently formatted (mixed text/datetime).
   After standardizing, 1,708 rows (17%) showed a Ship Date before the Order Date — a
   logical impossibility traced to the source data. These rows were transparently
   flagged and excluded only from shipping-time analysis, preserving all other metrics.
2. **SQL analysis** — Loaded the cleaned data into SQLite and wrote 10 queries covering
   regional profitability, discount impact, product performance, and customer segments.
3. **Python EDA** — Used pandas for aggregation and matplotlib/seaborn for visualization,
   including a correlation check confirming discount's negative relationship with profit.
4. **Dashboard** — Built an interactive HTML dashboard (Chart.js) to communicate findings
   visually for a non-technical audience.
5. **Insights & recommendations** — Synthesized findings into actionable business
   recommendations (see [`INSIGHTS.md`](./INSIGHTS.md)).

## Key Finding

Orders with **no discount run a 29.5% profit margin**. Orders discounted **31% or more
lose 48 cents per dollar of sales**. This pattern — not weak sales — is the primary
driver of the company's unprofitable segments, most visibly in the Furniture category
and in 10 specific states.

See [`INSIGHTS.md`](./INSIGHTS.md) for the full breakdown and recommendations.

---

*Dataset: Sample Superstore (publicly available sample retail dataset).*
