# My Learnings Log
> Personal notes — gitignored, never pushed. Updated as I build.

---

## Project 1 — The Unofficial Guide (RAG System)

### What is LangChain?
LangChain is a library that gives you pre-built tools for building AI pipelines. Instead of coding everything from scratch, it has ready-made components for loading documents, splitting text, connecting to vector stores, and talking to LLMs. Think of it like a toolbox specifically designed for AI app development. We only used one piece of it — the text splitter.

---

### What is a Text Splitter?
A text splitter cuts long documents into smaller chunks so an embedding model can process them. You can't just throw a whole document at a vector database — you need small, focused pieces so the search can find the exact relevant part. LangChain's `RecursiveCharacterTextSplitter` splits by paragraphs first, then sentences, then words, then characters — trying to keep meaningful chunks together.

---

### What is Chunking and Why Does It Matter?
Chunking is the process of splitting documents into smaller pieces before embedding them. The chunk size and overlap you choose directly affects retrieval quality:
- **Too small** = chunks lose context, embeddings carry no meaning
- **Too large** = chunks blend multiple topics, hard to match a specific query
- **Overlap** = a small repeated section between chunks so key thoughts don't get cut off at a boundary

For our project we used 300-character chunks with 50-character overlap because our documents are short student reviews, not long essays.

---

### What Does Each Function in ingest.py Do?
- `load_documents()` — reads every .txt file from the documents/ folder into memory
- `clean_text()` — strips extra blank lines and whitespace so chunks don't contain garbage
- `chunk_documents()` — cuts each document into 300-char chunks with 50-char overlap, keeping track of which file each chunk came from
- `inspect_chunks()` — randomly prints 5 chunks so you can visually check they look clean
- `if __name__ == "__main__"` — means "only run this code when you execute the file directly, not when it's imported by another file"

---

### Common Errors I Hit
**ModuleNotFoundError: No module named 'langchain.text_splitter'**
- Cause: newer versions of LangChain moved the text splitter to its own package
- Fix: `pip install langchain-text-splitters` and change the import to `from langchain_text_splitters import RecursiveCharacterTextSplitter`

---