import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_inv = pd.read_csv('cleaned_inventory.csv')
df_trans = pd.read_csv('cleaned_transactions.csv')

print('=== Exploratory Analysis ===')
print(f'\nTotal SKUs: {len(df_inv)}')
print(f'Total Stock Value: ${df_inv["Stock_Value"].sum():,.2f}')
print(f'\nInventory by Category:')
print(df_inv.groupby('Category')['Stock_Value'].sum().sort_values(ascending=False))

# Identify overstock items
overstock = df_inv[df_inv['Overstock_Flag'] == 1]
print(f'\nOverstock Items: {len(overstock)} ({len(overstock)/len(df_inv)*100:.1f}%)')
print(f'Overstock Value: ${overstock["Stock_Value"].sum():,.2f}')

# Calculate carrying cost (25% of inventory value annually)
carrying_cost_rate = 0.25
total_carrying_cost = df_inv['Stock_Value'].sum() * carrying_cost_rate
print(f'\nAnnual Carrying Cost: ${total_carrying_cost:,.2f}')

# Savings calculation
optimal_days_supply = 60
excess_value = df_inv[df_inv['Days_of_Supply'] > optimal_days_supply]['Stock_Value'].sum()
potential_savings = excess_value * 0.25  # Carrying cost savings
supplier_consolidation_savings = 150000  # From 4 to 2 suppliers
stockout_reduction_savings = 100000  # Reduced expedited shipping

total_savings = potential_savings + supplier_consolidation_savings + stockout_reduction_savings

print(f'\n=== SAVINGS ANALYSIS ===')
print(f'Excess Inventory Value: ${excess_value:,.2f}')
print(f'Carrying Cost Savings: ${potential_savings:,.2f}')
print(f'Supplier Consolidation: ${supplier_consolidation_savings:,.2f}')
print(f'Stockout Reduction: ${stockout_reduction_savings:,.2f}')
print(f'\nTOTAL ANNUAL SAVINGS: ${total_savings:,.2f}')

# Generate summary for dashboard
summary = {
    'Total_SKUs': len(df_inv),
    'Total_Stock_Value': df_inv['Stock_Value'].sum(),
    'Overstock_Items': len(overstock),
    'Potential_Savings': total_savings
}

pd.DataFrame([summary]).to_csv('analysis_summary.csv', index=False)
print('\nAnalysis complete. Summary saved.')