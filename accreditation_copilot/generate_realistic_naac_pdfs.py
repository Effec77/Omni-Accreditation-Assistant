"""
Generate REALISTIC NAAC SSR PDFs with proper structure
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from pathlib import Path

def create_realistic_a_plus_pdf():
    """Create realistic A+ grade SSR"""
    output_path = Path("D:/NAAC_Test_PDFs") / "Realistic_IIT_A+_SSR.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output_path), pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1e40af'), spaceAfter=12)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#1e40af'), spaceAfter=10)
    
    # Cover Page
    story.append(Paragraph("<b>SELF STUDY REPORT (SSR)</b>", title_style))
    story.append(Paragraph("<b>Indian Institute of Technology, Mumbai</b>", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("For NAAC Accreditation - Cycle 4", styles['Normal']))
    story.append(Paragraph("Academic Year: 2023-24", styles['Normal']))
    story.append(Spacer(1, 24))
    
    # Criterion 3.2.1
    story.append(PageBreak())
    story.append(Paragraph("<b>CRITERION 3: RESEARCH, INNOVATIONS AND EXTENSION</b>", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>3.2 Resource Mobilization for Research</b>", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>3.2.1 Grants received from Government and non-governmental agencies for research projects / endowments in the institution during the last five years (INR in Lakhs)</b>", heading_style))
    story.append(Spacer(1, 12))
    
    # Narrative
    narrative = """
    IIT Mumbai has consistently demonstrated excellence in securing extramural research funding from diverse sources. 
    The institution has established strong partnerships with premier funding agencies including DST, SERB, DBT, ICSSR, 
    and leading industry partners. Our research portfolio spans cutting-edge areas including Artificial Intelligence, 
    Renewable Energy, Nanotechnology, Biotechnology, and Advanced Materials Science.
    
    The institution has implemented a robust research support system including dedicated research cells, grant writing 
    workshops, and mentorship programs for faculty. This has resulted in a consistent growth in research funding over 
    the assessment period.
    """
    story.append(Paragraph(narrative, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Table 3.2.1: Year-wise funding
    story.append(Paragraph("<b>Table 3.2.1: Year-wise Research Funding Summary</b>", heading_style))
    story.append(Spacer(1, 10))
    
    table_data = [
        ['S.No', 'Academic Year', 'Number of\nProjects', 'Total Funding\n(INR Lakhs)', 'Funding Agencies', 'Average per\nProject (Lakhs)'],
        ['1', '2019-20', '85', '3250', 'DST, SERB, DBT, ICSSR, Industry', '38.24'],
        ['2', '2020-21', '92', '3580', 'SERB, DBT, DST, ICSSR, Corporate', '38.91'],
        ['3', '2021-22', '98', '3920', 'DST, SERB, Industry, DBT, ICSSR', '40.00'],
        ['4', '2022-23', '88', '3450', 'DBT, DST, SERB, Industry, ICSSR', '39.20'],
        ['5', '2023-24', '95', '3800', 'SERB, DST, Industry, DBT, Corporate', '40.00'],
        ['', '<b>Total (5 Years)</b>', '<b>458</b>', '<b>18000</b>', '<b>Multiple Agencies</b>', '<b>39.30</b>'],
    ]
    
    table = Table(table_data, colWidths=[0.6*inch, 1.2*inch, 1*inch, 1.2*inch, 2*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e0e7ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Table 3.2.2: Agency-wise distribution
    story.append(Paragraph("<b>Table 3.2.2: Funding Agency-wise Distribution</b>", heading_style))
    story.append(Spacer(1, 10))
    
    agency_data = [
        ['S.No', 'Funding Agency', 'No. of\nProjects', 'Total Funding\n(INR Lakhs)', 'Percentage', 'Key Research Areas'],
        ['1', 'DST (Department of Science\n& Technology)', '145', '5850', '32.5%', 'AI, Renewable Energy,\nMaterials Science'],
        ['2', 'SERB (Science & Engineering\nResearch Board)', '128', '5040', '28.0%', 'Nanotech, Biotech,\nQuantum Computing'],
        ['3', 'DBT (Department of\nBiotechnology)', '95', '3420', '19.0%', 'Genomics, Drug Discovery,\nAgri-biotech'],
        ['4', 'ICSSR (Indian Council of\nSocial Science Research)', '52', '1980', '11.0%', 'Economics, Policy,\nSociology'],
        ['5', 'Industry & Corporate\nPartners', '38', '1710', '9.5%', 'Applied Research,\nProduct Development'],
        ['', '<b>Total</b>', '<b>458</b>', '<b>18000</b>', '<b>100%</b>', '<b>Multi-disciplinary</b>'],
    ]
    
    agency_table = Table(agency_data, colWidths=[0.5*inch, 2*inch, 0.9*inch, 1.2*inch, 0.9*inch, 1.7*inch])
    agency_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e0e7ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
    ]))
    
    story.append(agency_table)
    story.append(Spacer(1, 20))
    
    # Supporting evidence
    evidence = """
    <b>Supporting Evidence:</b><br/>
    • Sanction letters from all funding agencies (Annexure 3.2.1-A)<br/>
    • Utilization certificates for completed projects (Annexure 3.2.1-B)<br/>
    • List of publications from funded projects (Annexure 3.2.1-C)<br/>
    • MoUs with industry partners (Annexure 3.2.1-D)<br/>
    • Research impact assessment reports (Annexure 3.2.1-E)
    """
    story.append(Paragraph(evidence, styles['Normal']))
    
    doc.build(story)
    print(f"✅ Created: {output_path.name} (Realistic A+ - 458 projects, ₹18000 Lakhs)")

def create_realistic_b_plus_pdf():
    """Create realistic B+ grade SSR"""
    output_path = Path("D:/NAAC_Test_PDFs") / "Realistic_State_University_B+_SSR.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output_path), pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1e40af'), spaceAfter=12)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#1e40af'), spaceAfter=10)
    
    # Cover
    story.append(Paragraph("<b>SELF STUDY REPORT (SSR)</b>", title_style))
    story.append(Paragraph("<b>State University of Excellence</b>", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("For NAAC Accreditation - Cycle 3", styles['Normal']))
    story.append(Paragraph("Academic Year: 2023-24", styles['Normal']))
    story.append(Spacer(1, 24))
    
    # Criterion 3.2.1
    story.append(PageBreak())
    story.append(Paragraph("<b>CRITERION 3: RESEARCH, INNOVATIONS AND EXTENSION</b>", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>3.2.1 Grants received from Government and non-governmental agencies for research projects</b>", heading_style))
    story.append(Spacer(1, 12))
    
    narrative = """
    The university has made significant progress in securing research funding from government agencies and industry partners.
    Our focus areas include regional development, sustainable agriculture, and applied sciences. The institution has 
    established research cells and provides seed funding to encourage faculty research initiatives.
    """
    story.append(Paragraph(narrative, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Table
    story.append(Paragraph("<b>Table 3.2.1: Year-wise Research Funding</b>", heading_style))
    story.append(Spacer(1, 10))
    
    table_data = [
        ['Year', 'Projects', 'Funding (Lakhs)', 'Agencies'],
        ['2019-20', '18', '420', 'UGC, State Govt, DST'],
        ['2020-21', '22', '510', 'UGC, DST, Industry'],
        ['2021-22', '25', '580', 'UGC, SERB, State Govt'],
        ['2022-23', '20', '465', 'UGC, DST, Industry'],
        ['2023-24', '23', '525', 'DST, UGC, Corporate'],
        ['<b>Total</b>', '<b>108</b>', '<b>2500</b>', '<b>Multiple</b>'],
    ]
    
    table = Table(table_data, colWidths=[1.5*inch, 1.2*inch, 1.5*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e0e7ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(table)
    
    doc.build(story)
    print(f"✅ Created: {output_path.name} (Realistic B+ - 108 projects, ₹2500 Lakhs)")

def create_realistic_c_pdf():
    """Create realistic C grade SSR"""
    output_path = Path("D:/NAAC_Test_PDFs") / "Realistic_Regional_College_C_SSR.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    story.append(Paragraph("<b>Self Study Report</b>", styles['Title']))
    story.append(Paragraph("<b>Regional College</b>", styles['Heading1']))
    story.append(Spacer(1, 24))
    
    story.append(Paragraph("<b>Criterion 3.2.1: Research Funding</b>", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    # Minimal table
    table_data = [
        ['Year', 'Projects', 'Funding (Lakhs)'],
        ['2019-20', '3', '45'],
        ['2020-21', '2', '28'],
        ['2021-22', '4', '62'],
        ['2022-23', '2', '35'],
        ['2023-24', '3', '50'],
        ['Total', '14', '220'],
    ]
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("The college is working to improve research infrastructure and faculty capacity.", styles['Normal']))
    
    doc.build(story)
    print(f"✅ Created: {output_path.name} (Realistic C - 14 projects, ₹220 Lakhs)")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("GENERATING REALISTIC NAAC SSR PDFs")
    print("="*80 + "\n")
    
    create_realistic_a_plus_pdf()
    create_realistic_b_plus_pdf()
    create_realistic_c_pdf()
    
    print("\n" + "="*80)
    print("REALISTIC PDFs CREATED!")
    print("="*80)
    print("\nExpected Results:")
    print("  - Realistic_IIT_A+_SSR.pdf -> Grade A+ (75-85% confidence)")
    print("  - Realistic_State_University_B+_SSR.pdf -> Grade B+ (55-65% confidence)")
    print("  - Realistic_Regional_College_C_SSR.pdf -> Grade C (25-35% confidence)")
