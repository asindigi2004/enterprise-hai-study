import sqlite3
import chromadb
import requests

DB_PATH = "data/business.db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

# --- setup chromadb ---
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("complaints")


def get_embedding(text):
    """Get embedding from Ollama for semantic search."""
    resp = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    return resp.json()["embedding"]


def seed_vectors():
    """Load complaints from SQLite and embed them into ChromaDB."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, issue, product, region FROM complaints"
    ).fetchall()
    conn.close()

    ids = [str(r[0]) for r in rows]
    docs = [r[1] for r in rows]
    metas = [{"product": r[2], "region": r[3]} for r in rows]

    if collection.count() == 0:
        embeddings = [get_embedding(d) for d in docs]
        collection.add(
            ids=ids,
            documents=docs,
            embeddings=embeddings,
            metadatas=metas
        )
        print(f"Embedded {len(docs)} complaints into ChromaDB")


def sql_query(question):
    """Ask Ollama to write SQL, run it, return results."""
    prompt = f"""Table: complaints
Columns: id, customer, product, issue, region, resolved
resolved is 0 (unresolved) or 1 (resolved).
regions are: North, South, East, West.

Write ONE simple SQL SELECT query only. No explanation. No markdown. No joins.
Question: {question}
SQL:"""

    resp = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    sql = resp.json()["response"].strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    sql = sql.split(";")[0].strip() + ";"
    print(f"\n[SQL generated]: {sql}")

    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(sql).fetchall()
        conn.close()
        return rows
    except Exception as e:
        return f"SQL error: {e}"


def semantic_query(question):
    """Embed the question, find similar complaints in ChromaDB."""
    embedding = get_embedding(question)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )
    return results["documents"][0]


def ask(question, mode="both"):
    print(f"\n{'='*50}")
    print(f"Question: {question}")
    print(f"{'='*50}")

    if mode in ("sql", "both"):
        print("\n--- SQL RESULT ---")
        results = sql_query(question)
        if isinstance(results, list):
            for r in results:
                print(r)
        else:
            print(results)

    if mode in ("semantic", "both"):
        print("\n--- SEMANTIC RESULT ---")
        results = semantic_query(question)
        for r in results:
            print(f"  - {r}")


if __name__ == "__main__":
    print("Seeding vectors...")
    seed_vectors()

    # Question 1 - exact filter, SQL should win
    ask("show me all unresolved complaints from North region")

    # Question 2 - semantic intent, semantic search should win
    ask("find complaints about drinks that lost their fizz")

    # Question 3 - ambiguous, see what each does
    ask("what packaging problems have customers reported")