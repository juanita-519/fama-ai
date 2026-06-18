import pandas as pd
import io
import os
from typing import Union, List, Dict, Any

REQUIRED_COLUMNS = ["Date", "Ri_Rf", "Rm_Rf", "SMB", "HML"]

# Equivalent column name mapping dictionary
COLUMN_KEYWORDS = {
    "Date": ["date", "trading date", "trade date", "timestamp", "day", "dt", "period"],
    "Close": ["close", "closing price", "adj close", "adjusted close", "last price", "close price"],
    "Open": ["open", "opening price"],
    "High": ["high", "high price"],
    "Low": ["low", "low price"],
    "Volume": ["volume", "total volume", "traded volume", "shares traded"],
    "Ticker": ["ticker", "symbol", "stock symbol", "company code"],
    "Ri_Rf": ["ri_rf", "ri-rf", "ri_minus_rf", "excess_return", "stock_return", "stock_excess", "stock return", "return"],
    "Rm_Rf": ["rm_rf", "rm-rf", "rm_minus_rf", "market_excess", "market_return", "market factor", "market", "nifty", "mkt"],
    "SMB": ["smb", "size", "small minus big", "small-cap", "small_minus_big"],
    "HML": ["hml", "value", "high minus low", "growth", "style", "high_minus_low"]
}

def inspect_excel_sheets(file_bytes: bytes) -> List[str]:
    """
    Returns list of sheet names in an Excel file.
    """
    try:
        xl = pd.ExcelFile(io.BytesIO(file_bytes))
        return xl.sheet_names
    except Exception as e:
        raise ValueError(f"Failed to inspect Excel sheets: {str(e)}")

def detect_columns(headers: List[str]) -> Dict[str, str]:
    """
    Fuzzy maps list of raw headers to standard Fama-French/financial columns.
    Returns a dict mapping standard column names to raw headers.
    """
    detected = {}
    used_headers = set()
    
    # Create normalized representations mapping (original_header, normalized_lowercase_header)
    normalized = []
    for h in headers:
        hc = str(h).strip()
        hc_norm = hc.lower().replace("_", " ").replace("-", " ")
        normalized.append((h, hc_norm))
    
    # 1. Exact/case-insensitive match on normalized
    for target, keywords in COLUMN_KEYWORDS.items():
        target_lower = target.lower().replace("_", " ")
        for orig, norm in normalized:
            if orig in used_headers:
                continue
            if norm == target_lower:
                detected[target] = orig
                used_headers.add(orig)
                break
                
    # 2. Partial keyword matching on normalized
    for target, keywords in COLUMN_KEYWORDS.items():
        if target in detected:
            continue
        for orig, norm in normalized:
            if orig in used_headers:
                continue
            for kw in keywords:
                kw_clean = kw.lower().replace("_", " ").replace("-", " ")
                if kw_clean in norm:
                    detected[target] = orig
                    used_headers.add(orig)
                    break
            if target in detected:
                break
                
    return detected

def load_mapped_data(df: pd.DataFrame, mapping: Dict[str, str], merge_factors: bool = False) -> pd.DataFrame:
    """
    Applies column mapping on raw DataFrame, handles Close->Return calculation,
    merges Fama-French factors if required/missing, and validates structures.
    """
    if df.empty:
        raise ValueError("Dataset is empty.")

    # Standardize headers (strip whitespace)
    df.columns = [str(col).strip() for col in df.columns]

    # Reverse the mapping dict to map raw_header -> standard_column
    rev_mapping = {v: k for k, v in mapping.items() if v}
    df = df.rename(columns=rev_mapping)

    # 1. Validate Date column exists
    if "Date" not in df.columns:
        raise ValueError("Date column must be mapped and present.")

    # 2. Parse Date
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    except Exception as e:
        raise ValueError(f"Error parsing Date column: {str(e)}")

    df = df.dropna(subset=['Date'])
    if df.empty:
        raise ValueError("No valid parseable dates found in the Date column.")

    # Format Date as YYYY-MM
    df['Date'] = df['Date'].dt.strftime('%Y-%m')

    # 3. Handle Ticker column if present
    if "Ticker" in df.columns:
        tickers = df["Ticker"].dropna().unique()
        if len(tickers) > 1:
            # Filter for the first ticker series to avoid mixing different stocks
            first_ticker = tickers[0]
            df = df[df["Ticker"] == first_ticker]

    # 4. Calculate Ri_Rf if missing
    if "Ri_Rf" not in df.columns:
        if "Close" not in df.columns:
            raise ValueError("Required column mapping missing: Map either 'Stock Excess Return (Ri_Rf)' or 'Close Price'.")
        
        # Sort by Date to compute pct_change
        df = df.sort_values("Date")
        
        try:
            df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        except Exception:
            raise ValueError("Close Price column contains non-numeric values.")
        
        df = df.dropna(subset=['Close'])
        if len(df) < 4:
            raise ValueError("Too few rows with valid Close Prices (minimum 4 required).")
            
        df['Return'] = df['Close'].pct_change()
        # Monthly excess return = Return - Rf (0.0055 monthly)
        df['Ri_Rf'] = df['Return'] - 0.0055
        df = df.dropna(subset=['Ri_Rf'])
    else:
        try:
            df['Ri_Rf'] = pd.to_numeric(df['Ri_Rf'], errors='coerce')
        except Exception:
            raise ValueError("Stock Excess Return (Ri_Rf) column contains non-numeric values.")
        df = df.dropna(subset=['Ri_Rf'])

    # 5. Handle factor mapping or merging
    has_factors_in_file = all(col in df.columns for col in ["Rm_Rf", "SMB", "HML"])
    
    if merge_factors or not has_factors_in_file:
        # Load platform Fama-French factors from sample database
        factors_file = os.path.join("backend", "sample_data", "infosys.csv")
        if not os.path.exists(factors_file):
            raise FileNotFoundError("Baseline market factor database is missing on the server.")
        factors_df = pd.read_csv(factors_file)
        factors_df['Date'] = pd.to_datetime(factors_df['Date']).dt.strftime('%Y-%m')
        
        # Merge on Date
        merged = pd.merge(factors_df[["Date", "Rm_Rf", "SMB", "HML"]], df[["Date", "Ri_Rf"]], on="Date", how="inner")
        if len(merged) < 4:
            raise ValueError("Insuffient overlapping dates between uploaded dataset and the platform factors database (minimum 4 monthly data points required).")
        return merged[["Date", "Ri_Rf", "Rm_Rf", "SMB", "HML"]]
    else:
        # Validate and clean factor columns
        for col in ["Rm_Rf", "SMB", "HML"]:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except Exception:
                raise ValueError(f"Column '{col}' must contain only numeric values.")
            df = df.dropna(subset=[col])
            
        if len(df) < 4:
            raise ValueError("Insufficient valid data points remaining (minimum 4 required).")
            
        return df[["Date", "Ri_Rf", "Rm_Rf", "SMB", "HML"]].sort_values("Date")

def load_tabular_data(file_source: Union[str, bytes, io.BytesIO], is_excel: bool = False, sheet_name: str = None) -> pd.DataFrame:
    """
    Loads Excel or CSV, runs auto column detection, and returns a verified DataFrame.
    (Backward-compatible wrapper).
    """
    try:
        if is_excel:
            if isinstance(file_source, bytes):
                df = pd.read_excel(io.BytesIO(file_source), sheet_name=sheet_name if sheet_name else 0)
            elif isinstance(file_source, io.BytesIO):
                df = pd.read_excel(file_source, sheet_name=sheet_name if sheet_name else 0)
            else:
                df = pd.read_excel(file_source, sheet_name=sheet_name if sheet_name else 0)
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
        raise ValueError("The uploaded dataset is empty.")

    # Run auto-detection
    mapping = detect_columns(list(df.columns))
    
    # Auto-merge factors if they aren't all present in the file
    merge_factors = not all(col in mapping for col in ["Rm_Rf", "SMB", "HML"])
    
    return load_mapped_data(df, mapping, merge_factors=merge_factors)

def load_csv(file_source: Union[str, bytes, io.BytesIO]) -> pd.DataFrame:
    """
    Backward-compatible wrapper for load_tabular_data.
    """
    return load_tabular_data(file_source, is_excel=False)
