// ===============================
// IMPORTS (CDN STYLE SAFE)
// ===============================
import {
  Header,
  QuickGuide,
  HeroSection,
  StockSelector,
  UploadComponent,
  ResultsTable,
  ModelDiagnostics,
  InterpretationPanel,
  ExportReportButton,
  ModelComparisonPanel
} from "./components.js";

const React = window.React;
const ReactDOM = window.ReactDOM;
const Plotly = window.Plotly;
const {
  useState,
  useEffect,
  useRef
} = React;


// ===============================
// CHART 1 - EXCESS RETURN TREND
// ===============================
function ExcessReturnTrendChart({ rawData }) {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current || !rawData || rawData.length === 0) return;

    const dates = rawData.map(d => d.Date);
    const riRf = rawData.map(d => d.Ri_Rf);
    const rmRf = rawData.map(d => d.Rm_Rf);

    const traces = [
      {
        x: dates,
        y: riRf,
        name: "Stock Excess Return",
        type: "scatter",
        mode: "lines+markers",
        line: { color: "#6366f1", width: 2.5 },
        marker: { size: 5, color: "#818cf8" },
        fill: "tozeroy",
        fillcolor: "rgba(99, 102, 241, 0.05)"
      },
      {
        x: dates,
        y: rmRf,
        name: "Market Excess Return",
        type: "scatter",
        mode: "lines",
        line: { color: "#06b6d4", width: 1.5, dash: "dash" }
      }
    ];

    Plotly.newPlot(chartRef.current, traces, {
      paper_bgcolor: "transparent",
      plot_bgcolor: "transparent",
      margin: { t: 20, l: 40, r: 20, b: 40 },
      font: { color: "#94a3b8", family: "Inter, sans-serif" },
      hovermode: "x unified",
      xaxis: {
        gridcolor: "#1e293b",
        tickcolor: "#334155",
        zeroline: false,
        rangeslider: { visible: true },
        type: "date"
      },
      yaxis: {
        gridcolor: "#1e293b",
        tickcolor: "#334155",
        zerolinecolor: "#475569"
      },
      legend: {
        orientation: "h",
        yanchor: "bottom",
        y: 1.02,
        xanchor: "right",
        x: 1
      }
    }, { responsive: true, displayModeBar: false });
  }, [rawData]);

  return React.createElement("div", { ref: chartRef, className: "w-full h-80" });
}


// ===============================
// CHART 2 - FACTOR EXPOSURE
// ===============================
function FactorExposureChart({ factors }) {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current || !factors) return;

    const values = [
      factors.Market.coefficient,
      factors.SMB.coefficient,
      factors.HML.coefficient
    ];

    Plotly.newPlot(chartRef.current, [{
      x: ["Market Sensitivity (Rm-Rf)", "Size Sensitivity (SMB)", "Style Sensitivity (HML)"],
      y: values,
      type: "bar",
      marker: { 
        color: ["#6366f1", "#06b6d4", "#10b981"],
        line: { color: "rgba(255,255,255,0.05)", width: 1 }
      },
      text: values.map(v => v.toFixed(3)),
      textposition: "outside",
      textfont: { color: "#f3f4f6", family: "Fira Code, monospace" }
    }], {
      paper_bgcolor: "transparent",
      plot_bgcolor: "transparent",
      font: { color: "#94a3b8", family: "Inter, sans-serif" },
      margin: { t: 25, l: 40, r: 20, b: 30 },
      xaxis: { gridcolor: "transparent" },
      yaxis: { gridcolor: "#1e293b", zerolinecolor: "#475569" }
    }, { responsive: true, displayModeBar: false });

  }, [factors]);

  return React.createElement("div", { ref: chartRef, className: "w-full h-80" });
}


// ===============================
// CHART 3 - P VALUE CHART
// ===============================
function PValueComparisonChart({ factors }) {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current || !factors) return;

    const pvals = [
      factors.Market.p_value,
      factors.SMB.p_value,
      factors.HML.p_value
    ];

    const colors = pvals.map(p => p < 0.05 ? "#10b981" : "#64748b");

    Plotly.newPlot(chartRef.current, [{
      x: ["Market (Rm-Rf)", "Size (SMB)", "Style (HML)"],
      y: pvals,
      type: "bar",
      marker: { color: colors },
      text: pvals.map(p => p.toFixed(4)),
      textposition: "outside",
      textfont: { color: "#f3f4f6", family: "Fira Code, monospace" }
    }], {
      paper_bgcolor: "transparent",
      plot_bgcolor: "transparent",
      font: { color: "#94a3b8", family: "Inter, sans-serif" },
      margin: { t: 30, l: 40, r: 20, b: 30 },
      xaxis: { gridcolor: "transparent" },
      yaxis: { 
        gridcolor: "#1e293b", 
        zerolinecolor: "#475569",
        range: [0, Math.max(0.1, ...pvals) * 1.15]
      },
      shapes: [{
        type: "line",
        x0: 0,
        x1: 1,
        y0: 0.05,
        y1: 0.05,
        xref: "paper",
        yref: "y",
        line: { color: "#ef4444", width: 1.5, dash: "dash" }
      }]
    }, { responsive: true, displayModeBar: false });

  }, [factors]);

  return React.createElement("div", { ref: chartRef, className: "w-full h-80" });
}


// ===============================
// MAIN APP
// ===============================
function App() {

  const [stocks, setStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState("");
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showUpload, setShowUpload] = useState(false);


  // Load stocks
  useEffect(() => {
    fetch("/api/stocks")
      .then(res => {
        if (!res.ok) {
          throw new Error("Failed to retrieve pre-configured stocks list.");
        }
        return res.json();
      })
      .then(data => {
        if (Array.isArray(data)) {
          setStocks(data);
          if (data.length > 0) {
            handleStockChange(data[0].id);
          }
        } else {
          throw new Error("Received invalid format for stocks list.");
        }
      })
      .catch(err => setError(err.message));
  }, []);


  const handleStockChange = async (id) => {
    if (id === "upload") {
      setShowUpload(true);
      return;
    }

    setSelectedStock(id);
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`/api/fama-analysis/${id}`);
      const data = await res.json();
      setCurrentAnalysis(data);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };


  const handleUploadSuccess = (data) => {
    setCurrentAnalysis(data);
    setSelectedStock("");
    setShowUpload(false);
  };


  return React.createElement("div", { className: "bg-slate-950 min-h-screen text-white" },
    React.createElement(HeroSection),
    React.createElement("div", { id: "main-dashboard", className: "min-h-screen px-4 md:px-8 py-6 max-w-7xl mx-auto flex flex-col text-white" },

      React.createElement(Header),
      React.createElement(QuickGuide),

      error && React.createElement("div", { className: "bg-red-500/20 p-3 rounded mb-4 text-sm border border-red-500/30 text-red-200" }, error),

      React.createElement(StockSelector, {
        stocks,
        selectedStock,
        onSelect: handleStockChange,
        onUploadClick: () => setShowUpload(true)
      }),

      loading ? React.createElement("div", { className: "flex-1 flex flex-col items-center justify-center py-20 gap-4" },
        React.createElement("svg", { className: "w-10 h-10 text-indigo-500 animate-spin", fill: "none", viewBox: "0 0 24 24" },
          React.createElement("circle", { className: "opacity-25", cx: "12", cy: "12", r: "10", stroke: "currentColor", strokeWidth: "4" }),
          React.createElement("path", { className: "opacity-75", fill: "currentColor", d: "M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" })
        ),
        React.createElement("p", { className: "text-gray-400 font-semibold text-sm" }, "Running OLS Regression Analysis...")
      ) : currentAnalysis && React.createElement("div", { className: "space-y-6 animate-fade-in" },
        
        // Stock title banner card
        React.createElement("div", { className: "glass-panel p-5 border border-gray-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4" },
          React.createElement("div", {},
            React.createElement("span", { className: "text-[10px] font-bold text-indigo-400 uppercase tracking-widest bg-indigo-500/10 px-2.5 py-1 rounded-full border border-indigo-500/20" }, "Active Analysis Target"),
            React.createElement("h2", { className: "text-2xl font-extrabold text-white mt-1.5 tracking-tight" }, currentAnalysis.stock_name)
          ),
          React.createElement(ExportReportButton, { 
            stockName: currentAnalysis.stock_name,
            results: currentAnalysis.results
          })
        ),

        // Beginner-friendly Card diagnostics
        React.createElement(ModelDiagnostics, { results: currentAnalysis.results }),

        // Grid Row: Results Table & Explanations side-by-side
        React.createElement("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6" },
          React.createElement("div", { className: "lg:col-span-2 flex flex-col justify-between" },
            React.createElement(ResultsTable, { results: currentAnalysis.results }),
            
            React.createElement("div", { className: "glass-panel p-6 border border-gray-800/80 shadow-xl flex-1 flex flex-col justify-between" },
              React.createElement("h3", { className: "text-sm font-semibold text-gray-200 uppercase tracking-wider mb-4 flex items-center gap-2" },
                React.createElement("span", { className: "w-1.5 h-3 bg-indigo-500 rounded-full" }),
                " Stock Excess Return Trend (Ri - Rf)"
              ),
              React.createElement(ExcessReturnTrendChart, { rawData: currentAnalysis.data })
            )
          ),
          React.createElement("div", {},
            React.createElement(InterpretationPanel, { results: currentAnalysis.results })
          )
        ),

        // ML Model Comparison Panel (Full width)
        React.createElement(ModelComparisonPanel, { results: currentAnalysis.results }),

        // Grid Row: Bar exposure charts side-by-side (No blank columns!)
        React.createElement("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6" },
          React.createElement("div", { className: "glass-panel p-6 border border-gray-800/80 shadow-xl" },
            React.createElement("h3", { className: "text-sm font-semibold text-gray-200 uppercase tracking-wider mb-4 flex items-center gap-2" },
              React.createElement("span", { className: "w-1.5 h-3 bg-indigo-500 rounded-full" }),
              " Factor Exposure Strength (Beta Loading)"
            ),
            React.createElement(FactorExposureChart, { factors: currentAnalysis.results.factors })
          ),
          React.createElement("div", { className: "glass-panel p-6 border border-gray-800/80 shadow-xl" },
            React.createElement("h3", { className: "text-sm font-semibold text-gray-200 uppercase tracking-wider mb-2 flex items-center gap-2" },
              React.createElement("span", { className: "w-1.5 h-3 bg-indigo-500 rounded-full" }),
              " Factor Significance (p-Value)"
            ),
            React.createElement("p", { className: "text-[11px] text-gray-500 mb-4" }, "Values below the red dashed line (p = 0.05) are statistically reliable."),
            React.createElement(PValueComparisonChart, { factors: currentAnalysis.results.factors })
          )
        )
      ),

      React.createElement("footer", { className: "mt-12 py-6 border-t border-gray-900 text-center text-xs text-gray-600" },
        React.createElement("p", {}, "© 2026 FAMA AI Platform. Built for MBA + BTech Academic Research & Presentation.")
      ),

      showUpload && React.createElement(UploadComponent, {
        onUploadSuccess: handleUploadSuccess,
        onClose: () => setShowUpload(false)
      })
    )
  );

}


// ===============================
// SAFE RENDER (FIXED)
// ===============================
const rootEl = document.getElementById("root");

if (rootEl) {
  const root = ReactDOM.createRoot(rootEl);
  root.render(React.createElement(App));
}
