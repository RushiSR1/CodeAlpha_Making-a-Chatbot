import sqlite3
from typing import List

class DatabaseManager:
    def __init__(self, db_path="data_store.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                data_hash TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_entry(self, content: str, data_hash: str) -> bool:
        """
        Adds a new entry if hash is unique.
        Returns True if added, False if duplicate (constraint violation).
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO entries (content, data_hash) VALUES (?, ?)", (content, data_hash))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def entry_exists(self, data_hash: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM entries WHERE data_hash = ?", (data_hash,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def get_all_entries(self) -> List[tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries")
        rows = cursor.fetchall()
        conn.close()
        return rows
