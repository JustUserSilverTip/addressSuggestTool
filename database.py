import sqlite3

class Database:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    base_url TEXT DEFAULT 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address',
                    key TEXT UNIQUE,
                    value TEXT,
                    language TEXT 
                )
            """)

    def get_setting(self, key, default=None):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM settings WHERE key=?", (key,))
            value = cursor.fetchone()
            return value[0] if value else default

    def set_setting(self, key, value):
        with self.conn:
            self.conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))