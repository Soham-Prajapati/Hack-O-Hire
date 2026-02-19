"""
PDF Generator — Creates professional FinCEN-style SAR PDFs.
"""
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch

def generate_sar_pdf(sar_data: dict) -> bytes:
    """
    Generate a PDF for the given SAR data.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # --- Styles ---
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        spaceAfter=12,
        alignment=1 # Center
    )
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=2 # Right
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=6,
        borderPadding=5,
        borderWidth=0,
        borderColor=colors.black,
        backColor=colors.lightgrey
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=10
    )
    
    # --- Data Extraction ---
    case_id = sar_data.get("case_id", "Unknown")
    sar_id = sar_data.get("sar_id", "Unknown")
    narrative = sar_data.get("narrative", {})
    typology = sar_data.get("typology", {})
    if not isinstance(typology, dict): typology = {}
    
    prediction = typology.get("prediction", "N/A").upper()
    confidence = typology.get("confidence", 0.0)
    
    # --- Official Header ---
    # FinCEN-style top bar
    story.append(Paragraph("<b>FINANCIAL CRIMES ENFORCEMENT NETWORK</b>", 
                           ParagraphStyle('Top', parent=styles['Normal'], fontSize=8, alignment=1)))
    story.append(Paragraph("SUSPICIOUS ACTIVITY REPORT (SAR)", title_style))
    story.append(Paragraph(f"Form 111 | OMB No. 1506-0065 | Generated: {datetime.now().strftime('%Y-%m-%d')}", 
                           ParagraphStyle('Sub', parent=styles['Normal'], fontSize=8, alignment=1)))
    story.append(Spacer(1, 0.3*inch))

    # --- Part I: Subject Information (Simulated) ---
    story.append(Paragraph("PART I: Subject Information", section_style))
    
    # Mock specific fields if not present (to look like a filled form)
    customer_name = sar_data.get("customer_name", "Unknown Subject") # Data dependent
    
    data_p1 = [
        [Paragraph("<b>1. Subject Name</b>", body_style), Paragraph(f"{customer_name}", body_style)],
        [Paragraph("<b>2. Case ID</b>", body_style), Paragraph(f"{case_id}", body_style)],
        [Paragraph("<b>3. SAR ID</b>", body_style), Paragraph(f"{sar_id}", body_style)],
    ]
    t1 = Table(data_p1, colWidths=[2*inch, 4*inch])
    t1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t1)
    story.append(Spacer(1, 0.2*inch))

    # --- Part II: Suspicious Activity Information ---
    story.append(Paragraph("PART II: Suspicious Activity Information", section_style))
    
    data_p2 = [
        [Paragraph("<b>4. Primary Typology</b>", body_style), Paragraph(f"{prediction} (Confidence: {confidence:.1%})", body_style)],
        [Paragraph("<b>5. Amount Involved</b>", body_style), Paragraph("See Transaction List", body_style)],
        [Paragraph("<b>6. Date Range</b>", body_style), Paragraph(f"{datetime.now().strftime('%Y-%m-%d')} (Current)", body_style)],
    ]
    t2 = Table(data_p2, colWidths=[2*inch, 4*inch])
    t2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.2*inch))

    # --- Part V: Narrative ---
    story.append(Paragraph("PART V: Suspicious Activity Information - Narrative", section_style))
    story.append(Paragraph("<i>Provide a chronological and complete account of the suspicious activity.</i>", 
                           ParagraphStyle('Inst', parent=styles['Normal'], fontSize=9, textColor=colors.grey)))
    story.append(Spacer(1, 0.1*inch))
    
    # Narrative Box
    story.append(Paragraph("<b>INTRODUCTION</b>", body_style))
    story.append(Paragraph(narrative.get("introduction", "N/A"), body_style))
    story.append(Spacer(1, 0.1*inch))
    
    body_text = narrative.get("body", "N/A")
    story.append(Paragraph("<b>BODY / ANALYSIS</b>", body_style))
    for line in body_text.split('\n'):
        if line.strip():
            story.append(Paragraph(line, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>CONCLUSION</b>", body_style))
    story.append(Paragraph(narrative.get("conclusion", "N/A"), body_style))

    # --- Footer ---
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<b>PRIVACY ACT NOTICE:</b> This report is exempt from disclosure under the Freedom of Information Act.", 
                           ParagraphStyle('Footer', parent=styles['Normal'], fontSize=7, alignment=1)))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
