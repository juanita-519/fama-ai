import numpy as np
import pandas as pd
import statsmodels.api as sm
from typing import Dict, Any

def run_fama_french_regression(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs Fama-French 3-Factor OLS regression.
    Formula: Ri_Rf = Alpha + Beta1*(Rm_Rf) + Beta2*(SMB) + Beta3*(HML)
    
    Parameters:
        df: pd.DataFrame with Date, Ri_Rf, Rm_Rf, SMB, HML
        
    Returns:
        Dict containing OLS summary statistics, coefficients, p-values, t-stats,
        R-squared, confidence intervals, and qualitative interpretations.
    """
    # Define variables
    y = df['Ri_Rf']
    X = df[['Rm_Rf', 'SMB', 'HML']]
    
    # Add constant for Alpha (intercept)
    X_with_const = sm.add_constant(X)
    
    # Run OLS regression
    model = sm.OLS(y, X_with_const)
    results = model.fit()
    
    # Extract coefficients
    params = results.params
    pvalues = results.pvalues
    tvalues = results.tvalues
    conf_int = results.conf_int()
    bse = results.bse  # Standard errors
    
    # Output structure
    regression_stats = {
        "num_observations": int(results.nobs),
        "r_squared": float(results.rsquared),
        "adj_r_squared": float(results.rsquared_adj),
        "f_statistic": float(results.fvalue),
        "f_pvalue": float(results.f_pvalue),
        "factors": {
            "Alpha": {
                "coefficient": float(params['const']),
                "p_value": float(pvalues['const']),
                "t_stat": float(tvalues['const']),
                "std_err": float(bse['const']),
                "conf_lower": float(conf_int.loc['const', 0]),
                "conf_upper": float(conf_int.loc['const', 1]),
                "significant": bool(pvalues['const'] < 0.05)
            },
            "Market": {
                "coefficient": float(params['Rm_Rf']),
                "p_value": float(pvalues['Rm_Rf']),
                "t_stat": float(tvalues['Rm_Rf']),
                "std_err": float(bse['Rm_Rf']),
                "conf_lower": float(conf_int.loc['Rm_Rf', 0]),
                "conf_upper": float(conf_int.loc['Rm_Rf', 1]),
                "significant": bool(pvalues['Rm_Rf'] < 0.05)
            },
            "SMB": {
                "coefficient": float(params['SMB']),
                "p_value": float(pvalues['SMB']),
                "t_stat": float(tvalues['SMB']),
                "std_err": float(bse['SMB']),
                "conf_lower": float(conf_int.loc['SMB', 0]),
                "conf_upper": float(conf_int.loc['SMB', 1]),
                "significant": bool(pvalues['SMB'] < 0.05)
            },
            "HML": {
                "coefficient": float(params['HML']),
                "p_value": float(pvalues['HML']),
                "t_stat": float(tvalues['HML']),
                "std_err": float(bse['HML']),
                "conf_lower": float(conf_int.loc['HML', 0]),
                "conf_upper": float(conf_int.loc['HML', 1]),
                "significant": bool(pvalues['HML'] < 0.05)
            }
        }
    }
    
    # Calculate OLS predictions and RMSE
    y_pred_ols = results.predict(X_with_const)
    rmse_ols = float(np.sqrt(np.mean((y - y_pred_ols)**2)))
    
    model_comparison = {
        "Fama-French OLS Regression": {
            "r2": float(results.rsquared),
            "rmse": rmse_ols,
            "status": "Success"
        }
    }
    
    # Linear Regression (Sklearn)
    try:
        from sklearn.linear_model import LinearRegression
        lr = LinearRegression()
        lr.fit(X, y)
        y_pred_lr = lr.predict(X)
        r2_lr = float(lr.score(X, y))
        rmse_lr = float(np.sqrt(np.mean((y - y_pred_lr)**2)))
        model_comparison["Linear Regression"] = {
            "r2": r2_lr,
            "rmse": rmse_lr,
            "status": "Success"
        }
    except ImportError:
        model_comparison["Linear Regression"] = {
            "r2": 0.0,
            "rmse": 0.0,
            "status": "Package 'scikit-learn' not installed"
        }
    except Exception as e:
        model_comparison["Linear Regression"] = {
            "r2": 0.0,
            "rmse": 0.0,
            "status": f"Error: {str(e)}"
        }
        
    # Random Forest (Sklearn)
    try:
        from sklearn.ensemble import RandomForestRegressor
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)
        y_pred_rf = rf.predict(X)
        r2_rf = float(rf.score(X, y))
        rmse_rf = float(np.sqrt(np.mean((y - y_pred_rf)**2)))
        model_comparison["Random Forest"] = {
            "r2": r2_rf,
            "rmse": rmse_rf,
            "status": "Success"
        }
    except ImportError:
        model_comparison["Random Forest"] = {
            "r2": 0.0,
            "rmse": 0.0,
            "status": "Package 'scikit-learn' not installed"
        }
    except Exception as e:
        model_comparison["Random Forest"] = {
            "r2": 0.0,
            "rmse": 0.0,
            "status": f"Error: {str(e)}"
        }
        
    # XGBoost
    try:
        from xgboost import XGBRegressor
        xgb_model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
        xgb_model.fit(X, y)
        y_pred_xgb = xgb_model.predict(X)
        r2_xgb = float(xgb_model.score(X, y))
        rmse_xgb = float(np.sqrt(np.mean((y - y_pred_xgb)**2)))
        model_comparison["XGBoost"] = {
            "r2": r2_xgb,
            "rmse": rmse_xgb,
            "status": "Success"
        }
    except ImportError:
        model_comparison["XGBoost"] = {
            "r2": 0.0,
            "rmse": 0.0,
            "status": "Package 'xgboost' not installed"
        }
    except Exception as e:
        model_comparison["XGBoost"] = {
            "r2": 0.0,
            "rmse": 0.0,
            "status": f"Error: {str(e)}"
        }
        
    # Add comparison to regression statistics
    regression_stats["model_comparison"] = model_comparison
    
    # Generate qualitative interpretations
    regression_stats["interpretations"] = generate_interpretations(regression_stats)
    
    return regression_stats

def generate_interpretations(stats: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates plain-English financial interpretations of regression metrics.
    """
    factors = stats["factors"]
    r2 = stats["r_squared"]
    
    mkt = factors["Market"]
    smb = factors["SMB"]
    hml = factors["HML"]
    alpha = factors["Alpha"]
    
    interpretations = {}
    
    # 1. Market Beta Interpretation
    mkt_coeff = mkt["coefficient"]
    mkt_sig = " (statistically significant)" if mkt["significant"] else " (not statistically significant)"
    if mkt_coeff > 1.1:
        interpretations["market"] = f"This stock is highly sensitive to market movements (Beta = {mkt_coeff:.2f}{mkt_sig}). It tends to amplify NIFTY 50 index movements, making it an aggressive stock."
    elif mkt_coeff < 0.9:
        interpretations["market"] = f"This stock is relatively stable compared to the market (Beta = {mkt_coeff:.2f}{mkt_sig}). It exhibits defensive properties, offering a buffer during market declines."
    else:
        interpretations["market"] = f"This stock moves in sync with the broad market index (Beta = {mkt_coeff:.2f}{mkt_sig}). It has market-like risk and return patterns."
        
    # 2. SMB (Size Factor) Interpretation
    smb_coeff = smb["coefficient"]
    smb_sig = " (statistically significant)" if smb["significant"] else " (not statistically significant)"
    if smb_coeff > 0.15:
        interpretations["smb"] = f"The stock shows characteristics associated with smaller companies (SMB Beta = {smb_coeff:.2f}{smb_sig}). It captures the small-firm premium and may experience higher growth potential but higher volatility."
    elif smb_coeff < -0.15:
        interpretations["smb"] = f"The stock behaves more like large-cap companies (SMB Beta = {smb_coeff:.2f}{smb_sig}). It shows high resilience and stability associated with market giants."
    else:
        interpretations["smb"] = f"The stock is size-neutral (SMB Beta = {smb_coeff:.2f}{smb_sig}). Its performance is not significantly driven by firm scale or capitalization differences."
        
    # 3. HML (Value vs Growth Factor) Interpretation
    hml_coeff = hml["coefficient"]
    hml_sig = " (statistically significant)" if hml["significant"] else " (not statistically significant)"
    if hml_coeff > 0.15:
        interpretations["hml"] = f"The stock exhibits value-oriented characteristics (HML Beta = {hml_coeff:.2f}{hml_sig}). It has a high book-to-market ratio, representing fundamentally sound but undervalued assets."
    elif hml_coeff < -0.15:
        interpretations["hml"] = f"The stock exhibits growth-oriented characteristics (HML Beta = {hml_coeff:.2f}{hml_sig}). It behaves like a growth stock, with premium valuations and high reliance on future earnings expansion."
    else:
        interpretations["hml"] = f"The stock behaves like a blend of value and growth (HML Beta = {hml_coeff:.2f}{hml_sig}). It has an even exposure to value and growth styles."
        
    # 4. Alpha (Abnormal Return) Interpretation
    alpha_coeff = alpha["coefficient"] * 100  # Convert to percent
    alpha_sig = " (statistically significant)" if alpha["significant"] else " (not statistically significant)"
    if alpha["significant"] and alpha_coeff > 0:
        interpretations["alpha"] = f"The stock generated a positive abnormal return of {alpha_coeff:.3f}% per period (Alpha = {alpha['coefficient']:.4f}{alpha_sig}) after adjusting for market, size, and style risks. This implies strong manager outperformance or unique asset advantages."
    elif alpha["significant"] and alpha_coeff < 0:
        interpretations["alpha"] = f"The stock underperformed by {alpha_coeff:.3f}% per period (Alpha = {alpha['coefficient']:.4f}{alpha_sig}) relative to its risk exposures, indicating structural headwinds or pricing inefficiencies in this timeframe."
    else:
        interpretations["alpha"] = f"The stock's abnormal return (Alpha = {alpha['coefficient']:.4f}{alpha_sig}) is statistically indistinguishable from zero. Its returns are entirely explained by its exposure to the market, size, and value risk factors."

    # 5. R-squared Interpretation
    r2_pct = r2 * 100
    if r2 > 0.85:
        interpretations["r_squared"] = f"The Fama-French 3-Factor model explains a very large portion ({r2_pct:.1f}%) of the stock's returns. The variation in stock price is almost entirely driven by market risk, size, and style factors."
    elif r2 >= 0.50:
        interpretations["r_squared"] = f"The Fama-French 3-Factor model explains a moderate portion ({r2_pct:.1f}%) of the returns. A significant amount of the price movement is driven by stock-specific news, industry events, or other factor dimensions."
    else:
        interpretations["r_squared"] = f"The Fama-French 3-Factor model explains a small portion ({r2_pct:.1f}%) of the returns. The stock's performance is heavily dominated by idiosyncratic factors (firm-specific variables) rather than systemic style factors."
        
    return interpretations
