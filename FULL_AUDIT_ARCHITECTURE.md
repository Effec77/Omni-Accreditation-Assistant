# Full NAAC Audit - System Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│                    (Frontend - Next.js/React)                        │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 1. Upload SSR PDF
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FILE UPLOAD ENDPOINT                            │
│                   POST /api/upload/                                  │
│                   POST /api/upload/ingest                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 2. Process & Store
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      VECTOR DATABASE                                 │
│                   (FAISS + SQLite)                                   │
│                                                                       │
│  • Institution Chunks: SSR document content                          │
│  • Framework Chunks: NAAC/NBA criteria documents                     │
│  • Embeddings: Vector representations for semantic search            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 3. Click "Run Full NAAC Audit"
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   FULL AUDIT ENDPOINT                                │
│              POST /api/audit/run-full-audit                          │
│                                                                       │
│  Orchestrates evaluation of all 11 NAAC criteria                    │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 4. For each criterion (1.2.1, 2.1.1, ...)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   CRITERION AUDITOR                                  │
│              (audit/criterion_auditor.py)                            │
│                                                                       │
│  Step 1: Retrieve relevant chunks from vector DB                    │
│  Step 2: Compare institution vs framework evidence                  │
│  Step 3: Calculate confidence score (0-1)                            │
│  Step 4: Identify gaps and missing dimensions                       │
│  Step 5: Generate recommendations                                    │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 5. Collect all criterion results
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   NAAC GRADING CALCULATOR                            │
│              (scoring/naac_grading.py)                               │
│                                                                       │
│  Step 1: Group results by main criterion (1, 2, 3, ...)             │
│  Step 2: Convert confidence scores to grade points (0-4)            │
│  Step 3: Calculate average grade points per criterion               │
│  Step 4: Apply NAAC weights:                                        │
│          • Criterion 1: 100 points                                   │
│          • Criterion 2: 350 points ⭐ HIGHEST                        │
│          • Criterion 3: 200 points                                   │
│          • Criterion 4: 100 points                                   │
│          • Criterion 5: 100 points                                   │
│          • Criterion 6: 100 points                                   │
│          • Criterion 7: 50 points                                    │
│  Step 5: Calculate weighted CGPA (0-4 scale)                        │
│  Step 6: Map CGPA to letter grade (A++, A+, A, ...)                 │
│  Step 7: Generate improvement suggestions                           │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 6. Return comprehensive result
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   FULL AUDIT DASHBOARD                               │
│          (frontend/components/FullAuditDashboard.tsx)                │
│                                                                       │
│  Displays:                                                           │
│  • Overall CGPA and letter grade                                     │
│  • Accreditation status                                              │
│  • Criterion-wise breakdown with weights                             │
│  • Progress bars and visualizations                                  │
│  • Improvement roadmap                                               │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Document Ingestion Phase
```
SSR PDF → PDF Parser → Text Chunks → Embeddings → Vector DB
                                                      ↓
                                            (Institution Chunks)
```

### 2. Criterion Evaluation Phase (per criterion)
```
Query Template → Vector Search → Retrieve Chunks → LLM Analysis → Confidence Score
                      ↓                                                    ↓
              Framework Chunks                                    Gap Analysis
              Institution Chunks                                  Recommendations
```

### 3. CGPA Calculation Phase
```
11 Criterion Results → Group by Main Criterion → Average Grade Points
                              ↓
                    Apply NAAC Weights (1000 points)
                              ↓
                    Calculate Weighted Average
                              ↓
                    CGPA (0-4 scale) → Letter Grade
```

## Component Responsibilities

### Backend Components

#### 1. Criterion Auditor (`audit/criterion_auditor.py`)
- **Input**: Criterion ID, framework, query template
- **Process**: 
  - Retrieves relevant chunks using semantic search
  - Compares institution evidence vs framework requirements
  - Calculates confidence score based on evidence quality
  - Identifies gaps and missing dimensions
- **Output**: Audit result with confidence score, gaps, recommendations

#### 2. NAAC Grading Calculator (`scoring/naac_grading.py`)
- **Input**: List of criterion audit results
- **Process**:
  - Groups results by main criterion (1-7)
  - Converts confidence scores to grade points
  - Applies official NAAC weights
  - Calculates weighted CGPA
  - Maps CGPA to letter grade
- **Output**: Overall CGPA, letter grade, breakdown, suggestions

#### 3. Audit Router (`api/routers/audit.py`)
- **Endpoints**:
  - `GET /api/audit/criteria/{framework}` - List available criteria
  - `POST /api/audit/run` - Run single criterion audit
  - `POST /api/audit/run-full-audit` - Run full NAAC audit
- **Responsibilities**:
  - Orchestrates audit execution
  - Handles caching
  - Standardizes responses
  - Error handling

### Frontend Components

#### 1. Query Panel (`components/QueryPanel.tsx`)
- **Features**:
  - Framework selection (NAAC/NBA)
  - Multi-criterion dropdown with search
  - File upload with auto-ingestion
  - "Run Audit" button (single/multi-criterion)
  - "Run Full NAAC Audit" button (all criteria)
- **State Management**:
  - Tracks uploaded files
  - Manages ingestion status
  - Handles loading states

#### 2. Full Audit Dashboard (`components/FullAuditDashboard.tsx`)
- **Sections**:
  - Overall grade card (CGPA, letter grade, status)
  - Summary statistics
  - Improvement roadmap
  - Criterion-wise breakdown with metrics
- **Visualizations**:
  - Progress bars for each criterion
  - Color-coded grades (green=A, yellow=B, red=C)
  - Animated transitions

#### 3. Main Page (`app/page.tsx`)
- **Routing Logic**:
  - Detects `is_full_audit` flag
  - Renders FullAuditDashboard for full audits
  - Renders AuditDashboard for single/multi-criterion
- **State Management**:
  - Manages audit results
  - Handles loading states
  - Authentication checks

## Key Algorithms

### Confidence to Grade Points Conversion
```python
def confidence_to_grade_points(confidence: float) -> float:
    if confidence >= 0.85:
        return 4.0
    elif confidence >= 0.70:
        return 3.0 + (confidence - 0.70) / 0.15
    elif confidence >= 0.55:
        return 2.0 + (confidence - 0.55) / 0.15
    elif confidence >= 0.40:
        return 1.0 + (confidence - 0.40) / 0.15
    else:
        return confidence / 0.40
```

### Weighted CGPA Calculation
```python
def calculate_weighted_cgpa(criterion_averages: dict) -> float:
    total_weighted_points = 0.0
    total_weight = 0
    
    for criterion, avg_grade_points in criterion_averages.items():
        weight = NAAC_CRITERION_WEIGHTS[criterion]
        total_weighted_points += avg_grade_points * weight
        total_weight += weight
    
    cgpa = total_weighted_points / total_weight
    return cgpa
```

### Grade Mapping
```python
GRADE_RANGES = [
    (3.51, 4.00, "A++", "Outstanding"),
    (3.26, 3.50, "A+", "Excellent"),
    (3.01, 3.25, "A", "Very Good"),
    (2.76, 3.00, "B++", "Good"),
    (2.51, 2.75, "B+", "Above Average"),
    (2.01, 2.50, "B", "Average"),
    (1.51, 2.00, "C", "Below Average"),
    (0.00, 1.50, "D", "Poor"),
]
```

## Performance Characteristics

### Time Complexity
- **Single Criterion Audit**: O(n) where n = number of chunks retrieved
- **Full NAAC Audit**: O(11 * n) = O(n) - linear in number of criteria
- **CGPA Calculation**: O(k) where k = number of criteria (constant, k=11)

### Space Complexity
- **Vector DB**: O(m) where m = total chunks (institution + framework)
- **Audit Results**: O(k) where k = number of criteria
- **Frontend State**: O(k) - stores results for all criteria

### Typical Execution Times
- **Single Criterion**: 10-30 seconds
- **Full NAAC Audit**: 2-5 minutes (11 criteria × 10-30 seconds)
- **CGPA Calculation**: < 1 second
- **Frontend Rendering**: < 1 second

## Scalability Considerations

### Current Limitations
- Sequential criterion evaluation (not parallelized)
- Single-threaded LLM inference
- In-memory result storage

### Future Optimizations
1. **Parallel Evaluation**: Run multiple criteria in parallel
2. **Batch Processing**: Group similar queries for efficiency
3. **Result Caching**: Cache criterion results to avoid re-evaluation
4. **Incremental Updates**: Only re-evaluate changed criteria

## Security & Privacy

### Data Protection
- All data stored locally (no external transmission)
- Vector embeddings are anonymized representations
- No PII stored in vector DB

### Access Control
- Frontend authentication required
- API endpoints protected by CORS
- File uploads validated for type and size

## Error Handling

### Backend
- Graceful degradation if criterion fails
- Continues with remaining criteria
- Logs errors for debugging
- Returns partial results if available

### Frontend
- Loading states during long operations
- Error messages for failed requests
- Retry mechanisms for transient failures
- Fallback UI for missing data

## Monitoring & Logging

### Backend Logs
```
[FULL AUDIT START] Running comprehensive NAAC audit
[FULL AUDIT] Processing criterion 1.2.1
[FULL AUDIT] Processing criterion 2.1.1
...
[FULL AUDIT COMPLETE] CGPA: 3.42, Grade: A+
```

### Frontend Logs
```
[QueryPanel] Starting full audit
[QueryPanel] Full audit completed
[FullAuditDashboard] Rendering results for 11 criteria
```

## Testing Strategy

### Unit Tests
- Test CGPA calculation with known inputs
- Test grade mapping edge cases
- Test confidence to grade points conversion

### Integration Tests
- Test full audit endpoint with mock data
- Test criterion auditor with sample documents
- Test frontend rendering with various results

### End-to-End Tests
- Upload SSR → Ingest → Run Full Audit → Verify Results
- Test with different document qualities
- Test with edge cases (all A+, all C, mixed)

---

This architecture ensures:
- ✅ Accurate NAAC grading using official weights
- ✅ Comprehensive evaluation of all criteria
- ✅ Clear visualization of results
- ✅ Actionable improvement suggestions
- ✅ Scalable and maintainable codebase
