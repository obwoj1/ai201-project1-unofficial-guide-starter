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

For our project we used 400-character chunks with 50-character overlap because our documents are short student reviews, not long essays.

---

### What Does Each Function in ingest.py Do?
- `load_documents()` — reads every .txt file from the documents/ folder into memory
- `clean_text()` — strips extra blank lines and whitespace so chunks don't contain garbage
- `chunk_documents()` — cuts each document into 400-char chunks with 50-char overlap, keeping track of which file each chunk came from and prepending the professor name to every chunk
- `inspect_chunks()` — randomly prints 5 chunks so you can visually check they look clean
- `if __name__ == "__main__"` — means "only run this code when you execute the file directly, not when it's imported by another file"

---

### Common Errors I Hit

**ModuleNotFoundError: No module named 'langchain.text_splitter'**
- Cause: newer versions of LangChain moved the text splitter to its own package
- Fix: `pip install langchain-text-splitters` and change the import to `from langchain_text_splitters import RecursiveCharacterTextSplitter`

---

### Chunk Size — How It Affects Retrieval Quality
When I first ran ingest.py I used 300-character chunks. Some chunks were cutting mid-sentence like:
". He never replied to emails and had zero flexibility. Everyone struggled."
That chunk is useless on its own — no context, no professor name, nothing searchable.

I bumped it to 500 characters and the chunks immediately got better — full reviews stayed together instead of getting split awkwardly. Eventually settled on 400 characters as the sweet spot.

**The general rule:**
- Too small = fragments with no meaning, embeddings carry no signal
- Too large = multiple topics blend together, hard to match a specific query
- Sweet spot = one complete thought or review per chunk

**Overlap reminder:** The 50-character overlap means the last 50 characters of one chunk are repeated at the start of the next. This catches cases where a key thought gets split across a boundary — both chunks will carry enough context to be retrievable.

---

## Milestone 3 & 4 — Ingestion, Chunking, Embedding, Retrieval

### What is a RAG System?
RAG stands for Retrieval Augmented Generation. Instead of asking an LLM a question and hoping it knows the answer from training, you first RETRIEVE relevant documents from your own data, then GENERATE an answer using only those documents as context. This means answers are grounded in real sources, not hallucinated.

Our pipeline has 5 stages:
1. Ingest — load raw .txt files
2. Chunk — split into small pieces
3. Embed — convert chunks to vectors
4. Retrieve — find relevant chunks for a query
5. Generate — use LLM to answer from retrieved chunks

---

### What is an Embedding / Vector?
An embedding is a list of numbers that represents the MEANING of a piece of text. Similar meanings produce similar vectors. This is how semantic search works — "Is Professor Samuel difficult?" and "Is Samuel's class hard?" produce similar vectors even though the words are different.

The model we used: `all-MiniLM-L6-v2` from sentence-transformers. Runs locally, no API key needed.

---

### What is ChromaDB?
ChromaDB is a vector database — it stores embeddings and lets you search them by similarity. When you query it, it finds the chunks whose vectors are closest in meaning to your query vector. It's persistent, meaning it saves to disk so you don't re-embed every time.

---

### Chunk Size Experimentation
I tried different chunk sizes and here's what happened:

| Chunk Size | Total Chunks | Problem |
|---|---|---|
| 300 chars | 35 | Cut mid-sentence, fragments with no context |
| 500 chars | 19 | Too few chunks, professors went missing entirely |
| 400 chars | 24 | Better but still missing some professors |
| 400 chars + name prepend | 38 | All professors retrievable, reviews intact |

**Key lesson:** chunk count matters. Too few chunks means some professors have no representation in the vector store at all.

---

### The Professor Name Fix
The biggest retrieval fix was prepending the professor's name to every chunk. Before the fix, chunks looked like:

```
Grade: C
Review: Does not give extra credit...
```

After the fix:

```
Professor: Julian Fuller
Grade: C
Review: Does not give extra credit...
```

This meant every chunk carried identity information, so queries like "What do students say about Professor Fuller?" could actually match Fuller's chunks instead of returning random other professors.

---

### What Does Each Function in embed.py Do?
- `SentenceTransformer("all-MiniLM-L6-v2")` — loads the embedding model locally onto your machine, no API key needed
- `chromadb.PersistentClient(path="./chroma_db")` — creates a local vector database saved to disk in a folder called chroma_db
- `client.delete_collection()` — wipes old data so we always start fresh when re-embedding
- `embed_and_store(chunks)` — converts all chunks into vectors and stores them in ChromaDB with source metadata
- `retrieve(query, k=5)` — converts a question into a vector and finds the 5 most similar chunks in ChromaDB

---

### Empty File Bug
Two of my .txt files (ProfJulian.txt and ProfOlukole.txt) appeared in VS Code but were actually empty — content was never saved. The symptom was: chunks loaded from 10 documents but those professors never appeared in retrieval results. Diagnosed by running `cat documents/ProfJulian.txt` in terminal which returned nothing. Fix: manually paste and save content in VS Code.

**Lesson:** always verify file contents with `cat filename.txt` in terminal before assuming a file is correct.

---

### Key Vocabulary

| Term | What it means |
|---|---|
| RAG | Retrieval Augmented Generation — grounding LLM answers in your own documents |
| Embedding | A list of numbers representing the meaning of text |
| Vector Store | A database that stores and searches embeddings by similarity |
| Chunk | A small piece of a document fed into the embedding model |
| Semantic Search | Finding relevant content by meaning, not exact keyword match |
| Top-k | How many chunks to retrieve per query |
| Grounding | Making sure the LLM only answers from retrieved documents, not training data |
| Hallucination | When an LLM makes up an answer not supported by any source |