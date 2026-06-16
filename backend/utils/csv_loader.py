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

    # Clean up column names (strip whitespace and handle casing)
    df.columns = [col.strip() for col in df.columns]
    
    # Case-insensitive column matching
    column_mapping = {}
    lower_required = [col.lower() for col in REQUIRED_COLUMNS]
    
    for col in df.columns:
        if col.lower() in lower_required:
            # Map the actual column name to the standard capitalized name
            idx = lower_required.index(col.lower())
            column_mapping[col] = REQUIRED_COLUMNS[idx]
            
    # Check if all required columns are found
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in column_mapping.values()]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}. The CSV must contain Date, Ri_Rf, Rm_Rf, SMB, HML.")
        
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
