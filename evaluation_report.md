# Evaluation Report: The Unofficial Guide
## Morgan State University Professor Reviews RAG System

---

## Overview

This evaluation tests the RAG system against 5 planned questions from the evaluation plan, plus 1 out-of-scope question to test grounding. Each question is graded as Accurate, Partially Accurate, or Inaccurate based on whether the retrieved chunks and generated answer match the expected answer.

---

## Test Results

### Question 1
**Question:** What do students say about Professor Fuller's grading in MATH110?

**Expected Answer:** Students say homework barely counts and tests make or break your grade. No extra credit or retakes given.

**System Response:** According to the context, students say that Professor Fuller's grading in MATH110 is primarily based on tests and quizzes, with homework weighing very little. One student mentioned that "Homework barely counts, tests and quizzes mainly make or break your grade" (Source 4: ProfJulian.txt), while another stated that "Homework weighs almost nothing and tests are the majority of your grade" (Source 2: ProfJulian.txt). Additionally, students warned about pop quizzes having a significant impact on the grade.

**Chunks Retrieved:** All 5 chunks from ProfJulian.txt — directly relevant reviews about grading and quizzes.

**Retrieval:** ✅ Accurate

**Response:** ✅ Accurate

**Notes:** Perfect retrieval and response. The system correctly identified Fuller's grading style and cited the right sources.

---

### Question 2
**Question:** Is Professor Samuel easy or hard?

**Expected Answer:** Professor Samuel is considered easy to very easy — difficulty rated 1.4/5 and 100% of students would take him again.

**System Response:** Professor Samuel has mixed reviews regarding difficulty. Some sources describe him as a "Tough grader" and "Strict grader" with test heavy courses and mandatory attendance. Other sources say his lectures were "not too hard to understand" and that he cares about students. Overall the system concluded he may be challenging but his teaching style makes material understandable.

**Chunks Retrieved:** Chunks from ProfOlukole.txt — relevant but skewed toward the "strict grader" tag rather than his overall 4.9/5 rating.

**Retrieval:** ⚠️ Partially Accurate

**Response:** ⚠️ Partially Accurate

**Notes:** The system found the right professor but gave a mixed picture when the overwhelming student consensus is that he is excellent and easy. The issue is that "tough grader" and "strict grader" tags in the chunks pulled the answer toward difficulty, even though the majority of reviews are very positive. The overall rating (4.9/5, 100% would take again) was not captured in the retrieved chunks.

---

### Question 3
**Question:** What is the workload like in Professor Morales' RELG305 class?

**Expected Answer:** Extremely heavy — multiple 10-page quizzes per week with only 7 minutes to complete, plus long essays and weekly summaries.

**System Response:** The workload in Professor Morales' class is described as heavy. The class has three 10-page quizzes a week with only 7 minutes to complete them, a 400 word minimum summary of readings/videos a week, and three 5-page 1500 word minimum essays later in the semester. Assignments are scattered and demanding for minimal grades.

**Chunks Retrieved:** All 5 chunks from ProfHarold.txt — highly relevant reviews about workload and assignments.

**Retrieval:** ✅ Accurate

**Response:** ✅ Accurate

**Notes:** Best performing query. All retrieved chunks were from the correct professor and the answer was detailed and well cited.

---

### Question 4
**Question:** Do students recommend Professor Zarif for Biology?

**Expected Answer:** Yes — 82% would take him again. Students say attending lectures, reading the textbook, and doing homework leads to success.

**System Response:** Yes, students highly recommend Professor Zarif for Biology. A student states that "Dr. Zarif is an extraordinary professor at MSU" and that if you study and attend lectures you will not have a problem passing the class. All sources have a "Would Take Again: Yes" rating. Students recommend reading the textbook, writing notes, doing homework, and then listening to lectures.

**Chunks Retrieved:** Chunks from ProfJelani.txt — directly relevant positive reviews about Professor Zarif.

**Retrieval:** ✅ Accurate

**Response:** ✅ Accurate

**Notes:** After re-embedding ChromaDB to include all 10 professors, this query worked perfectly. Initially failed because ChromaDB was built before the file was confirmed to have content.

---

### Question 5
**Question:** How does Professor Rose treat students in ENGL102?

**Expected Answer:** Reviews are very negative — students say she is rude, yells, gives no feedback, comes late and unprepared, and almost no one gets an A.

**System Response:** I don't have enough information about that in my documents. The provided sources do not mention a Professor Rose or the course ENGL102.

**Chunks Retrieved:** Chunks from ProfOlukole.txt, ProfHarold.txt, and ProfJulian.txt — none related to Professor Rose.

**Retrieval:** ❌ Inaccurate

**Response:** ❌ Inaccurate

**Notes:** This is the documented failure case. See failure analysis below.

---

### Question 6 (Out of Scope — Grounding Test)
**Question:** What is the best dorm at Morgan State?

**Expected Answer:** System should decline to answer since documents only cover professor reviews.

**System Response:** I don't have enough information about that in my documents. The provided sources contain information about professors at Morgan State University but do not mention dorms.

**Retrieval:** ✅ Correct behavior

**Response:** ✅ Correct behavior

**Notes:** Grounding works correctly. The system did not hallucinate or draw on outside knowledge when asked something outside its document scope.

---

## Failure Case Analysis

### Question 5 — Professor Rose Not Retrieved

**What happened:** When asked about Professor Rose, the system returned chunks from Samuel, Morales, and Fuller instead. It correctly identified it had no relevant information and declined to answer — but the real problem is that ProfDenise.txt exists and has content, yet Rose's chunks were never retrieved.

**Why it happened:** The semantic embedding for "How does Professor Rose treat students in ENGL102?" did not match strongly enough against Rose's chunks. The word "treat" pulled the retrieval toward reviews that used words like "difficult", "strict", and "demanding" — which are more common in the Biology and Math professor reviews. Rose's reviews use words like "rude", "yells", and "unprepared" which are semantically different enough that they ranked below other professors' chunks.

**What this reveals:** Semantic search is not perfect. When a query word like "treat" is ambiguous, the embedding model matches it to the most statistically common usage in the corpus rather than the intended meaning. This is a known limitation of small embedding models like all-MiniLM-L6-v2 on domain-specific text.

**How it could be fixed:** Adding keyword-based search (BM25) alongside semantic search (hybrid search) would catch cases where the professor's name appears in the document but the semantic similarity is low. This is listed as a stretch feature in the project spec.

---

## Summary

| # | Question | Retrieval | Response |
|---|---|---|---|
| 1 | Fuller grading | ✅ Accurate | ✅ Accurate |
| 2 | Samuel difficulty | ⚠️ Partial | ⚠️ Partial |
| 3 | Morales workload | ✅ Accurate | ✅ Accurate |
| 4 | Zarif recommendation | ✅ Accurate | ✅ Accurate |
| 5 | Rose treatment | ❌ Inaccurate | ❌ Inaccurate |
| 6 | Dorm (out of scope) | ✅ Correct | ✅ Correct |

**3 fully accurate, 1 partially accurate, 1 failure, 1 correct grounding rejection.**

The system performs well on professors with distinctive vocabulary in their reviews (Morales, Fuller, Zarif) and struggles with professors whose review language overlaps semantically with other professors in the corpus (Rose). The grounding mechanism works correctly — the system never hallucinated an answer outside its document scope.