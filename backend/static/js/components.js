const React = window.React;
const { useState, useEffect } = React;

// SVG Icons
const Icons = {
  Check: ({ className = "w-5 h-5" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
      React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M5 13l4 4L19 7" })
    )
  ),
  Alert: ({ className = "w-5 h-5" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
      React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" })
    )
  ),
  Download: ({ className = "w-5 h-5" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
      React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" })
    )
  ),
  Upload: ({ className = "w-5 h-5" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
      React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" })
    )
  ),
  Database: ({ className = "w-5 h-5" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
      React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" })
    )
  ),
  Trend: ({ className = "w-5 h-5" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
      React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" })
    )
  ),
  Info: ({ className = "w-4 h-4" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
      React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" })
    )
  ),
  Loader: ({ className = "w-5 h-5 animate-spin" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24" },
      React.createElement("circle", { className: "opacity-25", cx: "12", cy: "12", r: "10", stroke: "currentColor", strokeWidth: "4" }),
      React.createElement("path", { className: "opacity-75", fill: "currentColor", d: "M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" })
    )
  ),
  Academic: ({ className = "w-5 h-5" }) => (
    React.createElement("svg", { className, fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
      React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" })
    )
  )
};

// Tooltip helper component
function HelpTooltip({ text }) {
  const [visible, setVisible] = useState(false);
  return React.createElement("span", { className: "relative inline-block ml-1 cursor-help group text-gray-500 hover:text-indigo-400" },
    React.createElement("span", { 
      onMouseEnter: () => setVisible(true), 
      onMouseLeave: () => setVisible(false),
      className: "inline-flex items-center justify-center w-3.5 h-3.5 text-[10px] font-bold border border-gray-500 rounded-full" 
    }, "?"),
    visible && React.createElement("span", { 
      className: "absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2 text-xs bg-slate-900 border border-gray-800 text-gray-300 rounded shadow-xl z-50 leading-relaxed font-normal" 
    }, text)
  );
}

// 1. Header Component
export function Header() {
  return React.createElement("header", { className: "glass-panel px-6 py-4 flex items-center justify-between shadow-xl mb-6 border-b border-gray-800 animate-fade-in" },
    React.createElement("div", { className: "flex items-center gap-3" },
      React.createElement("div", { className: "bg-gradient-to-tr from-indigo-500 to-cyan-400 p-2.5 rounded-lg shadow-lg shadow-indigo-500/20" },
        React.createElement(Icons.Academic, { className: "w-6 h-6 text-slate-900" })
      ),
      React.createElement("div", {},
        React.createElement("h1", { className: "text-xl font-bold tracking-tight text-white flex items-center gap-2" },
          "FAMA AI ",
          React.createElement("span", { className: "text-xs bg-indigo-500/20 text-indigo-400 px-2 py-0.5 rounded font-mono font-medium border border-indigo-500/30" }, "V1.0")
        ),
        React.createElement("p", { className: "text-xs text-gray-400" }, "Fama-French 3-Factor Stock Analysis Platform")
      )
    ),
    React.createElement("div", { className: "flex items-center gap-4" },
      React.createElement("div", { className: "hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/50 border border-gray-800 text-xs" },
        React.createElement("span", { className: "w-2 h-2 rounded-full bg-emerald-500 animate-pulse" }),
        React.createElement("span", { className: "text-gray-400 font-medium font-mono" }, "OLS Engine: Active")
      )
    )
  );
}

// 1.5 Quick Start Tutorial Guide (Togglable)
export function QuickGuide() {
  const [open, setOpen] = useState(false);

  return React.createElement("div", { className: "glass-panel p-4 border border-gray-800/80 mb-6 shadow-xl animate-fade-in card-gradient-overlay" },
    React.createElement("div", { className: "flex justify-between items-center cursor-pointer select-none", onClick: () => setOpen(!open) },
      React.createElement("h4", { className: "text-xs font-bold text-indigo-400 uppercase tracking-widest flex items-center gap-2" },
        React.createElement("span", { className: "w-2 h-2 rounded-full bg-indigo-500 animate-pulse" }),
        "💡 Quick Operating Guide (Click to toggle)"
      ),
      React.createElement("span", { className: "text-xs text-gray-500 font-bold font-mono" }, open ? "Collapse [-]" : "Expand [+]")
    ),
    open && React.createElement("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 border-t border-gray-900 pt-4 text-xs animate-slide-up" },
      React.createElement("div", { className: "p-3.5 bg-slate-950/40 rounded-xl border border-gray-900" },
        React.createElement("div", { className: "font-semibold text-gray-200 mb-1 flex items-center gap-1.5" },
          React.createElement("span", { className: "w-4.5 h-4.5 bg-indigo-500/20 text-indigo-400 rounded-full flex items-center justify-center font-bold text-[10px]" }, "1"),
          "Select target stock"
        ),
        React.createElement("p", { className: "text-gray-400 leading-relaxed font-normal" },
          "Choose pre-loaded NIFTY 50 data (Infosys, Tata Motors) or click the upload button to parse your custom factor dataset CSV."
        )
      ),
      React.createElement("div", { className: "p-3.5 bg-slate-950/40 rounded-xl border border-gray-900" },
        React.createElement("div", { className: "font-semibold text-gray-200 mb-1 flex items-center gap-1.5" },
          React.createElement("span", { className: "w-4.5 h-4.5 bg-indigo-500/20 text-indigo-400 rounded-full flex items-center justify-center font-bold text-[10px]" }, "2"),
          "Analyze factor tags"
        ),
        React.createElement("p", { className: "text-gray-400 leading-relaxed font-normal" },
          "Look at the top horizontal cards to instantly understand if the stock behaves as defensive/aggressive, growth/value, or mega/small cap."
        )
      ),
      React.createElement("div", { className: "p-3.5 bg-slate-950/40 rounded-xl border border-gray-900" },
        React.createElement("div", { className: "font-semibold text-gray-200 mb-1 flex items-center gap-1.5" },
          React.createElement("span", { className: "w-4.5 h-4.5 bg-indigo-500/20 text-indigo-400 rounded-full flex items-center justify-center font-bold text-[10px]" }, "3"),
          "Hover over (?) symbols"
        ),
        React.createElement("p", { className: "text-gray-400 leading-relaxed font-normal" },
          "Confused by terms like R-squared, t-Stat, or p-Value? Hover your cursor over any question mark for a simple definition."
        )
      )
    )
  );
}

// 1.8 Hero Landing Page Component
export function HeroSection() {
  const [text, setText] = useState("");
  const [wordIndex, setWordIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const words = [
    "Fama-French Smart Analytics Platform",
    "Automated 3-Factor OLS Regression Engine",
    "Vibrant Plotly Financial Visualizations",
    "MBA + BTech Academic Project Excellence"
  ];

  const [animIndex, setAnimIndex] = useState(0);
  const [animKey, setAnimKey] = useState(0);

  useEffect(() => {
    const sequence = [
      { text: "F", isFull: false, duration: 250 },
      { text: "A", isFull: false, duration: 250 },
      { text: "M", isFull: false, duration: 250 },
      { text: "A", isFull: false, duration: 250 },
      { text: "A", isFull: false, duration: 250 },
      { text: "I", isFull: false, duration: 250 },
      { text: "FAMA AI", isFull: true, duration: 1800 }
    ];

    const currentStep = sequence[animIndex];
    const timer = setTimeout(() => {
      setAnimIndex((prev) => (prev + 1) % sequence.length);
      setAnimKey((prev) => prev + 1);
    }, currentStep.duration);

    return () => clearTimeout(timer);
  }, [animIndex]);

  useEffect(() => {
    let timer;
    const currentWord = words[wordIndex];
    
    const tick = () => {
      if (!isDeleting) {
        setText(currentWord.substring(0, text.length + 1));
        if (text.length + 1 === currentWord.length) {
          timer = setTimeout(() => setIsDeleting(true), 2500);
          return;
        }
      } else {
        setText(currentWord.substring(0, text.length - 1));
        if (text.length - 1 === 0) {
          setIsDeleting(false);
          setWordIndex((wordIndex + 1) % words.length);
          timer = setTimeout(() => {}, 500);
          return;
        }
      }
      
      const speed = isDeleting ? 30 : 60;
      timer = setTimeout(tick, speed);
    };
    
    timer = setTimeout(tick, 100);
    return () => clearTimeout(timer);
  }, [text, isDeleting, wordIndex]);

  const handleScrollDown = () => {
    const mainSection = document.getElementById("main-dashboard");
    if (mainSection) {
      mainSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  return React.createElement("div", { className: "relative min-h-screen flex flex-col justify-center items-center px-4 overflow-hidden border-b border-gray-950 bg-slate-950" },
    React.createElement("div", { className: "bg-gradient-orb" }),
    React.createElement("div", { className: "relative z-10 text-center max-w-4xl flex flex-col items-center gap-6" },
      React.createElement("div", { className: "bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-[10px] font-bold tracking-[0.25em] px-4 py-1.5 rounded-full uppercase mb-2 animate-fade-in" },
        "Academic equity research platform"
      ),
      React.createElement("div", { className: "title-container-fixed mb-2" },
        React.createElement("h1", {
          key: animKey,
          className: animIndex === 6
            ? "text-6xl sm:text-8xl font-black tracking-wider word-glow-in"
            : "text-7xl sm:text-9xl font-black letter-zoom-fade text-white drop-shadow-[0_0_20px_rgba(99,102,241,0.35)]"
        },
          animIndex === 6 ? "FAMA AI" : ["F", "A", "M", "A", "A", "I"][animIndex]
        )
      ),
      React.createElement("div", { className: "h-16 flex items-center justify-center" },
        React.createElement("h2", { className: "text-lg sm:text-2xl font-medium text-gray-300 font-mono tracking-tight" },
          text,
          React.createElement("span", { className: "cursor-blink text-indigo-400 ml-1 font-sans font-bold" }, "|")
        )
      ),
      React.createElement("p", { className: "text-xs sm:text-sm text-gray-500 max-w-xl leading-relaxed font-normal animate-slide-up mt-2" },
        "Analyze NIFTY 50 equities using the Fama-French 3-Factor pricing model. Built using FastAPI, Statsmodels OLS, React, and Plotly.js for academic evaluations and quantitative presentations."
      ),
      React.createElement("div", { className: "mt-12 animate-slide-up" },
        React.createElement("button", {
          onClick: handleScrollDown,
          className: "bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white font-semibold px-8 py-3.5 rounded-xl text-sm shadow-xl shadow-indigo-950/40 border border-indigo-500/20 transition-all hover:scale-105 active:scale-95 flex items-center gap-2"
        },
          "Launch Analytics Dashboard",
          React.createElement("svg", { className: "w-4 h-4", fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
            React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M14 5l7 7m0 0l-7 7m7-7H3" })
          )
        )
      )
    ),
    React.createElement("div", { className: "absolute bottom-8 left-1/2 -translate-x-1/2 cursor-pointer flex flex-col items-center gap-1.5 text-gray-600 hover:text-indigo-400 transition-colors select-none animate-bounce-slow", onClick: handleScrollDown },
      React.createElement("span", { className: "text-[10px] font-bold uppercase tracking-widest font-mono" }, "Scroll Down"),
      React.createElement("svg", { className: "w-5 h-5", fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2.5" },
        React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M19 14l-7 7m0 0l-7-7m7 7V3" })
      )
    )
  );
}


// 2. Stock Selection Panel
export function StockSelector({ stocks, selectedStock, onSelect, onUploadClick }) {
  return React.createElement("div", { className: "glass-panel p-6 shadow-xl border border-gray-800/80 mb-6 animate-slide-up" },
    React.createElement("h3", { className: "text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4 flex items-center gap-2" },
      React.createElement(Icons.Database, { className: "w-4 h-4 text-indigo-400" }),
      " Select Analysis Target"
    ),
    React.createElement("div", { className: "flex flex-col sm:flex-row gap-4 items-stretch sm:items-center" },
      React.createElement("div", { className: "flex-1 relative" },
        React.createElement("select", {
          value: selectedStock || "",
          onChange: (e) => onSelect(e.target.value),
          className: "w-full bg-slate-950 text-gray-200 border border-gray-800 rounded-lg py-2.5 px-4 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 cursor-pointer text-sm font-medium transition-all"
        },
          React.createElement("option", { value: "", disabled: true }, "-- Select a NIFTY 50 Stock --"),
          stocks.map((stock) => React.createElement("option", { key: stock.id, value: stock.id }, stock.name)),
          React.createElement("option", { value: "upload" }, "Upload Custom Factor Dataset (.csv, .xlsx)")
        )
      ),
      React.createElement("button", {
        onClick: onUploadClick,
        className: "flex items-center justify-center gap-2 bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white font-medium px-5 py-2.5 rounded-lg text-sm shadow-lg shadow-indigo-600/10 transition-all active:scale-95 border border-indigo-500/20"
      },
        React.createElement(Icons.Upload, { className: "w-4 h-4" }),
        " Upload Custom CSV"
      )
    )
  );
}

// 3. CSV Uploader Component
export function UploadComponent({ onUploadSuccess, onClose }) {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const processFile = async (file) => {
    if (!file) return;
    const isCsv = file.name.endsWith(".csv");
    const isExcel = file.name.endsWith(".xlsx") || file.name.endsWith(".xls");
    if (!isCsv && !isExcel) {
      setError("Only CSV and Excel (.xlsx, .xls) files are accepted.");
      return;
    }
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/fama-analysis/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Error analyzing uploaded file.");
      }

      const data = await response.json();
      onUploadSuccess(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  return React.createElement("div", { className: "fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in" },
    React.createElement("div", { className: "glass-panel w-full max-w-lg overflow-hidden border border-gray-800 shadow-2xl animate-slide-up" },
      React.createElement("div", { className: "px-6 py-4 bg-slate-900 border-b border-gray-800 flex items-center justify-between" },
        React.createElement("h3", { className: "text-base font-bold text-white flex items-center gap-2" },
          React.createElement(Icons.Upload, { className: "w-5 h-5 text-indigo-400" }),
          " Upload Factor Dataset"
        ),
        React.createElement("button", { 
          onClick: onClose,
          className: "text-gray-400 hover:text-white transition-colors p-1 hover:bg-slate-800 rounded"
        },
          React.createElement("svg", { className: "w-5 h-5", fill: "none", viewBox: "0 0 24 24", stroke: "currentColor" },
            React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", strokeWidth: "2", d: "M6 18L18 6M6 6l12 12" })
          )
        )
      ),
      React.createElement("div", { className: "p-6" },
        React.createElement("div", {
          onDragEnter: handleDrag,
          onDragOver: handleDrag,
          onDragLeave: handleDrag,
          onDrop: handleDrop,
          className: `border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-all ${
            dragActive 
              ? "border-indigo-500 bg-indigo-500/5" 
              : "border-gray-800 bg-slate-950/30 hover:border-gray-700 hover:bg-slate-950/50"
          }`,
          onClick: () => document.getElementById("file-upload").click()
        },
          React.createElement("input", { 
            id: "file-upload", 
            type: "file", 
            accept: ".csv, .xlsx, .xls", 
            className: "hidden", 
            onChange: handleFileChange,
            disabled: loading
          }),
          loading ? React.createElement("div", { className: "flex flex-col items-center gap-3 py-4" },
            React.createElement(Icons.Loader, { className: "w-10 h-10 text-indigo-400" }),
            React.createElement("p", { className: "text-sm text-indigo-300 font-medium" }, "Running OLS Regression Analysis...")
          ) : React.createElement(React.Fragment, {},
            React.createElement("div", { className: "bg-indigo-500/10 p-4 rounded-full mb-4 text-indigo-400" },
              React.createElement(Icons.Upload, { className: "w-8 h-8" })
            ),
            React.createElement("h4", { className: "text-sm font-semibold text-gray-200 mb-1" }, "Drag and drop your CSV or Excel file here"),
            React.createElement("p", { className: "text-xs text-gray-400 mb-4" }, "or click to browse your local machine"),
            React.createElement("div", { className: "bg-slate-900 border border-gray-800 px-3 py-1.5 rounded text-[11px] text-gray-400 font-mono" },
              "Expected Columns: Date, Ri_Rf, Rm_Rf, SMB, HML"
            )
          )
        ),
        error && React.createElement("div", { className: "mt-4 p-3.5 bg-rose-500/10 border border-rose-500/20 text-rose-300 rounded-lg text-xs flex gap-2.5 items-start" },
          React.createElement("div", { className: "text-rose-400 mt-0.5" }, React.createElement(Icons.Alert, {})),
          React.createElement("div", {},
            React.createElement("p", { className: "font-semibold mb-0.5" }, "Upload Failed"),
            React.createElement("p", { className: "leading-relaxed" }, error)
          )
        ),
        React.createElement("div", { className: "mt-6 flex justify-end gap-3" },
          React.createElement("button", {
            onClick: onClose,
            className: "px-4 py-2 border border-gray-800 hover:bg-slate-900 hover:border-gray-700 text-gray-300 font-semibold rounded-lg text-xs transition-colors"
          }, "Cancel")
        )
      )
    )
  );
}

// 4. Beginner-Friendly Diagnostics (Metrics Card Strip)
export function ModelDiagnostics({ results }) {
  if (!results) return null;
  const { r_squared, factors } = results;

  const mktBeta = factors.Market.coefficient;
  const smbBeta = factors.SMB.coefficient;
  const hmlBeta = factors.HML.coefficient;

  // Derive simple badges
  const getMktBadge = (val) => {
    if (val > 1.1) return { text: "Aggressive Risk", style: "text-rose-400 bg-rose-500/10 border-rose-500/20" };
    if (val < 0.9) return { text: "Defensive / Low Risk", style: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20" };
    return { text: "Market Risk Match", style: "text-indigo-400 bg-indigo-500/10 border-indigo-500/20" };
  };

  const getCapBadge = (val) => {
    if (val > 0.15) return { text: "Small-Cap Stock", style: "text-orange-400 bg-orange-500/10 border-orange-500/20" };
    if (val < -0.15) return { text: "Large-Cap Giant", style: "text-blue-400 bg-blue-500/10 border-blue-500/20" };
    return { text: "Size Neutral", style: "text-gray-400 bg-gray-500/10 border-gray-800" };
  };

  const getStyleBadge = (val) => {
    if (val > 0.15) return { text: "Value stock (Undervalued)", style: "text-amber-400 bg-amber-500/10 border-amber-500/20" };
    if (val < -0.15) return { text: "Growth stock (Premium)", style: "text-fuchsia-400 bg-fuchsia-500/10 border-fuchsia-500/20" };
    return { text: "Blend Stock Style", style: "text-gray-400 bg-gray-500/10 border-gray-800" };
  };

  const getReliability = (val) => {
    if (val > 0.85) return { text: "Highly Reliable", style: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20" };
    if (val >= 0.50) return { text: "Moderate Fit", style: "text-amber-400 bg-amber-500/10 border-amber-500/20" };
    return { text: "Low Explanatory Power", style: "text-rose-400 bg-rose-500/10 border-rose-500/20" };
  };

  const mkt = getMktBadge(mktBeta);
  const cap = getCapBadge(smbBeta);
  const style = getStyleBadge(hmlBeta);
  const rel = getReliability(r_squared);

  return React.createElement("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6 animate-slide-up" },
    // Card 1: Market Risk
    React.createElement("div", { className: "glass-panel p-4 border border-gray-800/80 flex flex-col justify-between" },
      React.createElement("div", {},
        React.createElement("div", { className: "flex justify-between items-center mb-1" },
          React.createElement("span", { className: "text-xs font-semibold text-gray-400 uppercase tracking-wider" }, "Market Beta"),
          React.createElement(HelpTooltip, { text: "Measures sensitivity to overall market index (NIFTY 50). Beta > 1 moves more than the market. Beta < 1 moves less." })
        ),
        React.createElement("h4", { className: "text-xl font-bold text-white font-mono" }, mktBeta.toFixed(2))
      ),
      React.createElement("div", { className: "mt-2" },
        React.createElement("span", { className: `text-[10px] font-bold px-2 py-0.5 rounded border ${mkt.style}` }, mkt.text)
      )
    ),
    // Card 2: Company Size
    React.createElement("div", { className: "glass-panel p-4 border border-gray-800/80 flex flex-col justify-between" },
      React.createElement("div", {},
        React.createElement("div", { className: "flex justify-between items-center mb-1" },
          React.createElement("span", { className: "text-xs font-semibold text-gray-400 uppercase tracking-wider" }, "Size Exposure (SMB)"),
          React.createElement(HelpTooltip, { text: "Positive SMB means the stock responds like a smaller-cap stock. Negative means it behaves like a large-cap stock." })
        ),
        React.createElement("h4", { className: "text-xl font-bold text-white font-mono" }, smbBeta.toFixed(2))
      ),
      React.createElement("div", { className: "mt-2" },
        React.createElement("span", { className: `text-[10px] font-bold px-2 py-0.5 rounded border ${cap.style}` }, cap.text)
      )
    ),
    // Card 3: Stock Style
    React.createElement("div", { className: "glass-panel p-4 border border-gray-800/80 flex flex-col justify-between" },
      React.createElement("div", {},
        React.createElement("div", { className: "flex justify-between items-center mb-1" },
          React.createElement("span", { className: "text-xs font-semibold text-gray-400 uppercase tracking-wider" }, "Value / Growth (HML)"),
          React.createElement(HelpTooltip, { text: "Positive HML means it is a value stock (cheap relative to book value). Negative HML means it is a growth stock (premium valuation)." })
        ),
        React.createElement("h4", { className: "text-xl font-bold text-white font-mono" }, hmlBeta.toFixed(2))
      ),
      React.createElement("div", { className: "mt-2" },
        React.createElement("span", { className: `text-[10px] font-bold px-2 py-0.5 rounded border ${style.style}` }, style.text)
      )
    ),
    // Card 4: Model Accuracy
    React.createElement("div", { className: "glass-panel p-4 border border-gray-800/80 flex flex-col justify-between" },
      React.createElement("div", {},
        React.createElement("div", { className: "flex justify-between items-center mb-1" },
          React.createElement("span", { className: "text-xs font-semibold text-gray-400 uppercase tracking-wider" }, "Model Explanatory (R²)"),
          React.createElement(HelpTooltip, { text: "R-squared shows what percentage of the stock's return movements is explained by these three Fama-French factors combined." })
        ),
        React.createElement("h4", { className: "text-xl font-bold text-white font-mono" }, `${(r_squared * 100).toFixed(1)}%`)
      ),
      React.createElement("div", { className: "mt-2" },
        React.createElement("span", { className: `text-[10px] font-bold px-2 py-0.5 rounded border ${rel.style}` }, rel.text)
      )
    )
  );
}

// 5. OLS Coefficients Table (with Tooltips)
export function ResultsTable({ results }) {
  if (!results) return null;
  const { factors } = results;

  const getPValueStyle = (val) => {
    if (val < 0.05) return "text-emerald-400 font-semibold";
    return "text-gray-400";
  };

  const getFactorLabel = (factorKey) => {
    return {
      "Alpha": "Alpha (Intercept)",
      "Market": "Market Factor (Rm - Rf)",
      "SMB": "Size Factor (SMB)",
      "HML": "Style Factor (HML)"
    }[factorKey] || factorKey;
  };

  return React.createElement("div", { className: "glass-panel overflow-hidden border border-gray-800/80 shadow-xl mb-6 animate-slide-up" },
    React.createElement("div", { className: "px-6 py-4 bg-slate-900/50 border-b border-gray-800 flex items-center justify-between" },
      React.createElement("h3", { className: "text-sm font-semibold text-gray-200 tracking-wide uppercase flex items-center gap-2" },
        React.createElement("span", { className: "w-1.5 h-3 bg-indigo-500 rounded-full" }),
        " Statistical Regression Results (OLS)"
      )
    ),
    React.createElement("div", { className: "overflow-x-auto text-xs sm:text-sm" },
      React.createElement("table", { className: "w-full text-left border-collapse styled-table" },
        React.createElement("thead", {},
          React.createElement("tr", { className: "border-b border-gray-800 bg-slate-950/40 text-gray-400 text-[11px] font-semibold uppercase tracking-wider" },
            React.createElement("th", { className: "py-3.5 px-5" }, 
              "Factor Name",
              React.createElement(HelpTooltip, { text: "The systemic market factor tested in the model." })
            ),
            React.createElement("th", { className: "py-3.5 px-5 text-right" }, 
              "Beta Coefficient",
              React.createElement(HelpTooltip, { text: "The slope or loading coefficient. A positive coefficient indicates direct sensitivity. Negative indicates inverse sensitivity." })
            ),
            React.createElement("th", { className: "py-3.5 px-5 text-right" }, 
              "t-Stat",
              React.createElement(HelpTooltip, { text: "The test statistic. Values below -2 or above +2 indicate that the coefficient is highly likely to be non-zero." })
            ),
            React.createElement("th", { className: "py-3.5 px-5 text-right" }, 
              "p-Value",
              React.createElement(HelpTooltip, { text: "The statistical probability of finding this result by chance. p-value < 0.05 means the relationship is highly reliable." })
            ),
            React.createElement("th", { className: "py-3.5 px-5 text-center" }, 
              "95% Confidence Interval",
              React.createElement(HelpTooltip, { text: "The range in which the true factor loading lies with 95% mathematical confidence." })
            ),
            React.createElement("th", { className: "py-3.5 px-5 text-center" }, 
              "Significant?",
              React.createElement(HelpTooltip, { text: "Reliable? Yes if p-value is less than 0.05, meaning this factor strongly affects this stock's performance." })
            )
          )
        ),
        React.createElement("tbody", { className: "divide-y divide-gray-800/50" },
          Object.keys(factors).map((key) => {
            const factor = factors[key];
            return React.createElement("tr", { key, className: "hover:bg-slate-900/25 transition-colors" },
              React.createElement("td", { className: "py-3.5 px-5 font-semibold text-gray-300" }, getFactorLabel(key)),
              React.createElement("td", { className: "py-3.5 px-5 text-right font-mono text-gray-100 font-semibold" }, factor.coefficient.toFixed(4)),
              React.createElement("td", { className: "py-3.5 px-5 text-right font-mono text-gray-300" }, factor.t_stat.toFixed(2)),
              React.createElement("td", { className: `py-3.5 px-5 text-right font-mono ${getPValueStyle(factor.p_value)}` }, factor.p_value.toFixed(4)),
              React.createElement("td", { className: "py-3.5 px-5 text-center font-mono text-gray-400" }, `[${factor.conf_lower.toFixed(4)}, ${factor.conf_upper.toFixed(4)}]`),
              React.createElement("td", { className: "py-3.5 px-5 text-center" },
                factor.significant 
                  ? React.createElement("span", { className: "inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" },
                      React.createElement("span", { className: "w-1.5 h-1.5 rounded-full bg-emerald-400" }),
                      " Reliable"
                    )
                  : React.createElement("span", { className: "inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium bg-gray-500/10 text-gray-400 border border-gray-800" },
                      React.createElement("span", { className: "w-1.5 h-1.5 rounded-full bg-gray-500" }),
                      " Unreliable"
                    )
              )
            );
          })
        )
      )
    )
  );
}

// 6. Interpretation Panel Component
export function InterpretationPanel({ results }) {
  if (!results) return null;
  const { interpretations, factors } = results;

  const getStyleTag = (key) => {
    if (key === "market") {
      const val = factors.Market.coefficient;
      if (val > 1.1) return { text: "Aggressive", color: "bg-rose-500/10 text-rose-400 border-rose-500/20" };
      if (val < 0.9) return { text: "Defensive", color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" };
      return { text: "Market Core", color: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20" };
    }
    if (key === "smb") {
      const val = factors.SMB.coefficient;
      if (val > 0.15) return { text: "Small-Cap Profile", color: "bg-orange-500/10 text-orange-400 border-orange-500/20" };
      if (val < -0.15) return { text: "Mega-Cap Giant", color: "bg-blue-500/10 text-blue-400 border-blue-500/20" };
      return { text: "Size Neutral", color: "bg-gray-500/10 text-gray-400 border-gray-800" };
    }
    if (key === "hml") {
      const val = factors.HML.coefficient;
      if (val > 0.15) return { text: "Value Style", color: "bg-amber-500/10 text-amber-400 border-amber-500/20" };
      if (val < -0.15) return { text: "Growth Style", color: "bg-fuchsia-500/10 text-fuchsia-400 border-fuchsia-500/20" };
      return { text: "Blend Style", color: "bg-gray-500/10 text-gray-400 border-gray-800" };
    }
    return { text: "Insight", color: "bg-gray-500/10 text-gray-400 border-gray-800" };
  };

  const getTitle = (key) => {
    return {
      "market": "Market Sensitivity (Beta)",
      "smb": "Company Size Exposure (SMB)",
      "hml": "Investment Style (HML)",
      "alpha": "Abnormal Outperformance (Alpha)",
      "r_squared": "Model Reliability (R²)"
    }[key] || key;
  };

  return React.createElement("div", { className: "glass-panel p-6 border border-gray-800/80 shadow-xl mb-6 animate-slide-up" },
    React.createElement("div", { className: "flex items-center gap-2 border-b border-gray-800 pb-4 mb-4" },
      React.createElement("div", { className: "text-indigo-400 bg-indigo-500/10 p-2 rounded-lg animate-pulse" },
        React.createElement(Icons.Trend, {})
      ),
      React.createElement("div", {},
        React.createElement("h3", { className: "text-sm font-bold text-white uppercase tracking-wider" }, "Fama-French Investment Insights"),
        React.createElement("p", { className: "text-xs text-gray-400" }, "Simplified translation of OLS statistical numbers")
      )
    ),
    React.createElement("div", { className: "space-y-4" },
      Object.keys(interpretations).map((key) => {
        const tag = getStyleTag(key);
        return React.createElement("div", { key, className: "p-4 bg-slate-950/40 border border-gray-900 rounded-xl hover:border-gray-800 transition-colors" },
          React.createElement("div", { className: "flex flex-wrap items-center justify-between gap-2 mb-2" },
            React.createElement("span", { className: "text-xs font-semibold text-gray-300 tracking-wide" }, getTitle(key)),
            React.createElement("span", { className: `text-[10px] font-bold px-2 py-0.5 rounded border ${tag.color}` }, tag.text)
          ),
          React.createElement("p", { className: "text-xs sm:text-sm text-gray-400 leading-relaxed font-normal" }, interpretations[key])
        );
      })
    )
  );
}

// 7. Report Export Component
export function ExportReportButton({ stockName, results }) {
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    if (!results || exporting) return;
    setExporting(true);

    try {
      const response = await fetch("/api/reports/export", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          stock_name: stockName,
          results: results,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to download PDF report");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Fama_French_Report_${stockName.replace(/\s+/g, "_")}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      alert(`Export Failed: ${err.message}`);
    } finally {
      setExporting(false);
    }
  };

  return React.createElement("button", {
    onClick: handleExport,
    disabled: exporting,
    className: "flex items-center justify-center gap-2 bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 disabled:from-emerald-800 disabled:to-emerald-900 disabled:cursor-not-allowed text-white font-semibold px-5 py-2.5 rounded-lg text-sm shadow-xl shadow-emerald-950/20 border border-emerald-500/10 transition-all active:scale-95 w-full sm:w-auto pulse-glow-emerald"
  },
    exporting ? React.createElement(React.Fragment, {}, 
      React.createElement(Icons.Loader, { className: "w-4 h-4 text-white" }), 
      " Creating PDF..."
    ) : React.createElement(React.Fragment, {}, 
      React.createElement(Icons.Download, { className: "w-4 h-4" }), 
      " Download PDF Report"
    )
  );
}

// 8. ML Model Comparison Component
export function ModelComparisonPanel({ results }) {
  const chartRef = React.useRef(null);

  React.useEffect(() => {
    if (!chartRef.current || !results || !results.model_comparison) return;

    const models = Object.keys(results.model_comparison);
    const r2Values = models.map(m => results.model_comparison[m].r2);
    const rmseValues = models.map(m => results.model_comparison[m].rmse);

    const traces = [
      {
        x: models,
        y: r2Values,
        name: "R-squared Score (R²)",
        type: "bar",
        marker: { color: "#6366f1" },
        text: r2Values.map(v => v.toFixed(4)),
        textposition: "outside",
        textfont: { color: "#f3f4f6", family: "Fira Code, monospace", size: 10 }
      },
      {
        x: models,
        y: rmseValues,
        name: "Root Mean Squared Error (RMSE)",
        type: "bar",
        marker: { color: "#ec4899" },
        text: rmseValues.map(v => v.toFixed(4)),
        textposition: "outside",
        textfont: { color: "#f3f4f6", family: "Fira Code, monospace", size: 10 }
      }
    ];

    Plotly.newPlot(chartRef.current, traces, {
      paper_bgcolor: "transparent",
      plot_bgcolor: "transparent",
      font: { color: "#94a3b8", family: "Inter, sans-serif" },
      margin: { t: 30, l: 40, r: 20, b: 30 },
      xaxis: { gridcolor: "transparent" },
      yaxis: { gridcolor: "#1e293b", zerolinecolor: "#475569" },
      legend: {
        orientation: "h",
        yanchor: "bottom",
        y: 1.05,
        xanchor: "right",
        x: 1
      },
      barmode: "group"
    }, { responsive: true, displayModeBar: false });

  }, [results]);

  if (!results || !results.model_comparison) return null;

  const comparison = results.model_comparison;

  return React.createElement("div", { className: "glass-panel p-6 border border-gray-800/80 shadow-xl mb-6 animate-slide-up" },
    React.createElement("div", { className: "flex items-center gap-2 border-b border-gray-800 pb-4 mb-4" },
      React.createElement("div", { className: "text-indigo-400 bg-indigo-500/10 p-2 rounded-lg" },
        React.createElement("svg", { className: "w-5 h-5", fill: "none", viewBox: "0 0 24 24", stroke: "currentColor", strokeWidth: "2" },
          React.createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z" })
        )
      ),
      React.createElement("div", {},
        React.createElement("h3", { className: "text-sm font-bold text-white uppercase tracking-wider" }, "Machine Learning Model Comparison"),
        React.createElement("p", { className: "text-xs text-gray-400" }, "Compare Fama-French baseline against standard ML regression models")
      )
    ),
    React.createElement("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6" },
      React.createElement("div", { className: "lg:col-span-1 overflow-x-auto" },
        React.createElement("table", { className: "w-full text-left border-collapse" },
          React.createElement("thead", {},
            React.createElement("tr", { className: "border-b border-gray-800 text-[10px] uppercase font-bold text-gray-500 tracking-wider" },
              React.createElement("th", { className: "pb-2" }, "Model"),
              React.createElement("th", { className: "pb-2 text-right" }, "R² Score"),
              React.createElement("th", { className: "pb-2 text-right" }, "RMSE")
            )
          ),
          React.createElement("tbody", { className: "divide-y divide-gray-900 text-xs" },
            Object.keys(comparison).map((modelName) => {
              const model = comparison[modelName];
              const isSuccess = model.status === "Success";
              return React.createElement("tr", { key: modelName, className: "hover:bg-slate-900/30 transition-colors" },
                React.createElement("td", { className: "py-3 font-semibold text-gray-200" }, 
                  modelName,
                  !isSuccess && React.createElement("span", { className: "block text-[9px] text-yellow-500 font-normal mt-0.5" }, model.status)
                ),
                React.createElement("td", { className: "py-3 text-right font-mono font-bold text-indigo-400" }, 
                  isSuccess ? model.r2.toFixed(4) : "—"
                ),
                React.createElement("td", { className: "py-3 text-right font-mono text-pink-400" }, 
                  isSuccess ? model.rmse.toFixed(4) : "—"
                )
              );
            })
          )
        )
      ),
      React.createElement("div", { className: "lg:col-span-2 flex flex-col justify-center bg-slate-950/40 border border-gray-900 rounded-xl p-4" },
        React.createElement("div", { ref: chartRef, className: "w-full h-64" })
      )
    )
  );
}

