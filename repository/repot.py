import os
import datetime
import sqlite3

from pathlib import Path

CURRENT_DIR = Path(__file__).absolute().parent.parent
DEFAULT_DATA_FILE = CURRENT_DIR / "data" / "database.db"



def _ensure_parent_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


class Repot:
    def __init__(self, path=None):
        if path is None:
            self.path = DEFAULT_DATA_FILE
        else:
            self.path = Path(path)

        _ensure_parent_dir(str(self.path))
        self.conn = sqlite3.connect(str(self.path))


    def __createDatabase__(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS objet_detecter (
            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            confident FLOAT NOT NULL,
            date TEXT NOT NULL
                          )
        """)


    def save(self, data):
        nom = data.get("nom")
        confident = data.get("confident")
        date = data.get("date")
        self.__createDatabase__()
        try:
            cursor = self.conn.cursor()


            cursor.execute(""" INSERT INTO objet_detecter (nom, confident, date) VALUES (?, ?, ?)""", (nom, confident, date))
            self.conn.commit()
        except Exception as e:
            return str(e)
        if cursor.lastrowid != 0:
            return True
        return False


    def get_objet_detecter(self):
        db = self.conn
        data =  db.execute('SELECT * FROM objet_detecter').fetchall()
        return data

    def get_last_now(self):
        db = self.conn.cursor()
        data = db.execute('SELECT nom, date FROM objet_detecter ORDER BY id DESC LIMIT 1').fetchone()
        if data is None:
            return None, None
        return data




if __name__ == '__main__':

    re = Repot()


    data = {
        "nom": "alaa",
        "confident": 3.8,
        "date": str(datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S"))
    }
    re.save(data)
    no, now = re.get_last_now()
    print(now)




