# 🌲 Field Terminal — Local RAG Assistant

An offline question-answering assistant that reads your own documents and answers questions using **only** that content — no internet connection required after setup.

Built as a learning project to understand Retrieval-Augmented Generation (RAG) from the ground up: embeddings, vector similarity search, local LLMs, and clean application architecture.

---

## What it does

You type a question. The app:

1. **Embeds** your question into a vector (a list of numbers representing its meaning).
2. **Searches** a local database of document chunks for the ones closest in meaning to your question.
3. **Augments** a prompt with those relevant chunks.
4. **Generates** an answer using a local LLM that reads only the retrieved chunks — and says "I don't have that information" if nothing relevant is found.

Everything — embeddings, search, and generation — runs on your own machine via [Foundry Local](https://learn.microsoft.com/en-us/windows/ai/foundry-local/), Microsoft's offline model runtime. No API keys, no cloud calls, no data leaving your computer.

---

## Architecture

```
YOU type a question
      │
      ▼
[1] EMBED the question → text becomes a vector
      │
      ▼
[2] SEARCH the database → find the closest-matching chunks
      │
      ▼
[3] AUGMENT the prompt → attach those chunks to your question
      │
      ▼
[4] GENERATE the answer → local LLM answers from the chunks only
      │
      ▼
ANSWER appears, with its source document, fully offline
```

The project follows a simple layered structure — each layer only talks to the one below it:

| Layer | Responsibility | Files |
|---|---|---|
| **App / UI** | Talk to the human | `app.py` (Streamlit), `main.py` (CLI) |
| **Logic** | Orchestrate the RAG loop | `src/retriever.py`, `src/generator.py`, `src/ingest.py` |
| **Data** | Store & fetch chunks + vectors | `src/database.py` (SQLite) |
| **AI** | Embeddings + local LLM | `src/embeddings.py`, Foundry Local |

---

## Project structure

```
local-rag-assistant/
├── app.py                 # Streamlit web UI ("Field Terminal")
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
├── data/
│   ├── docs/               # Source .txt documents (your knowledge base)
│   └── knowledge.db         # Generated SQLite DB (git-ignored, built by ingest.py)
├── src/
│   ├── config.py            # Central settings: paths, model names, chunk size
│   ├── database.py          # SQLite layer: init_db(), insert_chunk(), get_all_chunks()
│   ├── embeddings.py         # Text → vector, via sentence-transformers
│   ├── chunking.py           # Splits raw documents into passage-sized chunks
│   ├── ingest.py             # Pipeline: reads docs → chunks → embeds → stores
│   ├── retriever.py          # Finds the top-k most relevant chunks for a query
│   └── generator.py          # Builds the prompt, calls the local LLM, returns the answer
└── scratch/                 # Throwaway practice scripts from learning each piece
```

---

## Tech stack

| Tool | Purpose |
|---|---|
| **Python 3.11+** | Core language |
| **Foundry Local** | Runs the LLM locally, fully offline |
| **sentence-transformers** (`all-MiniLM-L6-v2`) | Turns text into embeddings |
| **SQLite** | Stores chunks and their embeddings |
| **NumPy** | Cosine similarity search |
| **Streamlit** | Web UI |

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Eda891/local-rag-assistant.git
cd local-rag-assistant
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1      # Windows PowerShell
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Install Foundry Local**
```bash
winget install Microsoft.FoundryLocal
```
Verify it works:
```bash
foundry run qwen2.5-0.5b
```

---

## Usage

**1. Add your documents**

Drop `.txt` files into `data/docs/`.

**2. Build the knowledge base**
```bash
python -m src.ingest
```
This reads every document, splits it into chunks, embeds each chunk, and stores everything in `data/knowledge.db`.

**3. Ask questions**

Command line:
```bash
python main.py
```

Or the web UI:
```bash
streamlit run app.py
```

---

## How retrieval works

Each question and each document chunk is turned into a 384-number vector using `all-MiniLM-L6-v2`. Similarity between two vectors is measured with **cosine similarity** — the closer to 1.0, the more similar the meaning, regardless of shared vocabulary.

Only chunks scoring above a minimum similarity threshold are passed to the LLM. If nothing scores high enough, the app returns "I don't have that information" instead of guessing — this is what keeps answers grounded in your actual documents rather than the model's general training knowledge.

---

## Limitations & deliberate choices

These are intentional simplifications for a learning project, not oversights:

- **Brute-force search**: every query is compared against every stored chunk (`O(n)`). Fine for a few thousand chunks; would need a proper vector index (e.g. FAISS) at larger scale.
- **Simple paragraph-based chunking**: splits on blank lines and glues paragraphs up to a character limit. No sentence-boundary or token-aware splitting — works well for structured documents, less well for dense unbroken prose.
- **Small local LLM** (`qwen2.5-0.5b`): fast and fully offline, but limited compared to larger models — occasionally prone to repetition or verbosity, mitigated via prompt constraints and generation limits.
- **Embeddings via sentence-transformers, not Foundry**: Foundry's embedding API was still maturing at the time of writing, so a well-established offline embedder was used instead. Swapping this out later only requires changing `src/embeddings.py`.

---

## Example questions

Try these once you've ingested documents on natural disasters, wilderness survival, or rebuilding infrastructure:

- "What should I do during an earthquake?"
- "How do I purify water in the wilderness?"
- "How do I make soap from scratch?"
- "What are signs of hypothermia?"

And to see the "I don't know" behavior in action, ask something unrelated to your docs, e.g. "What is a whale?"
