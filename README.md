# Omni Accreditation Copilot

> AI-powered accreditation compliance assessment platform for educational institutions

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Omni Accreditation Copilot automates the accreditation compliance assessment process for educational institutions. Using advanced AI and RAG (Retrieval-Augmented Generation) technology, it analyzes institutional documents against NAAC and NBA frameworks, providing detailed compliance reports, gap analysis, and actionable recommendations.

### Key Features

- ✅ **Automated Compliance Audits** - Evaluate 127 NAAC criteria automatically
- 📊 **CGPA Calculation** - Automatic NAAC CGPA scoring (0-4 scale) with grade assignment
- 🔍 **Intelligent Document Analysis** - RAG-based evidence extraction and analysis
- 📈 **Gap Detection** - Identifies missing evidence and compliance gaps
- 💡 **Actionable Recommendations** - Specific steps to improve accreditation scores
- 🤖 **AI-Powered Insights** - LLM-based compliance reasoning and synthesis
- 🔄 **Multi-Framework Support** - Supports both NAAC and NBA frameworks

### Demo

![Full Audit Dashboard](docs/images/dashboard.png)
*Full NAAC Audit Dashboard with CGPA calculation and criterion-wise breakdown*

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- CUDA-capable GPU (recommended)
- 16GB+ RAM

### Installation

```bash
# Clone repository
git clone https://github.com/Effec77/Omni-Accreditation-Assistant.git
cd Omni-Accreditation-Assistant
git checkout Testing

# Backend setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
cd accreditation_copilot
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Frontend setup
cd frontend
npm install

# Install Ollama (local LLM fallback)
# Download from https://ollama.ai/download
ollama pull llama3.1:8b
ollama pull llava
```

### Running the Application

```bash
# Terminal 1: Start backend
cd accreditation_copilot/api
python start_api.py

# Terminal 2: Start frontend
cd accreditation_copilot/frontend
npm run dev
```

Access the application at `http://localhost:3000`

## Documentation

- 📖 [Complete Documentation](DOCUMENTATION.md) - Full user and developer guide
- 🏗️ [System Architecture](SYSTEM_ARCHITECTURE.md) - Detailed technical architecture
- 🚀 [Quick Start Guide](QUICK_START_FULL_AUDIT.md) - Get started quickly
- 🔧 [Troubleshooting](TROUBLESHOOTING_FULL_AUDIT.md) - Common issues and solutions
- 🤖 [Ollama Fallback Guide](OLLAMA_FALLBACK_IMPLEMENTED.md) - LLM fallback system

## Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
│  Dashboard | Criteria Selector | Help Chatbot               │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  Audit Router | Upload Router | Chatbot Router              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                  Audit Engine (Core)                         │
│  Query Expansion → Dual Retrieval → Evidence Scoring        │
│  → Dimension Checking → Confidence Calculation → LLM        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                  Data & AI Layer                             │
│  FAISS Indexes | SQLite DB | Groq API | Ollama              │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend**:
- FastAPI (Python 3.12)
- FAISS (vector search)
- SQLite (metadata)
- BGE embeddings & reranker
- Groq API (Llama 3.3 70B)
- Ollama (Llama 3.1 8B, LLaVA)

**Frontend**:
- Next.js 14 (TypeScript)
- React 18
- Tailwind CSS
- shadcn/ui

## Features in Detail

### 1. Full NAAC Audit

Comprehensive evaluation of all 7 NAAC criteria (127 metrics):
- Automatic CGPA calculation
- Letter grade assignment (A++, A+, A, B++, B+, B, C, D)
- Criterion-wise breakdown
- Evidence sources
- Gap analysis
- Improvement suggestions

### 2. Criterion-Level Analysis

Detailed compliance assessment for individual criteria:
- Confidence scoring (0-1 scale)
- Dimension coverage analysis
- Evidence extraction and grounding
- Gap identification
- Actionable recommendations

### 3. Intelligent Document Processing

Advanced RAG pipeline:
- **Dual Retrieval**: Framework guidelines + institutional evidence
- **Semantic Search**: BGE embeddings for accurate retrieval
- **Reranking**: BGE reranker for relevance optimization
- **Evidence Scoring**: Multi-signal quality assessment
- **Quality Boost**: 30% boost for high-quality evidence

### 4. AI-Powered Analysis

LLM-based compliance reasoning:
- **Primary**: Groq API with Llama 3.3 70B
- **Fallback**: Local Ollama with Llama 3.1 8B
- **Multi-Key Pool**: 7+ API keys (700k tokens/day)
- **Automatic Failover**: Seamless Groq→Ollama switching

### 5. Help Chatbot

Context-aware assistance:
- Accreditation framework guidance
- Document upload help
- Troubleshooting support
- Powered by Google Gemini 1.5 Pro

## API Reference

### Full Audit

```http
POST /api/audit/run-full-audit
```

**Response**:
```json
{
  "overall_result": {
    "cgpa": 3.26,
    "letter_grade": "A+",
    "accreditation_status": "Accredited"
  },
  "individual_criteria": [...],
  "improvement_suggestions": [...]
}
```

### Criterion Audit

```http
POST /api/audit/run
Content-Type: application/json

{
  "framework": "NAAC",
  "criterion": "3.1.1",
  "query": "Optional custom query"
}
```

See [DOCUMENTATION.md](DOCUMENTATION.md) for complete API reference.

## Configuration

### Environment Variables

Create `.env` file in `accreditation_copilot/`:

```env
# Required
GROQ_API_KEY_1=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here

# Optional (for more capacity)
GROQ_API_KEY_2=additional_key
GROQ_API_KEY_3=additional_key
# ... up to GROQ_API_KEY_9

# Optional
HF_TOKEN=your_huggingface_token
LANGCHAIN_API_KEY=your_langsmith_key
OLLAMA_HOST=http://localhost:11434
```

Get API keys:
- Groq: https://console.groq.com/keys
- Gemini: https://makersuite.google.com/app/apikey
- HuggingFace: https://huggingface.co/settings/tokens

## Performance

### Metrics

- **Embedding Generation**: ~50ms per query (GPU)
- **FAISS Search**: ~10ms per query
- **Reranking**: ~100ms for 10 documents (GPU)
- **LLM Synthesis**: ~2s (Groq) / ~10s (Ollama)
- **Single Criterion Audit**: ~5-8 seconds
- **Full NAAC Audit**: ~10-15 minutes (127 criteria)

### Optimization

- Model caching (singleton pattern)
- Vector indexing (FAISS)
- GPU acceleration (CUDA)
- API key pooling (7x capacity)
- Result caching (24 hours)
- Batch processing

## Troubleshooting

### Common Issues

**Low Scores for Good Documents**:
```bash
# Check institution data
python check_institution_data.py

# Run diagnostics
python deep_score_diagnostic.py
```

**Rate Limit Errors**:
- System automatically falls back to Ollama
- Add more Groq API keys (up to 9 supported)

**Backend Not Starting**:
```bash
python restart_backend.py
```

See [TROUBLESHOOTING_FULL_AUDIT.md](TROUBLESHOOTING_FULL_AUDIT.md) for detailed solutions.

## Development

### Project Structure

```
accreditation_copilot/
├── api/              # FastAPI backend
├── frontend/         # Next.js frontend
├── audit/            # Audit engine
├── retrieval/        # Document retrieval
├── scoring/          # Scoring pipeline
├── llm/              # LLM components
├── utils/            # Utilities
└── models/           # Model management
```

### Adding New Criteria

1. Edit `criteria/criterion_registry.py`
2. Add criterion definition
3. Restart backend

### Modifying Scoring

1. Edit `scoring/evidence_scorer.py` or `scoring/confidence_calculator.py`
2. Test with `python deep_score_diagnostic.py`
3. Restart backend

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Groq** - Fast LLM inference
- **Ollama** - Local LLM deployment
- **BAAI** - BGE embedding and reranker models
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework
- **FAISS** - Efficient similarity search

## Support

- 📧 Email: support@example.com
- 💬 Discord: [Join our community](https://discord.gg/example)
- 🐛 Issues: [GitHub Issues](https://github.com/Effec77/Omni-Accreditation-Assistant/issues)
- 📖 Docs: [Documentation](DOCUMENTATION.md)

## Roadmap

- [ ] Multi-tenancy support
- [ ] Document versioning
- [ ] Comparative analysis
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Mobile applications
- [ ] Advanced analytics
- [ ] API webhooks

---

**Made with ❤️ for educational institutions**

**Version**: 1.0.0  
**Last Updated**: March 2026
