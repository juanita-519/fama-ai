import os
import sys
import pandas as pd
import numpy as np

# Add backend to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from utils.csv_loader import load_tabular_data, detect_columns

def create_sample_excel(filename):
    # Create random stock return dataset
    dates = pd.date_range(start="2023-01-01", periods=12, freq="ME")
    close = [100.0, 102.5, 101.0, 104.2, 103.8, 106.0, 107.5, 105.0, 108.2, 110.0, 109.5, 112.0]
    
    df = pd.DataFrame({
        "Trade Date": dates,
        "Closing Price": close
    })
    
    df.to_excel(filename, index=False)
    print(f"Created sample Excel file: {filename}")

def main():
    filename = "test_temp_stock.xlsx"
    try:
        create_sample_excel(filename)
        
        # Test 1: Column Detection Fuzzy Logic
        headers = ["Trade Date", "Closing Price"]
        detected = detect_columns(headers)
        print("Detected mappings:", detected)
        assert detected.get("Date") == "Trade Date", "Failed to detect Date column"
        assert detected.get("Close") == "Closing Price", "Failed to detect Close column"
        print("OK: Fuzzy column detection verified.")

        # Test 2: Excel Loading & Mapped Data Calculation
        df = load_tabular_data(filename, is_excel=True)
        print("Loaded DataFrame:\n", df.head())
        
        assert "Date" in df.columns, "Date column missing in mapped dataframe"
        assert "Ri_Rf" in df.columns, "Ri_Rf column missing/not calculated in mapped dataframe"
        assert "Rm_Rf" in df.columns, "Rm_Rf factor column missing/not merged"
        assert "SMB" in df.columns, "SMB factor column missing/not merged"
        assert "HML" in df.columns, "HML factor column missing/not merged"
        
        print("OK: Excel loader with auto-mapping & factors merging verified successfully.")
        
    finally:
        if os.path.exists(filename):
            os.remove(filename)
            print("Cleaned up temp excel file.")

if __name__ == "__main__":
    main()
