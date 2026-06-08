import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCUMENTS_DIR = "documents"

def load_documents():
    docs = []
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({
                "filename": filename,
                "text": text
            })
    print(f"Loaded {len(docs)} documents")
    return docs

def clean_text(text):
    # Remove excessive whitespace and blank lines
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)
def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = splitter.split_text(cleaned)

        # Extract professor name from the document
        prof_name = ""
        for line in cleaned.split("\n"):
            if line.startswith("Professor:"):
                prof_name = line.replace("Professor:", "").strip()
                break

        for i, chunk in enumerate(chunks):
            # Prepend professor name to every chunk so retrieval always knows who it's about
            labeled_chunk = f"Professor: {prof_name}\n{chunk}"
            all_chunks.append({
                "text": labeled_chunk,
                "source": doc["filename"],
                "chunk_index": i
            })

    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks

def inspect_chunks(chunks, n=5):
    import random
    print("\n--- SAMPLE CHUNKS ---")
    samples = random.sample(chunks, min(n, len(chunks)))
    for i, chunk in enumerate(samples):
        print(f"\nChunk {i+1} (source: {chunk['source']}, index: {chunk['chunk_index']}):")
        print(chunk["text"])
        print("-" * 40)

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    inspect_chunks(chunks)