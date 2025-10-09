import pandas as pd
import numpy as np

# Define the mapping from capital cities to states
city_to_state = {
    'Sydney': 'NSW',
    'Melbourne': 'VIC', 
    'Brisbane': 'QLD',
    'Adelaide': 'SA',
    'Perth': 'WA',
    'Hobart': 'TA',
    'Darwin': 'NT',
    'Canberra': 'ACT'
}

# Read all the CSV files
births_df = pd.read_csv('births_by_state_region.csv')
house_prices_df = pd.read_csv('House prices.csv')
inflation_df = pd.read_csv('Inflation rate.csv')
min_wage_df = pd.read_csv('Minimum wage.csv')

print("Data loaded successfully!")
print(f"Births data shape: {births_df.shape}")
print(f"House prices data shape: {house_prices_df.shape}")
print(f"Inflation data shape: {inflation_df.shape}")
print(f"Minimum wage data shape: {min_wage_df.shape}")

# Process births data
print("\n=== Processing births data ===")
# Group by state and year, sum the proportions
births_grouped = births_df.groupby(['state', 'year'])['proportion'].sum().reset_index()
births_grouped.rename(columns={'proportion': 'total_proportion'}, inplace=True)
print(f"Unique years in births data: {sorted(births_grouped['year'].unique())}")
print(f"Unique states in births data: {sorted(births_grouped['state'].unique())}")

# Process house prices data
print("\n=== Processing house prices data ===")
# Filter for December entries only and extract year
house_prices_df['Date'] = pd.to_datetime(house_prices_df['Date'], format='%b-%y')
house_prices_df['Year'] = house_prices_df['Date'].dt.year
december_prices = house_prices_df[house_prices_df['Date'].dt.month == 12].copy()

# Melt the dataframe to have city-price pairs
house_melted = pd.melt(december_prices, 
                      id_vars=['Year'], 
                      value_vars=['Sydney', 'Melbourne', 'Brisbane', 'Adelaide', 'Perth', 'Hobart', 'Darwin', 'Canberra'],
                      var_name='City', 
                      value_name='house_price')

# Map cities to states
house_melted['state'] = house_melted['City'].map(city_to_state)
house_melted = house_melted[['Year', 'state', 'house_price']].rename(columns={'Year': 'year'})
print(f"House prices years range: {house_melted['year'].min()}-{house_melted['year'].max()}")

# Process inflation data
print("\n=== Processing inflation data ===")
# Filter for December entries only and extract year
inflation_df['Date'] = pd.to_datetime(inflation_df['Date'], format='%b-%y')
inflation_df['Year'] = inflation_df['Date'].dt.year
december_inflation = inflation_df[inflation_df['Date'].dt.month == 12].copy()

# Melt the dataframe, excluding Australia column
city_columns = ['Sydney', 'Melbourne', 'Brisbane', 'Adelaide', 'Perth', 'Hobart', 'Darwin', 'Canberra']
inflation_melted = pd.melt(december_inflation, 
                          id_vars=['Year'], 
                          value_vars=city_columns,
                          var_name='City', 
                          value_name='inflation_rate')

# Map cities to states
inflation_melted['state'] = inflation_melted['City'].map(city_to_state)
inflation_melted = inflation_melted[['Year', 'state', 'inflation_rate']].rename(columns={'Year': 'year'})
print(f"Inflation data years range: {inflation_melted['year'].min()}-{inflation_melted['year'].max()}")

# Process minimum wage data
print("\n=== Processing minimum wage data ===")
# Filter for years 2001-2024
min_wage_filtered = min_wage_df[(min_wage_df['Date'] >= 2001) & (min_wage_df['Date'] <= 2024)].copy()
min_wage_filtered = min_wage_filtered[['Date', 'MinWagePerHr']].rename(columns={'Date': 'year', 'MinWagePerHr': 'min_wage'})
print(f"Min wage years range: {min_wage_filtered['year'].min()}-{min_wage_filtered['year'].max()}")

# Create all combinations for years 2001-2024 and all states
years = list(range(2001, 2025))
states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TA', 'VIC', 'WA']

print(f"\n=== Creating final combined dataset ===")
print(f"Target years: {years[0]}-{years[-1]}")
print(f"Target states: {states}")

# Create the base dataframe with all year-state combinations
from itertools import product
base_df = pd.DataFrame(list(product(years, states)), columns=['year', 'state'])

# Merge with births data
print("Merging births data...")
merged_df = base_df.merge(births_grouped, on=['year', 'state'], how='left')

# Forward fill missing birth proportion data
print("Forward filling missing birth proportion data...")
merged_df = merged_df.sort_values(['state', 'year'])
merged_df['total_proportion'] = merged_df.groupby('state')['total_proportion'].transform(lambda x: x.fillna(method='ffill'))

# Merge with house prices
print("Merging house prices data...")
merged_df = merged_df.merge(house_melted, on=['year', 'state'], how='left')

# Merge with inflation data
print("Merging inflation data...")
merged_df = merged_df.merge(inflation_melted, on=['year', 'state'], how='left')

# Merge with minimum wage (add min wage to all states for each year)
print("Merging minimum wage data...")
merged_df = merged_df.merge(min_wage_filtered, on='year', how='left')

# Reorder columns
final_df = merged_df[['year', 'state', 'total_proportion', 'house_price', 'inflation_rate', 'min_wage']]

print(f"\nFinal dataset shape: {final_df.shape}")
print(f"Missing values per column:")
print(final_df.isnull().sum())

# Save to CSV
output_file = 'combined_data.csv'
final_df.to_csv(output_file, index=False)
print(f"\nData saved to {output_file}")

# Display first few rows for verification
print("\nFirst 10 rows:")
print(final_df.head(10))

print("\nLast 10 rows:")
print(final_df.tail(10))

# Show sample for each state
print("\nSample data for year 2001:")
print(final_df[final_df['year'] == 2001].to_string(index=False))

print("\nSample data for year 2024:")
print(final_df[final_df['year'] == 2024].to_string(index=False))