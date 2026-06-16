# FAMA AI – Fama-French 3-Factor Stock Analysis Platform

**FAMA AI** is a clean, professional, and academically focused web application designed to automate **Fama-French 3-Factor Model analysis** for equities (specifically NIFTY 50 stocks like Infosys and Tata Motors) using pre-prepared financial factor datasets. 

The platform runs a high-precision Ordinary Least Squares (OLS) regression on historical excess returns against systemic factors, rendering interactive visualizations and generating comprehensive PDF academic reports.

---

## 🏗️ System Architecture

The application is structured as a lightweight, high-performance, single-server deployment. The FastAPI backend serves both the data analytics API endpoints and the modular React single-page frontend.

```mermaid
graph TD
    subgraph Client [Frontend (Browser-Executed React)]
        UI[Glassmorphic Dashboard]
        Plotly[Plotly.js Charts]
        Uploader[CSV Upload Component]
        Exporter[PDF Export Trigger]
    end

    subgraph Server [FastAPI Backend]
        API[FastAPI Router]
        Loader[CSV Loader & Validator]
        OLS[OLS Regression Engine]
        PDF[ReportLab PDF Generator]
    end

    subgraph Data [Data Layer]
        Samples[Sample CSVs: infosys.csv, tata_motors.csv]
        Uploaded[Uploaded Custom CSVs]
    end

    %% Interactions
    UI -->|1. Select Stock / Upload| API
    Uploader -->|2. Post CSV File| API
    API -->|3. Read & Validate| Loader
    Loader -->|4. Parse DataFrame| OLS
    Samples -->|Load| Loader
    Uploaded -->|Validate| Loader
    OLS -->|5. Compute Coefficients & Stats| API
    API -->|6. Return JSON Results| UI
    UI -->|7. Render Charts| Plotly
    Exporter -->|8. Request PDF| API
    API -->|9. Build PDF document| PDF
    PDF -->|10. Stream PDF Binary| UI
```

---

## 📈 Fama-French 3-Factor Model Overview

The platform executes the standard Fama-French 3-Factor asset pricing model:

$$R_i - R_f = \alpha + \beta_{Market}(R_m - R_f) + s(SMB) + h(HML) + \epsilon$$

Where:
* **$R_i - R_f$ (`Ri_Rf`)**: Excess return of the stock over the risk-free rate.
* **$R_m - R_f$ (`Rm_Rf`)**: Excess return of the market index (NIFTY 50) over the risk-free rate (Indian 10-Year Government Bond Yield).
* **`SMB` (Small Minus Big)**: The size premium factor (historical return spread of small-cap vs. big-cap firms).
* **`HML` (High Minus Low)**: The style/value premium factor (historical return spread of high book-to-market vs. low book-to-market firms).
* **$\alpha$ (Alpha)**: The abnormal/intercept return after adjusting for factor risk exposures.

---

## 📁 Expected CSV Format

Custom uploaded files must be in CSV format and include the following column headers (case-insensitive):

| Column Name | Type | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `Date` | `String` | Year-Month (YYYY-MM) or Date (YYYY-MM-DD) | `2023-01` |
| `Ri_Rf` | `Float` | Stock Excess Return ($R_i - R_f$) | `0.0215` |
| `Rm_Rf` | `Float` | Market Excess Return ($R_m - R_f$) | `0.0182` |
| `SMB` | `Float` | Small Minus Big Factor Return | `0.0054` |
| `HML` | `Float` | High Minus Low Factor Return | `-0.0021` |

*Example CSV content:*
```csv
Date, Ri_Rf, Rm_Rf, SMB, HML
2023-01, 0.0210, 0.0180, 0.0050, -0.0020
2023-02, 0.0150, 0.0120, 0.0040, -0.0010
```

---

## ⚡ Tech Stack

* **Frontend**: ReactJS (Single Page Application served as ES Modules via CDN), Tailwind CSS v3 (Responsive Styling), Plotly.js (Interactive Charts).
* **Backend**: Python FastAPI (Server & REST API), Uvicorn (ASGI web server).
* **Data & Statistics**: Pandas (Data Manipulation), NumPy (Matrix/Numerical Ops), Statsmodels (OLS Regressions).
* **Reports**: ReportLab (High-fidelity PDF document design).

---

## 🛠️ Installation & Setup

Ensure Python 3.8+ is installed on your computer.

1. **Clone or copy the project files** to your local workspace:
   ```bash
   cd c:\Users\Saira\Desktop\AntiGravity-AI
   ```

2. **Install dependencies** using `pip`:
   ```bash
   pip install fastapi uvicorn pandas numpy statsmodels reportlab python-multipart
   ```

---

## 🚀 Running the Platform

To start the FastAPI server locally:

```bash
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Once started, open your web browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧪 Testing & Verification Guide

The codebase includes an automated programmatic verification test suite.

Run the test suite in your terminal to verify OLS mathematical calculations, CSV loading safety checks, and PDF report creation:

```bash
python verify_fama_analysis.py
```

*Expected Terminal Output:*
```text
====================================================
FAMA AI - Programmatic Verification Test Suite
====================================================
Checking sample datasets...
OK: Sample CSV files verified.

Testing CSV Loader on backend\sample_data\infosys.csv...
OK: CSV loaded successfully. Dimensions: (24, 5)

Testing OLS Regression Engine...
OK: OLS regression completed successfully.
Observations: 24
R-squared: 0.9573
  - Alpha: Coefficient=0.0002, p-val=0.9152, significant=False
  - Market: Coefficient=0.9536, p-val=0.0000, significant=True
  - SMB: Coefficient=-0.3921, p-val=0.0004, significant=True
  - HML: Coefficient=-0.5222, p-val=0.0000, significant=True

Testing ReportLab PDF Generator...
OK: PDF generated in-memory. Size: 5173 bytes.

====================================================
ALL TESTS COMPLETED SUCCESSFULLY!
====================================================
```

---

## 🔌 API Documentation

| Endpoint | Method | Description | Payload / Response |
| :--- | :--- | :--- | :--- |
| `/api/stocks` | `GET` | List pre-configured sample NIFTY 50 stocks. | `Response: [{"id": "infosys", "name": "Infosys Limited"}]` |
| `/api/fama-analysis/{symbol}` | `GET` | Perform OLS regression on pre-configured stock dataset. | `Response: { stock_name: str, results: {...}, data: [...] }` |
| `/api/fama-analysis/upload` | `POST` | Upload and analyze a custom CSV factor dataset. | `Payload: Multipart Form-Data (file)`<br>`Response: { stock_name: str, results: {...}, data: [...] }` |
| `/api/reports/export` | `POST` | Generate and export PDF academic report (stateless). | `Payload: JSON { stock_name: str, results: {...} }`<br>`Response: Binary PDF stream` |

---

## 📂 Project Structure

```text
c:/Users/Saira/Desktop/AntiGravity-AI/
├── backend/
│   ├── main.py                     # FastAPI entrypoint, routes, & mounts
│   ├── sample_data/
│   │   ├── infosys.csv             # Synthetic 24-month factor data (Infosys)
│   │   └── tata_motors.csv         # Synthetic 24-month factor data (Tata Motors)
│   ├── services/
│   │   └── regression_service.py   # Statsmodels OLS regression calculations
│   ├── utils/
│   │   ├── csv_loader.py           # Validates and cleans CSV files
│   │   └── pdf_generator.py        # Generates PDF report layouts
│   └── static/                     # Frontend Single Page App (React/Tailwind)
│       ├── index.html              # HTML shell loading CDN packages
│       ├── css/
│       │   └── styles.css          # Design system & dark glassmorphic styles
│       └── js/
│           ├── app.js              # State management & Plotly configurations
│           └── components.js       # React design widgets
├── verify_fama_analysis.py         # OLS and PDF test suite
└── README.md                       # Documentation & presentation guide
```
