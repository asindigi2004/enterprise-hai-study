# Enterprise HAI Case Study
## How PepsiCo's Agentic AI Blueprint Holds Up Under Local Testing

**Context:** Microsoft Build 2026, BRK224
**Author:** Archita Sindigi
**Method:** Local replication of Data Analyst Agent architecture, 4 test questions across SQL and semantic query paths

---

## The Claim

PepsiCo and Microsoft argued at Build 2026 that the primary bottleneck for enterprise AI agents is not model capability; it is data context. Agents fail not because they are unintelligent, but because they start every session from zero, with no reliable understanding of where data lives, what schema looks like, or what rules apply.

The proposed solution was architectural: modernise the data layer first, then build agents on top of it.

I wanted to test whether that claim held up at a small scale, using only local, free tools.

---

## Method

Built a Data Analyst Agent over a SQLite database of 10 customer complaints, with two query paths: SQL generation via phi3:mini and semantic search via ChromaDB with nomic-embed-text embeddings. Asked 4 questions designed to stress different capabilities.

---

## Trust-Control Analysis

The most useful framework for interpreting results was not accuracy alone, but the relationship between trust and control across query types.

High trust, high control: SQL on exact filters. The query was readable, the result was correct, and the user could verify both. This is where enterprise AI should live.

High trust, low control: Semantic search. Results were correct but the retrieval process was opaque. Users had to trust the output without being able to inspect why those documents were returned.

Low trust, high control: SQL on aggregation questions. The query was readable but results were inconsistent across runs. Users could see what was queried but could not rely on it.

Low trust, low control: SQL on conceptual questions. The agent generated plausible-looking queries that returned wrong results, with no signal to the user that anything had gone wrong. This is the danger zone.

---

## Key Finding

PepsiCo's architectural claim was correct; the data layer matters enormously. But the testing revealed a second problem the session did not address: inconsistent failure modes.

Question 2 returned empty results in one run, then hallucinated an entirely different database schema in the next. Same question, different failure, no user-facing signal either time.

Consistent failure is a data architecture problem; you fix the schema, improve the prompt, retrain. Inconsistent failure is a human-AI interaction design problem; users cannot build a reliable mental model of when to trust the agent if the failure pattern changes unpredictably.

PepsiCo solved the first problem. The second remains open.

---

## Implication for HAI Design

Enterprise AI tools need two layers, not one:

- A data layer that gives agents reliable context
- An interaction layer that gives humans reliable signal

Most enterprise AI deployments, including the one described in BRK224, focus heavily on the first and lightly on the second. The result is agents that work well in demos and fail subtly in production; not because the data was wrong, but because users had no mechanism to detect when the agent's confidence was unjustified.

Designing that interaction layer; the signals, the uncertainty indicators, the graceful degradation patterns; is the open HAI problem this study points toward.

---

*Based on local replication of BRK224 architecture. All findings from personal experimentation, June 2026.*