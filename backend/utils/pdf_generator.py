import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from typing import Dict, Any

def generate_pdf_report(stock_name: str, results: Dict[str, Any]) -> io.BytesIO:
    """
    Generates a structured, presentation-ready PDF report of the OLS Fama-French analysis.
    
    Parameters:
        stock_name: Name of the stock analyzed.
        results: Dict from run_fama_french_regression.
        
    Returns:
        BytesIO stream of the PDF file.
    """
    buffer = io.BytesIO()
    
    # Page setup
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#0F172A'), # Slate 900
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor('#64748B'), # Slate 500
        spaceAfter=20
    )
    
    heading2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        textColor=colors.HexColor('#1E3A8A'), # Navy blue
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#334155'), # Slate 700
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        textColor=colors.HexColor('#1E293B'), # Slate 800
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6,
        leading=13
    )
    
    formula_style = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=10,
        textColor=colors.HexColor('#312E81'), # Indigo 900
        alignment=1, # Centered
        backColor=colors.HexColor('#EEF2F6'),
        borderPadding=8,
        spaceAfter=15
    )

    elements = []
    
    # Header Section
    elements.append(Paragraph("FAMA AI", title_style))
    elements.append(Paragraph(f"Fama-French 3-Factor Regression Report &bull; Academic Analysis &bull; {stock_name}", subtitle_style))
    
    # Divider line
    divider = Table([[""]], colWidths=[532], rowHeights=[2])
    divider.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E3A8A')),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(divider)
    elements.append(Spacer(1, 15))
    
    # Executive Summary / Regression Equation
    elements.append(Paragraph("Regression Equation", heading2_style))
    equation_text = (
        "R<sub>i</sub> - R<sub>f</sub> = &alpha; + &beta;<sub>Market</sub>(R<sub>m</sub> - R<sub>f</sub>) + "
        "s &times; SMB + h &times; HML + &epsilon;"
    )
    elements.append(Paragraph(equation_text, formula_style))
    
    # Stock Overview Description
    intro_p = (
        f"This academic report presents the OLS regression analysis results for <b>{stock_name}</b> "
        f"using the Fama-French 3-Factor Model. The analysis calculates exposure to systemic risk factors "
        f"over {results['num_observations']} observation periods. Below are the coefficients, p-values, "
        f"statistical significance, and economic interpretations."
    )
    elements.append(Paragraph(intro_p, body_style))
    elements.append(Spacer(1, 12))
    
    # Regression Results Table
    elements.append(Paragraph("Model Coefficients & Statistics", heading2_style))
    
    factors = results["factors"]
    
    # Prepare data for table
    table_data = [
        ["Factor", "Coefficient", "Std Error", "t-Statistic", "p-Value", "95% Conf. Interval", "Significant"]
    ]
    
    for factor_name, data in factors.items():
        # Map standard keys
        display_name = {
            "Alpha": "Alpha (Intercept)",
            "Market": "Market Premium (Rm-Rf)",
            "SMB": "Size Factor (SMB)",
            "HML": "Style Factor (HML)"
        }.get(factor_name, factor_name)
        
        conf_interval = f"[{data['conf_lower']:.4f}, {data['conf_upper']:.4f}]"
        sig_text = "Yes (p < 0.05)" if data["significant"] else "No"
        
        table_data.append([
            display_name,
            f"{data['coefficient']:.4f}",
            f"{data['std_err']:.4f}",
            f"{data['t_stat']:.2f}",
            f"{data['p_value']:.4f}",
            conf_interval,
            sig_text
        ])
        
    # Table layout & styles
    col_widths = [135, 65, 55, 60, 50, 110, 57]
    stats_table = Table(table_data, colWidths=col_widths)
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')), # Dark navy header
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,1), (0,-1), 'LEFT'), # Left align first column
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')), # Light grey border
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]), # Alternating rows
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 10))
    
    # Model Diagnostics Table
    elements.append(Paragraph("Model Fit Diagnostics", heading2_style))
    diagnostics_data = [
        [
            Paragraph("<b>Number of Observations:</b>", body_style), f"{results['num_observations']}",
            Paragraph("<b>R-Squared (R&sup2;):</b>", body_style), f"{results['r_squared']:.4f}"
        ],
        [
            Paragraph("<b>F-Statistic:</b>", body_style), f"{results['f_statistic']:.2f}",
            Paragraph("<b>Adjusted R-Squared:</b>", body_style), f"{results['adj_r_squared']:.4f}"
        ],
        [
            Paragraph("<b>Prob (F-statistic):</b>", body_style), f"{results['f_pvalue']:.4e}",
            "", ""
        ]
    ]
    diag_table = Table(diagnostics_data, colWidths=[150, 100, 150, 132])
    diag_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('SPAN', (2,2), (3,2)), # Span empty cells
    ]))
    elements.append(diag_table)
    elements.append(Spacer(1, 15))
    
    # Qualitative Interpretations
    elements.append(Paragraph("Fama-French Factor Interpretation", heading2_style))
    
    interpretations = results["interpretations"]
    
    bullets = [
        f"<b>Market Sensitivity (&beta;):</b> {interpretations['market']}",
        f"<b>Size Premium Exposure (SMB):</b> {interpretations['smb']}",
        f"<b>Style Premium Exposure (HML):</b> {interpretations['hml']}",
        f"<b>Abnormal Return (&alpha;):</b> {interpretations['alpha']}",
        f"<b>Model Explanatory Power (R&sup2;):</b> {interpretations['r_squared']}"
    ]
    
    for bullet in bullets:
        elements.append(Paragraph(f"&bull; {bullet}", bullet_style))
        
    elements.append(Spacer(1, 20))
    
    # Academic Disclaimer Footer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        textColor=colors.HexColor('#94A3B8'),
        alignment=1, # Centered
        spaceBefore=20
    )
    elements.append(Paragraph(
        "FAMA AI is an academic analysis project. This analysis is based on historical factor data and "
        "should not be construed as investment advice. Past performance is not indicative of future results.",
        disclaimer_style
    ))
    
    # Build Document
    doc.build(elements)
    buffer.seek(0)
    return buffer
