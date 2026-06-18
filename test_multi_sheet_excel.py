import os
import sys
import pandas as pd

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from utils.csv_loader import inspect_excel_sheets, load_tabular_data

def create_multisheet_excel(filename):
    # Setup data
    dates = pd.date_range(start="2023-01-01", periods=6, freq="ME")
    
    # Sheet 1: Summary info
    df_sum = pd.DataFrame({
        "Key": ["Model", "Created", "Author"],
        "Value": ["Fama French 3-Factor", "2026-06", "Student"]
    })
    
    # Sheet 2: Raw data
    df_data = pd.DataFrame({
        "trading_date": dates,
        "last_price": [150.0, 155.2, 153.0, 158.5, 157.0, 162.0]
    })
    
    with pd.ExcelWriter(filename) as writer:
        df_sum.to_excel(writer, sheet_name="Summary", index=False)
        df_data.to_excel(writer, sheet_name="DataSheet", index=False)
        
    print(f"Created multi-sheet Excel file: {filename}")

def main():
    filename = "test_temp_multisheet.xlsx"
    try:
        create_multisheet_excel(filename)
        
        # Test 1: Sheet Inspection
        with open(filename, "rb") as f:
            file_bytes = f.read()
        
        sheets = inspect_excel_sheets(file_bytes)
        print("Inspected sheets list:", sheets)
        assert sheets == ["Summary", "DataSheet"], f"Incorrect sheets list: {sheets}"
        print("OK: Sheet inspection verified.")
        
        # Test 2: Loading specific sheet
        # Should fail if loading sheet "Summary" since it lacks Date/Close columns
        try:
            load_tabular_data(file_bytes, is_excel=True, sheet_name="Summary")
            print("FAIL: Should have failed loading Summary sheet due to validation rules.")
            assert False, "Summary sheet load did not throw error"
        except ValueError as e:
            print(f"OK: Summary sheet load failed as expected: {str(e)}")
            
        # Should succeed if loading "DataSheet"
        df = load_tabular_data(file_bytes, is_excel=True, sheet_name="DataSheet")
        print("Loaded DataSheet dimensions:", df.shape)
        assert df.shape[0] > 0, "No rows loaded"
        assert "Date" in df.columns, "Date column missing"
        assert "Ri_Rf" in df.columns, "Ri_Rf column missing"
        
        print("OK: Specific sheet data loading & auto-mapping verified successfully.")
        
    finally:
        if os.path.exists(filename):
            os.remove(filename)
            print("Cleaned up multi-sheet temp file.")

if __name__ == "__main__":
    main()
