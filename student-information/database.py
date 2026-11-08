"""Shared in-memory data used by every module of the Student Information System."""

# username -> {password, role, student_id (students only)}
users_db = {
    "admin": {"password": "admin123", "role": "admin"},
    "student1": {"password": "pass123", "role": "student", "student_id": "2025-02642"},
}

student_records = [
    {"id": "2025-02642", "name": "WILSON D. MACARAEG", "age": "21", "course": "BSIT",
     "year": "SECOND YEAR", "email": "wilsonmacaraeg2023@gmail.com"},
    {"id": "2026-12345", "name": "RENE BATERBONIA", "age": "18", "course": "basketball",
     "year": "FIRST YEAR", "email": "RENETURN@GMAIL.COM"},
]


def find_student(student_id):
    """Return the record with the given ID, or None."""
    for record in student_records:
        if record["id"] == student_id:
            return record
    return None


import sqlite3

def connect_db():
    conn = sqlite3.connect("clearance.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = connect_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student'
        )
    """)

    conn.commit()
    conn.close()
