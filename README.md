# Enterprise HAI Study

A local replication of the PepsiCo Data Analyst Agent
architecture from Microsoft Build 2026 (BRK224).
Built entirely with free, local tools; no API keys, no cloud.

---

## Why this exists

BRK224 made a claim I wanted to test: that the bottleneck
for enterprise AI agents is not model capability, it is data
context. PepsiCo spent significant engineering effort
modernising their data layer before their agents could work
reliably. I wanted to understand why at a hands-on level,
not just take their word for it.

So I built a small Data Analyst Agent that answers business
questions two ways; SQL generation and semantic search, then
compared which approach wins for which type of question.

---

## What I built

A local pipeline over a SQLite database of 10 customer
complaints, with two query paths:

- SQL path: phi3:mini generates a SQL query from natural
  language, which runs against SQLite
- Semantic path: nomic-embed-text embeds the question,
  ChromaDB finds the most similar complaint vectors

Four test questions, designed to stress different capabilities.

---

## Results

| Question | SQL | Semantic | Winner |
|---|---|---|---|
| Unresolved complaints from North region | Correct | Ignored filter | SQL |
| Drinks that lost fizz or carbonation | Hallucinated foreign schema | Found by meaning | Semantic |
| Packaging problems reported | Misunderstood concept | Correct | Semantic |
| Which product has most complaints | Correct GROUP BY | Not useful for aggregation | SQL |

Final score: SQL 2, Semantic 2.

---

## The interesting part

SQL and semantic search failed on completely opposite
question types, which is exactly what PepsiCo's session
argued. Neither alone is sufficient; you need both,
routing intelligently between them.

But there was a finding the session did not cover: SQL
failure modes were inconsistent across runs. Question 2
returned empty results in one run, then hallucinated an
entirely different database schema in the next; fake tables,
fake columns, an unrelated question about coffee and emails
injected into its own SQL output. Same question, different
failure each time.

Consistent failure is workable; users learn to route around
it. Unpredictable failure is a trust calibration problem.
Users cannot build a reliable mental model of when to trust
the agent if the failure pattern changes run to run.

---

## HAI finding

The interface between human language and database structure
is not a solved problem, even with a well-designed schema.
Small local models understand the intent of a question but
cannot reliably translate that intent into correct SQL. The
failure mode is subtle; the agent looks confident, generates
a query, returns results, and the user has no signal that
the question was misunderstood.

This is the deeper point of BRK224: PepsiCo did not just
modernise their database; they built a validation and
routing layer around it. The data architecture exists to
give the agent reliable context, but the interaction design
exists to give the human reliable signal. Both matter;
most teams only think about the first.

---

## Stack

- SQLite (local structured database)
- ChromaDB (local vector search)
- Ollama phi3:mini (SQL generation)
- Ollama nomic-embed-text (embeddings)
- Python

---

## Relation to broader study

This project is part of a larger observational study of
Microsoft Build 2026 sessions through a human-AI interaction
lens. 