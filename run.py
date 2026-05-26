import hashlib
import json
import random
import sqlite3
from datetime import datetime

# =========================
# DATABASE SETUP
# =========================

conn = sqlite3.connect("provenance.db")
cursor = conn.cursor()

# Documents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    doc_id TEXT PRIMARY KEY,
    content TEXT,
    source TEXT,
    created_at TEXT
)
""")

# Influence table
cursor.execute("""
CREATE TABLE IF NOT EXISTS influence_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id TEXT,
    influence REAL
)
""")

conn.commit()

# =========================
# CREATE DOCUMENT ID
# =========================

def create_document_id(content, source):

    raw_data = (
        content +
        source +
        str(datetime.utcnow())
    )

    return hashlib.sha256(
        raw_data.encode()
    ).hexdigest()

# =========================
# STORE DOCUMENT
# =========================

def save_document(content, source):

    doc_id = create_document_id(
        content,
        source
    )

    created_at = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT INTO documents (
        doc_id,
        content,
        source,
        created_at
    )
    VALUES (?, ?, ?, ?)
    """, (
        doc_id,
        content,
        source,
        created_at
    ))

    conn.commit()

    print("\nDOCUMENT STORED")
    print("-------------------")
    print("Doc ID:", doc_id)

# =========================
# TRAIN AI
# =========================

def train_ai():

    cursor.execute("""
    SELECT doc_id, content
    FROM documents
    """)

    documents = cursor.fetchall()

    ai_weight = 0

    print("\nAI TRAINING")
    print("-------------------")

    for doc in documents:

        doc_id = doc[0]
        content = doc[1]

        influence = random.uniform(0.1, 1.0)

        ai_weight += influence

        cursor.execute("""
        INSERT INTO influence_log (
            doc_id,
            influence
        )
        VALUES (?, ?)
        """, (
            doc_id,
            influence
        ))

        conn.commit()

        print("\nLearned:", content)
        print("Influence:",
              round(influence, 3))

    print("\nFINAL AI WEIGHT:",
          round(ai_weight, 3))

# =========================
# SHOW INFLUENCE
# =========================

def show_influence():

    cursor.execute("""
    SELECT doc_id, influence
    FROM influence_log
    ORDER BY influence DESC
    """)

    rows = cursor.fetchall()

    print("\nINFLUENCE REPORT")
    print("-------------------")

    for row in rows:

        print("Doc ID:", row[0])
        print("Influence:",
              round(row[1], 3))
        print()

# =========================
# UNLEARN DOCUMENT
# =========================

def unlearn_document():

    doc_id = input(
        "\nEnter Document ID to remove: "
    )

    cursor.execute("""
    DELETE FROM influence_log
    WHERE doc_id = ?
    """, (doc_id,))

    conn.commit()

    print("\nDOCUMENT REMOVED")

# =========================
# MENU SYSTEM
# =========================

while True:

    print("\nAI PROVENANCE SYSTEM")
    print("-----------------------")
    print("1. Store Document")
    print("2. Train AI")
    print("3. Show Influence")
    print("4. Unlearn Document")
    print("5. Exit")

    choice = input("\nChoose option: ")

    # Store document
    if choice == "1":

        content = input(
            "\nEnter document content: "
        )

        source = input(
            "Enter document source: "
        )

        save_document(content, source)

    # Train AI
    elif choice == "2":

        train_ai()

    # Show influence
    elif choice == "3":

        show_influence()

    # Unlearn
    elif choice == "4":

        unlearn_document()

    # Exit
    elif choice == "5":

        print("\nSYSTEM CLOSED")
        break

    else:

        print("\nInvalid option")