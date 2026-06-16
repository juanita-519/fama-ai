import pandas as pd
import io
from typing import Union

REQUIRED_COLUMNS = ["Date", "Ri_Rf", "Rm_Rf", "SMB", "HML"]

def load_tabular_data(file_source: Union[str, bytes, io.BytesIO], is_excel: bool = False) -> pd.DataFrame:
    """
    Loads and validates a Fama-French CSV or Excel dataset.
    
    Parameters:
        file_source: Can be a file path (str), raw bytes (from file upload), or a BytesIO stream.
        is_excel: Boolean flag to load Excel (.xlsx) instead of CSV.
        
    Returns:
        pd.DataFrame containing columns: Date, Ri_Rf, Rm_Rf, SMB, HML
        
    Raises:
        ValueError: If required columns are missing, data is empty, or numeric columns contain non-numeric data.
    """
    try:
        if is_excel:
            if isinstance(file_source, bytes):
                df = pd.read_excel(io.BytesIO(file_source))
            elif isinstance(file_source, io.BytesIO):
                df = pd.read_excel(file_source)
            else:
                df = pd.read_excel(file_source)
        else:
            if isinstance(file_source, bytes):
                df = pd.read_csv(io.BytesIO(file_source))
            elif isinstance(file_source, io.BytesIO):
                df = pd.read_csv(file_source)
            else:
                df = pd.read_csv(file_source)
    except Exception as e:
        file_type = "Excel" if is_excel else "CSV"
        raise ValueError(f"Failed to read {file_type} file: {str(e)}")

    if df.empty:
        raise ValueError("The uploaded CSV file is empty.")

    # Clean up column names (strip whitespace)
    df.columns = [str(col).strip() for col in df.columns]
    
    # Fuzzy column mapping
    column_mapping = {}
    
    # Define keywords for each required column
    date_keywords = ["date", "time", "month", "year", "period", "dt", "timestamp"]
    ri_rf_keywords = ["ri_rf", "ri-rf", "ri_minus_rf", "excess_return", "stock_return", "stock_excess", "stock", "return", "asset", "infosys", "tata", "close", "price"]
    rm_rf_keywords = ["rm_rf", "rm-rf", "rm_minus_rf", "market_excess", "market_return", "market", "nifty", "mkt"]
    smb_keywords = ["smb", "size", "small minus big", "small-cap", "small_minus_big"]
    hml_keywords = ["hml", "value", "high minus low", "growth", "style", "high_minus_low"]
    
    # Track which columns we've mapped
    mapped_source_cols = set()
    
    # Helper to find a matching column
    def find_matching_column(keywords, target_name):
        # 1. Try exact/case-insensitive match first
        for col in df.columns:
            if col in mapped_source_cols:
                continue
            if col.lower() == target_name.lower():
                mapped_source_cols.add(col)
                return col
                
        # 2. Try partial keyword matches
        for col in df.columns:
            if col in mapped_source_cols:
                continue
            for kw in keywords:
                if kw in col.lower():
                    mapped_source_cols.add(col)
                    return col
        return None

    # Find matches for each required column in order of specificity
    date_col = find_matching_column(date_keywords, "Date")
    # If date_col not found, default to first column
    if not date_col and len(df.columns) > 0:
        date_col = df.columns[0]
        mapped_source_cols.add(date_col)
        
    rm_rf_col = find_matching_column(rm_rf_keywords, "Rm_Rf")
    smb_col = find_matching_column(smb_keywords, "SMB")
    hml_col = find_matching_column(hml_keywords, "HML")
    ri_rf_col = find_matching_column(ri_rf_keywords, "Ri_Rf")
    
    # Fallback: if we still have unmapped columns, assign them in order of standard columns
    unmapped_targets = []
    if not date_col: unmapped_targets.append("Date")
    if not ri_rf_col: unmapped_targets.append("Ri_Rf")
    if not rm_rf_col: unmapped_targets.append("Rm_Rf")
    if not smb_col: unmapped_targets.append("SMB")
    if not hml_col: unmapped_targets.append("HML")
    
    for target in unmapped_targets:
        for col in df.columns:
            if col not in mapped_source_cols:
                mapped_source_cols.add(col)
                if target == "Date": date_col = col
                elif target == "Ri_Rf": ri_rf_col = col
                elif target == "Rm_Rf": rm_rf_col = col
                elif target == "SMB": smb_col = col
                elif target == "HML": hml_col = col
                break
                
    # Build final mapping
    if date_col: column_mapping[date_col] = "Date"
    if ri_rf_col: column_mapping[ri_rf_col] = "Ri_Rf"
    if rm_rf_col: column_mapping[rm_rf_col] = "Rm_Rf"
    if smb_col: column_mapping[smb_col] = "SMB"
    if hml_col: column_mapping[hml_col] = "HML"
    
    # Check if all required columns are mapped
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in column_mapping.values()]
    if missing_cols:
        raise ValueError(f"Fuzzy column matching failed. Could not map the columns to match Fama-French inputs: {', '.join(missing_cols)}.")
        
    # Rename columns to our standard format
    df = df.rename(columns=column_mapping)
    
    # Select only the required columns
    df = df[REQUIRED_COLUMNS]
    
    # Drop rows where all elements are NaN
    df = df.dropna(how='all')
    
    # Check if we have at least 3 rows to run OLS regression
    if len(df) < 4:
        raise ValueError("At least 4 data points are required to run the Fama-French 3-Factor regression.")

    # Validate Date column
    df['Date'] = df['Date'].astype(str).str.strip()
    if df['Date'].isnull().any() or (df['Date'] == '').any():
        raise ValueError("The 'Date' column contains empty or null values.")

    # Validate numeric columns
    numeric_cols = ["Ri_Rf", "Rm_Rf", "SMB", "HML"]
    for col in numeric_cols:
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception:
            raise ValueError(f"Column '{col}' must contain only numeric values.")
            
        # Drop rows where numeric columns are NaN
        df = df.dropna(subset=[col])
        
    if len(df) < 4:
        raise ValueError("Not enough valid numeric rows to perform regression analysis.")
        
    return df

def load_csv(file_source: Union[str, bytes, io.BytesIO]) -> pd.DataFrame:
    """
    Backward-compatible wrapper for load_tabular_data (CSV default).
    """
    return load_tabular_data(file_source, is_excel=False)
