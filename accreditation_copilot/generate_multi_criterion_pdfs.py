"""
Generate comprehensive test PDFs covering multiple NAAC criteria
Based on real NAAC documentation structure (like Chitkara University)
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from pathlib import Path


def create_comprehensive_a_plus_ssr():
    """
    Generate A+ grade SSR covering all 7 NAAC criteria
    Based on Chitkara University structure (CGPA 3.26, Grade A+)
    """
    output_path = Path("D:/NAAC_Test_PDFs") / "Comprehensive_University_A+_SSR.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=1*inch, bottomMargin=0.75*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    criterion_style = ParagraphStyle(
        'CriterionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Cover Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("<b>NAAC Self Study Report</b>", title_style))
    story.append(Paragraph("<b>Excellence University</b>", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Institutional Assessment and Accreditation", styles['Normal']))
    story.append(Paragraph("Cycle: 1 | Year: 2024", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<b>Expected Grade: A+</b>", styles['Heading3']))
    story.append(PageBreak())
    
    # ========== CRITERION 1: CURRICULAR ASPECTS ==========
    story.append(Paragraph("<b>CRITERION 1: CURRICULAR ASPECTS</b>", criterion_style))
    story.append(Spacer(1, 12))
    
    # 1.2.1 - Curriculum Enrichment
    story.append(Paragraph("<b>1.2.1: Certificate/Add-on Programs</b>", styles['Heading3']))
    story.append(Paragraph("""
    The university offers 45 certificate and add-on programs aligned with industry requirements.
    These programs enhance student employability and provide specialized skills.
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    table_121_data = [
        ['Year', 'Certificate Programs', 'Add-on Programs', 'Students Enrolled', 'Completion Rate'],
        ['2019-20', '8', '4', '450', '92%'],
        ['2020-21', '10', '5', '580', '94%'],
        ['2021-22', '12', '6', '720', '95%'],
        ['2022-23', '14', '7', '890', '96%'],
        ['2023-24', '16', '8', '1050', '97%'],
    ]
    
    table_121 = Table(table_121_data, colWidths=[1.2*inch, 1.5*inch, 1.3*inch, 1.5*inch, 1.2*inch])
    table_121.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_121)
    story.append(Spacer(1, 20))
    
    # ========== CRITERION 2: TEACHING-LEARNING AND EVALUATION ==========
    story.append(Paragraph("<b>CRITERION 2: TEACHING-LEARNING AND EVALUATION</b>", criterion_style))
    story.append(Spacer(1, 12))
    
    # 2.1.1 - Student Enrollment
    story.append(Paragraph("<b>2.1.1: Average Enrollment Percentage</b>", styles['Heading3']))
    story.append(Paragraph("""
    The university maintains high enrollment rates with an average of 95% seats filled across all programs.
    Demand ratio: 3.5 applications per seat.
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    table_211_data = [
        ['Year', 'Sanctioned Intake', 'Students Admitted', 'Enrollment %', 'Applications Received'],
        ['2019-20', '2500', '2380', '95.2%', '8750'],
        ['2020-21', '2600', '2470', '95.0%', '9100'],
        ['2021-22', '2700', '2565', '95.0%', '9450'],
        ['2022-23', '2800', '2660', '95.0%', '9800'],
        ['2023-24', '2900', '2755', '95.0%', '10150'],
    ]
    
    table_211 = Table(table_211_data, colWidths=[1.2*inch, 1.4*inch, 1.4*inch, 1.2*inch, 1.5*inch])
    table_211.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_211)
    story.append(PageBreak())
    
    # ========== CRITERION 3: RESEARCH, INNOVATIONS AND EXTENSION ==========
    story.append(Paragraph("<b>CRITERION 3: RESEARCH, INNOVATIONS AND EXTENSION</b>", criterion_style))
    story.append(Spacer(1, 12))
    
    # 3.2.1 - Extramural Funding
    story.append(Paragraph("<b>3.2.1: Extramural Funding for Research</b>", styles['Heading3']))
    story.append(Paragraph("""
    Total extramural funding: INR 4580 Lakhs from 127 projects over 5 years.
    Major funding agencies: DST, SERB, DBT, ICSSR, Industry partners.
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    table_321_data = [
        ['Year', 'Projects', 'Funding (₹ Lakhs)', 'Agencies', 'Avg/Project'],
        ['2019-20', '22', '785', 'DST, SERB, DBT, Industry', '35.68'],
        ['2020-21', '28', '920', 'SERB, DBT, ICSSR, DST', '32.86'],
        ['2021-22', '31', '1150', 'DST, SERB, Industry', '37.10'],
        ['2022-23', '24', '890', 'DBT, DST, SERB, ICSSR', '37.08'],
        ['2023-24', '22', '835', 'ICSSR, DST, Industry', '37.95'],
        ['<b>Total</b>', '<b>127</b>', '<b>4580</b>', '<b>Multiple</b>', '<b>36.06</b>'],
    ]
    
    table_321 = Table(table_321_data, colWidths=[1.2*inch, 1.2*inch, 1.5*inch, 2*inch, 1.2*inch])
    table_321.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d0d0d0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_321)
    story.append(Spacer(1, 20))
    
    # 3.3.1 - Research Publications
    story.append(Paragraph("<b>3.3.1: Research Publications in UGC CARE Journals</b>", styles['Heading3']))
    story.append(Paragraph("""
    Total publications: 485 papers in UGC CARE listed journals.
    Average per teacher: 3.2 publications over 5 years.
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    table_331_data = [
        ['Year', 'Faculty Count', 'Publications', 'Per Teacher', 'Impact Factor Range'],
        ['2019-20', '145', '88', '0.61', '0.5 - 4.2'],
        ['2020-21', '148', '92', '0.62', '0.6 - 4.5'],
        ['2021-22', '152', '105', '0.69', '0.7 - 5.1'],
        ['2022-23', '155', '98', '0.63', '0.6 - 4.8'],
        ['2023-24', '158', '102', '0.65', '0.7 - 5.3'],
        ['<b>Total</b>', '<b>158</b>', '<b>485</b>', '<b>3.07</b>', '<b>-</b>'],
    ]
    
    table_331 = Table(table_331_data, colWidths=[1.2*inch, 1.3*inch, 1.3*inch, 1.2*inch, 1.8*inch])
    table_331.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d0d0d0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_331)
    story.append(Spacer(1, 20))
    
    # 3.4.1 - Extension Activities
    story.append(Paragraph("<b>3.4.1: Extension and Outreach Activities</b>", styles['Heading3']))
    story.append(Paragraph("""
    The university conducted 285 extension activities reaching 45,000+ beneficiaries.
    Focus areas: Health camps, skill development, environmental awareness, digital literacy.
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    table_341_data = [
        ['Year', 'Activities', 'Beneficiaries', 'Villages Adopted', 'Student Participation'],
        ['2019-20', '52', '8200', '12', '1850'],
        ['2020-21', '48', '7500', '12', '1650'],
        ['2021-22', '58', '9500', '15', '2100'],
        ['2022-23', '62', '10200', '15', '2250'],
        ['2023-24', '65', '10600', '18', '2400'],
        ['<b>Total</b>', '<b>285</b>', '<b>46000</b>', '<b>18</b>', '<b>10250</b>'],
    ]
    
    table_341 = Table(table_341_data, colWidths=[1.2*inch, 1.2*inch, 1.4*inch, 1.5*inch, 1.8*inch])
    table_341.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d0d0d0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_341)
    story.append(PageBreak())
    
    # ========== CRITERION 4: INFRASTRUCTURE AND LEARNING RESOURCES ==========
    story.append(Paragraph("<b>CRITERION 4: INFRASTRUCTURE AND LEARNING RESOURCES</b>", criterion_style))
    story.append(Spacer(1, 12))
    
    # 4.1.2 - Physical Facilities
    story.append(Paragraph("<b>4.1.2: Facilities for Cultural and Sports Activities</b>", styles['Heading3']))
    story.append(Paragraph("""
    The university has comprehensive facilities including auditorium (1500 capacity), sports complex,
    gymnasium, indoor stadium, and dedicated spaces for cultural activities.
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    facilities_data = [
        ['Facility Type', 'Count', 'Capacity', 'Utilization %', 'Annual Events'],
        ['Auditoriums', '3', '2500 total', '85%', '120'],
        ['Sports Grounds', '5', '500 students', '90%', '45'],
        ['Indoor Stadium', '1', '300 students', '80%', '35'],
        ['Gymnasium', '2', '150 students', '95%', 'Daily'],
        ['Cultural Halls', '4', '800 total', '75%', '80'],
        ['Seminar Halls', '12', '1200 total', '88%', '250'],
    ]
    
    table_412 = Table(facilities_data, colWidths=[1.8*inch, 1*inch, 1.3*inch, 1.3*inch, 1.5*inch])
    table_412.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_412)
    story.append(Spacer(1, 20))
    
    # ========== CRITERION 5: STUDENT SUPPORT AND PROGRESSION ==========
    story.append(Paragraph("<b>CRITERION 5: STUDENT SUPPORT AND PROGRESSION</b>", criterion_style))
    story.append(Spacer(1, 12))
    
    # 5.1.1 - Scholarships
    story.append(Paragraph("<b>5.1.1: Scholarships and Financial Support</b>", styles['Heading3']))
    story.append(Paragraph("""
    Total scholarships disbursed: INR 285 Lakhs to 3,450 students over 5 years.
    Sources: Government schemes, institutional merit scholarships, need-based support.
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    scholarship_data = [
        ['Year', 'Students Benefited', 'Amount (₹ Lakhs)', 'Govt Schemes', 'Institutional'],
        ['2019-20', '620', '52', '380', '240'],
        ['2020-21', '680', '58', '420', '260'],
        ['2021-22', '720', '62', '450', '270'],
        ['2022-23', '710', '56', '440', '270'],
        ['2023-24', '720', '57', '445', '275'],
        ['<b>Total</b>', '<b>3450</b>', '<b>285</b>', '<b>2135</b>', '<b>1315</b>'],
    ]
    
    table_511 = Table(scholarship_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 1.3*inch, 1.3*inch])
    table_511.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d0d0d0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_511)
    story.append(PageBreak())
    
    # ========== CRITERION 6: GOVERNANCE, LEADERSHIP AND MANAGEMENT ==========
    story.append(Paragraph("<b>CRITERION 6: GOVERNANCE, LEADERSHIP AND MANAGEMENT</b>", criterion_style))
    story.append(Spacer(1, 12))
    
    # 6.2.2 - E-Governance
    story.append(Paragraph("<b>6.2.2: Implementation of E-Governance</b>", styles['Heading3']))
    story.append(Paragraph("""
    The university has implemented comprehensive e-governance across all operations:
    Administration, Finance, Student Admission, Examination, Library, and HR Management.
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    egovernance_data = [
        ['Module', 'Implementation Year', 'Coverage %', 'Users', 'Transactions/Year'],
        ['Administration', '2018', '100%', '250', '15000'],
        ['Finance & Accounts', '2018', '100%', '180', '25000'],
        ['Student Admission', '2019', '100%', '3000', '8000'],
        ['Examination', '2019', '100%', '3200', '12000'],
        ['Library Management', '2020', '100%', '3500', '50000'],
        ['HR & Payroll', '2020', '100%', '450', '6000'],
    ]
    
    table_622 = Table(egovernance_data, colWidths=[1.8*inch, 1.3*inch, 1.2*inch, 1*inch, 1.5*inch])
    table_622.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_622)
    story.append(Spacer(1, 20))
    
    # ========== CRITERION 7: INSTITUTIONAL VALUES AND BEST PRACTICES ==========
    story.append(Paragraph("<b>CRITERION 7: INSTITUTIONAL VALUES AND BEST PRACTICES</b>", criterion_style))
    story.append(Spacer(1, 12))
    
    # 7.1.2 - Environmental Initiatives
    story.append(Paragraph("<b>7.1.2: Environmental Sustainability Initiatives</b>", styles['Heading3']))
    story.append(Paragraph("""
    The university has implemented comprehensive green initiatives:
    Solar power (500 KW), rainwater harvesting, waste management, green campus (60% green cover).
    """, styles['Normal']))
    story.append(Spacer(1, 6))
    
    green_data = [
        ['Initiative', 'Implementation', 'Capacity/Coverage', 'Annual Savings', 'Impact'],
        ['Solar Power', '2019', '500 KW', '₹45 Lakhs', '40% energy from solar'],
        ['Rainwater Harvesting', '2018', '15 units', '8 ML water', '30% water needs met'],
        ['Waste Management', '2020', '100% campus', '₹12 Lakhs', 'Zero waste to landfill'],
        ['Green Cover', 'Ongoing', '60% area', '-', 'Carbon neutral campus'],
        ['LED Lighting', '2019', '100% campus', '₹18 Lakhs', '60% energy savings'],
        ['E-Vehicles', '2021', '12 vehicles', '₹8 Lakhs', 'Reduced emissions'],
    ]
    
    table_712 = Table(green_data, colWidths=[1.5*inch, 1.2*inch, 1.4*inch, 1.2*inch, 1.5*inch])
    table_712.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(table_712)
    story.append(Spacer(1, 20))
    
    # Summary
    story.append(PageBreak())
    story.append(Paragraph("<b>SUMMARY OF INSTITUTIONAL PERFORMANCE</b>", criterion_style))
    story.append(Spacer(1, 12))
    
    summary_text = """
    Excellence University demonstrates outstanding performance across all seven NAAC criteria:
    
    • Criterion 1 (Curricular Aspects): 45 certificate/add-on programs with 97% completion rate
    • Criterion 2 (Teaching-Learning): 95% enrollment rate with 3.5:1 demand ratio
    • Criterion 3 (Research): ₹4580 Lakhs research funding, 485 publications, 285 extension activities
    • Criterion 4 (Infrastructure): Comprehensive facilities with 85%+ utilization
    • Criterion 5 (Student Support): ₹285 Lakhs scholarships to 3,450 students
    • Criterion 6 (Governance): 100% e-governance implementation across all modules
    • Criterion 7 (Institutional Values): Carbon neutral campus with 60% green cover
    
    The university's systematic approach to quality enhancement, strong research culture, 
    comprehensive student support, and commitment to sustainability position it for A+ accreditation.
    """
    
    story.append(Paragraph(summary_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✓ Created: {output_path.name} (Grade A+ - Comprehensive)")
    return output_path


if __name__ == "__main__":
    print("\n" + "="*80)
    print("GENERATING COMPREHENSIVE MULTI-CRITERION TEST PDF")
    print("="*80 + "\n")
    
    pdf_path = create_comprehensive_a_plus_ssr()
    
    print("\n" + "="*80)
    print("COMPREHENSIVE TEST PDF CREATED SUCCESSFULLY!")
    print("="*80)
    print(f"\nSaved to: {pdf_path}")
    print("\nThis PDF covers all 7 NAAC criteria:")
    print("  1. Curricular Aspects (1.2.1)")
    print("  2. Teaching-Learning (2.1.1)")
    print("  3. Research & Extension (3.2.1, 3.3.1, 3.4.1)")
    print("  4. Infrastructure (4.1.2)")
    print("  5. Student Support (5.1.1)")
    print("  6. Governance (6.2.2)")
    print("  7. Institutional Values (7.1.2)")
    print("\nExpected Grade: A+ (85%+ confidence across all criteria)")
    print("\nUpload this PDF to test multiple criteria audits!")
