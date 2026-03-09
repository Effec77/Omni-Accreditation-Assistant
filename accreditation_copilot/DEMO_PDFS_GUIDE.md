# Demo PDFs Guide - NAAC Criterion 3.2.1

## Overview

Two demo Self Study Reports (SSRs) have been created to demonstrate the system's ability to evaluate institutional compliance with NAAC standards.

## Demo Files

### 1. Excellence_University_A+_SSR.pdf ✅
**Expected Grade: A+ (85-100% confidence)**

**What's Included:**
- ✅ Complete funding amount: INR 45.8 Crores (4580 Lakhs)
- ✅ Total projects: 127 funded projects
- ✅ Year-wise breakdown: 2019-2024 (5 years)
- ✅ Funding agencies: DST, SERB, DBT, ICSSR, Industry Partners
- ✅ Detailed table with quantitative data
- ✅ Agency-wise distribution with amounts

**NAAC 3.2.1 Dimensions Coverage:**
- `funding_amount`: ✅ Fully covered (INR 4580 Lakhs)
- `project_count`: ✅ Fully covered (127 projects)
- `funding_agencies`: ✅ Fully covered (5 major agencies)
- `time_period`: ✅ Fully covered (2019-2024)

**Expected System Response:**
- High confidence score (85-95%)
- Grade: A+
- Status: Compliant
- All dimensions marked as "covered"
- Strong evidence with high relevance scores
- Minimal or no recommendations

---

### 2. Struggling_College_C_SSR.pdf ❌
**Expected Grade: C (0-30% confidence)**

**What's Missing:**
- ❌ No specific funding amounts mentioned
- ❌ No project count provided
- ❌ No funding agency names specified
- ❌ Vague statements without data
- ❌ Incomplete table with generic entries
- ❌ No quantitative evidence

**NAAC 3.2.1 Dimensions Coverage:**
- `funding_amount`: ❌ Missing (no amounts specified)
- `project_count`: ❌ Missing (no numbers provided)
- `funding_agencies`: ❌ Missing (no agencies named)
- `time_period`: ⚠️ Partial (years mentioned but no data)

**Expected System Response:**
- Low confidence score (5-15%)
- Grade: C
- Status: Non-compliant or Partially Compliant
- Most dimensions marked as "missing"
- Weak evidence with low relevance scores
- Multiple critical recommendations

---

## Testing Instructions

### Step 1: Ingest the Demo PDFs

1. Start the backend and frontend servers
2. Go to the Dashboard
3. Upload both PDFs:
   - `Excellence_University_A+_SSR.pdf`
   - `Struggling_College_C_SSR.pdf`
4. Click "Ingest" to process them

### Step 2: Run Audits

**For Excellence University (Expected A+):**
1. Select Framework: NAAC
2. Select Criterion: 3.2.1
3. Click "Run Audit"
4. Observe:
   - Grade should be A or A+
   - Confidence score: 85-95%
   - All dimensions covered (green checkmarks)
   - Strong evidence with high relevance
   - Minimal recommendations

**For Struggling College (Expected C):**
1. Select Framework: NAAC
2. Select Criterion: 3.2.1
3. Click "Run Audit"
4. Observe:
   - Grade should be C
   - Confidence score: 5-15%
   - Most dimensions missing (red X marks)
   - Weak or no evidence
   - Multiple critical recommendations

---

## What the New UI Will Show

### For Excellence University (A+):
- **GradeCalculator**: Large "A+" badge in green
- **ConfidenceScoreVisualizer**: 85-95% with green progress bar
- **ComparisonComponent**: 
  - NAAC Requirements vs Institutional Evidence side-by-side
  - All dimensions with green checkmarks
- **EvidenceHumanizer**: 
  - "Strong Evidence" badges
  - Human-readable: "Relevance: 92%"
  - Source: "Excellence University A+ SSR"
- **RecommendationEngine**: 
  - "Excellent Work!" message
  - Or minor suggestions for improvement

### For Struggling College (C):
- **GradeCalculator**: Large "C" badge in red with "Weak" label
- **ConfidenceScoreVisualizer**: 5-15% with red progress bar and warning
- **ComparisonComponent**: 
  - Most dimensions with red X marks
  - "Critical: 3 Missing Dimensions" alert
- **EvidenceHumanizer**: 
  - "Weak Evidence" badges or no evidence
  - Low relevance scores
- **RecommendationEngine**: 
  - Critical priority recommendations
  - "Strengthen Evidence Base"
  - "Address 3 Missing Dimensions"
  - Specific action items for each gap

---

## Key Differences to Observe

| Aspect | Excellence University | Struggling College |
|--------|----------------------|-------------------|
| Grade | A+ (green) | C (red) |
| Confidence | 85-95% | 5-15% |
| Coverage | 100% (4/4 dimensions) | 0-25% (0-1/4 dimensions) |
| Evidence Quality | Strong (green badges) | Weak (red badges) |
| Recommendations | Minimal/None | Multiple Critical |
| Status | Compliant | Non-compliant |

---

## Regenerating Demo PDFs

To create new demo PDFs with different data:

```bash
cd accreditation_copilot
python scripts/create_demo_pdfs.py
```

The script will overwrite the existing demo PDFs with fresh versions.

---

## Notes

- These PDFs are specifically designed for NAAC Criterion 3.2.1 (Extramural Funding)
- The system should clearly differentiate between excellent and poor alignment
- All new UI components (GradeCalculator, EvidenceHumanizer, ComparisonComponent, RecommendationEngine) will be tested
- The demo showcases the system's ability to provide actionable, human-readable feedback
