# Physics Chatbot (RAG prep + chat UIs)

A small, learn-by-doing project for experimenting with:

- Ingesting a PDF and creating embeddings into a local Chroma vector store
- Chatting with a local LLM via Ollama (CLI chatbot)
- Chatting with OpenAI models through a simple Streamlit UI

This repo contains separate scripts for each task so you can run them independently.

## Repository Structure

- `chatbot.py` — Simple CLI chatbot using Ollama (`mistral:7b`).
- `streamlit.py` — Streamlit chat UI backed by OpenAI (`gpt-3.5-turbo`).
- `hello.py` — PDF → chunks → embeddings → persist to Chroma (Ollama embeddings, PyPDF2).
- `test.py` — Same idea as `hello.py` but using Hugging Face embeddings.
- `pdf_processing.py` — PDF text extraction with PyMuPDF (fitz) and Hugging Face embeddings; includes a small retrieval test.
- `db/chroma_db_physics` — Persisted Chroma database directory (created on first run).

Note: The CLI chatbot and Streamlit UI do not currently retrieve from the vector store. The vector store scripts help you prepare data for a future RAG workflow.

## Requirements

- Python 3.9+
- Ollama (for local LLM and, optionally, local embedding models)
- An OpenAI API key (only if you want to use the Streamlit UI)

Recommended Python packages:

```
pip install \
  streamlit openai \
  langchain langchain-community langchain-ollama langchain-chroma langchain-huggingface \
  chromadb \
  PyPDF2 pymupdf sentence-transformers
```

If you use Ollama models, install Ollama and pull models you need, for example:

```
# LLM used by chatbot.py
ollama pull mistral:7b

# Embedding model used by hello.py (via langchain_ollama)
ollama pull all-minilm:33m
```

## Quickstart

1) Prepare your PDF and vector store

- Place your PDF (e.g., `physics_notes.pdf`) at the project root.
- Option A — Ollama embeddings (PyPDF2):
  - `python hello.py`
- Option B — Hugging Face embeddings (PyPDF2):
  - `python test.py`
- Option C — Hugging Face embeddings (PyMuPDF):
  - Edit `pdf_processing.py` and set `pdf_path` to your file
  - `python pdf_processing.py`

All options will persist vectors under `db/chroma_db_physics`.

2) Run the CLI chatbot (local LLM)

- Ensure Ollama is running: `ollama serve`
- Run: `python chatbot.py`
- Type your question at the prompt, type `exit` or `quit` to stop.

3) Run the Streamlit chat (OpenAI API)

- `streamlit run streamlit.py`
- Enter your OpenAI API key in the sidebar when prompted.
- Start chatting in the UI.

## Configuration Notes

- Embeddings vs. LLMs:
  - `hello.py` uses `OllamaEmbeddings(model="all-minilm:33m")`.
  - `test.py` and `pdf_processing.py` use `HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")`.
  - Chroma stores are persisted to the same directory (`db/chroma_db_physics`). For consistency, prefer using the same embedding family when creating and querying a given collection.

- Retrieval example:
  - `pdf_processing.py` includes `check_db()` which demonstrates a simple similarity query using a Chroma retriever.

- Streamlit UI:
  - Uses OpenAI’s `gpt-3.5-turbo` out of the box. You can change the model in `streamlit.py`.

## Troubleshooting

- Chroma errors or stale state:
  - Stop your script and remove the directory `db/chroma_db_physics` if you want a clean start, then re-run an ingestion script.

- Ollama not responding:
  - Ensure the daemon is running (`ollama serve`) and that the requested model is pulled.

- PDF text extraction:
  - If a PDF extracts poorly with PyPDF2, try the PyMuPDF route (`pdf_processing.py`).

## Next Steps (Ideas)

- Wire the vector store into the chatbot for RAG-style answers.
- Add a small API wrapper and tests.
- Add a `requirements.txt` for reproducible installs.

---



