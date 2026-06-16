import os
import sys

# Add backend directory to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from utils.csv_loader import load_csv
from services.regression_service import run_fama_french_regression
from utils.pdf_generator import generate_pdf_report

def main():
    print("====================================================")
    print("FAMA AI - Programmatic Verification Test Suite")
    print("====================================================")
    
    # 1. Test sample files existence
    infosys_path = os.path.join("backend", "sample_data", "infosys.csv")
    tata_path = os.path.join("backend", "sample_data", "tata_motors.csv")
    
    print(f"Checking sample datasets...")
    assert os.path.exists(infosys_path), "Error: infosys.csv is missing"
    assert os.path.exists(tata_path), "Error: tata_motors.csv is missing"
    print("OK: Sample CSV files verified.")
    
    # 2. Test CSV Loader
    print(f"\nTesting CSV Loader on {infosys_path}...")
    try:
        df = load_csv(infosys_path)
        print(f"OK: CSV loaded successfully. Dimensions: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(df.head(2))
    except Exception as e:
        print(f"FAIL: CSV loader failed with error: {str(e)}")
        sys.exit(1)
        
    # 3. Test OLS Regression Engine
    print("\nTesting OLS Regression Engine...")
    try:
        results = run_fama_french_regression(df)
        print("OK: OLS regression completed successfully.")
        print(f"Observations: {results['num_observations']}")
        print(f"R-squared: {results['r_squared']:.4f}")
        
        # Check factors
        for factor, details in results["factors"].items():
            print(f"  - {factor}: Coefficient={details['coefficient']:.4f}, p-val={details['p_value']:.4f}, significant={details['significant']}")
            
        print("\nInterpretations Sample:")
        print(f"  - Market: {results['interpretations']['market']}")
        print(f"  - Size: {results['interpretations']['smb']}")
        print(f"  - Style: {results['interpretations']['hml']}")
    except Exception as e:
        print(f"FAIL: OLS regression failed with error: {str(e)}")
        sys.exit(1)
        
    # 4. Test PDF Generator
    print("\nTesting ReportLab PDF Generator...")
    try:
        pdf_buffer = generate_pdf_report("Infosys Limited (TEST)", results)
        pdf_bytes = pdf_buffer.getvalue()
        print(f"OK: PDF generated in-memory. Size: {len(pdf_bytes)} bytes.")
        assert len(pdf_bytes) > 1000, "Error: PDF file size is suspiciously small"
    except Exception as e:
        print(f"FAIL: PDF generator failed with error: {str(e)}")
        sys.exit(1)
        
    print("\n====================================================")
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("====================================================")

if __name__ == "__main__":
    main()
