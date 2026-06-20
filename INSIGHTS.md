# Retail Sales Performance — Insights Summary

**Dataset:** Sample Superstore | 9,994 orders | 2014–2017
**Tools used:** SQL (SQLite), Python (pandas, matplotlib), HTML/Chart.js dashboard

---

## The Question

The business looks healthy on the surface — $2.3M in total sales. But is it actually
profitable everywhere it sells? This analysis digs into *where* profit is being made,
and more importantly, *where it's being lost.*

## Headline Finding

> **Discounting, not weak sales, is the company's core profitability problem.**

| Discount Level | Profit Margin |
|---|---|
| No discount | 29.5% |
| 1–20% discount | 11.6–16.6% |
| 21–30% discount | **-10.1%** |
| 31%+ discount | **-48.2%** |

Once discounts cross ~20%, orders stop being profitable. Past 30%, the company loses
nearly 50 cents for every dollar of sales. This single pattern explains a large share
of the company's lost profit.

## Supporting Findings

**1. Furniture — Tables is structurally unprofitable.**
$207K in sales, but a **-$17.7K loss** — driven by heavy average discounting on
big-ticket items. Bookcases shows the same pattern on a smaller scale (-$3.5K).

**2. Profitability varies sharply by region.**
West region leads at 14.9% margin; Central trails at just 7.9% — despite Central
having higher total sales than South.

**3. Ten states are net unprofitable**, led by Texas (-$25.7K), Ohio (-$17.0K), and
Pennsylvania (-$15.6K) — all worth a pricing/discount policy review.

**4. A small number of products account for outsized losses.**
The Cubify CubeX 3D Printer alone lost $8.9K, at a 53% average discount —
an example of a single product/discount combination doing real damage.

**5. Consumer segment is the most valuable**, contributing the most customers,
sales, and profit — though Corporate and Home Office are healthy contributors too.

**6. Sales grew steadily year over year**, with consistent seasonal peaks in
September and November (holiday season).

## Recommendations

1. **Cap discounts at 20%** on Furniture and Technology categories, where margins
   are thinnest and most discount-sensitive.
2. **Review pricing policy in the 10 loss-making states**, starting with Texas,
   Ohio, and Pennsylvania.
3. **Re-evaluate underperforming products** like the Cubify 3D Printer line —
   either reduce discount depth or reconsider whether to keep stocking them.
4. **Protect the West region's playbook** — its higher margin suggests a pricing
   or sales approach worth replicating elsewhere.

## Methodology Note

Order and ship dates in the source file were stored in inconsistent formats.
After cleaning, 1,708 rows (17%) showed a Ship Date earlier than the Order Date —
a data integrity issue traced to the source file rather than a parsing error.
These rows were flagged (not deleted or guessed) and excluded only from
shipping-time calculations; all profit/sales figures above are unaffected.
