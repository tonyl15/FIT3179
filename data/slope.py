import pandas as pd
import numpy as np

def calculate_ratio(start_value, end_value):
    """Calculate ratio of end_value to start_value (how many times greater/lesser)."""
    if start_value == 0:
        return np.inf if end_value != 0 else 1.0
    return end_value / start_value

def get_ratio_analysis():
    """Calculate ratios for all fields across all states in 5-year intervals."""
    
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
    
    print("Ratio Analysis - 5-Year Intervals")
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
                
                ratio = calculate_ratio(start_value, end_value)
                
                interval_results[f'{field}_ratio'] = round(ratio, 3)
                
                print(f"  {field}:")
                if ratio > 1:
                    print(f"    Ratio: {ratio:.3f}x (increased by {ratio:.3f} times)")
                elif ratio < 1:
                    print(f"    Ratio: {ratio:.3f}x (decreased to {ratio:.3f} of original)")
                else:
                    print(f"    Ratio: {ratio:.3f}x (no change)")
            
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
        ratio_col = f'{field}_ratio'
        if ratio_col in results_df.columns:
            print(f"\n{field.upper()} Ratio Statistics:")
            print(f"  Mean: {results_df[ratio_col].mean():.3f}x")
            print(f"  Median: {results_df[ratio_col].median():.3f}x")
            print(f"  Min: {results_df[ratio_col].min():.3f}x")
            print(f"  Max: {results_df[ratio_col].max():.3f}x")
            print(f"  Std Dev: {results_df[ratio_col].std():.3f}")
    
    return results_df

if __name__ == "__main__":
    results = get_ratio_analysis()