# Phase 1 Criterion Extraction Fix - Summary

## Problem Statement

The original Phase 1 ingestion had a criterion extraction bug where chunks were mislabeled with carryover criteria from previous sections. For example:
- Chunk containing "Weightage 3.2.1 QnM Extramural funding..." was labeled as "3.1.6" 
- This caused retrieval failures when users queried for specific criteria like "NAAC 3.2.1"

## Root Cause

The original extraction logic picked the **first criterion** found in chunk text, which was often carryover text from the previous section due to PDF chunking boundaries.

## Solution Implemented

### 1. Position-Based Scoring Strategy

Replaced the simple "first-valid-match-in-second-half" approach with a **position-based scoring system**:

```python
def extract_criterion_by_position(text: str, framework: str) -> str | None:
    # Collect all candidates with position scores
    candidates = []
    
    for match in re.finditer(pattern, text):
        candidate = match.group(1)
        
        # Skip if not relevant
        if not verify_criterion_relevance(text, candidate):
            continue
        
        # Calculate relevance score based on position
        position_score = 1.0 - (position / len(text))
        
        # Penalize reference contexts
        if is_reference:
            position_score *= 0.3
        
        candidates.append((candidate, position_score))
    
    # Return candidate with highest score
    if candidates:
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
```

### 2. Reference Context Detection

Added logic to detect and penalize criteria appearing in reference contexts:
- "as per", "as of", "refer", "see", "template", "data template"
- These get 0.3x penalty on position score

### 3. Relevance Verification

Kept the `verify_criterion_relevance()` function to ensure criteria are actually discussed:
- Must appear multiple times, OR
- Must appear once with evidence keywords (weightage, QnM, data required, etc.)

### 4. Embedding Enrichment

Added metadata prefix to embeddings for better discrimination:

```python
def prepare_text_for_embedding(chunk: Dict) -> str:
    prefix = f"Framework: {framework} | Criterion: {criterion} | Type: {doc_type} | Content: "
    return prefix + text
```

## Results

### Before Fix
```
Chunk ID: b09f1681-9066-425c-ac53-8d5e25d116ae
Label: 3.1.6  ❌ WRONG
Page: 64
Text: "Weightage 3.2.1 QnM Extramural funding for Research..."
```

### After Fix
```
Chunk ID: f0b09b1f-5d7b-4db2-be1c-ad6996876309
Label: 3.2.1  ✅ CORRECT
Page: 64
Text: "Weightage 3.2.1 QnM Extramural funding for Research..."
```

### Diagnostic Results

```
================================================================================
3.2.X CONTENT-LABEL ALIGNMENT CHECK
================================================================================

Found 3 chunks labeled with 3.2.x criteria
✓ 3.2.1 (page 64): Label matches content
✓ 3.2.2 (page 15): Label matches content
✓ 3.2.2 (page 64): Label matches content

✓ All 3.2.x chunks have aligned labels
```

### Retrieval Test Results

**NAAC 3.2.1 Query:**
- Before: Not in top-5 results
- After: Appears at rank 5 (criterion correctly extracted)

The chunk now appears in results, though not at rank 1 yet. This is a Phase 2 reranking issue, not a Phase 1 extraction issue.

## Files Modified

1. `accreditation_copilot/ingestion/semantic_chunker.py`
   - Updated `extract_criterion_by_position()` with position-based scoring
   - Updated `_chunk_naac()` to use new extraction
   - Updated `_chunk_nba()` to use new extraction

2. `accreditation_copilot/retrieval/index_builder.py`
   - Added `prepare_text_for_embedding()` function
   - Updated `build_index()` to use enriched text

3. `accreditation_copilot/tests/diagnostic_criterion_quality.py` (NEW)
   - Criterion distribution check
   - Content-label alignment verification
   - Keyword search regardless of label

## Key Improvements

1. ✅ **Correct criterion extraction** - 3.2.1 now properly labeled
2. ✅ **Reference context handling** - Penalizes criteria in "as per" contexts
3. ✅ **Position-based scoring** - Prefers criteria appearing early in chunk
4. ✅ **Embedding enrichment** - Better semantic discrimination
5. ✅ **Diagnostic tooling** - Can validate extraction quality

## Remaining Work

The Phase 1 fix is complete. The 3.2.1 chunk is now correctly labeled and appears in retrieval results. To get it to rank 1, Phase 2 reranking may need further tuning, but that's outside the scope of Phase 1 ingestion fixes.

## External PDF Path

**IMPORTANT:** PDFs are stored externally at:
```
D:/Accreditation Frameworks/NAAC/
D:/Accreditation Frameworks/NBA/
```

Run ingestion with:
```bash
python ingestion/run_ingestion.py \
  --naac-dir "D:/Accreditation Frameworks/NAAC" \
  --nba-dir "D:/Accreditation Frameworks/NBA"
```

## Validation

Run diagnostic after any ingestion:
```bash
python tests/diagnostic_criterion_quality.py
```

Expected output:
- ✓ All 3.2.x chunks have aligned labels
- ℹ️ 6 chunks contain '3.2.1' keyword
- At least one chunk labeled as '3.2.1'
