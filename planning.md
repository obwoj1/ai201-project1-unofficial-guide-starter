# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

This guide covers student-generated reviews of professors at Morgan State University, sourced from Rate My Professors. This knowledge is valuable because official university channels never tell you how a professor actually teaches, grades, or treats students in reality. Students rely on word of mouth and review sites to make informed decisions about which professors to take — this system makes that scattered knowledge searchable and answerable in one place.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | Benjamin Morgan, Engineering (CMGT420) | documents/ProfBenjamin.txt |
| 2 | Rate My Professors | Harold Morales, Religion (RELG305) | documents/ProfHarold.txt |
| 3 | Rate My Professors | Denise Rose, English (ENGL102) | documents/ProfDenise.txt |
| 4 | Rate My Professors | Mahdi Gharagozloo, Business (BUAD699, ENTR655) | documents/ProfMahdi.txt |
| 5 | Rate My Professors | Olukole Samuel, Biology (Biology202, Biology209) | documents/ProfOlukole.txt |
| 6 | Rate My Professors | Julian Fuller, Mathematics (MATH110, MATH107) | documents/ProfJulian.txt |
| 7 | Rate My Professors | Gerald Rameau, Biology (BIO101, BIOL106) | documents/ProjGerald.txt |
| 8 | Rate My Professors | Jelani Zarif, Biology (BIOL405, BIOL210) | documents/ProfJelani.txt |
| 9 | Rate My Professors | Safae Hamdoun, Biology (BIO310, BIOL210) | documents/ProfSafae.txt |
| 10 | Rate My Professors | Paminas Mayaka, Mathematics (MATH106, MATH113) | documents/ProfPaminas.txt |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:** Our documents are short, opinion-based student reviews — most individual reviews are only 2–5 sentences long. Using a small chunk size of 300 characters means each chunk captures one complete student review or a focused part of it, rather than blending multiple reviews together. A 50-character overlap ensures that if a key thought spans two chunks, both chunks carry enough context to be retrievable. Larger chunks would dilute the specific opinions we want to match against queries.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key needed)

**Top-k:** 5 chunks per query

**Production tradeoff reflection:** If deploying for real users, I would consider OpenAI's text-embedding-3-large for higher accuracy on nuanced opinion text, but it comes with API costs and rate limits. For a multilingual student body, a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would be worth the tradeoff. For latency-sensitive use, a locally hosted model like all-MiniLM-L6-v2 is ideal. Top-k of 5 gives the LLM enough context without flooding it with loosely related reviews.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Professor Fuller's grading in MATH110? | Students say homework barely counts and tests make or break your grade. No extra credit or retakes given. |
| 2 | Is Professor Samuel easy or hard? | Professor Samuel is considered easy to very easy — difficulty rated 1.4/5 and 100% of students would take him again. |
| 3 | What is the workload like in Professor Morales' RELG305 class? | Extremely heavy — multiple 10-page quizzes per week with only 7 minutes to complete, plus long essays and weekly summaries. |
| 4 | Do students recommend Professor Zarif for Biology? | Yes — 82% would take him again. Students say attending lectures, reading the textbook, and doing homework leads to success. |
| 5 | How does Professor Rose treat students in ENGL102? | Reviews are very negative — students say she is rude, yells, gives no feedback, comes late and unprepared, and almost no one gets an A. |

---

## Anticipated Challenges

1. **Sparse reviews for some professors:** Professor Morgan only has 1 review and Professor Gharagozloo has short reviews with little detail. Queries about these professors may return weak or incomplete answers because there simply isn't enough source material to draw from.

2. **Multiple Biology professors causing retrieval confusion:** Five of our ten documents are Biology professors. A vague query like "Is the Biology professor hard?" may retrieve chunks from multiple professors and produce a blended or confusing answer. The system needs to retrieve professor-specific chunks rather than mixing reviews across professors.

---

## Architecture