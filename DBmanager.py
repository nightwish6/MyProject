import sqlite3

class DBmanager(object):
    def __init__(self, name_db):
        self.conn=sqlite3.connect(name_db)
        self.dbcursor=self.conn.cursor()
        self.dbcursor.execute('CREATE TABLE words (id int NOT NULL, word txt NOT NULL, PRIMARY KEY(id))')
    def insert_into(self, *values):
        list_val=list(values)
        self.dbcursor.executemany('INSERT INTO words VALUES(?,?)',list_val)
        self.conn.commit()
    def select_all_values(self):
        self.dbcursor.execute('SELECT * FROM words')
        return self.dbcursor.fetchall()
    def select_last_value(self):
        self.dbcursor.execute('SELECT word FROM words WHERE id=(SELECT MAX(id) FROM words)')
        return self.dbcursor.fetchone()
    def del_all_values(self):
        self.dbcursor.execute('DELETE FROM words')
        self.conn.commit()
    def del_last_value(self):
        self.dbcursor.execute('DELETE FROM words WHERE id=(SELECT MAX(id) FROM words)')
        self.conn.commit()

















