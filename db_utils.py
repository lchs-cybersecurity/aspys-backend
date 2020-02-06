from datetime import datetime
import sqlite3

class ReportDatabase:
    db_filename = ""

    def __init__(self, filename: str):
        self.db_filename = filename

    def create(self):
        """
        Create report database
        """
        dbconn = sqlite3.connect(self.db_filename)
        c = dbconn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS reports(timestamp TEXT, fromAddress TEXT, content TEXT)')

        c.close()
        dbconn.close()

    def new_entry(self, from_addr: str, content: str):
        """
        Insert item
        """
        dbconn = sqlite3.connect(self.db_filename)
        c = dbconn.cursor()

        c.execute('INSERT INTO reports (timestamp, fromAddress, content) VALUES (?, ?, ?)',
                (datetime.now().strftime("%H:%M:%S"), from_addr, content))

        dbconn.commit()
        c.close()
        dbconn.close()
