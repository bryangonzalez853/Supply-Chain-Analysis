"""
Supply Chain Analytics Project
Author: Portfolio Demonstration
Date: February 2026

This script performs comprehensive supply chain analysis including:
- Order fulfillment metrics
- Inventory optimization
- Supplier performance evaluation
- Cost analysis and optimization opportunities
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# 1. DATA LOADING AND PREPARATION
# ============================================================================

print("=" * 80)
print("SUPPLY CHAIN ANALYTICS - COMPREHENSIVE ANALYSIS")
print("=" * 80)

# Load datasets
orders_df = pd.read_csv('orders_data.csv', parse_dates=['Order_Date', 'Expected_Delivery', 'Actual_Delivery'])
inventory_df = pd.read_csv('inventory_data.csv')
supplier_df = pd.read_csv('supplier_performance.csv')
shipping_df = pd.read_csv('shipping_costs.csv')

print("\n1. DATA LOADED SUCCESSFULLY")
print(f"   - Orders: {len(orders_df):,} records")
print(f"   - Inventory Items: {len(inventory_df):,} SKUs")
print(f"   - Suppliers: {len(supplier_df):,} vendors")
print(f"   - Shipments: {len(shipping_df):,} deliveries")

# ============================================================================
# 2. ORDER FULFILLMENT ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("2. ORDER FULFILLMENT METRICS")
print("=" * 80)

# Calculate delivery performance
total_orders = len(orders_df)
on_time_orders = len(orders_df[orders_df['On_Time_Delivery'] == 'Yes'])
on_time_rate = (on_time_orders / total_orders) * 100

# Calculate average delivery time
orders_df['Delivery_Time_Days'] = (orders_df['Actual_Delivery'] - orders_df['Order_Date']).dt.days
avg_delivery_time = orders_df['Delivery_Time_Days'].mean()

# Calculate late deliveries
late_orders = orders_df[orders_df['On_Time_Delivery'] == 'No']
avg_delay = (late_orders['Actual_Delivery'] - late_orders['Expected_Delivery']).dt.days.mean()

print(f"\n   On-Time Delivery Rate: {on_time_rate:.1f}%")
print(f"   Average Delivery Time: {avg_delivery_time:.1f} days")
print(f"   Late Deliveries: {len(late_orders):,} ({(len(late_orders)/total_orders)*100:.1f}%)")
print(f"   Average Delay (when late): {avg_delay:.1f} days")

# Performance by warehouse
warehouse_performance = orders_df.groupby('Warehouse').agg({
    'Order_ID': 'count',
    'On_Time_Delivery': lambda x: (x == 'Yes').sum() / len(x) * 100,
    'Total_Value': 'sum',
    'Delivery_Time_Days': 'mean'
}).round(2)

warehouse_performance.columns = ['Total_Orders', 'On_Time_Rate_%', 'Total_Revenue', 'Avg_Delivery_Days']
warehouse_performance = warehouse_performance.sort_values('On_Time_Rate_%', ascending=False)

print("\n   Performance by Warehouse:")
print(warehouse_performance.to_string())

# ============================================================================
# 3. INVENTORY ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("3. INVENTORY OPTIMIZATION ANALYSIS")
print("=" * 80)

# Inventory status summary
stock_status_summary = inventory_df['Stock_Status'].value_counts()
print("\n   Inventory Status Distribution:")
for status, count in stock_status_summary.items():
    print(f"   - {status}: {count} items ({count/len(inventory_df)*100:.1f}%)")

# Items requiring attention
low_stock_items = inventory_df[inventory_df['Stock_Status'] == 'Low Stock'].sort_values('Days_of_Inventory')
overstock_items = inventory_df[inventory_df['Stock_Status'] == 'Overstock'].sort_values('Current_Stock', ascending=False)

print(f"\n   Low Stock Alerts: {len(low_stock_items)} items need reordering")
print(f"   Overstock Alerts: {len(overstock_items)} items have excess inventory")

# Top 10 low stock items
if len(low_stock_items) > 0:
    print("\n   Top 10 Critical Low Stock Items:")
    print(low_stock_items[['Product', 'Warehouse', 'Current_Stock', 'Reorder_Point', 'Days_of_Inventory']].head(10).to_string(index=False))

# Inventory turnover by category
inventory_summary = inventory_df.groupby('Category').agg({
    'Current_Stock': 'sum',
    'Avg_Monthly_Demand': 'sum',
    'Days_of_Inventory': 'mean'
}).round(2)

inventory_summary['Turnover_Ratio'] = (inventory_summary['Avg_Monthly_Demand'] * 12 / inventory_summary['Current_Stock']).round(2)
print("\n   Inventory Metrics by Category:")
print(inventory_summary.to_string())

# ============================================================================
# 4. SUPPLIER PERFORMANCE ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("4. SUPPLIER PERFORMANCE EVALUATION")
print("=" * 80)

# Overall supplier metrics
avg_on_time = supplier_df['On_Time_Delivery_Rate'].mean()
avg_quality = supplier_df['Quality_Score'].mean()
avg_defect = supplier_df['Defect_Rate_Percent'].mean()

print(f"\n   Average On-Time Delivery: {avg_on_time:.1f}%")
print(f"   Average Quality Score: {avg_quality:.1f}/100")
print(f"   Average Defect Rate: {avg_defect:.2f}%")

# Top performers
supplier_df['Performance_Score'] = (
    supplier_df['On_Time_Delivery_Rate'] * 0.4 +
    supplier_df['Quality_Score'] * 0.4 -
    supplier_df['Defect_Rate_Percent'] * 2
).round(2)

top_suppliers = supplier_df.nlargest(5, 'Performance_Score')[['Supplier', 'Category', 'On_Time_Delivery_Rate', 'Quality_Score', 'Performance_Score']]
print("\n   Top 5 Performing Suppliers:")
print(top_suppliers.to_string(index=False))

# Underperforming suppliers
bottom_suppliers = supplier_df.nsmallest(3, 'Performance_Score')[['Supplier', 'Category', 'On_Time_Delivery_Rate', 'Quality_Score', 'Performance_Score']]
print("\n   Suppliers Requiring Improvement:")
print(bottom_suppliers.to_string(index=False))

# ============================================================================
# 5. COST ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("5. COST ANALYSIS & OPTIMIZATION OPPORTUNITIES")
print("=" * 80)

# Merge orders with shipping costs
orders_with_shipping = orders_df.merge(shipping_df, on='Order_ID')

# Total costs
total_order_value = orders_df['Total_Value'].sum()
total_shipping_cost = shipping_df['Shipping_Cost'].sum()
total_cost = total_order_value + total_shipping_cost

print(f"\n   Total Order Value: ${total_order_value:,.2f}")
print(f"   Total Shipping Cost: ${total_shipping_cost:,.2f}")
print(f"   Shipping as % of Order Value: {(total_shipping_cost/total_order_value)*100:.2f}%")

# Shipping cost by carrier
carrier_analysis = shipping_df.groupby('Carrier').agg({
    'Shipping_ID': 'count',
    'Shipping_Cost': ['sum', 'mean'],
    'Distance_KM': 'mean'
}).round(2)

carrier_analysis.columns = ['Shipments', 'Total_Cost', 'Avg_Cost', 'Avg_Distance']
carrier_analysis['Cost_per_KM'] = (carrier_analysis['Total_Cost'] / (carrier_analysis['Shipments'] * carrier_analysis['Avg_Distance'])).round(2)
carrier_analysis = carrier_analysis.sort_values('Total_Cost', ascending=False)

print("\n   Shipping Cost Analysis by Carrier:")
print(carrier_analysis.to_string())

# Cost optimization opportunities
# 1. Identify high-cost routes
high_cost_threshold = shipping_df['Shipping_Cost'].quantile(0.90)
high_cost_shipments = orders_with_shipping[orders_with_shipping['Shipping_Cost'] > high_cost_threshold]

print(f"\n   High-Cost Shipments (>90th percentile): {len(high_cost_shipments)}")
print(f"   Potential savings from route optimization: ${high_cost_shipments['Shipping_Cost'].sum() * 0.15:,.2f} (15% reduction)")

# ============================================================================
# 6. TIME SERIES ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("6. TREND ANALYSIS")
print("=" * 80)

# Monthly order trends
orders_df['Year_Month'] = orders_df['Order_Date'].dt.to_period('M')
monthly_trends = orders_df.groupby('Year_Month').agg({
    'Order_ID': 'count',
    'Total_Value': 'sum',
    'On_Time_Delivery': lambda x: (x == 'Yes').sum() / len(x) * 100
}).round(2)

monthly_trends.columns = ['Orders', 'Revenue', 'On_Time_Rate_%']

# Calculate growth rates
monthly_trends['Order_Growth_%'] = monthly_trends['Orders'].pct_change() * 100
monthly_trends['Revenue_Growth_%'] = monthly_trends['Revenue'].pct_change() * 100

print("\n   Recent Monthly Performance (Last 6 Months):")
print(monthly_trends.tail(6).to_string())

# ============================================================================
# 7. KEY INSIGHTS & RECOMMENDATIONS
# ============================================================================

print("\n" + "=" * 80)
print("7. KEY INSIGHTS & RECOMMENDATIONS")
print("=" * 80)

print("\n   STRENGTHS:")
print(f"   ✓ Overall on-time delivery rate of {on_time_rate:.1f}% meets industry standards")
print(f"   ✓ {warehouse_performance.iloc[0].name} warehouse leads with {warehouse_performance.iloc[0]['On_Time_Rate_%']:.1f}% on-time rate")
print(f"   ✓ Top suppliers maintain {top_suppliers['On_Time_Delivery_Rate'].mean():.1f}% on-time delivery")

print("\n   OPPORTUNITIES FOR IMPROVEMENT:")
print(f"   • {len(low_stock_items)} items at low stock - implement automated reordering")
print(f"   • {len(overstock_items)} items overstocked - optimize inventory levels")
print(f"   • Shipping costs at {(total_shipping_cost/total_order_value)*100:.1f}% of order value - negotiate carrier rates")
print(f"   • {len(late_orders)} late deliveries - strengthen supplier relationships")

print("\n   RECOMMENDED ACTIONS:")
print("   1. Implement ABC analysis for inventory prioritization")
print("   2. Consolidate shipments to reduce per-unit shipping costs")
print("   3. Develop supplier scorecards and quarterly business reviews")
print("   4. Invest in demand forecasting to reduce stockouts")
print("   5. Negotiate volume discounts with top carriers")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - See visualizations and Tableau dashboard for details")
print("=" * 80 + "\n")

# ============================================================================
# 8. SAVE ANALYSIS RESULTS
# ============================================================================

# Save key metrics to Excel for reference
with pd.ExcelWriter('supply_chain_analysis_results.xlsx', engine='openpyxl') as writer:
    warehouse_performance.to_excel(writer, sheet_name='Warehouse_Performance')
    supplier_df.sort_values('Performance_Score', ascending=False).to_excel(writer, sheet_name='Supplier_Rankings', index=False)
    inventory_summary.to_excel(writer, sheet_name='Inventory_Summary')
    carrier_analysis.to_excel(writer, sheet_name='Carrier_Analysis')
    monthly_trends.to_excel(writer, sheet_name='Monthly_Trends')
    
    # Top insights
    insights_df = pd.DataFrame({
        'Metric': [
            'On-Time Delivery Rate',
            'Average Delivery Time (days)',
            'Low Stock Items',
            'Overstock Items',
            'Total Shipping Cost',
            'Best Performing Warehouse',
            'Top Supplier'
        ],
        'Value': [
            f"{on_time_rate:.1f}%",
            f"{avg_delivery_time:.1f}",
            len(low_stock_items),
            len(overstock_items),
            f"${total_shipping_cost:,.2f}",
            warehouse_performance.iloc[0].name,
            top_suppliers.iloc[0]['Supplier']
        ]
    })
    insights_df.to_excel(writer, sheet_name='Executive_Summary', index=False)

print("Analysis results saved to: supply_chain_analysis_results.xlsx")
