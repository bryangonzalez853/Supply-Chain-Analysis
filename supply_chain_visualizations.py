"""
Supply Chain Visualization Script
Creates comprehensive visualizations for supply chain analytics
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")

# Load data
orders_df = pd.read_csv('orders_data.csv', parse_dates=['Order_Date', 'Expected_Delivery', 'Actual_Delivery'])
inventory_df = pd.read_csv('inventory_data.csv')
supplier_df = pd.read_csv('supplier_performance.csv')
shipping_df = pd.read_csv('shipping_costs.csv')

# Calculate performance score
supplier_df['Performance_Score'] = (
    supplier_df['On_Time_Delivery_Rate'] * 0.4 +
    supplier_df['Quality_Score'] * 0.4 -
    supplier_df['Defect_Rate_Percent'] * 2
).round(2)

# ============================================================================
# VISUALIZATION 1: Order Volume and Revenue Trends
# ============================================================================

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Monthly orders
orders_df['Year_Month'] = orders_df['Order_Date'].dt.to_period('M').astype(str)
monthly_orders = orders_df.groupby('Year_Month').agg({
    'Order_ID': 'count',
    'Total_Value': 'sum'
})

axes[0].plot(monthly_orders.index, monthly_orders['Order_ID'], marker='o', linewidth=2, markersize=6)
axes[0].set_title('Monthly Order Volume Trend', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Number of Orders')
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

axes[1].bar(monthly_orders.index, monthly_orders['Total_Value']/1000, color='steelblue', alpha=0.7)
axes[1].set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Revenue ($000s)')
axes[1].grid(True, alpha=0.3, axis='y')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('visualization_1_trends.png', dpi=300, bbox_inches='tight')
print("Saved: visualization_1_trends.png")

# ============================================================================
# VISUALIZATION 2: On-Time Delivery Performance
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# By warehouse
warehouse_perf = orders_df.groupby('Warehouse')['On_Time_Delivery'].apply(
    lambda x: (x == 'Yes').sum() / len(x) * 100
).sort_values(ascending=False)

axes[0].barh(warehouse_perf.index, warehouse_perf.values, color='green', alpha=0.7)
axes[0].axvline(x=85, color='red', linestyle='--', label='Target (85%)')
axes[0].set_title('On-Time Delivery Rate by Warehouse', fontsize=14, fontweight='bold')
axes[0].set_xlabel('On-Time Delivery Rate (%)')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='x')

# By category
category_perf = orders_df.groupby('Category')['On_Time_Delivery'].apply(
    lambda x: (x == 'Yes').sum() / len(x) * 100
)

colors = ['#2ecc71' if x > 85 else '#e74c3c' for x in category_perf.values]
axes[1].bar(category_perf.index, category_perf.values, color=colors, alpha=0.7)
axes[1].axhline(y=85, color='red', linestyle='--', label='Target (85%)')
axes[1].set_title('On-Time Delivery Rate by Category', fontsize=14, fontweight='bold')
axes[1].set_ylabel('On-Time Delivery Rate (%)')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('visualization_2_delivery_performance.png', dpi=300, bbox_inches='tight')
print("Saved: visualization_2_delivery_performance.png")

# ============================================================================
# VISUALIZATION 3: Inventory Status Dashboard
# ============================================================================

fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# Stock status pie chart
ax1 = fig.add_subplot(gs[0, 0])
stock_status = inventory_df['Stock_Status'].value_counts()
colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
ax1.pie(stock_status.values, labels=stock_status.index, autopct='%1.1f%%', 
        colors=colors_pie, startangle=90)
ax1.set_title('Inventory Status Distribution', fontsize=12, fontweight='bold')

# Inventory by category
ax2 = fig.add_subplot(gs[0, 1])
category_stock = inventory_df.groupby('Category')['Current_Stock'].sum().sort_values(ascending=True)
ax2.barh(category_stock.index, category_stock.values, color='steelblue', alpha=0.7)
ax2.set_title('Total Inventory by Category', fontsize=12, fontweight='bold')
ax2.set_xlabel('Total Units')
ax2.grid(True, alpha=0.3, axis='x')

# Days of inventory by warehouse
ax3 = fig.add_subplot(gs[1, :])
warehouse_inventory = inventory_df.groupby('Warehouse')['Days_of_Inventory'].mean().sort_values()
colors_bar = ['#e74c3c' if x < 30 else '#2ecc71' if x > 60 else '#f39c12' for x in warehouse_inventory.values]
ax3.bar(warehouse_inventory.index, warehouse_inventory.values, color=colors_bar, alpha=0.7)
ax3.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='Min Target (30 days)')
ax3.axhline(y=60, color='orange', linestyle='--', alpha=0.5, label='Max Target (60 days)')
ax3.set_title('Average Days of Inventory by Warehouse', fontsize=12, fontweight='bold')
ax3.set_ylabel('Days')
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

plt.savefig('visualization_3_inventory_dashboard.png', dpi=300, bbox_inches='tight')
print("Saved: visualization_3_inventory_dashboard.png")

# ============================================================================
# VISUALIZATION 4: Supplier Performance Scorecard
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Performance score ranking
supplier_df_sorted = supplier_df.sort_values('Performance_Score', ascending=True)
colors_supplier = ['#2ecc71' if x > 80 else '#f39c12' if x > 70 else '#e74c3c' 
                   for x in supplier_df_sorted['Performance_Score']]

axes[0].barh(supplier_df_sorted['Supplier'], supplier_df_sorted['Performance_Score'], 
             color=colors_supplier, alpha=0.7)
axes[0].set_title('Supplier Performance Scores', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Performance Score')
axes[0].grid(True, alpha=0.3, axis='x')

# On-time vs Quality scatter
axes[1].scatter(supplier_df['On_Time_Delivery_Rate'], supplier_df['Quality_Score'], 
                s=supplier_df['Total_Orders']/10, alpha=0.6, c=supplier_df['Performance_Score'],
                cmap='RdYlGn', edgecolors='black', linewidth=0.5)
axes[1].set_title('Supplier On-Time vs Quality Performance', fontsize=14, fontweight='bold')
axes[1].set_xlabel('On-Time Delivery Rate (%)')
axes[1].set_ylabel('Quality Score')
axes[1].grid(True, alpha=0.3)

# Add reference lines
axes[1].axvline(x=85, color='red', linestyle='--', alpha=0.3)
axes[1].axhline(y=90, color='red', linestyle='--', alpha=0.3)

plt.colorbar(axes[1].collections[0], ax=axes[1], label='Performance Score')
plt.tight_layout()
plt.savefig('visualization_4_supplier_scorecard.png', dpi=300, bbox_inches='tight')
print("Saved: visualization_4_supplier_scorecard.png")

# ============================================================================
# VISUALIZATION 5: Shipping Cost Analysis
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Cost by carrier
carrier_costs = shipping_df.groupby('Carrier')['Shipping_Cost'].agg(['sum', 'mean', 'count'])
axes[0, 0].bar(carrier_costs.index, carrier_costs['sum']/1000, color='coral', alpha=0.7)
axes[0, 0].set_title('Total Shipping Cost by Carrier', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Cost ($000s)')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Cost by method
method_costs = shipping_df.groupby('Shipping_Method')['Shipping_Cost'].mean().sort_values()
axes[0, 1].barh(method_costs.index, method_costs.values, color='teal', alpha=0.7)
axes[0, 1].set_title('Average Shipping Cost by Method', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Average Cost ($)')
axes[0, 1].grid(True, alpha=0.3, axis='x')

# Distance vs Cost scatter
axes[1, 0].scatter(shipping_df['Distance_KM'], shipping_df['Shipping_Cost'], 
                   alpha=0.3, s=10, c='steelblue')
axes[1, 0].set_title('Shipping Cost vs Distance', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Distance (KM)')
axes[1, 0].set_ylabel('Shipping Cost ($)')
axes[1, 0].grid(True, alpha=0.3)

# Weight vs Cost scatter
axes[1, 1].scatter(shipping_df['Weight_KG'], shipping_df['Shipping_Cost'], 
                   alpha=0.3, s=10, c='darkgreen')
axes[1, 1].set_title('Shipping Cost vs Weight', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Weight (KG)')
axes[1, 1].set_ylabel('Shipping Cost ($)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('visualization_5_shipping_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: visualization_5_shipping_analysis.png")

# ============================================================================
# VISUALIZATION 6: Executive Summary Dashboard
# ============================================================================

fig = plt.figure(figsize=(16, 10))
fig.suptitle('SUPPLY CHAIN PERFORMANCE DASHBOARD', fontsize=16, fontweight='bold', y=0.98)

gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.4)

# KPI 1: Total Orders
ax1 = fig.add_subplot(gs[0, 0])
ax1.text(0.5, 0.5, f"{len(orders_df):,}", ha='center', va='center', fontsize=36, fontweight='bold', color='steelblue')
ax1.text(0.5, 0.2, 'Total Orders', ha='center', va='center', fontsize=12)
ax1.axis('off')
ax1.set_facecolor('#f0f0f0')

# KPI 2: On-Time Delivery
ax2 = fig.add_subplot(gs[0, 1])
on_time_pct = (orders_df['On_Time_Delivery'] == 'Yes').sum() / len(orders_df) * 100
color_otd = '#2ecc71' if on_time_pct > 85 else '#e74c3c'
ax2.text(0.5, 0.5, f"{on_time_pct:.1f}%", ha='center', va='center', fontsize=36, fontweight='bold', color=color_otd)
ax2.text(0.5, 0.2, 'On-Time Delivery', ha='center', va='center', fontsize=12)
ax2.axis('off')
ax2.set_facecolor('#f0f0f0')

# KPI 3: Total Revenue
ax3 = fig.add_subplot(gs[0, 2])
total_revenue = orders_df['Total_Value'].sum()
ax3.text(0.5, 0.5, f"${total_revenue/1e6:.1f}M", ha='center', va='center', fontsize=36, fontweight='bold', color='green')
ax3.text(0.5, 0.2, 'Total Revenue', ha='center', va='center', fontsize=12)
ax3.axis('off')
ax3.set_facecolor('#f0f0f0')

# Trend line
ax4 = fig.add_subplot(gs[1, :])
monthly_orders = orders_df.groupby(orders_df['Order_Date'].dt.to_period('M').astype(str))['Order_ID'].count()
ax4.plot(monthly_orders.index, monthly_orders.values, marker='o', linewidth=2, markersize=6, color='steelblue')
ax4.fill_between(range(len(monthly_orders)), monthly_orders.values, alpha=0.3, color='steelblue')
ax4.set_title('Order Volume Trend', fontsize=12, fontweight='bold')
ax4.set_xlabel('Month')
ax4.set_ylabel('Orders')
ax4.grid(True, alpha=0.3)
ax4.tick_params(axis='x', rotation=45)

# Category breakdown
ax5 = fig.add_subplot(gs[2, :2])
category_revenue = orders_df.groupby('Category')['Total_Value'].sum().sort_values(ascending=True)
ax5.barh(category_revenue.index, category_revenue.values/1000, color='coral', alpha=0.7)
ax5.set_title('Revenue by Product Category', fontsize=12, fontweight='bold')
ax5.set_xlabel('Revenue ($000s)')
ax5.grid(True, alpha=0.3, axis='x')

# Stock status
ax6 = fig.add_subplot(gs[2, 2])
stock_status = inventory_df['Stock_Status'].value_counts()
colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
ax6.pie(stock_status.values, labels=stock_status.index, autopct='%1.0f%%', 
        colors=colors_pie, startangle=90)
ax6.set_title('Inventory Status', fontsize=12, fontweight='bold')

plt.savefig('visualization_6_executive_dashboard.png', dpi=300, bbox_inches='tight')
print("Saved: visualization_6_executive_dashboard.png")

plt.close('all')
print("\nAll visualizations created successfully!")
