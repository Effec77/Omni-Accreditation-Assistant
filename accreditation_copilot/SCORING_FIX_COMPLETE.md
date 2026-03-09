# Scoring System Fix - Complete

## Problem Identified
The backend scoring system was giving low confidence scores (28%) for Excellence University despite having good evidence. The UI was correctly displaying the data, but the backend scoring logic had multiple issues.

## Root Causes

### 1. Generic Query Template
**Issue**: The query template for NAAC 3.2.1 was too generic: "research funding grants from government and non-governmental agencies"

**Impact**: The reranker was scoring NAAC manual chunks higher than institution evidence because the query matched the manual's description better than actual data.

**Fix**: Updated query to be more data-oriented: "extramural research funding amount lakhs projects DST SERB DBT ICSSR government agencies year-wise"

**File**: `criteria/criterion_registry.py`

### 2. Currency Pattern Matching
**Issue**: The evidence scorer's CURRENCY_PATTERN required "INR" or "Rs." prefix, but table cells only had numbers like "785 Lakhs"

**Impact**: Many chunks with valid funding data were not being recognized as having numeric evidence.

**Fix**: Updated CURRENCY_PATTERN to match "Funding: 1240 Lakhs" format without requiring currency prefix.

**File**: `scoring/evidence_scorer.py`

### 3. Project Count Pattern
**Issue**: PROJECT_COUNT_PATTERN only matched "14 projects" but not "Projects: 14" (table format)

**Impact**: Project count evidence was not being detected in table-formatted data.

**Fix**: Updated pattern to match both formats: `(projects?|grants?):\s*\d+|\d+\s+(projects?|grants?)`

**File**: `scoring/evidence_scorer.py`

### 4. Framework Chunks in Scoring
**Issue**: The confidence calculator was averaging ALL chunks (institution + framework), bringing scores down from 76.6% to 47%

**Impact**: Framework chunks (NAAC manual) were diluting the institution evidence scores.

**Fix**: Updated confidence calculator to filter to only institution chunks for scoring (framework chunks remain available for LLM context).

**File**: `scoring/confidence_calculator.py`

## Results

### Before Fix
- Confidence Score: 28%
- Compliance Status: Weak
- Avg Evidence Score: 0.000 (broken)
- Avg Retrieval Score: 0.000 (broken)

### After Fix
- **Confidence Score: 82.3%** ✅
- **Compliance Status: Compliant** ✅
- **Avg Evidence Score: 72.0%** ✅
- **Avg Retrieval Score: 97.7%** ✅
- **Coverage Ratio: 100%** (all dimensions covered) ✅

### Score Breakdown by Source Type

**Institution Chunks (Excellence University):**
- Average Reranker: 94.1%
- Average Evidence: 64.9%
- Average Combined: 76.6%

**Framework Chunks (NAAC Manual):**
- Average Reranker: 91.3%
- Average Evidence: 24.8% (correctly penalized with 0.6x multiplier)
- Average Combined: 51.4%

## Files Modified

1. `criteria/criterion_registry.py` - Updated query template for NAAC 3.2.1
2. `scoring/evidence_scorer.py` - Fixed CURRENCY_PATTERN and PROJECT_COUNT_PATTERN
3. `scoring/confidence_calculator.py` - Filter to only institution chunks for scoring
4. `scripts/create_table_heavy_pdfs.py` - Updated PDFs to use "INR Lakhs" in headers

## Testing

Run the following to verify:

```bash
# Clear cache and run audit
Remove-Item audit_results/cache_*.json -Force
python debug_audit.py
```

Expected output:
- Confidence Score: ~82%
- Compliance Status: Compliant
- All dimensions covered
- Top 5 evidence sources all from Excellence University

## Next Steps

1. ✅ Backend scoring fixed
2. ✅ Evidence detection improved
3. ✅ Query templates optimized
4. ✅ Framework/institution separation working
5. 🔄 UI already displays scores correctly - no changes needed
6. 🔄 Test with real institution data
7. 🔄 Verify other NAAC criteria work similarly

## Notes

- The system correctly retrieves the best evidence from ALL institutions in the database
- For institution-specific audits, ingest only that institution's data
- Framework chunks are still available for LLM context but don't affect scoring
- The 0.6x penalty for framework chunks is working as designed
