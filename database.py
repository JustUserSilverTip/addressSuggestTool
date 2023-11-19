import sqlite3

class Database:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.insert_defaults()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    key TEXT UNIQUE,
                    value TEXT
                )
            """)
    
    def insert_defaults(self):
        self.set_setting_if_not_exist("language", "ru")
        self.set_setting_if_not_exist("base_url", "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address")
        self.set_setting_if_not_exist("api_key", "")

    # def get_all(self) -> list:
    #     with self.conn:
    #         c = self.conn.execute("select * from settings")
    #         return c.fetchall()

    def get_setting(self, key, default=None):
        with self.conn:
            cursor = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,))
            value = cursor.fetchone()
            return value[0] if value else default
    
    def set_setting_if_not_exist(self, key, value):
        if not self.get_setting(key): self.set_setting(key, value)

    def set_setting(self, key, value):
        with self.conn:
            self.conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
