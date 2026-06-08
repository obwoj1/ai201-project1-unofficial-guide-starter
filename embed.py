import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, clean_text, chunk_documents

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Delete collection if it already exists (fresh start)
try:
    client.delete_collection("professor_reviews")
except:
    pass

collection = client.create_collection("professor_reviews")

def embed_and_store(chunks):
    print(f"Embedding {len(chunks)} chunks...")
    texts = [chunk["text"] for chunk in chunks]
    sources = [chunk["source"] for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": s} for s in sources],
        ids=ids
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB!")

def retrieve(query, k=5):
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    print(f"\nQuery: {query}")
    print("--- TOP RESULTS ---")
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"\nResult {i+1} (source: {meta['source']}):")
        print(doc)
        print("-" * 40)

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    embed_and_store(chunks)

    # Test retrieval with 3 evaluation questions
    retrieve("What do students say about Professor Fuller's grading?")
    retrieve("Is Professor Samuel easy or hard?")
    retrieve("What is the workload like in Professor Morales class?")