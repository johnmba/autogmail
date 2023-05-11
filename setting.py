
import sqlite3


class Dbset:
    
    def __init__(self) -> None:
        self._con = sqlite3.connect("datahouse.db")
        #self._con.row_factory = sqlite3.Row
        self._cur = self._con.cursor()

    def connect(self):
        """
        Create all required tables for the application
        """

        self._cur.execute( """ CREATE TABLE IF NOT EXISTS emails(
                id INTEGER PRIMARY KEY, fullname TEXT, username TEXT,
                address TEXT UNIQUE, password TEXT, active TEXT, registered TEXT, dated timestamp
        )""")

        self._con.commit()
        self._con.close()
        
sett = Dbset()
sett.connect()
        