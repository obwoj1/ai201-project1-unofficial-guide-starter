# The Unofficial Guide — Project 1

---

## Demo Video

<!-- Add your demo video link here after recording -->
🎥 **Demo Video:** [Insert link here]

---

## Domain

This system covers student-generated reviews of professors at Morgan State University, sourced from Rate My Professors. This knowledge is valuable because official university channels — course catalogs, department websites, and syllabi — never tell you how a professor actually teaches, grades, or treats students in practice. Students rely on word of mouth and review sites to make informed decisions about which professors to take. This system makes that scattered, hard-to-search knowledge answerable through plain-language questions.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors — Benjamin Morgan | Web review page | documents/ProfBenjamin.txt |
| 2 | Rate My Professors — Harold Morales | Web review page | documents/ProfHarold.txt |
| 3 | Rate My Professors — Denise Rose | Web review page | documents/ProfDenise.txt |
| 4 | Rate My Professors — Mahdi Gharagozloo | Web review page | documents/ProfMahdi.txt |
| 5 | Rate My Professors — Olukole Samuel | Web review page | documents/ProfOlukole.txt |
| 6 | Rate My Professors — Julian Fuller | Web review page | documents/ProfJulian.txt |
| 7 | Rate My Professors — Gerald Rameau | Web review page | documents/ProjGerald.txt |
| 8 | Rate My Professors — Jelani Zarif | Web review page | documents/ProfJelani.txt |
| 9 | Rate My Professors — Safae Hamdoun | Web review page | documents/ProfSafae.txt |
| 10 | Rate My Professors — Paminas Mayaka | Web review page | documents/ProfPaminas.txt |

All documents were manually copied from Rate My Professors (ratemyprofessors.com/school/638) since the site blocks automated scraping due to JavaScript rendering.

---

## Chunking Strategy

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** Our documents are short, opinion-based student reviews — most individual reviews are only 2–5 sentences long. A 400-character chunk size captures one complete student review or a focused part of it without blending multiple reviews together. We initially tried 300 characters but chunks were cutting mid-sentence, producing fragments with no standalone meaning. We tried 500 characters but that produced only 19 chunks across 10 documents, meaning some professors had almost no representation in the vector store. 400 characters was the sweet spot. The 50-character overlap ensures that if a key thought spans two chunk boundaries, both chunks carry enough context to still be retrievable. Additionally, every chunk is prepended with the professor's name so retrieval always knows who a chunk is about, even when the review text itself doesn't mention the name.

**Final chunk count:** 38 chunks across 10 documents

---

## Sample Chunks

Below are 5 labeled sample chunks from the final pipeline after prepending professor names:

**Chunk 1 — Source: ProfJulian.txt**
```
Professor: Julian Fuller
Attendance: Not Mandatory
Grade: C-
Textbook: Yes
Review: Does not give extra credit or retakes. Can be rude and snappy. High ego. Homework weighs almost nothing and tests are the majority of your grade. He doesn't let you know when the next quiz is, you must pay attention to the information on Canvas.
Tags: Lots of homework, Beware of pop quizzes, Lecture heavy
```

**Chunk 2 — Source: ProfHarold.txt**
```
Professor: Harold Morales
Textbook: Yes
Online Class: Yes
Review: Way too much work. Three 10-page quizzes a week with only 7 minutes to complete them. On top of that, a 400 word minimum summary of readings/videos a week. And later in the semester, three 5-page, 1500 word minimum essays. Also didn't post assignments until the week after classes started.
```

**Chunk 3 — Source: ProfOlukole.txt**
```
Professor: Olukole Samuel
Would Take Again: Yes
Grade: A
Textbook: N/A
Review: Professor O was an AMAZING professor, his lectures were very organized and not too hard to understand. He explains things in an easy way. Professor O also really cares about his students, he makes adjustments for his students needs and schedules. Overall a 10/10.
```

**Chunk 4 — Source: ProfJelani.txt**
```
Professor: Jelani Zarif
Would Take Again: Yes
Grade: A+
Textbook: Yes
Review: I took Dr. Zarif's microbiology course at Morgan State University and really enjoyed it. The secret to passing: read the textbook, write notes while reading, do the homework while you read, and then listen to his lecture. It's easy if you follow the steps. He expects greatness and gives no handouts.
```

**Chunk 5 — Source: ProfPaminas.txt**
```
Professor: Paminas Mayaka
Would Take Again: Yes
Grade: A+
Textbook: Yes
Review: Great teacher. Gives great feedback. All work is posted already so just do it and you will be fine. He's a great explainer. No matter how often you say you don't understand, he will try his best to help you without making you feel stupid. Highly recommended.
Tags: Clear grading criteria, Gives good feedback, Lots of homework
```

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers, running locally with no API key or rate limits.

**Production tradeoff reflection:** For a real deployment serving all Morgan State students, I would evaluate OpenAI's text-embedding-3-large for higher accuracy on nuanced opinion text — it handles short, informal writing better than MiniLM but comes with API costs and rate limits. If the student body is multilingual, paraphrase-multilingual-MiniLM-L12-v2 would be worth the tradeoff since it supports 50+ languages. For latency-sensitive use cases, a locally hosted model like all-MiniLM-L6-v2 is ideal since there's no network round-trip. The main limitation of our current model is context length — at 256 tokens max, longer reviews can get truncated during embedding, which reduces retrieval accuracy for detailed reviews.

---

## Retrieval Test Results

**Query 1: "What do students say about Professor Fuller's grading?"**

Top returned chunks:
- Chunk 1 (ProfJulian.txt): "Does not give extra credit or retakes. Homework weighs almost nothing and tests are the majority of your grade."
- Chunk 2 (ProfJulian.txt): "Homework barely counts, tests and quizzes mainly make or break your grade."
- Chunk 3 (ProfJulian.txt): "Don't take this professor, he doesn't work with students. No extra credit at all."
- Chunk 4 (ProfJulian.txt): "He gives too many assignments and doesn't let you make up tests even if you were absent."
- Chunk 5 (ProfJulian.txt): "Extremely difficult and unaccommodating professor. Would not recommend."

**Why these chunks are relevant:** All 5 returned chunks are from ProfJulian.txt and directly address Fuller's grading style, extra credit policy, and test weight. The query word "grading" semantically matched the review text about tests, quizzes, and homework weights. The professor name prepending ensured all chunks were correctly attributed to Fuller.

---

**Query 2: "Is Professor Samuel easy or hard?"**

Top returned chunks:
- Chunk 1 (ProfOlukole.txt): "The professor teaches in a way that's easy to understand. He is helpful and encourages students to succeed."
- Chunk 2 (ProfOlukole.txt): "Professor O was an AMAZING professor, his lectures were very organized and not too hard to understand."
- Chunk 3 (ProfOlukole.txt): "Fall 2025 session was lecture heavy with no labs, test heavy, mandatory attendance and participation. Strict grader."
- Chunk 4 (ProjGerald.txt): "Extremely difficult. Lectures were confusing, he barely explained the slides."
- Chunk 5 (ProfHarold.txt): "Dr. Morales was by far the worst professor I've ever had."

**Why these chunks are relevant (and where they fall short):** The top 3 chunks correctly retrieved Samuel's reviews. Chunks 4 and 5 are off-target — they come from Gerald Rameau and Harold Morales. The words "easy" and "hard" in the query matched other professors' reviews that used similar vocabulary. This is a partial retrieval success.

---

**Query 3: "What is the workload like in Professor Morales' class?"**

Top returned chunks:
- Chunk 1 (ProfHarold.txt): "Heavy workload, leaving little time to actually study. Tests with many questions but only 7 minutes to complete."
- Chunk 2 (ProfHarold.txt): "Three 10-page quizzes a week with only 7 minutes to complete. 400 word minimum summary of readings/videos a week."
- Chunk 3 (ProfHarold.txt): "Professor Morales' teaching style is inconsistent, with assignments scattered and demanding for minimal grades."
- Chunk 4 (ProfHarold.txt): "Dr. Morales was by far the worst professor I've ever had. He isn't understanding."
- Chunk 5 (ProfHarold.txt): "Lots of homework, Lecture heavy."

**Why these chunks are relevant:** All 5 chunks are from ProfHarold.txt and directly address workload — quizzes, essays, summaries, and assignment volume. The query word "workload" semantically matched review text about homework, assignments, and quizzes. This was the strongest performing query in the evaluation.

---

## Grounded Generation

**System prompt grounding instruction:**
```
You are a helpful assistant that answers questions about professors at Morgan State University.
You must answer ONLY using the information provided in the context below.
If the context does not contain enough information to answer the question, say "I don't have enough information about that in my documents."
Do NOT use any outside knowledge. Always mention which source your answer comes from.
```

The user prompt also explicitly instructs the model: "Answer based only on the context above and cite which source(s) you used." Retrieved chunks are formatted with numbered source labels (e.g., [Source 1: ProfJulian.txt]) so the model can reference them in its response. Source attribution is also pulled programmatically from ChromaDB metadata and displayed in a separate UI panel, guaranteeing attribution even if the model omits it.

---

## Example Responses

**Response 1 — Query: "What do students say about Professor Fuller's grading in MATH110?"**

> According to the context, students say that Professor Fuller's grading in MATH110 is primarily based on tests and quizzes, with homework weighing very little. One student mentioned that "Homework barely counts, tests and quizzes mainly make or break your grade" (Source 4: ProfJulian.txt), while another stated that "Homework weighs almost nothing and tests are the majority of your grade" (Source 2: ProfJulian.txt). No extra credit or retakes are given.
>
> **Sources:** ProfJulian.txt

---

**Response 2 — Query: "Do students recommend Professor Zarif for Biology?"**

> Yes, students highly recommend Professor Zarif for Biology. According to Source 1 (ProfJelani.txt), a student describes him as "an extraordinary professor at MSU" and states that if you study and attend lectures, you will not have a problem passing the class. Source 2 (ProfJelani.txt) provides a strategy for passing: read the textbook, write notes while reading, do homework while reading, then listen to the lecture. All sources show "Would Take Again: Yes."
>
> **Sources:** ProfJelani.txt

---

**Response 3 — Out-of-scope query: "What is the best dorm at Morgan State?"**

> I don't have enough information about that in my documents. The provided sources contain information about professors at Morgan State University but do not mention dorms.
>
> **Sources:** ProfHarold.txt, ProjGerald.txt, ProfPaminas.txt, ProfJulian.txt, ProfOlukole.txt

---

## Query Interface

The system uses a Gradio web UI accessible at `http://127.0.0.1:7860` when running `python3 app.py`.

**Input fields:**
- Question text box — user types a plain-language question about any Morgan State professor

**Output fields:**
- Answer box — the LLM's grounded response citing which sources it used
- Sources box — a list of the document filenames retrieved from ChromaDB for that query

**Sample interaction transcript:**

> **User:** What is the workload like in Professor Morales' RELG305 class?
>
> **Answer:** The workload in Professor Morales' class is described as extremely heavy. According to Source 1 (ProfHarold.txt), the class has three 10-page quizzes a week with only 7 minutes to complete them, a 400 word minimum summary of readings/videos a week, and three 5-page 1500 word minimum essays later in the semester. Source 2 (ProfHarold.txt) also mentions that the professor constantly assigns a heavy workload leaving little time to study. Assignments were also posted late, preventing students from switching to another class.
>
> **Sources:**
> • ProfHarold.txt

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Professor Fuller's grading in MATH110? | Homework barely counts, tests make or break grade, no extra credit or retakes | Homework barely counts, tests and quizzes are majority of grade, beware of pop quizzes — cited ProfJulian.txt | Relevant | Accurate |
| 2 | Is Professor Samuel easy or hard? | Easy — 4.9/5 rating, 100% would take again | Mixed — described as both strict grader and easy to understand, concluded he may be challenging | Partially relevant | Partially accurate |
| 3 | What is the workload like in Professor Morales' RELG305 class? | Extremely heavy — 10-page quizzes, long essays, weekly summaries | Heavy workload — three 10-page quizzes per week, 400 word summaries, three 5-page essays — cited ProfHarold.txt | Relevant | Accurate |
| 4 | Do students recommend Professor Zarif for Biology? | Yes — 82% would take again, study and attend lectures | Yes — described as extraordinary, all sources show Would Take Again: Yes, strategy for passing provided | Relevant | Accurate |
| 5 | How does Professor Rose treat students in ENGL102? | Very negative — rude, yells, no feedback, comes late | I don't have enough information about that in my documents | Off-target | Inaccurate |

---

## Failure Case Analysis

**Question that failed:** How does Professor Rose treat students in ENGL102?

**What the system returned:** "I don't have enough information about that in my documents." The system retrieved chunks from ProfOlukole.txt, ProfHarold.txt, and ProfJulian.txt — none of which are about Professor Rose.

**Root cause (tied to a specific pipeline stage):** The failure occurred at the retrieval stage. The query "How does Professor Rose treat students in ENGL102?" uses the word "treat" which semantically matched more strongly to reviews containing words like "difficult", "strict", and "demanding" — common in Biology and Math professor chunks — rather than Rose's reviews which use words like "rude", "yells", and "unprepared". The all-MiniLM-L6-v2 model is a general-purpose model not trained on academic review text, so it matched the emotional tone of the query to the wrong professor's reviews. Rose's chunks existed in ChromaDB but ranked below other professors' chunks in similarity score.

**What you would change to fix it:** Adding hybrid search — combining semantic search with keyword (BM25) search — would fix this. BM25 would catch the exact match on "Rose" and "ENGL102" even when the semantic similarity is low. Alternatively, adding the professor's full name more prominently throughout each chunk would increase the chance of a name-based semantic match.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before touching any code forced me to think through what my documents actually looked like before deciding how to split them. Because I had already decided on a concrete chunk size in the spec, I had a clear baseline to test against — and when retrieval failed I knew exactly what parameter to change and why. Without the spec I would have just guessed at chunk sizes without understanding the tradeoff.

**One way your implementation diverged from the spec, and why:** The spec originally described 300-character chunks, but the final implementation uses 400 characters with professor name prepending — neither of which was in the original plan. This change was driven by real retrieval failures during testing: at 300 characters chunks were cutting mid-sentence, and without the professor name prepended, queries like "Is Professor Samuel easy?" returned results from completely different professors. The spec was updated in planning.md to reflect these changes as required.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Documents section and Chunking Strategy section of planning.md, along with the requirement to load .txt files from the documents/ folder and split them using LangChain's RecursiveCharacterTextSplitter.
- *What it produced:* A complete ingest.py script with load_documents(), clean_text(), chunk_documents(), and inspect_chunks() functions using the specified chunk size and overlap.
- *What I changed or overrode:* I changed the chunk size from 300 to 400 characters after testing showed 300 produced too many mid-sentence fragments. I also added professor name prepending to every chunk after discovering that retrieval was returning wrong professors — this was not in the original spec and came from debugging real output.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section and Architecture diagram from planning.md, along with the grounding requirement that the LLM must answer only from retrieved context and always cite sources.
- *What it produced:* A complete app.py with retrieve(), generate(), and ask() functions, plus a Gradio UI with a question input, answer output, and sources output box.
- *What I changed or overrode:* I verified grounding by testing an out-of-scope question ("What is the best dorm at Morgan State?") — the system correctly declined rather than hallucinating. I confirmed source attribution was pulled programmatically from ChromaDB metadata rather than relying on the LLM to cite sources on its own, making attribution structurally guaranteed.