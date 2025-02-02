# syntaxmatrix/db.py
import sqlite3
import os

# Define the path for the SQLite database file.
DB_PATH = os.path.join(os.path.dirname(__file__), "syntaxmatrix.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database by creating the pages table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            name TEXT PRIMARY KEY,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_pages():
    """Return a dictionary mapping page names to their content."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, content FROM pages")
    rows = cursor.fetchall()
    conn.close()
    return {row["name"]: row["content"] for row in rows}

def add_page(name, content):
    """Add a new page to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pages (name, content) VALUES (?, ?)", (name, content))
    conn.commit()
    conn.close()

def update_page(old_name, new_name, content):
    """Update an existing page's name and content."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE pages SET name = ?, content = ? WHERE name = ?", (new_name, content, old_name))
    conn.commit()
    conn.close()

def delete_page(name):
    """Delete a page from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pages WHERE name = ?", (name,))
    conn.commit()
    conn.close()
