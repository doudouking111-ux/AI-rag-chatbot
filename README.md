# AI Demo Projects

Three demo projects showcasing practical LLM applications: RAG document Q&A, AI customer service chatbot, and AI-powered workflow automation.

## Project 1: RAG Document Q&A

Upload PDF/Word documents and ask questions — the system retrieves relevant chunks and generates answers with source citations.

### Architecture

```
Upload (PDF/Word) → Parse → Chunk (500 tokens) → Embed (OpenAI) → FAISS Vector Store
User Question → Retrieval (top-4) → GPT-4o-mini → Answer + Source Citations
```

### Features

- PDF and Word (.docx) document parsing
- Recursive text splitting with 80-token overlap
- FAISS vector similarity search
- Multi-turn conversation with sliding window memory (last 5 turns)
- Source document citations in responses

### Files

| File | Description |
|------|-------------|
| `rag.py` | Core pipeline: parse → chunk → embed → retrieval chain |
| `app.py` | Streamlit web UI with sidebar upload and chat interface |

### Usage

```bash
pip install -r requirements.txt
# Edit .env with your OpenAI API key
streamlit run app.py
```

---

## Project 2: AI Customer Service Chatbot

A conversational chatbot that answers FAQs, checks inventory, creates orders, and books reservations — powered by LLM tool calling.

### Architecture

```
User (Gradio Web UI)
  → LangChain Agent (GPT-4o-mini)
    → System Prompt (company knowledge base)
    → Tool Calling: check_inventory / create_order / reserve_seat
    → Multi-turn memory (per session)
```

### Features

- FAQ answering from embedded knowledge base (menu, hours, location)
- 3 callable tools: inventory check, order creation, seat reservation
- Automatic tool selection by LLM based on user intent
- Per-session conversation history
- Gradio ChatInterface with example prompts

### Files

| File | Description |
|------|-------------|
| `chatbot/agent.py` | LangChain agent with tool calling and conversation memory |
| `chatbot/tools.py` | Tool definitions: `check_inventory`, `create_order`, `reserve_seat` |
| `chatbot/knowledge.py` | Company info and system prompt |
| `chatbot/config.py` | Environment variable loader |
| `chatbot/app.py` | Gradio web UI |

### Usage

```bash
cd chatbot
pip install -r requirements.txt
# Edit .env with your OpenAI API key
python app.py
# Open http://localhost:7860
```

---

## Project 3: AI Invoice Processing Workflow

Upload invoice PDFs — AI extracts structured data (vendor, items, amounts) → saves to spreadsheet → sends notification. Simulates a full automation pipeline.

### Architecture

```
Upload PDF → Parse Text (PyMuPDF)
           → AI Extraction (GPT-4o-mini → structured JSON)
           → Save to CSV (simulates Google Sheets)
           → Send Notification (simulates Slack Webhook)
           → Streamlit UI displays each step + history
```

### Features

- PDF text extraction with PyMuPDF
- LLM-powered structured data extraction (invoice number, vendor, line items, amounts)
- CSV storage with append mode (simulates Google Sheets API)
- Notification simulation (simulates Slack Webhook)
- Processing history dashboard
- Sample invoice PDF included for demo

### Files

| File | Description |
|------|-------------|
| `ai_workflow/app.py` | Streamlit web UI — upload, process, display results |
| `ai_workflow/pipeline.py` | Core pipeline: parse → extract → store → notify |
| `ai_workflow/extractor.py` | OpenAI structured extraction (returns JSON) |
| `ai_workflow/storage.py` | CSV storage (simulates Google Sheets) |
| `ai_workflow/notifier.py` | Notification (simulates Slack Webhook) |
| `ai_workflow/config.py` | Environment variable loader |
| `ai_workflow/sample_invoices/` | Sample invoice PDF for demo |

### Usage

```bash
cd ai_workflow
pip install -r requirements.txt
# Edit .env with your OpenAI API key
streamlit run app.py
```

---

## Configuration

All projects read from `.env`:

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
```

## Tech Stack

- Python, LangChain, OpenAI API (GPT-4o-mini)
- Project 1: Streamlit, FAISS, PyMuPDF, python-docx
- Project 2: Gradio, LangChain Tool Calling
- Project 3: Streamlit, PyMuPDF, LangChain structured extraction
