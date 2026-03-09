"""
Create Table-Heavy Demo PDFs for NAAC Criterion 3.2.1
Optimized for the table-based chunking system
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from pathlib import Path

def create_excellent_table_heavy_ssr():
    """Create an SSR with multiple detailed tables for excellent alignment"""
    output_path = Path(__file__).parent.parent / "data" / "raw_docs" / "Excellence_University_A+_SSR.pdf"
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=1
    )
    
    story.append(Paragraph("Excellence University", title_style))
    story.append(Paragraph("Self Study Report - NAAC Accreditation", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Criterion Header
    story.append(Paragraph("Criterion 3.2.1: Extramural Funding for Research", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))
    
    # Table 1: Year-wise Summary (NAAC 3.2.1 - time_period, funding_amount, project_count)
    story.append(Paragraph("Table 1: Year-wise Extramural Research Funding Summary", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    year_data = [
        ['Year', 'Number of Projects', 'Total Funding (INR Lakhs)', 'Funding Agencies', 'Average per Project (INR Lakhs)'],
        ['2019-20', '22', '785', 'DST, SERB, DBT, Industry', '35.68'],
        ['2020-21', '28', '920', 'SERB, DBT, ICSSR, DST', '32.86'],
        ['2021-22', '31', '1150', 'DST, SERB, Industry, Corporate', '37.10'],
        ['2022-23', '24', '890', 'DBT, DST, SERB, ICSSR', '37.08'],
        ['2023-24', '22', '835', 'ICSSR, DST, Industry, SERB', '37.95'],
        ['Total (5 Years)', '127', '4580', 'Multiple Agencies', '36.06']
    ]
    
    table1 = Table(year_data, colWidths=[1*inch, 1.3*inch, 1.5*inch, 2*inch, 1.2*inch])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4e6f1')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(table1)
    story.append(Spacer(1, 0.2*inch))
    
    # Table 2: Funding Agency-wise Breakdown (NAAC 3.2.1 - funding_agencies, funding_amount, project_count)
    story.append(Paragraph("Table 2: Funding Agency-wise Distribution", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    agency_data = [
        ['Funding Agency', 'Projects', 'Total Funding (INR Lakhs)', 'Percentage', 'Key Research Areas'],
        ['DST (Dept of Science & Technology)', '38', '1580', '34.5%', 'AI, Renewable Energy, Materials'],
        ['SERB (Science & Engg Research Board)', '32', '1240', '27.1%', 'Nanotech, Biotech, Computing'],
        ['DBT (Dept of Biotechnology)', '24', '890', '19.4%', 'Genomics, Drug Discovery, Agri-biotech'],
        ['ICSSR (Indian Council Social Science)', '18', '520', '11.4%', 'Economics, Sociology, Policy'],
        ['Industry & Corporate Partners', '15', '350', '7.6%', 'Applied Research, Product Dev'],
        ['Total', '127', '4580', '100%', 'Multi-disciplinary Research']
    ]
    
    table2 = Table(agency_data, colWidths=[2*inch, 0.8*inch, 1.3*inch, 1*inch, 1.9*inch])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4e6f1')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(table2)
    story.append(Spacer(1, 0.2*inch))
    
    # Page break for more tables
    story.append(PageBreak())
    
    # Table 3: Major Research Projects (Detailed evidence)
    story.append(Paragraph("Table 3: Major Extramural Funded Research Projects (Sample)", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    projects_data = [
        ['Project Title', 'PI/Dept', 'Agency', 'Amount (INR Lakhs)', 'Duration', 'Year'],
        ['AI-Driven Healthcare Diagnostics', 'Dr. Sharma/CSE', 'DST', '85', '3 years', '2021-22'],
        ['Sustainable Solar Energy Systems', 'Dr. Patel/EE', 'SERB', '72', '2 years', '2020-21'],
        ['Genomic Crop Improvement', 'Dr. Kumar/Biotech', 'DBT', '95', '4 years', '2019-20'],
        ['Smart City Urban Planning', 'Dr. Singh/Civil', 'ICSSR', '45', '2 years', '2022-23'],
        ['Industrial IoT Applications', 'Dr. Reddy/ECE', 'Industry', '60', '2 years', '2021-22'],
        ['Nanomaterials for Water Purification', 'Dr. Gupta/Chem', 'DST', '68', '3 years', '2020-21'],
        ['Machine Learning for Agriculture', 'Dr. Verma/CSE', 'SERB', '55', '2 years', '2022-23'],
        ['Biofuel Production Technology', 'Dr. Rao/Biotech', 'DBT', '78', '3 years', '2021-22'],
        ['Social Media Impact Study', 'Dr. Mehta/Sociology', 'ICSSR', '42', '2 years', '2023-24'],
        ['Robotics for Manufacturing', 'Dr. Joshi/Mech', 'Industry', '65', '2 years', '2022-23'],
    ]
    
    table3 = Table(projects_data, colWidths=[2*inch, 1.3*inch, 0.9*inch, 1*inch, 0.9*inch, 0.9*inch])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(table3)
    story.append(Spacer(1, 0.2*inch))
    
    # Table 4: Department-wise Distribution
    story.append(Paragraph("Table 4: Department-wise Research Funding Distribution", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    dept_data = [
        ['Department', 'Projects', 'Funding (INR Lakhs)', 'Primary Agencies', 'Success Rate'],
        ['Computer Science & Engineering', '28', '1240', 'DST, SERB, Industry', '82%'],
        ['Biotechnology', '22', '980', 'DBT, DST, SERB', '78%'],
        ['Electrical Engineering', '18', '720', 'DST, SERB, Industry', '75%'],
        ['Mechanical Engineering', '15', '580', 'DST, Industry', '71%'],
        ['Civil Engineering', '12', '450', 'DST, ICSSR', '68%'],
        ['Chemistry', '10', '380', 'DST, SERB', '72%'],
        ['Physics', '8', '290', 'DST, SERB', '70%'],
        ['Social Sciences', '14', '540', 'ICSSR, DST', '76%'],
        ['Total', '127', '4580', 'Multiple', '75%']
    ]
    
    table4 = Table(dept_data, colWidths=[2.2*inch, 0.9*inch, 1.2*inch, 1.8*inch, 1*inch])
    table4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4e6f1')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(table4)
    story.append(Spacer(1, 0.2*inch))
    
    # Table 5: Research Output and Impact
    story.append(Paragraph("Table 5: Research Output from Extramural Funded Projects", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    output_data = [
        ['Output Type', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24', 'Total'],
        ['Research Publications (Scopus)', '82', '95', '108', '92', '88', '465'],
        ['Patents Filed', '4', '6', '8', '5', '4', '27'],
        ['PhD Scholars Supported', '18', '22', '26', '24', '20', '110'],
        ['Industry Collaborations', '3', '4', '5', '4', '3', '19'],
        ['Technology Transfers', '1', '2', '3', '2', '1', '9'],
        ['International Collaborations', '5', '7', '9', '8', '6', '35'],
    ]
    
    table5 = Table(output_data, colWidths=[2*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch])
    table5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('BACKGROUND', (-1, 1), (-1, -1), colors.HexColor('#d4e6f1')),
        ('FONTNAME', (-1, 1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(table5)
    
    doc.build(story)
    print(f"✓ Created: {output_path}")
    return output_path



def create_poor_table_heavy_ssr():
    """Create an SSR with incomplete/vague tables for poor alignment"""
    output_path = Path(__file__).parent.parent / "data" / "raw_docs" / "Struggling_College_C_SSR.pdf"
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=1
    )
    
    story.append(Paragraph("Struggling College", title_style))
    story.append(Paragraph("Self Study Report - NAAC Accreditation", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Criterion Header
    story.append(Paragraph("Criterion 3.2.1: Extramural Funding for Research", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))
    
    # Vague intro
    intro = """
    The college has been making efforts to secure external research funding. Faculty members 
    are encouraged to apply for grants from various agencies. We are committed to improving 
    our research infrastructure and capabilities.
    """
    story.append(Paragraph(intro, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Table 1: Vague year-wise data (missing amounts and specifics)
    story.append(Paragraph("Table 1: Research Funding Status", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    vague_year_data = [
        ['Year', 'Status', 'Remarks'],
        ['2019-20', 'Some projects funded', 'Applied to various agencies'],
        ['2020-21', 'Proposals submitted', 'Awaiting approval'],
        ['2021-22', 'Received grants', 'Details being compiled'],
        ['2022-23', 'Ongoing projects', 'Under review'],
        ['2023-24', 'Applications in process', 'Expected funding'],
    ]
    
    table1 = Table(vague_year_data, colWidths=[1.5*inch, 2.5*inch, 3*inch])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(table1)
    story.append(Spacer(1, 0.2*inch))
    
    # Table 2: Generic activities (no funding data)
    story.append(Paragraph("Table 2: Research Activities", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    activities_data = [
        ['Activity', 'Description'],
        ['Faculty Training', 'Workshops conducted on grant writing'],
        ['Proposal Development', 'Faculty assisted in preparing proposals'],
        ['Research Committee', 'Regular meetings held to discuss funding'],
        ['Collaborations', 'Exploring partnerships with institutions'],
        ['Infrastructure', 'Planning to upgrade research facilities'],
    ]
    
    table2 = Table(activities_data, colWidths=[2*inch, 5*inch])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table2)
    story.append(Spacer(1, 0.2*inch))
    
    # Table 3: Future plans (no actual data)
    story.append(Paragraph("Table 3: Future Research Funding Plans", styles['Heading3']))
    story.append(Spacer(1, 0.1*inch))
    
    future_data = [
        ['Plan', 'Timeline', 'Expected Outcome'],
        ['Apply to DST', '2024-25', 'Hoping for approval'],
        ['Industry partnerships', 'Ongoing', 'Under discussion'],
        ['Faculty development', '2024-25', 'Training programs planned'],
        ['Research infrastructure', '2025-26', 'Budget allocation pending'],
    ]
    
    table3 = Table(future_data, colWidths=[2.5*inch, 1.5*inch, 3*inch])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(table3)
    story.append(Spacer(1, 0.2*inch))
    
    # Closing note
    closing = """
    <b>Note:</b> The college is in the process of compiling detailed funding information. 
    Complete quantitative data will be provided in subsequent reports. We are committed to 
    improving our research output and securing more extramural funding in the coming years.
    """
    story.append(Paragraph(closing, styles['BodyText']))
    
    doc.build(story)
    print(f"✓ Created: {output_path}")
    return output_path


if __name__ == "__main__":
    print("\n" + "="*70)
    print("CREATING TABLE-HEAVY DEMO SSR PDFs FOR NAAC 3.2.1")
    print("="*70 + "\n")
    
    excellent_path = create_excellent_table_heavy_ssr()
    poor_path = create_poor_table_heavy_ssr()
    
    print("\n" + "="*70)
    print("TABLE-HEAVY DEMO PDFs CREATED SUCCESSFULLY")
    print("="*70)
    print(f"\n1. Excellent Alignment (A+ Grade Expected):")
    print(f"   {excellent_path.name}")
    print(f"   - 5 detailed tables with 40+ rows of data")
    print(f"   - Complete: Amounts (INR 4580 Lakhs), Projects (127), Agencies (DST, SERB, DBT, ICSSR, Industry)")
    print(f"   - Year-wise breakdown (2019-2024)")
    print(f"   - Department-wise, Project-wise, Output data")
    
    print(f"\n2. Poor Alignment (C Grade Expected):")
    print(f"   {poor_path.name}")
    print(f"   - 3 vague tables with generic information")
    print(f"   - Missing: Specific amounts, project counts, agency names")
    print(f"   - Only status updates and future plans")
    print(f"   - No quantitative evidence")
    print("\n")
