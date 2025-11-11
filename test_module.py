"""
Test script to demonstrate using the data_processing module.
"""

from src.data_processing import SolarDataCleaner
import pandas as pd

# Create sample data for testing
def create_sample_data():
    """Create sample DataFrame for testing."""
    data = {
        'solar_radiation': [850, 920, None, 780, 810],
        'temperature': [25.0, 26.5, 24.8, None, None],
        'efficiency': [0.85, 0.82, 0.79, 0.81, 0.83],
        'voltage': [240, 238, 239, None, 241]
    }
    return pd.DataFrame(data)

def main():
    """Main function to test the SolarDataCleaner."""
    print("Testing SolarDataCleaner module...")
    
    # Create sample data
    df = create_sample_data()
    print("Original DataFrame:")
    print(df)
    print(f"\nShape: {df.shape}")
    
    # Use the cleaner
    cleaner = SolarDataCleaner(df)
    cleaned_df = cleaner.drop_high_missing(threshold=0.3)
    
    print("\nCleaned DataFrame:")
    print(cleaned_df)
    print(f"Shape: {cleaned_df.shape}")

if __name__ == "__main__":
    main()
