import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List

from backend.utils.csv_loader import load_tabular_data
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

# Sample stock mapping
SAMPLE_STOCKS = {
    "infosys": {
        "name": "Infosys Limited (INFY)",
        "file_name": "infosys.csv"
    },
    "tata_motors": {
        "name": "Tata Motors Limited (TATAMOTORS)",
        "file_name": "tata_motors.csv"
    }
}

class ReportRequest(BaseModel):
    stock_name: str
    results: Dict[str, Any]

@app.get("/api/stocks")
def get_stocks():
    """
    Returns the list of pre-configured sample stocks.
    """
    return [
        {"id": symbol, "name": meta["name"]} 
        for symbol, meta in SAMPLE_STOCKS.items()
    ]

@app.get("/api/fama-analysis/{symbol}")
def analyze_stock(symbol: str):
    """
    Loads stock factor dataset, performs regression, and returns raw data + results.
    Works for pre-configured sample stocks as well as custom symbols globally.
    """
    symbol_lower = symbol.lower().strip()
    
    if symbol_lower in SAMPLE_STOCKS:
        stock_meta = SAMPLE_STOCKS[symbol_lower]
        file_path = os.path.join("backend", "sample_data", stock_meta["file_name"])
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=500, 
                detail=f"Sample data file {stock_meta['file_name']} is missing on the server."
            )
            
        try:
            df = load_tabular_data(file_path, is_excel=file_path.endswith('.xlsx'))
            stock_name = stock_meta["name"]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        # Fetch/Simulate custom stock data
        try:
            from backend.services.regression_service import load_custom_stock_data
            df = load_custom_stock_data(symbol)
            stock_name = f"{symbol.strip().upper()} (Market Analysis)"
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to fetch data for stock ticker '{symbol.upper()}': {str(e)}"
            )
        
    try:
        # Run regression
        results = run_fama_french_regression(df)
        # Prepare raw data points for graphs
        raw_data = df.to_dict(orient="records")
        
        return {
            "stock_name": stock_name,
            "results": results,
            "data": raw_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fama-analysis/upload")
async def analyze_uploaded_csv(file: UploadFile = File(...)):
    """
    Validates uploaded CSV or Excel file, runs Fama-French regression, and returns data + results.
    """
    is_excel = file.filename.endswith('.xlsx') or file.filename.endswith('.xls')
    if not (file.filename.endswith('.csv') or is_excel):
        raise HTTPException(status_code=400, detail="Only CSV and Excel (.xlsx, .xls) files are accepted.")
        
    try:
        contents = await file.read()
        # Load and validate CSV or Excel from bytes
        df = load_tabular_data(contents, is_excel=is_excel)
        # Run regression
        results = run_fama_french_regression(df)
        # Raw records
        raw_data = df.to_dict(orient="records")
        
        # Extrapolate name from filename
        stock_name = os.path.splitext(file.filename)[0].replace("_", " ").title() + " (Uploaded)"
        
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
