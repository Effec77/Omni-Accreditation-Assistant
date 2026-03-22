# Omni Accreditation Copilot - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Technology Stack](#technology-stack)
5. [Installation & Setup](#installation--setup)
6. [User Guide](#user-guide)
7. [API Reference](#api-reference)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Development](#development)

---

## Overview

**Omni Accreditation Copilot** is an AI-powered platform that automates the accreditation compliance assessment process for educational institutions. It analyzes institutional documents against NAAC (National Assessment and Accreditation Council) and NBA (National Board of Accreditation) frameworks, providing detailed compliance reports, gap analysis, and actionable recommendations.

### Key Capabilities
- **Automated Compliance Audits**: Evaluate institutional documents against 100+ accreditation criteria
- **Intelligent Document Analysis**: RAG-based system extracts and analyzes evidence from institutional documents
- **CGPA Calculation**: Automatic calculation of NAAC CGPA scores (0-4 scale) with grade assignment
- **Gap Detection**: Identifies missing evidence and compliance gaps
- **Actionable Recommendations**: Provides specific steps to improve accreditation scores
- **Multi-Framework Support**: Supports both NAAC and NBA accreditation frameworks

### Target Users
- **Educational Institutions**: Universities, colleges preparing for accreditation
- **Accreditation Consultants**: Professionals assisting institutions with compliance
- **Quality Assurance Teams**: Internal teams managing accreditation processes
- **Administrators**: Leadership tracking institutional compliance status

---

## Features

### 1. Full NAAC Audit System
- Comprehensive evaluation of all 7 NAAC criteria (127 metrics)
- Automatic CGPA calculation with letter grade (A++, A+, A, B++, B+, B, C, D)
- Criterion-wise breakdown with individual scores
- Accreditation status determination
- Improvement suggestions prioritized by impact

### 2. Criterion-Level Analysis
- Detailed compliance assessment for individual criteria
- Evidence extraction and grounding
- Dimension coverage analysis
- Confidence scoring (0-1 scale)
- Gap identification with specific missing elements

### 3. Intelligent Document Processing
- **Dual Retrieval System**: Combines framework guidelines with institutional evidence
- **Semantic Search**: BGE embeddings for accurate document retrieval
- **Reranking**: BGE reranker for relevance optimization
- **Evidence Scoring**: Multi-signal scoring (numeric data, entities, keywords, structure)
- **Quality Boost**: 30% boost for high-quality evidence chunks

### 4. AI-Powered Analysis
- **LLM Synthesis**: Groq API with Llama 3.3 70B for compliance reasoning
- **Automatic Fallback**: Seamless switch to local Ollama models on rate limits
- **Multi-Key Pool**: Round-robin rotation across 7+ API keys (700k tokens/day)
- **Query Expansion**: Generates multiple search variants for better retrieval

### 5. Interactive Dashboard
- Real-time audit progress tracking
- Visual CGPA display with grade indicators
- Criterion-wise score breakdown
- Evidence preview and source tracking
- Gap analysis with actionable recommendations
- Export functionality for reports

### 6. Help Chatbot
- Context-aware assistance using Gemini API
- Accreditation framework guidance
- Document upload help
- Troubleshooting support

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Full Audit   │  │ Criterion    │  │ Help         │         │
│  │ Dashboard    │  │ Selector     │  │ Chatbot      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST API
┌────────────────────────────┴────────────────────────────────────┐
│                    Backend (FastAPI)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Audit Router │  │ Upload       │  │ Chatbot      │         │
│  │              │  │ Router       │  │ Router       │         │
│  └──────┬───────┘  └──────────────┘  └──────────────┘         │
│         │                                                        │
│  ┌──────┴───────────────────────────────────────────┐          │
│  │         Criterion Auditor (Core Engine)          │          │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │          │
│  │  │ Query      │  │ Dual       │  │ Scoring    │ │          │
│  │  │ Expander   │  │ Retrieval  │  │ Pipeline   │ │          │
│  │  └────────────┘  └────────────┘  └────────────┘ │          │
│  └──────────────────────────────────────────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Data & AI Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ FAISS        │  │ SQLite       │  │ LLM          │         │
│  │ Indexes      │  │ Metadata DB  │  │ Fallback     │         │
│  │              │  │              │  │ Manager      │         │
│  │ - Framework  │  │ - Chunks     │  │              │         │
│  │ - Institution│  │ - Sources    │  │ Groq → Ollama│         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow: Full Audit Process

```
1. User Request
   └─> Frontend: Click "Run Full NAAC Audit"
       └─> API: POST /api/audit/run-full-audit

2. Audit Orchestration
   └─> For each criterion (1.1.1 to 7.3.1):
       ├─> Query Expansion (6 variants)
       ├─> Dual Retrieval (Framework + Institution)
       ├─> Evidence Scoring (Multi-signal)
       ├─> Dimension Checking (Coverage)
       ├─> Confidence Calculation
       └─> LLM Synthesis (Groq/Ollama)

3. CGPA Calculation
   └─> Aggregate criterion scores
       ├─> Apply NAAC weights
       ├─> Calculate weighted average
       └─> Assign letter grade

4. Response
   └─> Return comprehensive report
       ├─> Overall CGPA & Grade
       ├─> Criterion-wise breakdown
       ├─> Evidence sources
       ├─> Gaps & Recommendations
       └─> Accreditation status
```

### Component Breakdown

#### 1. Query Expander
**Purpose**: Generates multiple search variants for better retrieval coverage

**Process**:
```python
Input: "Details of funding received from government agencies"
       ↓
LLM Expansion (Groq/Ollama)
       ↓
Output: [
  "Government funding details for research projects",
  "Grants received from government bodies",
  "External funding from govt agencies",
  "Research project funding sources",
  "Government-sponsored research details",
  "Funding agencies and amounts received"
]
```

**Technology**: Llama 3.3 70B via Groq API with Ollama fallback

#### 2. Dual Retrieval System
**Purpose**: Retrieves relevant chunks from both framework and institution documents

**Process**:
```
Query → Embedding (BGE-base) → FAISS Search
                                    ↓
                    ┌───────────────┴───────────────┐
                    │                               │
            Framework Index                 Institution Index
            (NAAC/NBA docs)                (Uploaded docs)
                    │                               │
                    └───────────────┬───────────────┘
                                    ↓
                            BM25 + Reranking
                                    ↓
                            Top 10 chunks
                            (3 framework + 7 institution)
```

**Models**:
- Embeddings: BAAI/bge-base-en-v1.5
- Reranker: BAAI/bge-reranker-base

#### 3. Evidence Scorer
**Purpose**: Scores evidence quality using multiple signals

**Signals & Weights**:
```python
Numeric Evidence (40%):  Currency, counts, dates
Entity Evidence (30%):   Agency names (DST, SERB, DBT, etc.)
Keyword Evidence (10%):  Domain terms (grant, funded, etc.)
Structure Evidence (10%): Tables, lists, formatting
Reranker Score (10%):    Semantic relevance
```

**Quality Boost**: +30% for chunks with numeric ≥ 0.6 AND entity ≥ 0.6

**Example**:
```
Chunk: "Year: 2020-21, Projects: 28, Funding: ₹920 Lakhs, Agencies: SERB, DBT"
       ↓
Signals: numeric=0.8, entity=1.0, keyword=0.0, structure=0.0, reranker=0.037
       ↓
Base Score: 0.40×0.8 + 0.30×1.0 + 0.10×0.0 + 0.10×0.0 + 0.10×0.037 = 0.624
       ↓
Quality Boost: 0.624 × 1.3 = 0.811
```

#### 4. Dimension Checker
**Purpose**: Verifies coverage of required dimensions for each criterion

**Process**:
```
Criterion 3.1.1 Requirements:
  - project_count: Number of research projects
  - funding_agencies: Names of funding bodies
       ↓
Semantic Similarity Check (BGE embeddings)
       ↓
Coverage Ratio: dimensions_covered / total_dimensions
```

#### 5. Confidence Calculator
**Purpose**: Computes final confidence score

**Formula**:
```python
# Filter to institution chunks only
institution_chunks = [c for c in chunks if c.source_type == 'institution']

# Calculate averages
avg_evidence = mean([chunk.evidence_score for chunk in institution_chunks])
avg_reranker = mean([chunk.reranker_score for chunk in institution_chunks])

# Weighted combination
base_score = 0.75 × avg_evidence + 0.25 × avg_reranker

# Apply coverage penalty
final_confidence = base_score × coverage_ratio
```

#### 6. LLM Synthesizer
**Purpose**: Generates human-readable compliance explanation

**Process**:
```
Input: Confidence, Coverage, Evidence chunks
       ↓
Prompt Builder (Secure XML format)
       ↓
LLM Fallback Manager
       ├─> Try Groq API (7 keys, round-robin)
       └─> Fallback to Ollama (llama3.1:8b)
       ↓
JSON Output: {
  evidence_summary: "...",
  gaps: [...],
  recommendation: "..."
}
```

#### 7. NAAC Grading System
**Purpose**: Converts confidence scores to NAAC CGPA and grades

**Conversion**:
```python
Confidence → Grade Points (0-4 scale):
  ≥ 0.85 → 4.0 (Excellent)
  ≥ 0.70 → 3.0-4.0 (Very Good to Excellent)
  ≥ 0.55 → 2.0-3.0 (Good to Very Good)
  ≥ 0.40 → 1.0-2.0 (Satisfactory to Good)
  < 0.40 → 0.0-1.0 (Unsatisfactory to Satisfactory)

CGPA Calculation:
  CGPA = Σ(criterion_grade_points × weight) / Σ(weights)

Grade Assignment:
  3.51-4.00 → A++ (Outstanding)
  3.26-3.50 → A+  (Excellent)
  3.01-3.25 → A   (Very Good)
  2.76-3.00 → B++ (Good)
  2.51-2.75 → B+  (Above Average)
  2.01-2.50 → B   (Average)
  1.51-2.00 → C   (Below Average)
  0.00-1.50 → D   (Poor)
```

---

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.12
- **Database**: SQLite (metadata storage)
- **Vector Store**: FAISS (document embeddings)
- **Search**: BM25 (keyword search)

### AI/ML Models
- **Embeddings**: BAAI/bge-base-en-v1.5 (768-dim)
- **Reranker**: BAAI/bge-reranker-base
- **LLM (Cloud)**: Llama 3.3 70B via Groq API
- **LLM (Local)**: Llama 3.1 8B via Ollama
- **Vision**: LLaVA (for future image analysis)
- **Chatbot**: Google Gemini 1.5 Pro

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **State**: React Hooks

### Infrastructure
- **Compute**: CUDA-enabled GPU (for embeddings/reranking)
- **API Gateway**: FastAPI with CORS
- **Process Management**: Python multiprocessing
- **Caching**: In-memory + file-based

### Development Tools
- **Version Control**: Git
- **Package Manager**: pip (Python), npm (Node.js)
- **Environment**: venv (Python), .env files
- **Testing**: pytest, manual testing scripts

---

## Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- CUDA-capable GPU (recommended)
- 16GB+ RAM
- 50GB+ disk space

### Step 1: Clone Repository
```bash
git clone https://github.com/Effec77/Omni-Accreditation-Assistant.git
cd Omni-Accreditation-Assistant
git checkout Testing
```

### Step 2: Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
cd accreditation_copilot
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
# Required:
#   - GROQ_API_KEY_1 to GROQ_API_KEY_7 (get from https://console.groq.com/)
#   - GEMINI_API_KEY (get from https://makersuite.google.com/app/apikey)
# Optional:
#   - HF_TOKEN (for HuggingFace models)
#   - LANGCHAIN_API_KEY (for observability)
```

### Step 4: Install Ollama (Local LLM Fallback)
```bash
# Download from https://ollama.ai/download
# After installation:
ollama pull llama3.1:8b
ollama pull llava
```

### Step 5: Frontend Setup
```bash
cd frontend
npm install
```

### Step 6: Start Services
```bash
# Terminal 1: Start backend
cd accreditation_copilot/api
python start_api.py

# Terminal 2: Start frontend
cd accreditation_copilot/frontend
npm run dev
```

### Step 7: Verify Installation
```bash
# Test Groq keys
python test_groq_keys.py

# Test LLM fallback
python test_llm_fallback.py

# Check institution data
python check_institution_data.py
```

### Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## User Guide

### Uploading Documents
1. Navigate to the upload section
2. Select institutional documents (PDF, DOCX)
3. Documents are automatically processed and indexed
4. Verify upload in the dashboard

### Running a Full Audit
1. Click "Run Full NAAC Audit" button
2. System evaluates all 127 NAAC metrics
3. Progress bar shows real-time status
4. Results display:
   - Overall CGPA and letter grade
   - Criterion-wise breakdown
   - Evidence sources
   - Gaps and recommendations
   - Accreditation status

### Analyzing Individual Criteria
1. Select framework (NAAC/NBA)
2. Choose specific criterion (e.g., 3.1.1)
3. Optionally add custom query
4. View detailed analysis:
   - Compliance status
   - Confidence score
   - Coverage ratio
   - Evidence chunks
   - Missing dimensions
   - Recommendations

### Using the Help Chatbot
1. Click chatbot icon
2. Ask questions about:
   - Accreditation requirements
   - Document preparation
   - System usage
   - Troubleshooting
3. Get context-aware responses

### Interpreting Results

**CGPA Scale**:
- 3.51-4.00: A++ (Outstanding) - Top tier institutions
- 3.26-3.50: A+ (Excellent) - Highly competitive
- 3.01-3.25: A (Very Good) - Strong performance
- 2.76-3.00: B++ (Good) - Above average
- 2.51-2.75: B+ (Above Average) - Satisfactory
- 2.01-2.50: B (Average) - Needs improvement
- 1.51-2.00: C (Below Average) - Significant gaps
- 0.00-1.50: D (Poor) - Major deficiencies

**Confidence Score**:
- 0.85-1.00: Strong evidence, comprehensive coverage
- 0.70-0.84: Good evidence, minor gaps
- 0.50-0.69: Moderate evidence, some gaps
- 0.30-0.49: Weak evidence, significant gaps
- 0.00-0.29: Insufficient evidence

---

## API Reference

### Full Audit Endpoint
```http
POST /api/audit/run-full-audit
```

**Response**:
```json
{
  "audit_type": "full_naac_audit",
  "framework": "NAAC",
  "timestamp": "2026-03-23T00:00:00",
  "overall_result": {
    "cgpa": 3.26,
    "letter_grade": "A+",
    "description": "Excellent",
    "accreditation_status": "Accredited",
    "total_criteria_evaluated": 7,
    "total_metrics_evaluated": 127
  },
  "individual_criteria": [...],
  "improvement_suggestions": [...]
}
```

### Criterion Audit Endpoint
```http
POST /api/audit/run
Content-Type: application/json

{
  "framework": "NAAC",
  "criterion": "3.1.1",
  "query": "Optional custom query"
}
```

**Response**:
```json
{
  "criterion": "3.1.1",
  "framework": "NAAC",
  "compliance_status": "Compliant",
  "confidence_score": 0.811,
  "coverage_ratio": 1.000,
  "grade": "A+",
  "evidence_count": 7,
  "evidence": [...],
  "gaps": [...],
  "recommendations": [...],
  "explanation": "..."
}
```

### Available Criteria Endpoint
```http
GET /api/audit/criteria/{framework}
```

**Response**:
```json
{
  "framework": "NAAC",
  "criteria": [
    {
      "criterion": "1.1.1",
      "description": "...",
      "query_template": "..."
    },
    ...
  ],
  "count": 127
}
```

---

## Configuration

### Environment Variables

**Required**:
```env
GROQ_API_KEY_1=gsk_your_key_here
GEMINI_API_KEY=your_gemini_key_here
```

**Optional**:
```env
GROQ_API_KEY_2=gsk_additional_key
GROQ_API_KEY_3=gsk_additional_key
# ... up to GROQ_API_KEY_9

HF_TOKEN=your_huggingface_token
LANGCHAIN_API_KEY=your_langsmith_key
OLLAMA_HOST=http://localhost:11434
```

### Scoring Configuration

Edit `accreditation_copilot/scoring/evidence_scorer.py`:
```python
WEIGHTS = {
    'numeric': 0.40,   # Weight for numeric evidence
    'entity': 0.30,    # Weight for entity evidence
    'keyword': 0.10,   # Weight for keyword matches
    'structure': 0.10, # Weight for structured data
    'reranker': 0.10   # Weight for semantic relevance
}
```

Edit `accreditation_copilot/scoring/confidence_calculator.py`:
```python
base_score = (
    0.75 * avg_evidence_score +  # Evidence weight
    0.25 * avg_retrieval_score   # Reranker weight
)
```

---

## Troubleshooting

See [TROUBLESHOOTING_FULL_AUDIT.md](TROUBLESHOOTING_FULL_AUDIT.md) for detailed troubleshooting guide.

### Common Issues

**Low Scores for Good Documents**:
- Upload more comprehensive institutional documents
- Ensure documents contain numeric data (amounts, counts, dates)
- Verify documents have agency names and structured data

**Rate Limit Errors**:
- System automatically falls back to Ollama
- Add more Groq API keys (up to 9 supported)
- Wait for rate limits to reset (midnight UTC)

**Backend Not Starting**:
```bash
python restart_backend.py
```

**Frontend Not Loading**:
```bash
cd accreditation_copilot/frontend
npm install
npm run dev
```

---

## Development

### Project Structure
See [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for detailed structure.

### Adding New Criteria
1. Edit `accreditation_copilot/criteria/criterion_registry.py`
2. Add criterion definition with query template
3. Restart backend

### Modifying Scoring Logic
1. Edit scoring components in `accreditation_copilot/scoring/`
2. Test with `python deep_score_diagnostic.py`
3. Restart backend

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

## License & Credits

**Project**: Omni Accreditation Copilot  
**Version**: 1.0.0  
**Last Updated**: March 2026

**Technologies**:
- Groq API (Llama 3.3 70B)
- Ollama (Llama 3.1 8B, LLaVA)
- BAAI BGE Models
- FastAPI, Next.js, FAISS

---

For additional help, see:
- [Quick Start Guide](QUICK_START_FULL_AUDIT.md)
- [System Architecture](SYSTEM_ARCHITECTURE.md)
- [Troubleshooting](TROUBLESHOOTING_FULL_AUDIT.md)
- [Ollama Fallback Guide](OLLAMA_FALLBACK_IMPLEMENTED.md)
