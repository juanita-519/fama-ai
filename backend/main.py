import os
import io
import json
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List

from backend.utils.csv_loader import load_tabular_data, load_mapped_data
from backend.services.regression_service import run_fama_french_regression
from backend.utils.pdf_generator import generate_pdf_report

app = FastAPI(
    title="FAMA AI – Fama-French 3-Factor Stock Analysis Platform",
    description="Backend API and web server for statistical equity factor analysis."
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIG_PATH = os.path.join("backend", "sample_data", "stocks_config.json")

def load_stocks_config() -> List[Dict[str, Any]]:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

class ReportRequest(BaseModel):
    stock_name: str
    results: Dict[str, Any]

@app.get("/api/stocks")
def get_stocks():
    """
    Returns the list of stocks from the configuration file.
    """
    try:
        return load_stocks_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load stocks config: {str(e)}")

@app.get("/api/fama-analysis/{symbol}")
def analyze_stock(symbol: str):
    """
    Loads stock factor dataset, performs regression, and returns raw data + results.
    """
    symbol_clean = symbol.strip().upper()
    stocks_config = load_stocks_config()
    stock_meta = None
    
    # Check if stock exists in configuration
    for s in stocks_config:
        if s["id"].upper() == symbol_clean or s["ticker"].upper() == symbol_clean or s["id"].lower() == symbol.lower().strip():
            stock_meta = s
            break
            
    if stock_meta:
        if stock_meta.get("is_sample", False):
            file_name = "infosys.csv" if stock_meta["id"] == "infosys" else "tata_motors.csv"
            file_path = os.path.join("backend", "sample_data", file_name)
            
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=500, 
                    detail=f"Sample data file {file_name} is missing on the server."
                )
                
            try:
                df = load_tabular_data(file_path, is_excel=file_path.endswith('.xlsx'))
                stock_name = stock_meta["name"]
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        else:
            # Fetch custom stock data
            try:
                from backend.services.regression_service import load_custom_stock_data
                df = load_custom_stock_data(stock_meta["ticker"])
                stock_name = f"{stock_meta['name']} ({stock_meta['id']})"
            except Exception as e:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Failed to fetch data for stock ticker '{stock_meta['id']}': {str(e)}"
                )
    else:
        # Dynamic fallback lookup
        try:
            from backend.services.regression_service import load_custom_stock_data
            df = load_custom_stock_data(symbol_clean)
            stock_name = f"{symbol_clean} (Market Analysis)"
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to fetch data for stock ticker '{symbol_clean}': {str(e)}"
            )
        
    try:
        # Run regression
        results = run_fama_french_regression(df)
        raw_data = df.to_dict(orient="records")
        
        return {
            "stock_name": stock_name,
            "results": results,
            "data": raw_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fama-analysis/upload-preview")
async def get_upload_preview(file: UploadFile = File(...), sheet_name: str = Form(None)):
    """
    Parses headers, sheet names (for Excel), and detects columns before executing analysis.
    """
    filename = file.filename
    is_excel = filename.endswith('.xlsx') or filename.endswith('.xls')
    if not (filename.endswith('.csv') or is_excel):
        raise HTTPException(status_code=400, detail="Only CSV and Excel (.xlsx, .xls) files are supported.")
        
    try:
        contents = await file.read()
        
        sheets = []
        if is_excel:
            from backend.utils.csv_loader import inspect_excel_sheets
            sheets = inspect_excel_sheets(contents)
            active_sheet = sheet_name if sheet_name else (sheets[0] if sheets else None)
        else:
            active_sheet = None

        # Load raw dataframe to inspect headers & rows
        try:
            if is_excel:
                df = pd.read_excel(io.BytesIO(contents), sheet_name=active_sheet)
            else:
                df = pd.read_csv(io.BytesIO(contents))
        except Exception as e:
            raise ValueError(f"Error reading file structure: {str(e)}")

        if df.empty:
            raise ValueError("The uploaded file contains no data.")

        # Clean headers
        raw_headers = [str(col).strip() for col in df.columns]
        
        # Get preview data (first 5 rows as dict)
        preview_df = df.head(5).fillna("")
        preview_rows = preview_df.to_dict(orient="records")
        
        # Detect mapping
        from backend.utils.csv_loader import detect_columns
        detected_mapping = detect_columns(raw_headers)
        
        return {
            "filename": filename,
            "is_excel": is_excel,
            "sheets": sheets,
            "active_sheet": active_sheet,
            "headers": raw_headers,
            "detected_mapping": detected_mapping,
            "preview_rows": preview_rows
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fama-analysis/upload")
async def analyze_uploaded_csv(
    file: UploadFile = File(...),
    sheet_name: str = Form(None),
    column_mapping: str = Form(...)  # JSON string
):
    """
    Executes Fama-French regression using client-specified column mappings.
    """
    is_excel = file.filename.endswith('.xlsx') or file.filename.endswith('.xls')
    if not (file.filename.endswith('.csv') or is_excel):
        raise HTTPException(status_code=400, detail="Only CSV and Excel (.xlsx, .xls) files are accepted.")
        
    try:
        mapping = json.loads(column_mapping)
        contents = await file.read()
        
        # Load raw dataframe
        if is_excel:
            df = pd.read_excel(io.BytesIO(contents), sheet_name=sheet_name if sheet_name else 0)
        else:
            df = pd.read_csv(io.BytesIO(contents))
            
        # Determine if we need to merge baseline market factors
        has_factors = all(col in mapping and mapping[col] for col in ["Rm_Rf", "SMB", "HML"])
        
        # Load mapped data
        processed_df = load_mapped_data(df, mapping, merge_factors=not has_factors)
        
        # Run regression
        results = run_fama_french_regression(processed_df)
        raw_data = processed_df.to_dict(orient="records")
        
        # Extrapolate name from filename
        name_prefix = os.path.splitext(file.filename)[0].replace("_", " ").title()
        sheet_suffix = f" [{sheet_name}]" if sheet_name else ""
        stock_name = f"{name_prefix}{sheet_suffix} (Uploaded)"
        
        return {
            "stock_name": stock_name,
            "results": results,
            "data": raw_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/reports/export")
def export_pdf_report(payload: ReportRequest):
    """
    Stateless endpoint that generates and downloads the OLS report PDF based on client inputs.
    """
    try:
        pdf_buffer = generate_pdf_report(payload.stock_name, payload.results)
        
        # Clean filename
        safe_name = "".join(c for c in payload.stock_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(" ", "_")
        filename = f"Fama_French_Report_{safe_name}.pdf"
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

# Fallback serving of SPA root index.html
@app.get("/")
def serve_index():
    index_path = os.path.join("backend", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "FAMA AI server is running. Frontend static directory is empty or setup failed."}

# Mount static files (javascript, styles, favicon)
# Must be mounted AFTER other specific endpoints to avoid route interception.
static_dir = os.path.join("backend", "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    # Create directory structure for static files
    os.makedirs(os.path.join(static_dir, "js"), exist_ok=True)
    os.makedirs(os.path.join(static_dir, "css"), exist_ok=True)
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
