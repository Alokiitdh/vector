# Product Research Agent

A powerful, AI-driven product research assistant that combines LangGraph agentic workflows with a beautiful Streamlit UI.

## 🚀 Quick Start

### Prerequisites
- Python >= 3.13
- `uv` package manager (recommended)
- OpenAI API Key
- Exa API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_key
   EXA_API_KEY=your_exa_key
   # Optional Configuration
   USER_LOCATION="US"      # Default: US
   CURRENCY="USD"          # Default: USD
   ```

### Running the Application

You can run the entire stack (FastAPI Backend + Streamlit Frontend) with a single command:

```bash
python run_app.py
```

Alternatively, run services individually:

**Backend (FastAPI)**
```bash
uvicorn src.api.main:app --reload --port 8000
```

**Frontend (Streamlit)**
```bash
streamlit run streamlit_app.py --server.port 8501
```

## 🏗 Architecture

- **Backend**: FastAPI serving a LangGraph workflow.
- **Agent**: A reacting agent graph (`src/graph`) that:
  1. Understands user specifications (`specs_agent`).
  2. Searches the web for products using Exa (`search_agent`).
  3. Synthesizes findings into a final recommendation (`combine_results`).
- **Frontend**: Streamlit application with a polished UI, creating a seamless chat-like experience for product research.

## 🛠 Configuration

| Environment Variable | Description | Default |
|----------------------|-------------|---------|
| `OPENAI_API_KEY` | Required for LLM inference | - |
| `EXA_API_KEY` | Required for web search | - |
| `USER_LOCATION` | Region for search results (2-letter code) | `US` |
| `CURRENCY` | Preferred currency for pricing | `USD` |

## 📚 Documentation

For more detailed frontend documentation, see [STREAMLIT_README.md](STREAMLIT_README.md).
