import datetime
import math
import sqlite3


class ECFRDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)

        conn.execute(
            """CREATE TABLE IF NOT EXISTS titles (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            latest_issue_date TEXT,
            last_refresh_date TEXT)"""
        )

        conn.execute(
            """CREATE TABLE IF NOT EXISTS agencies (
                id TEXT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                short_name TEXT,
                parent_id TEXT,
                burden_score REAL,
                burden_category TEXT,
                total_word_count INTEGER,
                FOREIGN KEY (parent_id) REFERENCES agencies(id))"""
        )

        conn.execute("CREATE INDEX IF NOT EXISTS idx_agencies_name ON agencies(name)")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_agencies_short_name ON agencies(short_name)"
        )
        # SQLite foreign keys are not indexed by default
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_agencies_parent_id ON agencies(parent_id)"
        )

        conn.execute(
            """CREATE TABLE IF NOT EXISTS code_references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency_id TEXT NOT NULL,
            title_id INTEGER NOT NULL,
            subtitle TEXT,
            chapter TEXT,
            subchapter TEXT,
            part TEXT,
            subpart TEXT,
            section TEXT,
            processed INTEGER DEFAULT 0,
            reference_text TEXT,
            name TEXT,
            link TEXT,
            burden_score REAL,
            word_count INTEGER,
            burden_category TEXT,
            FOREIGN KEY (agency_id) REFERENCES agencies(id),
            FOREIGN KEY (title_id) REFERENCES titles(id))"""
        )

        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_code_references_agency_id ON code_references(agency_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_code_references_title_id ON code_references(title_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_codee_references_processed ON code_references(processed)"
        )

        conn.row_factory = sqlite3.Row

        return conn

    def insert_agency(self, agency, parent_id):
        self.conn.execute(
            """INSERT INTO agencies (id, name, short_name, parent_id) 
            VALUES (?, ?, ?, ?) 
            ON CONFLICT (id) DO UPDATE 
                SET name = excluded.name, short_name = excluded.short_name, parent_id = excluded.parent_id""",
            (agency["slug"], agency["name"], agency["short_name"], parent_id),
        )

    def insert_title(self, title):
        self.conn.execute(
            """INSERT INTO titles (id, name, latest_issue_date, last_refresh_date) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT (id) DO UPDATE 
                SET name = excluded.name, latest_issue_date = excluded.latest_issue_date, last_refresh_date = excluded.last_refresh_date""",
            (
                title["number"],
                title["name"],
                title["latest_issue_date"],
                datetime.date.today().strftime("%Y-%m-%d"),
            ),
        )

    def clear_code_references(self, agency_id):
        self.conn.execute(
            "DELETE FROM code_references WHERE agency_id = ?", (agency_id,)
        )

    def insert_code_reference(
        self, agency_id, title_id, subtitle, chapter, subchapter, part, subpart, section
    ):
        self.conn.execute(
            """INSERT INTO code_references (agency_id, title_id, subtitle, chapter, subchapter, part, subpart, section) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                agency_id,
                title_id,
                subtitle,
                chapter,
                subchapter,
                part,
                subpart,
                section,
            ),
        )

    def data_load_in_progress(self):
        return (
            self.conn.execute(
                "SELECT COUNT(*) FROM code_references WHERE processed = 0"
            ).fetchone()[0]
            > 0
        )

    def get_code_references_for_processing(self):
        return self.conn.execute(
            """SELECT cr.id, title_id, cr.subtitle, cr.chapter, cr.subchapter, cr.part, cr.subpart, cr.section, t.latest_issue_date 
            FROM code_references cr 
            JOIN titles t ON cr.title_id = t.id 
            WHERE processed = 0"""
        ).fetchall()

    def get_code_references_for_burden_score(self):
        return self.conn.execute(
            """SELECT cr.id, title_id, cr.subtitle, cr.chapter, cr.subchapter, cr.part, cr.subpart, cr.section, t.latest_issue_date 
            FROM code_references cr 
            JOIN titles t ON cr.title_id = t.id 
            WHERE processed = 1 AND word_count > 200000 AND word_count < 240000"""
        ).fetchall()

    def set_code_reference_metrics(
        self, id, reference_text, name, link, burden_score, word_count
    ):
        self.conn.execute(
            "UPDATE code_references SET processed = 1, reference_text = ?, name = ?, link = ?, burden_score = ?, word_count = ? WHERE id = ?",
            (reference_text, name, link, burden_score, word_count, id),
        )

    def set_code_reference_processing_failed(self, id):
        self.conn.execute(
            "UPDATE code_references SET processed = -1 WHERE id = ?",
            (id,),
        )

    def calculate_burden_categories(self):
        # Get statistical measures of the burden scores
        stats = self.conn.execute(
            """SELECT AVG(burden_score) AS mean, AVG((cr.burden_score - sub.a) * (cr.burden_score - sub.a)) AS var FROM code_references cr, (SELECT avg(burden_score) AS a FROM code_references) AS sub WHERE processed = 1"""
        ).fetchone()

        mean = stats[0]
        variance = stats[1]
        std_dev = math.sqrt(variance)
        print(f"{mean} {std_dev}")

        # Calculate the burden category for each code reference
        self.conn.execute(
            """UPDATE code_references
            SET burden_category = 
                CASE 
                    WHEN burden_score > (? + ?) THEN 'HIGH'
                    WHEN burden_score < (? - ?) THEN 'LOW'
                    ELSE 'MEDIUM'
                END
            WHERE processed = 1""",
            (mean, std_dev, mean, std_dev),
        )
    
    def calculate_agency_burden(self):
        # Calculate the compliance burden for each agency.
        self.conn.execute("""
                          UPDATE agencies
                          SET
                            burden_score = subq.weighted_burden,
                            total_word_count = subq.total_word_count
                          FROM (
                              SELECT 
                                    agency_id, 
                                    SUM(burden_score * word_count) / SUM(word_count) AS weighted_burden,
                                    SUM(word_count) AS total_word_count
                              FROM code_references
                              WHERE processed = 1
                              GROUP BY agency_id
                          ) AS subq
                          WHERE agencies.id = subq.agency_id
                          """)
        
        # Get stats for the weighted burden scores
        stats = self.conn.execute(
            """SELECT AVG(burden_score) AS mean, AVG((ag.burden_score - sub.a) * (ag.burden_score - sub.a)) AS var FROM agencies ag, (SELECT avg(burden_score) AS a FROM agencies) AS sub WHERE ag.burden_score IS NOT NULL"""
        ).fetchone()

        mean = stats[0]
        variance = stats[1]
        std_dev = math.sqrt(variance)

        # Calculate the burden category for each agency
        self.conn.execute(
            """UPDATE agencies
            SET burden_category = 
                CASE 
                    WHEN burden_score > (? + ?) THEN 'HIGH'
                    WHEN burden_score < (? - ?) THEN 'LOW'
                    ELSE 'MEDIUM'
                END
            WHERE burden_score IS NOT NULL""",
            (mean, std_dev, mean, std_dev),
        )

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
