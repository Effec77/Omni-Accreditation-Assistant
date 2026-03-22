# System Architecture - Omni Accreditation Copilot

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [File Structure](#file-structure)
6. [Frontend Architecture](#frontend-architecture)
7. [Backend Architecture](#backend-architecture)
8. [AI/ML Pipeline](#aiml-pipeline)
9. [Database Schema](#database-schema)
10. [API Design](#api-design)

---

## System Overview

The Omni Accreditation Copilot is a full-stack AI application built on a modern microservices-inspired architecture with clear separation of concerns.

### Architecture Principles
- **Modularity**: Each component has a single responsibility
- **Scalability**: Horizontal scaling through API key pooling and caching
- **Reliability**: Automatic fallback mechanisms (Groq → Ollama)
- **Security**: API keys protected, input sanitization, secure prompts
- **Performance**: GPU acceleration, vector indexing, intelligent caching

### System Layers
```
┌─────────────────────────────────────────────────────────┐
│  Presentation Layer (Next.js Frontend)                  │
├─────────────────────────────────────────────────────────┤
│  API Layer (FastAPI Backend)                            │
├─────────────────────────────────────────────────────────┤
│  Business Logic Layer (Audit Engine)                    │
├─────────────────────────────────────────────────────────┤
│  AI/ML Layer (Models & LLMs)                            │
├─────────────────────────────────────────────────────────┤
│  Data Layer (FAISS, SQLite, File System)                │
└─────────────────────────────────────────────────────────┘
```

---

## Architecture Layers

### 1. Presentation Layer (Frontend)
**Technology**: Next.js 14 with TypeScript, Tailwind CSS

**Components**:
- `FullAuditDashboard.tsx` - Main audit interface
- `CriteriaSelector.tsx` - Criterion selection UI
- `HelpChatbot.tsx` - AI assistant interface
- `QueryPanel.tsx` - Search and query interface

**Responsibilities**:
- User interaction and input validation
- Real-time progress tracking
- Data visualization (scores, grades, charts)
- API communication
- State management

### 2. API Layer (Backend)
**Technology**: FastAPI with Python 3.12

**Routers**:
- `audit.py` - Audit endpoints
- `upload.py` - Document upload
- `metrics.py` - Analytics
- `chatbot.py` - Help assistant

**Responsibilities**:
- Request validation
- Authentication (future)
- Rate limiting
- Error handling
- Response formatting

### 3. Business Logic Layer
**Core Components**:
- `CriterionAuditor` - Orchestrates audit process
- `ScoringPipeline` - Manages scoring workflow
- `AuditEnricher` - Adds metadata and context
- `GapDetector` - Identifies compliance gaps

**Responsibilities**:
- Audit orchestration
- Business rule enforcement
- Workflow management
- Result aggregation

### 4. AI/ML Layer
**Components**:
- `ModelManager` - Singleton model loader
- `LLMFallbackManager` - LLM failover
- `GroqKeyPool` - API key rotation
- `QueryExpander` - Query generation
- `DualRetriever` - Document retrieval
- `EvidenceScorer` - Quality assessment

**Responsibilities**:
- Model lifecycle management
- Inference execution
- Fallback handling
- Performance optimization

### 5. Data Layer
**Storage**:
- FAISS indexes (vector embeddings)
- SQLite database (metadata)
- File system (documents, cache)

**Responsibilities**:
- Data persistence
- Fast retrieval
- Metadata management
- Cache management

---

## Component Details

### Frontend Components

#### FullAuditDashboard.tsx
**Purpose**: Main interface for running and viewing full NAAC audits

**Key Features**:
- Progress tracking with real-time updates
- CGPA display with visual grade indicator
- Criterion-wise breakdown table
- Evidence preview
- Gap analysis section
- Recommendations list
- Export functionality

**State Management**:
```typescript
interface AuditState {
  isRunning: boolean;
  progress: number;
  results: AuditResult | null;
  error: string | null;
}
```

**API Integration**:
```typescript
const runFullAudit = async () => {
  const response = await fetch('/api/audit/run-full-audit', {
    method: 'POST'
  });
  const data = await response.json();
  // Process and display results
};
```

#### CriteriaSelector.tsx
**Purpose**: Allows users to select and analyze individual criteria

**Features**:
- Framework selection (NAAC/NBA)
- Criterion dropdown with search
- Custom query input
- Real-time analysis
- Detailed results view

#### HelpChatbot.tsx
**Purpose**: AI-powered help assistant

**Features**:
- Context-aware responses
- Conversation history
- Quick action buttons
- Markdown rendering
- Copy functionality

---


### Backend Components

#### CriterionAuditor (Core Engine)
**File**: `accreditation_copilot/audit/criterion_auditor.py`

**Purpose**: Orchestrates the complete audit process for a single criterion

**Workflow**:
```python
def audit_criterion(criterion_id, framework, query_template):
    # Step 1: Expand query
    query_variants = query_expander.expand_query(query_template, framework)
    
    # Step 2: Retrieve documents
    results, inst_available = dual_retriever.retrieve(
        query, query_variants, framework
    )
    
    # Step 3: Score evidence
    compliance_report = scoring_pipeline.process(
        query, framework, criterion_id, results
    )
    
    # Step 4: Enrich with metadata
    enriched = audit_enricher.enrich_sources(results)
    
    # Step 5: Detect gaps
    gaps = gap_detector.detect_gaps(coverage, confidence)
    
    # Step 6: Return structured result
    return {
        'confidence_score': confidence,
        'coverage_ratio': coverage,
        'gaps': gaps,
        'recommendations': recommendations,
        'evidence_sources': enriched
    }
```

**Dependencies**:
- QueryExpander
- DualRetriever
- ScoringPipeline
- AuditEnricher
- GapDetector
- EvidenceGrounder

#### ScoringPipeline
**File**: `accreditation_copilot/scoring/scoring_pipeline.py`

**Purpose**: Manages the complete scoring workflow

**Components**:
1. **EvidenceScorer** - Scores chunk quality
2. **DimensionChecker** - Verifies coverage
3. **ConfidenceCalculator** - Computes confidence
4. **ComplianceSynthesizer** - Generates explanation

**Process Flow**:
```python
def process(query, framework, criterion, retrieval_results):
    # C1: Score evidence quality
    evidence_scores = evidence_scorer.score(retrieval_results)
    
    # C2: Check dimension coverage
    coverage = dimension_checker.check(retrieval_results, framework, criterion)
    
    # C3: Calculate confidence
    confidence = confidence_calculator.calculate(
        evidence_scores, coverage, retrieval_results
    )
    
    # C4: Generate synthesis (LLM)
    synthesis = synthesizer.generate(
        criterion, framework, confidence, coverage, 
        retrieval_results, evidence_scores
    )
    
    # C5: Format output
    return output_formatter.format(
        query, framework, criterion, confidence, 
        coverage, synthesis, retrieval_results, evidence_scores
    )
```

#### LLMFallbackManager
**File**: `accreditation_copilot/utils/llm_fallback.py`

**Purpose**: Manages LLM calls with automatic fallback

**Architecture**:
```python
class LLMFallbackManager:
    def __init__(self):
        self.groq_pool = GroqKeyPool()  # 7 keys, round-robin
        self.ollama_host = "http://localhost:11434"
        self.ollama_text_model = "llama3.1:8b"
        self.ollama_vision_model = "llava"
    
    def completion(self, model, messages, **kwargs):
        # Try Groq first
        try:
            response, key_index = self.groq_pool.completion(...)
            return response, 'groq'
        except RateLimitError:
            # Fallback to Ollama
            response = self._ollama_completion(...)
            return response, 'ollama'
```

**Fallback Logic**:
```
Request → Groq Key 1 → Success ✓
       ↓
    Rate Limit
       ↓
Request → Groq Key 2 → Success ✓
       ↓
    Rate Limit
       ↓
    ... (Keys 3-7)
       ↓
    All Keys Exhausted
       ↓
Request → Ollama llama3.1:8b → Success ✓
```

#### DualRetriever
**File**: `accreditation_copilot/retrieval/dual_retrieval.py`

**Purpose**: Retrieves relevant chunks from both framework and institution indexes

**Process**:
```python
def retrieve(query, query_variants, framework, top_k_framework=3, top_k_institution=7):
    # Step 1: Embed query
    query_embedding = embedder.encode(query)
    
    # Step 2: Search framework index
    framework_results = faiss_search(
        framework_index, query_embedding, top_k_framework
    )
    
    # Step 3: Search institution index
    institution_results = faiss_search(
        institution_index, query_embedding, top_k_institution
    )
    
    # Step 4: Combine results
    combined = framework_results + institution_results
    
    # Step 5: Rerank
    reranked = reranker.rerank(query, combined)
    
    # Step 6: Add metadata
    enriched = add_metadata(reranked)
    
    return enriched, institution_available
```

**Indexes**:
- Framework: `indexes/framework/{framework}_{type}.index`
- Institution: `indexes/institution/institution.index`

---

## Data Flow

### Full Audit Flow (Detailed)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Initiates Audit                                     │
│    Frontend: Click "Run Full NAAC Audit"                    │
│    → POST /api/audit/run-full-audit                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│ 2. Backend Receives Request                                 │
│    audit.py: run_full_naac_audit()                          │
│    → Get all NAAC criteria (127 metrics)                    │
│    → Initialize auditor                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│ 3. For Each Criterion (Loop 127 times)                      │
│    ┌──────────────────────────────────────────────┐        │
│    │ 3.1 Query Expansion                          │        │
│    │     Input: "Details of funding..."           │        │
│    │     LLM: Generate 6 variants                 │        │
│    │     Output: [variant1, variant2, ...]        │        │
│    └──────────────────────────────────────────────┘        │
│                     │                                        │
│    ┌──────────────────────────────────────────────┐        │
│    │ 3.2 Dual Retrieval                           │        │
│    │     Embed: query → 768-dim vector            │        │
│    │     Search: Framework index (top 3)          │        │
│    │     Search: Institution index (top 7)        │        │
│    │     Rerank: BGE reranker                     │        │
│    │     Output: 10 ranked chunks                 │        │
│    └──────────────────────────────────────────────┘        │
│                     │                                        │
│    ┌──────────────────────────────────────────────┐        │
│    │ 3.3 Evidence Scoring                         │        │
│    │     For each chunk:                          │        │
│    │       - Detect numeric evidence (0.40)       │        │
│    │       - Detect entities (0.30)               │        │
│    │       - Detect keywords (0.10)               │        │
│    │       - Detect structure (0.10)              │        │
│    │       - Use reranker score (0.10)            │        │
│    │       - Apply quality boost if high          │        │
│    │     Output: evidence_scores[]                │        │
│    └──────────────────────────────────────────────┘        │
│                     │                                        │
│    ┌──────────────────────────────────────────────┐        │
│    │ 3.4 Dimension Checking                       │        │
│    │     Get required dimensions for criterion    │        │
│    │     Check semantic similarity with chunks    │        │
│    │     Calculate coverage ratio                 │        │
│    │     Output: coverage{ratio, covered, missing}│        │
│    └──────────────────────────────────────────────┘        │
│                     │                                        │
│    ┌──────────────────────────────────────────────┐        │
│    │ 3.5 Confidence Calculation                   │        │
│    │     Filter to institution chunks only        │        │
│    │     avg_evidence = mean(evidence_scores)     │        │
│    │     avg_reranker = mean(reranker_scores)     │        │
│    │     base = 0.75×evidence + 0.25×reranker     │        │
│    │     final = base × coverage_ratio            │        │
│    │     Output: confidence_score                 │        │
│    └──────────────────────────────────────────────┘        │
│                     │                                        │
│    ┌──────────────────────────────────────────────┐        │
│    │ 3.6 LLM Synthesis                            │        │
│    │     Build secure XML prompt                  │        │
│    │     Try: Groq API (keys 1-7)                 │        │
│    │     Fallback: Ollama llama3.1:8b             │        │
│    │     Parse JSON response                      │        │
│    │     Output: {summary, gaps, recommendations} │        │
│    └──────────────────────────────────────────────┘        │
│                     │                                        │
│    ┌──────────────────────────────────────────────┐        │
│    │ 3.7 Grade Assignment                         │        │
│    │     confidence → grade_points (0-4)          │        │
│    │     grade_points → letter_grade              │        │
│    │     Output: grade (A+, A, B+, etc.)          │        │
│    └──────────────────────────────────────────────┘        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│ 4. CGPA Calculation                                          │
│    Group by main criterion (1-7)                            │
│    Calculate average grade points per criterion             │
│    Apply NAAC weights:                                      │
│      - Criterion 1: 100 points                              │
│      - Criterion 2: 350 points (highest)                    │
│      - Criterion 3: 200 points                              │
│      - Criterion 4: 100 points                              │
│      - Criterion 5: 100 points                              │
│      - Criterion 6: 100 points                              │
│      - Criterion 7: 50 points                               │
│    CGPA = Σ(grade_points × weight) / Σ(weights)            │
│    Assign letter grade based on CGPA                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│ 5. Generate Improvement Suggestions                         │
│    Identify weak criteria (grade_points < 2.5)              │
│    Prioritize by weight (focus on Criterion 2 & 3)          │
│    Generate actionable recommendations                      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│ 6. Return Response                                           │
│    {                                                         │
│      overall_result: {cgpa, grade, status},                 │
│      individual_criteria: [...],                            │
│      improvement_suggestions: [...],                        │
│      summary: {...}                                         │
│    }                                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│ 7. Frontend Displays Results                                │
│    - CGPA with visual grade indicator                       │
│    - Criterion-wise breakdown table                         │
│    - Evidence sources                                       │
│    - Gaps and recommendations                               │
│    - Export options                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
Omni-Accreditation-Assistant/
│
├── accreditation_copilot/          # Main application directory
│   │
│   ├── api/                         # FastAPI backend
│   │   ├── routers/
│   │   │   ├── audit.py            # Audit endpoints
│   │   │   ├── upload.py           # Document upload
│   │   │   ├── metrics.py          # Analytics
│   │   │   └── chatbot.py          # Help assistant
│   │   ├── main.py                 # FastAPI app
│   │   ├── start_api.py            # Server startup
│   │   └── error_handler.py        # Error handling
│   │
│   ├── audit/                       # Audit engine
│   │   ├── criterion_auditor.py    # Core auditor
│   │   ├── audit_enricher.py       # Metadata enrichment
│   │   └── full_audit_runner.py    # Full audit orchestration
│   │
│   ├── retrieval/                   # Document retrieval
│   │   ├── dual_retrieval.py       # Dual index search
│   │   ├── query_expander.py       # Query generation
│   │   ├── hyde_retriever.py       # HyDE retrieval
│   │   └── index_loader.py         # Index management
│   │
│   ├── scoring/                     # Scoring pipeline
│   │   ├── scoring_pipeline.py     # Main pipeline
│   │   ├── evidence_scorer.py      # Evidence quality
│   │   ├── confidence_calculator.py # Confidence score
│   │   ├── semantic_dimension_checker.py # Coverage
│   │   ├── synthesizer.py          # LLM synthesis
│   │   ├── naac_grading.py         # CGPA calculation
│   │   └── output_formatter.py     # Response formatting
│   │
│   ├── analysis/                    # Analysis components
│   │   ├── evidence_grounder.py    # Evidence grounding
│   │   ├── gap_detector.py         # Gap detection
│   │   └── evidence_strength.py    # Strength scoring
│   │
│   ├── llm/                         # LLM components
│   │   └── compliance_auditor.py   # LLM auditor
│   │
│   ├── utils/                       # Utilities
│   │   ├── llm_fallback.py         # LLM fallback manager
│   │   └── groq_pool.py            # API key pool
│   │
│   ├── security/                    # Security layer
│   │   ├── context_sanitizer.py    # Input sanitization
│   │   └── prompt_builder.py       # Secure prompts
│   │
│   ├── models/                      # Model management
│   │   └── model_manager.py        # Singleton model loader
│   │
│   ├── criteria/                    # Criterion definitions
│   │   └── criterion_registry.py   # NAAC/NBA criteria
│   │
│   ├── cache/                       # Caching
│   │   └── audit_cache.py          # Audit result cache
│   │
│   ├── validation/                  # Validation
│   │   ├── report_validator.py     # Report validation
│   │   └── json_validator.py       # JSON schema validation
│   │
│   ├── frontend/                    # Next.js frontend
│   │   ├── app/                    # App router
│   │   │   ├── page.tsx            # Home page
│   │   │   ├── metrics/            # Metrics page
│   │   │   ├── history/            # History page
│   │   │   ├── settings/           # Settings page
│   │   │   └── profile/            # Profile page
│   │   │
│   │   ├── components/             # React components
│   │   │   ├── FullAuditDashboard.tsx
│   │   │   ├── CriteriaSelector.tsx
│   │   │   ├── HelpChatbot.tsx
│   │   │   ├── QueryPanel.tsx
│   │   │   └── AuditDashboard.tsx
│   │   │
│   │   ├── public/                 # Static assets
│   │   ├── styles/                 # CSS styles
│   │   └── package.json            # Dependencies
│   │
│   ├── data/                        # Data storage
│   │   └── metadata.db             # SQLite database
│   │
│   ├── indexes/                     # FAISS indexes
│   │   ├── framework/              # Framework indexes
│   │   │   ├── naac_metric.index
│   │   │   ├── naac_policy.index
│   │   │   ├── nba_metric.index
│   │   │   └── nba_policy.index
│   │   └── institution/            # Institution index
│   │       └── institution.index
│   │
│   ├── .env                         # Environment variables (not in git)
│   └── .env.example                # Environment template
│
├── docs/                            # Documentation
│   ├── DOCUMENTATION.md            # Main documentation
│   ├── SYSTEM_ARCHITECTURE.md      # This file
│   ├── TROUBLESHOOTING_FULL_AUDIT.md
│   └── QUICK_START_FULL_AUDIT.md
│
├── tests/                           # Test scripts
│   ├── test_groq_keys.py
│   ├── test_llm_fallback.py
│   ├── deep_score_diagnostic.py
│   └── diagnose_audit_issue.py
│
├── .gitignore                       # Git ignore rules
├── README.md                        # Project readme
└── requirements.txt                 # Python dependencies
```

---


## Frontend Architecture

### Technology Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: React Hooks (useState, useEffect)
- **API Client**: Fetch API
- **Real-time Updates**: Polling / Server-Sent Events

### Component Hierarchy

```
App (app/page.tsx)
│
├── FullAuditDashboard
│   ├── AuditControls
│   │   └── Button (Run Full Audit)
│   ├── ProgressBar
│   ├── CGPADisplay
│   │   ├── GradeIndicator
│   │   └── ScoreBreakdown
│   ├── CriteriaTable
│   │   └── CriterionRow[]
│   ├── EvidenceSection
│   │   └── EvidenceCard[]
│   ├── GapAnalysis
│   │   └── GapItem[]
│   └── RecommendationsPanel
│       └── RecommendationCard[]
│
├── CriteriaSelector
│   ├── FrameworkDropdown
│   ├── CriterionDropdown
│   ├── QueryInput
│   ├── AnalyzeButton
│   └── ResultsDisplay
│       ├── ComplianceStatus
│       ├── ConfidenceScore
│       ├── EvidenceList
│       └── RecommendationsList
│
└── HelpChatbot
    ├── ChatHeader
    ├── MessageList
    │   └── Message[]
    ├── InputArea
    └── QuickActions
```

### State Management Pattern

```typescript
// Global state (if using Context API)
interface AppState {
  user: User | null;
  auditHistory: Audit[];
  currentAudit: AuditResult | null;
}

// Component state
interface AuditDashboardState {
  isRunning: boolean;
  progress: number;
  results: AuditResult | null;
  error: string | null;
  selectedCriterion: string | null;
}

// API state
interface APIState {
  loading: boolean;
  data: any | null;
  error: Error | null;
}
```

### API Integration Pattern

```typescript
// Custom hook for API calls
const useAudit = () => {
  const [state, setState] = useState<APIState>({
    loading: false,
    data: null,
    error: null
  });

  const runFullAudit = async () => {
    setState({ loading: true, data: null, error: null });
    
    try {
      const response = await fetch('/api/audit/run-full-audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (!response.ok) throw new Error('Audit failed');
      
      const data = await response.json();
      setState({ loading: false, data, error: null });
    } catch (error) {
      setState({ loading: false, data: null, error });
    }
  };

  return { ...state, runFullAudit };
};
```

### Styling Guidelines

**Color Palette**:
```css
/* Primary Colors */
--primary: #3B82F6;      /* Blue */
--secondary: #10B981;    /* Green */
--accent: #F59E0B;       /* Amber */

/* Grade Colors */
--grade-a-plus: #10B981;  /* Green */
--grade-a: #3B82F6;       /* Blue */
--grade-b: #F59E0B;       /* Amber */
--grade-c: #EF4444;       /* Red */

/* Neutral Colors */
--background: #FFFFFF;
--foreground: #1F2937;
--muted: #F3F4F6;
--border: #E5E7EB;
```

**Typography**:
```css
/* Headings */
h1: text-4xl font-bold
h2: text-3xl font-semibold
h3: text-2xl font-semibold
h4: text-xl font-medium

/* Body */
body: text-base
small: text-sm
tiny: text-xs
```

### Responsive Design

**Breakpoints**:
```css
sm: 640px   /* Mobile landscape */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
2xl: 1536px /* Extra large */
```

**Layout Strategy**:
- Mobile-first approach
- Flexible grid system
- Collapsible sidebars
- Responsive tables (horizontal scroll on mobile)
- Touch-friendly buttons (min 44x44px)

---

## Backend Architecture

### FastAPI Application Structure

```python
# main.py
app = FastAPI(
    title="Omni Accreditation Copilot API",
    description="API for accreditation audit system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
```

### Request/Response Flow

```
Client Request
    ↓
FastAPI Router
    ↓
Request Validation (Pydantic)
    ↓
Business Logic (Auditor)
    ↓
AI/ML Processing
    ↓
Response Formatting
    ↓
JSON Response
```

### Error Handling Strategy

```python
# Custom exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

# Audit-specific error handling
def safe_audit_execution(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutError:
            return {"error": "Audit timeout", "status": "timeout"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    return wrapper
```

### Caching Strategy

```python
# Audit cache
class AuditCache:
    def __init__(self, ttl_hours=24):
        self.cache_dir = Path("cache/audits")
        self.ttl = timedelta(hours=ttl_hours)
    
    def get_cached_audit(self, cache_key):
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            # Check if expired
            if self._is_expired(cache_file):
                return None
            return json.loads(cache_file.read_text())
        return None
    
    def save_audit_cache(self, cache_key, report):
        cache_file = self.cache_dir / f"{cache_key}.json"
        cache_file.write_text(json.dumps(report))
```

---

## AI/ML Pipeline

### Model Loading (Singleton Pattern)

```python
class ModelManager:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ModelManager()
            cls._instance.load_models()
        return cls._instance
    
    def load_models(self):
        # Load once at startup
        self.embedder = SentenceTransformer('BAAI/bge-base-en-v1.5')
        self.reranker_model = AutoModelForSequenceClassification.from_pretrained(
            'BAAI/bge-reranker-base'
        )
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY_1'))
```

### Embedding Pipeline

```python
def embed_documents(texts: List[str]) -> np.ndarray:
    """
    Convert texts to 768-dim embeddings
    
    Input: ["text1", "text2", ...]
    Output: np.array([[0.1, 0.2, ...], [0.3, 0.4, ...]])
    """
    embeddings = model_manager.get_embedder().encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    return embeddings
```

### Reranking Pipeline

```python
def rerank(query: str, documents: List[str]) -> List[float]:
    """
    Rerank documents by relevance to query
    
    Input: query, [doc1, doc2, ...]
    Output: [score1, score2, ...] (0-1 range)
    """
    pairs = [[query, doc] for doc in documents]
    
    with torch.no_grad():
        inputs = tokenizer(
            pairs,
            padding=True,
            truncation=True,
            return_tensors='pt',
            max_length=512
        )
        scores = model(** inputs).logits.squeeze(-1)
        scores = torch.sigmoid(scores).cpu().numpy()
    
    return scores.tolist()
```

### LLM Inference Pipeline

```python
def llm_completion(prompt: str, max_tokens: int = 800):
    """
    Generate completion with fallback
    
    Priority:
    1. Groq API (keys 1-7)
    2. Ollama llama3.1:8b
    """
    manager = get_llm_fallback_manager()
    
    response, source = manager.completion(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert..."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content, source
```

---

## Database Schema

### SQLite Schema

```sql
-- Chunks table (document chunks)
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chunk_id TEXT UNIQUE NOT NULL,
    child_text TEXT NOT NULL,
    parent_context TEXT,
    source_file TEXT NOT NULL,
    source_type TEXT NOT NULL,  -- 'framework' or 'institution'
    framework TEXT,              -- 'NAAC' or 'NBA'
    page_number INTEGER,
    chunk_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast lookups
CREATE INDEX idx_source_type ON chunks(source_type);
CREATE INDEX idx_framework ON chunks(framework);
CREATE INDEX idx_chunk_id ON chunks(chunk_id);

-- Audit cache table (optional)
CREATE TABLE audit_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT UNIQUE NOT NULL,
    framework TEXT NOT NULL,
    criterion TEXT NOT NULL,
    report JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);
```

### FAISS Index Structure

```python
# Index metadata
{
    "dimension": 768,
    "index_type": "IndexFlatIP",  # Inner product (cosine similarity)
    "num_vectors": 1500,
    "mapping": {
        0: "chunk_id_1",
        1: "chunk_id_2",
        ...
    }
}

# BM25 index (pickle)
{
    "corpus": ["text1", "text2", ...],
    "bm25": BM25Okapi(corpus),
    "mapping": {0: "chunk_id_1", ...}
}
```

---

## API Design

### RESTful Endpoints

```
POST   /api/audit/run-full-audit          # Run full NAAC audit
POST   /api/audit/run                     # Run single criterion audit
GET    /api/audit/criteria/{framework}    # Get available criteria
GET    /api/audit/cache                   # Get cached audits
DELETE /api/audit/cache                   # Clear cache

POST   /api/upload/documents              # Upload institutional documents
GET    /api/upload/status/{upload_id}     # Check upload status

GET    /api/metrics/dashboard              # Get dashboard metrics
GET    /api/metrics/history                # Get audit history

POST   /api/chatbot/message                # Send message to chatbot
GET    /api/chatbot/history                # Get chat history
```

### Request/Response Examples

**Full Audit Request**:
```http
POST /api/audit/run-full-audit
Content-Type: application/json

{}
```

**Full Audit Response**:
```json
{
  "audit_type": "full_naac_audit",
  "framework": "NAAC",
  "timestamp": "2026-03-23T12:00:00",
  "overall_result": {
    "cgpa": 3.26,
    "letter_grade": "A+",
    "description": "Excellent",
    "accreditation_status": "Accredited",
    "total_criteria_evaluated": 7,
    "total_metrics_evaluated": 127,
    "breakdown": [
      {
        "criterion": "Criterion 1",
        "average_grade_points": 3.45,
        "grade": "A+",
        "weight": 100,
        "weighted_contribution": 0.345
      },
      ...
    ]
  },
  "individual_criteria": [
    {
      "criterion": "1.1.1",
      "confidence_score": 0.856,
      "grade": "A+",
      "compliance_status": "Compliant",
      "evidence_count": 7,
      "gaps": [],
      "recommendations": [...]
    },
    ...
  ],
  "improvement_suggestions": [
    "Focus on improving Criterion 2 (Teaching-Learning)",
    "Strengthen documentation for research projects",
    ...
  ],
  "summary": {
    "total_criteria": 127,
    "criteria_evaluated": 127,
    "cgpa": 3.26,
    "grade": "A+",
    "accreditation_status": "Accredited"
  }
}
```

---

## Performance Optimization

### Strategies Implemented

1. **Model Caching**: Load models once at startup (singleton pattern)
2. **Vector Indexing**: FAISS for fast similarity search (O(log n))
3. **GPU Acceleration**: CUDA for embeddings and reranking
4. **API Key Pooling**: Round-robin across 7 keys (7x capacity)
5. **Result Caching**: Cache audit results for 24 hours
6. **Batch Processing**: Process multiple queries in batches
7. **Lazy Loading**: Load indexes on-demand
8. **Connection Pooling**: Reuse database connections

### Performance Metrics

```
Embedding Generation: ~50ms per query (GPU)
FAISS Search: ~10ms per query
Reranking: ~100ms for 10 documents (GPU)
LLM Synthesis: ~2s (Groq) / ~10s (Ollama)
Full Criterion Audit: ~5-8s
Full NAAC Audit (127 criteria): ~10-15 minutes
```

---

## Security Considerations

### Implemented Security Measures

1. **API Key Protection**: Keys in .env, not in git
2. **Input Sanitization**: Clean user inputs before processing
3. **Secure Prompts**: XML-based prompt templates
4. **CORS Configuration**: Whitelist frontend origins
5. **Rate Limiting**: API key rotation prevents abuse
6. **Error Handling**: Don't expose internal errors to users
7. **Validation**: Pydantic models for request validation

### Future Security Enhancements

1. **Authentication**: JWT-based user authentication
2. **Authorization**: Role-based access control
3. **Encryption**: Encrypt sensitive data at rest
4. **Audit Logging**: Log all API calls
5. **Rate Limiting**: Per-user rate limits
6. **HTTPS**: SSL/TLS for production

---

## Deployment Architecture

### Development Environment
```
Local Machine
├── Backend: localhost:8000
├── Frontend: localhost:3000
├── Ollama: localhost:11434
└── Database: SQLite file
```

### Production Environment (Recommended)
```
Cloud Infrastructure
├── Frontend: Vercel / Netlify
├── Backend: AWS EC2 / Google Cloud
│   ├── FastAPI (Gunicorn + Uvicorn)
│   ├── NGINX (Reverse proxy)
│   └── GPU Instance (for models)
├── Database: PostgreSQL / MongoDB
├── Vector Store: Pinecone / Weaviate
└── LLM: Groq API + Ollama backup
```

---

## Monitoring & Observability

### Metrics to Track

1. **Performance Metrics**:
   - API response times
   - LLM inference latency
   - Database query times
   - Cache hit rates

2. **Business Metrics**:
   - Audits per day
   - Average CGPA scores
   - Most audited criteria
   - User engagement

3. **System Metrics**:
   - CPU/GPU utilization
   - Memory usage
   - Disk I/O
   - Network bandwidth

4. **Error Metrics**:
   - API error rates
   - LLM failures
   - Timeout occurrences
   - Fallback usage

### Logging Strategy

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

# Log important events
logger.info(f"[AUDIT START] Criterion: {criterion_id}")
logger.info(f"[LLM] Used {source} for synthesis")
logger.error(f"[ERROR] Audit failed: {error}")
```

---

## Future Enhancements

### Planned Features

1. **Multi-tenancy**: Support multiple institutions
2. **Document Versioning**: Track document changes over time
3. **Comparative Analysis**: Compare with peer institutions
4. **Automated Reporting**: Generate PDF reports
5. **Email Notifications**: Alert on audit completion
6. **Advanced Analytics**: Trend analysis, predictions
7. **Mobile App**: iOS/Android applications
8. **API Webhooks**: Real-time event notifications

### Technical Improvements

1. **Microservices**: Split into smaller services
2. **Message Queue**: RabbitMQ/Kafka for async processing
3. **Container Orchestration**: Kubernetes deployment
4. **CI/CD Pipeline**: Automated testing and deployment
5. **Load Balancing**: Distribute traffic across instances
6. **Database Sharding**: Scale database horizontally
7. **CDN Integration**: Faster static asset delivery
8. **GraphQL API**: More flexible data fetching

---

**Document Version**: 1.0  
**Last Updated**: March 2026  
**Maintained By**: Development Team

For questions or clarifications, refer to [DOCUMENTATION.md](DOCUMENTATION.md)
