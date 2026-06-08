# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system covers student-generated reviews of professors at Morgan State University, sourced from Rate My Professors. This knowledge is valuable because official university channels — course catalogs, department websites, and syllabi — never tell you how a professor actually teaches, grades, or treats students in practice. Students rely on word of mouth and review sites to make informed decisions about which professors to take. This system makes that scattered, hard-to-search knowledge answerable through plain-language questions.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors | Web review page | documents/ProfBenjamin.txt |
| 2 | Rate My Professors | Web review page | documents/ProfHarold.txt |
| 3 | Rate My Professors | Web review page | documents/ProfDenise.txt |
| 4 | Rate My Professors | Web review page | documents/ProfMahdi.txt |
| 5 | Rate My Professors | Web review page | documents/ProfOlukole.txt |
| 6 | Rate My Professors | Web review page | documents/ProfJulian.txt |
| 7 | Rate My Professors | Web review page | documents/ProjGerald.txt |
| 8 | Rate My Professors | Web review page | documents/ProfJelani.txt |
| 9 | Rate My Professors | Web review page | documents/ProfSafae.txt |
| 10 | Rate My Professors | Web review page | documents/ProfPaminas.txt |

---

## Chunking Strategy

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** Our documents are short, opinion-based student reviews — most individual reviews are only 2–5 sentences long. A 400-character chunk size captures one complete student review or a focused part of it without blending multiple reviews together. We initially tried 300 characters but chunks were cutting mid-sentence, producing fragments with no standalone meaning. We tried 500 characters but that produced only 19 chunks across 10 documents, meaning some professors had almost no representation in the vector store. 400 characters was the sweet spot — enough context per chunk while keeping enough chunks for reliable retrieval. The 50-character overlap ensures that if a key thought spans two chunk boundaries, both chunks carry enough context to still be retrievable. Additionally, every chunk is prepended with the professor's name so retrieval always knows who a chunk is about, even when the review text itself doesn't mention the name.

**Final chunk count:** 38 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers, running locally with no API key or rate limits.

**Production tradeoff reflection:** For a real deployment serving all Morgan State students, I would evaluate OpenAI's text-embedding-3-large for higher accuracy on nuanced opinion text — it handles short, informal writing better than MiniLM but comes with API costs and rate limits that would need to be managed. If the student body is multilingual, paraphrase-multilingual-MiniLM-L12-v2 would be worth the tradeoff since it supports 50+ languages. For latency-sensitive use cases where responses need to be near-instant, a locally hosted model like all-MiniLM-L6-v2 is ideal since there's no network round-trip. The main limitation of our current model is context length — at 256 tokens max, longer reviews can get truncated during embedding, which reduces retrieval accuracy for detailed reviews.

---

## Grounded Generation

**System prompt grounding instruction:**
```
You are a helpful assistant that answers questions about professors at Morgan State University.
You must answer ONLY using the information provided in the context below.
If the context does not contain enough information to answer the question, say "I don't have enough information about that in my documents."
Do NOT use any outside knowledge. Always mention which source your answer comes from.
```

The user prompt also explicitly instructs the model: "Answer based only on the context above and cite which source(s) you used." The retrieved chunks are formatted with numbered source labels (e.g., [Source 1: ProfJulian.txt]) so the model can reference them directly in its response.

**How source attribution is surfaced in the response:** The Gradio UI displays two separate output boxes — one for the answer and one for the sources. The sources box lists every document that contributed to the retrieval, pulled programmatically from ChromaDB metadata rather than relying on the LLM to cite them. This guarantees attribution even if the model forgets to mention the source in its answer.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Professor Fuller's grading in MATH110? | Homework barely counts, tests make or break grade, no extra credit or retakes | Homework barely counts, tests and quizzes are majority of grade, beware of pop quizzes — cited ProfJulian.txt | Relevant | Accurate |
| 2 | Is Professor Samuel easy or hard? | Easy — 4.9/5 rating, 100% would take again | Mixed — described as both strict grader and easy to understand, concluded he may be challenging | Partially relevant | Partially accurate |
| 3 | What is the workload like in Professor Morales' RELG305 class? | Extremely heavy — 10-page quizzes, long essays, weekly summaries | Heavy workload — three 10-page quizzes per week, 400 word summaries, three 5-page essays — cited ProfHarold.txt | Relevant | Accurate |
| 4 | Do students recommend Professor Zarif for Biology? | Yes — 82% would take again, study and attend lectures | Yes — described as extraordinary, all sources show Would Take Again: Yes, strategy for passing provided | Relevant | Accurate |
| 5 | How does Professor Rose treat students in ENGL102? | Very negative — rude, yells, no feedback, comes late | I don't have enough information about that in my documents | Off-target | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** How does Professor Rose treat students in ENGL102?

**What the system returned:** "I don't have enough information about that in my documents." The system retrieved chunks from ProfOlukole.txt, ProfHarold.txt, and ProfJulian.txt — none of which are about Professor Rose — and correctly identified it had no relevant information.

**Root cause (tied to a specific pipeline stage):** The failure occurred at the retrieval stage. The query "How does Professor Rose treat students in ENGL102?" uses the word "treat" which semantically matched more strongly to reviews containing words like "difficult", "strict", and "demanding" — common in the Biology and Math professor chunks — rather than Rose's reviews which use words like "rude", "yells", and "unprepared". The all-MiniLM-L6-v2 embedding model is a general-purpose model not trained on academic review text, so it matched the emotional tone of the query to the wrong professor's reviews. Rose's chunks existed in ChromaDB but ranked below other professors' chunks in similarity score.

**What you would change to fix it:** Adding hybrid search — combining semantic search with keyword (BM25) search — would fix this. BM25 would catch the exact match on "Rose" and "ENGL102" even when the semantic similarity is low. This is the hybrid search stretch feature listed in the project spec. Alternatively, adding the professor's full name more prominently throughout each chunk (not just at the start) would increase the chance of a name-based semantic match.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before touching any code forced me to think through what my documents actually looked like before deciding how to split them. Because I had already decided on 300-character chunks with 50-character overlap in the spec, I had a concrete baseline to test against — and when retrieval failed I knew exactly what parameter to change and why. Without the spec I would have just guessed at chunk sizes without understanding the tradeoff.

**One way your implementation diverged from the spec, and why:** The spec described chunking at 300 characters but the final implementation uses 400 characters with professor name prepending — neither of which was in the original plan. This change was driven by real retrieval failures during testing: at 300 characters chunks were cutting mid-sentence, and without the professor name prepended, queries like "Is Professor Samuel easy?" returned results from completely different professors. The spec was updated in planning.md to reflect these changes as required.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Documents section and Chunking Strategy section of planning.md, along with the requirement to load .txt files from the documents/ folder and split them using LangChain's RecursiveCharacterTextSplitter.
- *What it produced:* A complete ingest.py script with load_documents(), clean_text(), chunk_documents(), and inspect_chunks() functions using the specified 300-character chunk size and 50-character overlap.
- *What I changed or overrode:* I changed the chunk size from 300 to 400 characters after testing showed 300 produced too many mid-sentence fragments. I also added professor name prepending to every chunk after discovering that retrieval was returning wrong professors — this was not in the original spec and came from debugging the output.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section and Architecture diagram from planning.md, along with the grounding requirement that the LLM must answer only from retrieved context and always cite sources.
- *What it produced:* A complete app.py with retrieve(), generate(), and ask() functions, plus a Gradio UI with a question input, answer output, and sources output box.
- *What I changed or overrode:* I verified that the system prompt actually enforced grounding by testing a question outside the document scope ("What is the best dorm at Morgan State?") — the system correctly declined to answer rather than hallucinating, confirming the grounding instruction was working. I also confirmed that source attribution was pulled programmatically from ChromaDB metadata rather than relying on the LLM to cite sources on its own.