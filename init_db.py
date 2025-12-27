import sqlite3
import pandas as pd
import os

def create_database():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect("data/indian_banks.db")
    cursor = conn.cursor()

    print("Creating tables...")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS branches (
        ifsc TEXT PRIMARY KEY,
        branch TEXT,
        address TEXT,
        city TEXT,
        district TEXT,
        state TEXT,
        bank_id INTEGER,
        FOREIGN KEY (bank_id) REFERENCES banks (id)
    );
    """)

    print("Reading CSV data...")

    try:
        df = pd.read_csv("data/bank_branches.csv")
    except FileNotFoundError:
        print("Error: bank_branches.csv not found!")
        return

    print("Processing data...")
    
    unique_banks = df['bank_name'].unique()
    bank_data = [(bank,) for bank in unique_banks]
    cursor.executemany("INSERT OR IGNORE INTO banks (name) VALUES (?)", bank_data)
 
    cursor.execute("SELECT name, id FROM banks")
    bank_map = dict(cursor.fetchall())

    branches_to_insert = []
    for _, row in df.iterrows():
        bank_id = bank_map.get(row['bank_name'])
        branches_to_insert.append((
            row['ifsc'],
            row['branch'],
            row['address'],
            row['city'],
            row['district'],
            row['state'],
            bank_id
        ))

    print(f"Inserting {len(branches_to_insert)} branches...")
    cursor.executemany("""
        INSERT OR IGNORE INTO branches (ifsc, branch, address, city, district, state, bank_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, branches_to_insert)

    conn.commit()
    conn.close()
    print("Success! Database 'data/indian_banks.db' created.")

if __name__ == "__main__":
    create_database()