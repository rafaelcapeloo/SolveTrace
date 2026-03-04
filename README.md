<p align="center">
  <h1 align="center">⚡ SolveTrace</h1>
  <p align="center">
    <strong>Open-source competitive programming problem analyzer</strong>
    <br />
    Paste a URL → Get a step-by-step solution with complexity analysis, code, and interview tips.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
  <img src="https://img.shields.io/badge/python-3.11+-blue" alt="Python" />
  <img src="https://img.shields.io/badge/next.js-14+-black" alt="Next.js" />
  <img src="https://img.shields.io/badge/fastapi-0.115+-teal" alt="FastAPI" />
</p>

---

## 📋 Table of Contents

- [What It Does](#-what-it-does)
- [Supported Platforms](#-supported-platforms)
- [Choose Your LLM](#-choose-your-llm)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Setup on Linux / macOS](#setup-on-linux--macos)
  - [Setup on Windows](#setup-on-windows)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [How the Analysis Pipeline Works](#-how-the-analysis-pipeline-works)
- [API Reference](#-api-reference)
- [Tech Stack](#-tech-stack)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🎯 What It Does

SolveTrace takes a competitive programming problem (via URL or pasted text) and generates a comprehensive analysis:

1. **Auto-scrapes** the problem statement, examples, input/output constraints
2. **Queries a RAG knowledge base** of 30+ algorithm patterns for relevant techniques
3. **Sends everything to your chosen LLM** with a carefully crafted prompt
4. **Returns a structured breakdown**:
   - 🔢 Step-by-step approach with reasoning
   - ⏱️ Time & space complexity with explanations
   - 💻 Clean, well-commented code solution
   - 💡 Key insights & common pitfalls
   - 🔗 Related problems from other platforms
   - 🎓 Interview tips

## 🌐 Supported Platforms

| Platform | Scraping | Example URL |
|----------|----------|-------------|
| **Codeforces** | ✅ Full support | `codeforces.com/problemset/problem/1/A` |
| **LeetCode** | ✅ Full support | `leetcode.com/problems/two-sum` |
| **AtCoder** | ✅ Full support | `atcoder.jp/contests/abc001/tasks/abc001_1` |
| **HackerRank** | ✅ Full support | `hackerrank.com/challenges/solve-me-first` |

> You can also paste problem text directly if your platform isn't supported.

## 🧠 Choose Your LLM

SolveTrace supports **3 LLM providers** — pick the one that fits your needs:

| Provider | Type | Cost | Setup | Best For |
|----------|------|------|-------|----------|
| **Ollama** | Local | Free | Install Ollama + pull a model | Privacy, offline use, no API costs |
| **Google Gemini** | Cloud API | Free tier available | Get API key from Google AI Studio | Fast, generous free tier |
| **OpenAI** | Cloud API | Paid | Get API key from OpenAI | GPT-4o quality |

### Ollama (Recommended for Getting Started)

Ollama lets you run AI models locally on your machine — **completely free, no API key needed**.

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh   # Linux/macOS
# Windows: download from https://ollama.com/download

# Pull a coding-optimized model (recommended)
ollama pull qwen2.5-coder:7b

# Or use a larger model for better quality
ollama pull qwen2.5-coder:14b
ollama pull llama3.1:8b
ollama pull codellama:13b
```

### Google Gemini

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create an API key (free tier: 15 requests/minute)
3. Set `GEMINI_API_KEY=your_key_here` in `backend/.env`
4. Set `LLM_PROVIDER=gemini` in `backend/.env`

### OpenAI

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create an API key (requires billing setup)
3. Set `OPENAI_API_KEY=your_key_here` in `backend/.env`
4. Set `LLM_PROVIDER=openai` in `backend/.env`

---

## 🚀 Quick Start

### Prerequisites

| Software | Version | Download |
|----------|---------|----------|
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org/) |
| **Git** | Any | [git-scm.com](https://git-scm.com/) |
| **Ollama** *(or API key)* | Latest | [ollama.com](https://ollama.com/) |

### Setup on Linux / macOS

```bash
# 1. Clone the repository
git clone https://github.com/rafaelcapeloo/SolveTrace.git
cd SolveTrace

# 2. Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure your LLM provider
cp .env.example .env
nano .env   # or use your preferred editor
# → Set LLM_PROVIDER to "ollama", "gemini", or "openai"
# → Set the corresponding API key if using a cloud provider

# 4. Start the backend server
uvicorn app.main:app --reload --port 8000

# 5. Open a new terminal tab, setup Frontend
cd ../frontend
npm install
npm run dev
```

**Open [http://localhost:3000](http://localhost:3000) and start analyzing! 🎉**

### Setup on Windows

```powershell
# 1. Clone the repository
git clone https://github.com/rafaelcapeloo/SolveTrace.git
cd SolveTrace

# 2. Setup Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure your LLM provider
copy .env.example .env
notepad .env
# → Set LLM_PROVIDER to "ollama", "gemini", or "openai"
# → Set the corresponding API key if using a cloud provider

# 4. Start the backend server
uvicorn app.main:app --reload --port 8000

# 5. Open a new terminal window, setup Frontend
cd ..\frontend
npm install
npm run dev
```

**Open [http://localhost:3000](http://localhost:3000) and start analyzing! 🎉**

> **Note for Windows users:** If `uvicorn` is not recognized, try `python -m uvicorn app.main:app --reload --port 8000`

---

## ⚙️ Configuration

All configuration is done through the `backend/.env` file. Here's a complete reference:

```env
# ===========================
# LLM Provider Configuration
# ===========================

# Which LLM to use: "ollama" (local), "gemini" (Google), or "openai"
LLM_PROVIDER=ollama

# --- Ollama (Local) ---
# Make sure Ollama is running: ollama serve
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b

# --- Google Gemini ---
# Get your key: https://aistudio.google.com/apikey
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.0-flash

# --- OpenAI ---
# Get your key: https://platform.openai.com/api-keys
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# ===========================
# Server Configuration
# ===========================

# SQLite database for caching scraped problems and analyses
DATABASE_URL=sqlite+aiosqlite:///./solvetrace.db

# Frontend URL (for CORS)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Set to true for verbose SQL and debug logging
DEBUG=false
```

### Switching LLM Providers

You can switch providers at any time by changing the `LLM_PROVIDER` value and restarting the backend. You can also switch providers **from the UI** using the LLM Provider dropdown on the Solve page — providers with a ✓ are configured and ready, while providers with ⚠ need their API key set in `.env`.

---

## 📁 Project Structure

```
SolveTrace/
├── backend/                          # FastAPI Python backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── analysis.py           # POST /api/analyze — main analysis endpoint
│   │   │   └── problems.py           # GET /api/problems — browse cached problems
│   │   ├── models/
│   │   │   ├── analysis.py           # Analysis SQLAlchemy model (stores LLM results)
│   │   │   └── problem.py            # Problem model (caches scraped data)
│   │   ├── schemas/
│   │   │   └── analysis.py           # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── analyzer.py           # 🧠 Core pipeline: Scrape → RAG → LLM → Store
│   │   │   ├── llm/
│   │   │   │   ├── gemini.py         # Google Gemini API client
│   │   │   │   ├── ollama.py         # Local Ollama client
│   │   │   │   ├── openai_client.py  # OpenAI GPT client
│   │   │   │   ├── parser.py         # JSON response parser + validator
│   │   │   │   └── prompts.py        # LLM prompt templates
│   │   │   ├── rag/
│   │   │   │   ├── knowledge.py      # 30+ algorithm pattern definitions
│   │   │   │   └── vectorstore.py    # Lightweight vector store (Gemini embeddings / keyword fallback)
│   │   │   └── scraper/
│   │   │       ├── base.py           # Base scraper interface
│   │   │       ├── codeforces.py     # Codeforces scraper
│   │   │       ├── leetcode.py       # LeetCode scraper
│   │   │       ├── atcoder.py        # AtCoder scraper
│   │   │       └── hackerrank.py     # HackerRank scraper
│   │   ├── utils/
│   │   │   └── helpers.py            # URL parsing, language validation
│   │   ├── config.py                 # Settings from environment variables
│   │   ├── database.py               # Async SQLAlchemy + SQLite setup
│   │   └── main.py                   # FastAPI app entry point
│   ├── .env.example                  # Configuration template
│   └── requirements.txt              # Python dependencies
│
├── frontend/                         # Next.js React frontend
│   └── src/
│       ├── app/
│       │   ├── page.tsx              # Landing page
│       │   ├── page.module.css       # Landing styles
│       │   └── solve/
│       │       ├── page.tsx          # 🎯 Main solve page (URL input, results, code)
│       │       └── page.module.css   # Solve page styles
│       ├── components/
│       │   └── layout/
│       │       ├── Navbar.tsx        # Navigation bar
│       │       └── Navbar.module.css # Navbar styles
│       ├── services/
│       │   └── api.ts               # API client (fetch wrapper)
│       └── types/
│           └── index.ts             # TypeScript interfaces
│
└── README.md                         # This file
```

---

## 🔄 How the Analysis Pipeline Works

```
User Input (URL or text)
         │
         ▼
┌─────────────────┐
│  1. SCRAPE       │  Auto-detect platform → scrape title, statement,
│     or PARSE     │  examples, constraints, tags, difficulty
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. CACHE CHECK  │  Check SQLite DB — if this problem was already
│                  │  analyzed in the same language, return cached result
└────────┬────────┘
         │ (cache miss)
         ▼
┌─────────────────┐
│  3. RAG QUERY    │  Query 30+ algorithm patterns (DP, graphs, greedy...)
│                  │  using embeddings or keyword matching
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. LLM CALL     │  Build structured prompt with problem + RAG context
│                  │  → Send to Ollama / Gemini / OpenAI
│                  │  → Parse JSON response
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. STORE & RETURN│  Save analysis to SQLite → return structured result
│                  │  with approach, complexity, code, insights, tips
└─────────────────┘
```

---

## 📡 API Reference

### `POST /api/analyze`

Analyze a competitive programming problem.

**Request Body:**
```json
{
  "url": "https://codeforces.com/problemset/problem/1/A",
  "problem_text": null,
  "language": "python",
  "provider": "ollama",
  "model": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | One of url/problem_text | Problem URL |
| `problem_text` | string | One of url/problem_text | Raw problem text |
| `language` | string | No (default: python) | Solution language |
| `provider` | string | No | Override LLM provider |
| `model` | string | No | Override model name |

**Response:** Full analysis with approach steps, complexity, code, insights, tips.

### `GET /api/analyze/{id}`
Retrieve a previously generated analysis by ID.

### `GET /api/config`
Get available LLM providers and their configuration status.

### `GET /api/problems`
List cached scraped problems. Optional `?platform=` filter.

### `GET /api/health`
Health check — returns status and current LLM provider.

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14+, TypeScript | UI, routing, SSR |
| **Styling** | CSS Modules | Scoped component styles |
| **Syntax Highlighting** | highlight.js | Code block rendering |
| **Backend** | FastAPI, Python 3.11+ | API, analysis pipeline |
| **Database** | SQLAlchemy (async) + SQLite | Cache & persistence |
| **Scraping** | httpx + BeautifulSoup4 | Platform-specific scrapers |
| **RAG** | Custom vector store | Algorithm pattern matching |
| **LLM (Local)** | Ollama | Run models locally |
| **LLM (Cloud)** | Google Gemini / OpenAI | Cloud API models |

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

### Easy
- Add more algorithm patterns to `backend/app/services/rag/knowledge.py`
- Improve LLM prompts in `backend/app/services/llm/prompts.py`
- Add more supported languages

### Medium
- Add scrapers for more platforms (SPOJ, UVa, DMOJ, Kattis)
- Add localStorage-based history in the frontend
- Add problem comparison (side-by-side analysis)
- Add export to PDF/Markdown

### Advanced
- Add more LLM providers (Anthropic Claude, Mistral, Groq)
- Add WebSocket streaming for real-time analysis progress
- Add a VS Code extension

### How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test locally (both frontend and backend)
5. Submit a pull request

---

## 🔧 Troubleshooting

### Backend won't start
```
ModuleNotFoundError: No module named 'app'
```
**Fix:** Make sure you're running from the `backend/` directory and your virtual environment is activated.

### Ollama connection refused
```
httpx.ConnectError: [Errno 111] Connection refused
```
**Fix:** Make sure Ollama is running. Start it with:
```bash
ollama serve          # Start the Ollama server
ollama pull qwen2.5-coder:7b   # Pull a model if not done yet
```

### Gemini / OpenAI API errors
```
ValueError: LLM analysis failed (Gemini): 403 ...
```
**Fix:** Check that your API key is correct in `backend/.env` and that you have sufficient quota/credits.

### Frontend can't connect to backend
```
TypeError: Failed to fetch
```
**Fix:** Make sure the backend is running on port 8000 and that `CORS_ORIGINS` in `.env` includes your frontend URL (`http://localhost:3000`).

### LeetCode scraping fails
LeetCode uses client-side rendering, which makes scraping harder. If scraping fails, try pasting the problem text directly using the "Paste Problem" mode.

---

## 📄 License

MIT — use it however you want.

---

<p align="center">
  Built with ☕ by <a href="https://github.com/rafaelcapeloo">@rafaelcapeloo</a>
</p>
