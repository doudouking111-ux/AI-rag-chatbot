# AI Demo Projects

Two demo projects showcasing practical LLM applications: a RAG document Q&A system and an AI-powered customer service chatbot.

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

## Configuration

Both projects read from `.env`:

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
```

## Tech Stack

- Python, LangChain, OpenAI API (GPT-4o-mini)
- Project 1: Streamlit, FAISS, PyMuPDF, python-docx
- Project 2: Gradio, LangChain Tool Calling
