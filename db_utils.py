from string import ascii_letters
from random import choice as random_choose
from datetime import datetime
import sqlite3

class ReportDatabase:
    db_filename = ""

    def __init__(self, filename: str):
        self.db_filename = filename

    def create_db(self):
        """
        Create report database
        """
        dbconn = sqlite3.connect(self.db_filename)
        c = dbconn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS reports(id TEXT, timestamp TEXT, fromAddress TEXT, content TEXT)')

        c.close()
        dbconn.close()

    def new_entry(self, from_addr: str, content: str):
        """
        Insert item
        """

        dbconn = sqlite3.connect(self.db_filename)
        c = dbconn.cursor()

        # Generate Report Identifier
        c.execute("SELECT * FROM reports")
        taken = [item[0] for item in c.fetchall()]
        id = ""
        while True:
            id = ""
            for i in range(10):
                id += random_choose(ascii_letters)
            if id not in taken:
                break

        # Insert item
        c.execute('INSERT INTO reports (id, timestamp, fromAddress, content) VALUES (?, ?, ?, ?)',
                (id, datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), from_addr, content))

        dbconn.commit()
        c.close()
        dbconn.close()

    def items(self):
        """
        Return database items as a list of string-tuples `(<identifier>, <timestamp>, <sender>, <content>)`
        """
        dbconn = sqlite3.connect(self.db_filename)
        c = dbconn.cursor()

        c.execute("SELECT * FROM reports")
        reports = c.fetchall()

        c.close()
        dbconn.close()

        return reports

    # TODO: Delete by report ID
    def delete(self, id: str):
        dbconn = sqlite3.connect(self.db_filename)
        c = dbconn.cursor()

        c.execute("DELETE FROM reports WHERE id = \'{}\'".format(id))

        dbconn.commit()
        c.close()
        dbconn.close()

    def clear(self):
        dbconn = sqlite3.connect(self.db_filename)
        c = dbconn.cursor()
        
        c.execute("DELETE FROM reports")

        dbconn.commit()
        c.close()
        dbconn.close()
