"""
Create Demo PDFs for NAAC Criterion 3.2.1 Testing
One excellent alignment, one poor alignment
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from pathlib import Path

def create_excellent_ssr():
    """Create an SSR that aligns excellently with NAAC 3.2.1"""
    output_path = Path(__file__).parent.parent / "data" / "raw_docs" / "Excellence_University_A+_SSR.pdf"
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story.append(Paragraph("Excellence University", title_style))
    story.append(Paragraph("Self Study Report (SSR)", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Criterion 3.2.1 Header
    story.append(Paragraph("Criterion 3.2.1: Extramural Funding for Research", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    # Detailed overview with keyword-rich content
    overview = """
    <b>Criterion 3.2.1: Extramural Funding for Research - Excellence University Performance Report</b><br/><br/>
    
    Excellence University has demonstrated exceptional performance in securing extramural funding 
    for research projects during the last five years (2019-2024). The institution has received 
    substantial grants totaling <b>INR 45.8 Crores (4580 Lakhs)</b> from prestigious funding agencies.<br/><br/>
    
    <b>Total Research Projects Funded: 127 projects</b><br/>
    <b>Total Funding Amount: INR 4580 Lakhs (45.8 Crores)</b><br/>
    <b>Time Period: Last Five Years (2019-2020 to 2023-2024)</b><br/><br/>
    
    <b>Major Funding Agencies:</b><br/>
    • Department of Science and Technology (DST): 38 projects, INR 1580 Lakhs<br/>
    • Science and Engineering Research Board (SERB): 32 projects, INR 1240 Lakhs<br/>
    • Department of Biotechnology (DBT): 24 projects, INR 890 Lakhs<br/>
    • Indian Council of Social Science Research (ICSSR): 18 projects, INR 520 Lakhs<br/>
    • Industry and Corporate Partners: 15 projects, INR 350 Lakhs<br/><br/>
    
    The university has established strong collaborations with government funding agencies and 
    industry partners, resulting in consistent growth in research funding year over year.
    """
    story.append(Paragraph(overview, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Year-wise funding table
    story.append(Paragraph("Year-wise Extramural Funding Details", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    funding_data = [
        ['Year', 'Number of Projects', 'Funding Amount (INR Lakhs)', 'Major Funding Agencies'],
        ['2019-20', '22', '785', 'DST, SERB, Industry Partners'],
        ['2020-21', '28', '920', 'DBT, ICSSR, DST'],
        ['2021-22', '31', '1150', 'SERB, Industry, Corporate'],
        ['2022-23', '24', '890', 'DST, DBT, SERB'],
        ['2023-24', '22', '835', 'ICSSR, Industry, DST'],
        ['Total', '127', '4580', 'Multiple Agencies']
    ]
    
    table = Table(funding_data, colWidths=[1.2*inch, 1.5*inch, 2*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f4f8')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    
    # Funding agency details with more content
    agency_text = """
    <b>Detailed Funding Agency Breakdown for Criterion 3.2.1:</b><br/><br/>
    
    <b>1. Department of Science and Technology (DST):</b><br/>
    Total Projects: 38 | Total Funding: INR 1580 Lakhs<br/>
    The DST has been our primary funding partner for basic and applied research across 
    engineering, science, and technology departments. Major grants include projects in 
    artificial intelligence, renewable energy, and materials science.<br/><br/>
    
    <b>2. Science and Engineering Research Board (SERB):</b><br/>
    Total Projects: 32 | Total Funding: INR 1240 Lakhs<br/>
    SERB funding has supported early career researchers and established faculty in pursuing 
    cutting-edge research. Projects span nanotechnology, biotechnology, and computational sciences.<br/><br/>
    
    <b>3. Department of Biotechnology (DBT):</b><br/>
    Total Projects: 24 | Total Funding: INR 890 Lakhs<br/>
    DBT grants have enabled significant research in genomics, drug discovery, and agricultural 
    biotechnology. The university has established state-of-the-art biotech research facilities.<br/><br/>
    
    <b>4. Indian Council of Social Science Research (ICSSR):</b><br/>
    Total Projects: 18 | Total Funding: INR 520 Lakhs<br/>
    ICSSR funding supports research in economics, sociology, psychology, and public policy. 
    Projects address critical social issues and policy formulation.<br/><br/>
    
    <b>5. Industry and Corporate Partners:</b><br/>
    Total Projects: 15 | Total Funding: INR 350 Lakhs<br/>
    Industry collaborations include partnerships with leading corporations for applied research, 
    product development, and technology transfer initiatives.<br/><br/>
    
    <b>Research Impact:</b> The extramural funding has resulted in 450+ research publications, 
    25 patents filed, and significant contributions to national research priorities.
    """
    story.append(Paragraph(agency_text, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Add more detailed project information
    project_details = """
    <b>Sample Major Research Projects (Criterion 3.2.1 Evidence):</b><br/><br/>
    
    1. <b>AI-Driven Healthcare Solutions</b> - DST Grant: INR 85 Lakhs - Duration: 3 years<br/>
    2. <b>Sustainable Energy Systems</b> - SERB Grant: INR 72 Lakhs - Duration: 2 years<br/>
    3. <b>Genomic Research for Crop Improvement</b> - DBT Grant: INR 95 Lakhs - Duration: 4 years<br/>
    4. <b>Urban Planning and Smart Cities</b> - ICSSR Grant: INR 45 Lakhs - Duration: 2 years<br/>
    5. <b>Industrial IoT Applications</b> - Industry Grant: INR 60 Lakhs - Duration: 2 years<br/><br/>
    
    All projects align with NAAC Criterion 3.2.1 requirements for extramural research funding 
    documentation, including funding amounts, agency names, project counts, and time periods.
    """
    story.append(Paragraph(project_details, styles['BodyText']))
    
    doc.build(story)
    print(f"✓ Created: {output_path}")
    return output_path


def create_poor_ssr():
    """Create an SSR that poorly aligns with NAAC 3.2.1"""
    output_path = Path(__file__).parent.parent / "data" / "raw_docs" / "Struggling_College_C_SSR.pdf"
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1
    )
    
    story.append(Paragraph("Struggling College", title_style))
    story.append(Paragraph("Self Study Report (SSR)", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Criterion 3.2.1 Header
    story.append(Paragraph("Criterion 3.2.1: Extramural Funding for Research", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    # Vague overview - missing key dimensions
    overview = """
    Our college has been working on improving research activities. Faculty members are encouraged 
    to apply for research grants. We have received some funding from various sources. The college 
    management is committed to promoting research culture among faculty and students. Several 
    initiatives have been taken to enhance research output.
    """
    story.append(Paragraph(overview, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Incomplete table - missing critical data
    story.append(Paragraph("Research Funding Information", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    funding_data = [
        ['Year', 'Status'],
        ['2019-20', 'Some projects funded'],
        ['2020-21', 'Applied for grants'],
        ['2021-22', 'Received funding'],
        ['2022-23', 'Ongoing projects'],
        ['2023-24', 'Under process']
    ]
    
    table = Table(funding_data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Vague statements without specifics
    additional_text = """
    The college has made efforts to secure external funding. Faculty members have submitted 
    proposals to different agencies. We are hopeful of receiving more grants in the future. 
    The research committee meets regularly to discuss funding opportunities. Students are 
    also involved in research activities under faculty guidance.
    """
    story.append(Paragraph(additional_text, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Generic statement without data
    conclusion = """
    <b>Note:</b> The college is in the process of compiling detailed funding information. 
    Complete data will be provided in subsequent reports. We are committed to improving 
    our research infrastructure and securing more extramural funding.
    """
    story.append(Paragraph(conclusion, styles['BodyText']))
    
    doc.build(story)
    print(f"✓ Created: {output_path}")
    return output_path


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CREATING DEMO SSR PDFs FOR NAAC 3.2.1")
    print("="*60 + "\n")
    
    excellent_path = create_excellent_ssr()
    poor_path = create_poor_ssr()
    
    print("\n" + "="*60)
    print("DEMO PDFs CREATED SUCCESSFULLY")
    print("="*60)
    print(f"\n1. Excellent Alignment (A+ Grade Expected):")
    print(f"   {excellent_path}")
    print(f"   - Complete funding data (INR 45.8 Crores)")
    print(f"   - 127 projects with year-wise breakdown")
    print(f"   - All funding agencies specified (DST, SERB, DBT, ICSSR, Industry)")
    print(f"   - Time period clearly mentioned (2019-2024)")
    
    print(f"\n2. Poor Alignment (C Grade Expected):")
    print(f"   {poor_path}")
    print(f"   - Missing: Specific funding amounts")
    print(f"   - Missing: Number of projects")
    print(f"   - Missing: Funding agency names")
    print(f"   - Vague statements without quantitative data")
    print("\n")
