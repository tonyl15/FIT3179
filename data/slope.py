import pandas as pd
import numpy as np

def calculate_rate_of_change(start_value, end_value):
    """Calculate percentage rate of change between two values."""
    if start_value == 0:
        return np.inf if end_value != 0 else 0
    return ((end_value - start_value) / start_value) * 100

def get_rate_of_change_analysis():
    """Calculate rate of change for all fields across all states in 5-year intervals."""
    
    # Read the data
    df = pd.read_csv('combined_data.csv')
    
    # Define the fields to analyze
    fields = ['total_proportion', 'house_price', 'inflation_rate', 'min_wage']
    
    # Define the 5-year intervals
    intervals = [
        (2001, 2006),
        (2006, 2011),
        (2011, 2016),
        (2016, 2021)
    ]
    
    # Get unique states
    states = df['state'].unique()
    
    # Results storage
    results = []
    
    print("Rate of Change Analysis (%) - 5-Year Intervals")
    print("=" * 80)
    
    for state in states:
        print(f"\nState: {state}")
        print("-" * 40)
        
        # Filter data for current state
        state_data = df[df['state'] == state].copy()
        
        for start_year, end_year in intervals:
            print(f"\n{start_year} to {end_year}:")
            
            # Get data for start and end years
            start_data = state_data[state_data['year'] == start_year]
            end_data = state_data[state_data['year'] == end_year]
            
            if len(start_data) == 0 or len(end_data) == 0:
                print(f"  Data missing for {start_year} or {end_year}")
                continue
            
            interval_results = {
                'state': state,
                'period': f"{start_year}-{end_year}",
                'start_year': start_year,
                'end_year': end_year
            }
            
            for field in fields:
                start_value = start_data[field].iloc[0]
                end_value = end_data[field].iloc[0]
                
                rate_change = calculate_rate_of_change(start_value, end_value)
                
                interval_results[f'{field}_rate_change'] = round(rate_change, 2)
                
                print(f"  {field}:")
                print(f"    Rate of change: {rate_change:.2f}%")
            
            results.append(interval_results)
    
    # Convert results to DataFrame for easier analysis
    results_df = pd.DataFrame(results)
    
    # Save detailed results to CSV
    results_df.to_csv('rate_of_change.csv', index=False)
    print(f"\n\nDetailed results saved to 'rate_of_change.csv'")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    for field in fields:
        rate_col = f'{field}_rate_change'
        if rate_col in results_df.columns:
            print(f"\n{field.upper()} Rate of Change Statistics:")
            print(f"  Mean: {results_df[rate_col].mean():.2f}%")
            print(f"  Median: {results_df[rate_col].median():.2f}%")
            print(f"  Min: {results_df[rate_col].min():.2f}%")
            print(f"  Max: {results_df[rate_col].max():.2f}%")
            print(f"  Std Dev: {results_df[rate_col].std():.2f}%")
    
    return results_df

if __name__ == "__main__":
    results = get_rate_of_change_analysis()