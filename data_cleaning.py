import pandas as pd
import numpy as np

# Load raw data
df_inv = pd.read_csv('raw_inventory.csv')
df_trans = pd.read_csv('raw_transactions.csv')

print('=== Data Cleaning Started ===')
print(f'Initial inventory records: {len(df_inv)}')
print(f'Initial transaction records: {len(df_trans)}')

# Clean inventory data
df_inv = df_inv.drop_duplicates(subset=['SKU'])
df_inv['Unit_Cost'] = df_inv['Unit_Cost'].clip(lower=0.1)
df_inv['Current_Stock'] = df_inv['Current_Stock'].clip(lower=0)
df_inv['Annual_Demand'] = df_inv['Annual_Demand'].clip(lower=1)

# Clean transaction data
df_trans['Date'] = pd.to_datetime(df_trans['Date'])
df_trans = df_trans.dropna()
df_trans = df_trans[df_trans['Quantity'] > 0]
df_trans = df_trans[df_trans['Cost'] > 0]
df_trans = df_trans.sort_values('Date')

# Add calculated fields
df_inv['Stock_Value'] = df_inv['Current_Stock'] * df_inv['Unit_Cost']
df_inv['Days_of_Supply'] = (df_inv['Current_Stock'] / df_inv['Annual_Demand'] * 365).round(1)
df_inv['Overstock_Flag'] = (df_inv['Days_of_Supply'] > 90).astype(int)

# Save cleaned data
df_inv.to_csv('cleaned_inventory.csv', index=False)
df_trans.to_csv('cleaned_transactions.csv', index=False)

print(f'Cleaned inventory records: {len(df_inv)}')
print(f'Cleaned transaction records: {len(df_trans)}')
print('=== Data Cleaning Complete ===')