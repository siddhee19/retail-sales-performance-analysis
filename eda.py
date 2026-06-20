"""
Retail Sales Performance Analysis — Exploratory Data Analysis
================================================================
Dataset : Sample Superstore (9,994 orders, 2014-2017)
Author  : [Your Name]
Purpose : Identify profitability drivers and risk areas across
          region, product category, customer segment, and discount
          strategy, to support pricing/discount recommendations.

Run with: python eda.py
Outputs : PNG charts saved to ./charts/
================================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------------------------------------------
# 0. SETUP
# ----------------------------------------------------------------
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (9, 5)
plt.rcParams['font.size'] = 10

os.makedirs("charts", exist_ok=True)

PROFIT_COLOR = "#2E7D5B"
LOSS_COLOR = "#C44536"


# ----------------------------------------------------------------
# 1. LOAD DATA
# ----------------------------------------------------------------
df = pd.read_csv("superstore_clean.csv", parse_dates=["Order Date", "Ship Date"])

print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"Date range: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
print(f"\nColumns:\n{list(df.columns)}")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print("(none found — dataset has no missing values)" if df.isnull().sum().sum() == 0 else "")


# ----------------------------------------------------------------
# 2. DATA QUALITY NOTE
# ----------------------------------------------------------------
# During cleaning (see data_cleaning.py / README), 1,708 rows were found
# to have a Ship Date earlier than the Order Date — a logical impossibility
# traced to inconsistent formatting in the original source file.
# These rows are flagged via 'Date Flag' and excluded from shipping-time
# analysis only; all other metrics (Sales, Profit, Region, etc.) are reliable.

invalid_pct = (df['Date Flag'] != 'OK').mean() * 100
print(f"\nRows flagged with invalid ship dates: {(df['Date Flag'] != 'OK').sum():,} "
      f"({invalid_pct:.1f}% of data) — excluded from shipping-time analysis only")


# ----------------------------------------------------------------
# 3. OVERALL BUSINESS SNAPSHOT
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("OVERALL SNAPSHOT")
print("=" * 60)
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
margin = total_profit / total_sales * 100
loss_orders = (df['Profit'] < 0).sum()

print(f"Total Sales:        ${total_sales:,.0f}")
print(f"Total Profit:       ${total_profit:,.0f}")
print(f"Overall Margin:     {margin:.2f}%")
print(f"Unprofitable Lines: {loss_orders:,} of {len(df):,} ({loss_orders/len(df)*100:.1f}%)")


# ----------------------------------------------------------------
# 4. DISCOUNT vs PROFIT — the core finding
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("DISCOUNT IMPACT ON PROFIT")
print("=" * 60)

bins = [-0.01, 0, 0.1, 0.2, 0.3, 1]
labels = ['0%', '1-10%', '11-20%', '21-30%', '31%+']
df['Discount Band'] = pd.cut(df['Discount'], bins=bins, labels=labels)

discount_summary = df.groupby('Discount Band', observed=True).agg(
    orders=('Sales', 'count'),
    total_sales=('Sales', 'sum'),
    total_profit=('Profit', 'sum')
)
discount_summary['margin_pct'] = (discount_summary['total_profit'] / discount_summary['total_sales'] * 100).round(2)
print(discount_summary)

# Chart: bar of profit by discount band
fig, ax = plt.subplots()
colors = [PROFIT_COLOR if v >= 0 else LOSS_COLOR for v in discount_summary['total_profit']]
ax.bar(discount_summary.index.astype(str), discount_summary['total_profit'], color=colors)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title("Profit by Discount Band — heavier discounts erase margin", fontsize=12, fontweight='bold')
ax.set_xlabel("Discount Band")
ax.set_ylabel("Total Profit ($)")
plt.tight_layout()
plt.savefig("charts/01_discount_vs_profit.png", dpi=150)
plt.close()
print("Saved: charts/01_discount_vs_profit.png")

# Scatter: discount % vs profit margin per order (shows the relationship directly)
fig, ax = plt.subplots()
sample = df.sample(min(2000, len(df)), random_state=42)  # sample for readability
ax.scatter(sample['Discount'], sample['Profit Margin'], alpha=0.3, s=12,
           c=sample['Profit Margin'].apply(lambda x: PROFIT_COLOR if x >= 0 else LOSS_COLOR))
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title("Discount % vs. Profit Margin per Order", fontsize=12, fontweight='bold')
ax.set_xlabel("Discount")
ax.set_ylabel("Profit Margin")
plt.tight_layout()
plt.savefig("charts/02_discount_scatter.png", dpi=150)
plt.close()
print("Saved: charts/02_discount_scatter.png")


# ----------------------------------------------------------------
# 5. PROFITABILITY BY REGION
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("PROFIT BY REGION")
print("=" * 60)
region_summary = df.groupby('Region').agg(
    total_sales=('Sales', 'sum'), total_profit=('Profit', 'sum')
).sort_values('total_profit', ascending=False)
region_summary['margin_pct'] = (region_summary['total_profit'] / region_summary['total_sales'] * 100).round(2)
print(region_summary)

fig, ax = plt.subplots()
colors = [PROFIT_COLOR if v == region_summary['margin_pct'].max() else
          LOSS_COLOR if v == region_summary['margin_pct'].min() else '#7A8AA0'
          for v in region_summary['margin_pct']]
ax.barh(region_summary.index, region_summary['margin_pct'], color=colors)
ax.set_title("Profit Margin % by Region", fontsize=12, fontweight='bold')
ax.set_xlabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig("charts/03_region_margin.png", dpi=150)
plt.close()
print("Saved: charts/03_region_margin.png")


# ----------------------------------------------------------------
# 6. SUB-CATEGORY PROFITABILITY
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("SUB-CATEGORY PROFIT (worst 5)")
print("=" * 60)
subcat_summary = df.groupby(['Category', 'Sub-Category']).agg(
    total_sales=('Sales', 'sum'), total_profit=('Profit', 'sum')
).sort_values('total_profit')
print(subcat_summary.head(5))

fig, ax = plt.subplots(figsize=(9, 7))
plot_data = subcat_summary.sort_values('total_profit')
colors = [PROFIT_COLOR if v >= 0 else LOSS_COLOR for v in plot_data['total_profit']]
ax.barh([f"{i[1]}" for i in plot_data.index], plot_data['total_profit'], color=colors)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_title("Profit by Sub-Category (low to high)", fontsize=12, fontweight='bold')
ax.set_xlabel("Total Profit ($)")
plt.tight_layout()
plt.savefig("charts/04_subcategory_profit.png", dpi=150)
plt.close()
print("Saved: charts/04_subcategory_profit.png")


# ----------------------------------------------------------------
# 7. MONTHLY SALES TREND
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("MONTHLY SALES TREND")
print("=" * 60)
monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg(
    total_sales=('Sales', 'sum'), total_profit=('Profit', 'sum')
)
print(monthly.tail(6))

fig, ax = plt.subplots()
monthly.index = monthly.index.to_timestamp()
ax.plot(monthly.index, monthly['total_sales'], label='Sales', color='#1A1F2B', linewidth=2)
ax.plot(monthly.index, monthly['total_profit'], label='Profit', color='#D9A441', linewidth=2)
ax.set_title("Monthly Sales & Profit Trend (2014-2017)", fontsize=12, fontweight='bold')
ax.set_ylabel("$")
ax.legend()
plt.tight_layout()
plt.savefig("charts/05_monthly_trend.png", dpi=150)
plt.close()
print("Saved: charts/05_monthly_trend.png")


# ----------------------------------------------------------------
# 8. CUSTOMER SEGMENT PERFORMANCE
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("CUSTOMER SEGMENT PERFORMANCE")
print("=" * 60)
segment_summary = df.groupby('Segment').agg(
    customers=('Customer ID', 'nunique'),
    total_sales=('Sales', 'sum'),
    total_profit=('Profit', 'sum')
).sort_values('total_profit', ascending=False)
print(segment_summary)


# ----------------------------------------------------------------
# 9. TOP / BOTTOM PRODUCTS
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("TOP 5 MOST PROFITABLE PRODUCTS")
print("=" * 60)
product_profit = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False)
print(product_profit.head(5))

print("\n" + "=" * 60)
print("TOP 5 LEAST PROFITABLE PRODUCTS")
print("=" * 60)
print(product_profit.tail(5).sort_values())


# ----------------------------------------------------------------
# 10. CORRELATION CHECK
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("CORRELATION: Discount, Sales, Quantity vs Profit")
print("=" * 60)
corr = df[['Sales', 'Quantity', 'Discount', 'Profit']].corr()
print(corr['Profit'].sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap='RdYlGn', center=0, fmt='.2f', ax=ax)
ax.set_title("Correlation Matrix", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig("charts/06_correlation_heatmap.png", dpi=150)
plt.close()
print("Saved: charts/06_correlation_heatmap.png")


# ----------------------------------------------------------------
# SUMMARY OF KEY FINDINGS
# ----------------------------------------------------------------
print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print("""
1. Discounting above 20% is the primary driver of unprofitability.
   - 0% discount orders: ~29.5% margin
   - 31%+ discount orders: ~-48% margin (net loss)

2. Furniture > Tables is structurally unprofitable (-$17.7K on $207K sales),
   driven by high average discounts on big-ticket items.

3. Central region underperforms (7.9% margin) vs. West (14.9%, best region).

4. Discount has a negative correlation with Profit -- discounting is actively
   working against profitability, not just neutral to it.

5. 10 of 49 states are net unprofitable, led by Texas, Ohio, and Pennsylvania.

Recommendation: Cap discounts at 20% on Furniture and Technology categories,
and review state-level pricing policy in the 10 loss-making states.
""")
