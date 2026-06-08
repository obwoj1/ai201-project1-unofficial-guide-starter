import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
import gradio as gr

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("professor_reviews")

# Connect to Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve(query, k=5):
    """Convert query to vector and find top-k most relevant chunks from ChromaDB."""
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    chunks = results["documents"][0]
    sources = [meta["source"] for meta in results["metadatas"][0]]
    return chunks, sources


def generate(query, chunks, sources):
    """Send retrieved chunks to Groq LLM and get a grounded answer."""
    # Build context from retrieved chunks
    context = ""
    for i, (chunk, source) in enumerate(zip(chunks, sources)):
        context += f"[Source {i+1}: {source}]\n{chunk}\n\n"

    # System prompt enforces grounding
    system_prompt = """You are a helpful assistant that answers questions about professors at Morgan State University.
You must answer ONLY using the information provided in the context below.
If the context does not contain enough information to answer the question, say "I don't have enough information about that in my documents."
Do NOT use any outside knowledge. Always mention which source your answer comes from."""

    user_prompt = f"""Context:
{context}

Question: {query}

Answer based only on the context above and cite which source(s) you used."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content


def ask(question):
    """Full pipeline: retrieve chunks then generate grounded answer."""
    if not question.strip():
        return "Please enter a question.", ""

    chunks, sources = retrieve(question)
    answer = generate(question, chunks, sources)

    # Format sources list
    unique_sources = list(dict.fromkeys(sources))
    sources_text = "\n".join(f"• {s}" for s in unique_sources)

    return answer, sources_text


# Build Gradio UI
with gr.Blocks(title="Morgan State Unofficial Professor Guide") as demo:
    gr.Markdown("# 🎓 Morgan State Unofficial Professor Guide")
    gr.Markdown("Ask anything about Morgan State professors based on real student reviews from Rate My Professors.")

    with gr.Row():
        inp = gr.Textbox(
            label="Your Question",
            placeholder="e.g. Is Professor Samuel easy or hard?",
            lines=2
        )

    btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=10)
        sources = gr.Textbox(label="Sources", lines=10)

    btn.click(ask, inputs=inp, outputs=[answer, sources])
    inp.submit(ask, inputs=inp, outputs=[answer, sources])

    gr.Markdown("### Example Questions")
    gr.Markdown("""
- What do students say about Professor Fuller's grading?
- Is Professor Samuel easy or hard?
- What is the workload like in Professor Morales' class?
- Do students recommend Professor Zarif for Biology?
- How does Professor Rose treat students in ENGL102?
""")

if __name__ == "__main__":
    demo.launch()