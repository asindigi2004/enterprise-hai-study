import sqlite3
import json

DB_PATH = "data/business.db"

complaints = [
    {"id": 1, "customer": "Raj Mehta", "product": "Pepsi 500ml", "issue": "bottle was leaking when I opened it", "region": "North", "resolved": False},
    {"id": 2, "customer": "Priya Sharma", "product": "Lay's Classic", "issue": "packet was more than half empty", "region": "South", "resolved": True},
    {"id": 3, "customer": "Amit Verma", "product": "Pepsi 2L", "issue": "drink tasted flat and had no fizz", "region": "West", "resolved": False},
    {"id": 4, "customer": "Sunita Rao", "product": "Kurkure Masala", "issue": "found a foreign object inside the packet", "region": "South", "resolved": False},
    {"id": 5, "customer": "Vikram Singh", "product": "Pepsi 500ml", "issue": "expiry date was already passed when purchased", "region": "North", "resolved": True},
    {"id": 6, "customer": "Neha Gupta", "product": "7UP 500ml", "issue": "no carbonation at all, tasted like plain water", "region": "East", "resolved": False},
    {"id": 7, "customer": "Ravi Kumar", "product": "Lay's Magic Masala", "issue": "packaging was torn and chips were stale", "region": "West", "resolved": True},
    {"id": 8, "customer": "Anjali Desai", "product": "Pepsi 2L", "issue": "bottle cap was cracked and drink had spilled", "region": "East", "resolved": False},
    {"id": 9, "customer": "Kiran Patel", "product": "Kurkure Chilli", "issue": "much less quantity than what is shown on packet", "region": "North", "resolved": False},
    {"id": 10, "customer": "Meena Nair", "product": "7UP 2L", "issue": "strange smell coming from the drink", "region": "South", "resolved": False},
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS complaints")
    c.execute("""
        CREATE TABLE complaints (
            id INTEGER PRIMARY KEY,
            customer TEXT,
            product TEXT,
            issue TEXT,
            region TEXT,
            resolved INTEGER
        )
    """)
    for row in complaints:
        c.execute(
            "INSERT INTO complaints VALUES (?,?,?,?,?,?)",
            (row["id"], row["customer"], row["product"],
             row["issue"], row["region"], int(row["resolved"]))
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(complaints)} complaints into {DB_PATH}")

if __name__ == "__main__":
    seed()