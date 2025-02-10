import datetime
import sqlite3

class ECFRDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def init_db(self):
        conn = sqlite3.connect(self.db_path)

        conn.execute("""CREATE TABLE IF NOT EXISTS titles (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            latest_issue_date TEXT,
            last_refresh_date TEXT)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS agencies (
                id TEXT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                short_name TEXT,
                parent_id TEXT,
                FOREIGN KEY (parent_id) REFERENCES agencies(id))""")

        conn.execute("CREATE INDEX IF NOT EXISTS idx_agencies_name ON agencies(name)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_agencies_short_name ON agencies(short_name)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_agencies_parent_id ON agencies(parent_id)")

        return conn

    def insert_agency(self, agency, parent_id):
        conn = self.init_db()
        conn.execute("""INSERT INTO agencies (id, name, short_name, parent_id) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT (id) DO UPDATE SET name = excluded.name, short_name = excluded.short_name, parent_id = excluded.parent_id""", 
            (agency['slug'], agency['name'], agency['short_name'], parent_id))
        conn.commit()
        return agency['slug']

    def insert_title(self, title):
        conn = self.init_db()
        conn.execute("""INSERT INTO titles (id, name, latest_issue_date, last_refresh_date) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT (id) DO UPDATE SET name = excluded.name, latest_issue_date = excluded.latest_issue_date, last_refresh_date = excluded.last_refresh_date""", 
            (title['number'], title['name'], title['latest_issue_date'], datetime.date.today().strftime('%Y-%m-%d')))
        conn.commit()
        return title['number']
