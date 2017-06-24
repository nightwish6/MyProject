import sqlite3

class DBmanager(object):
    def __init__(self, name_db):
        self.conn=sqlite3.connect('/home/admin1/GitProject/%s.sqlite'%(name_db))
        self.dbcursor=self.conn.cursor()
    def create_table(self):
        self.dbcursor.execute('CREATE TABLE valute (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                              'date txt NOT NULL,'
                              'charcode txt NOT NULL, '
                              'name txt NOT NULL,'
                              'nominal int NOT NULL,'
                              'numcode int NOT NULL,'
                              'value int NOT NULL)')
    def insert_into(self, data):
        values = list()
        for item in list(data.values()):
            if len(item.keys()) > 2:
                values.append((data['ValCurs']['Date'], item['CharCode'], item['Name'], item['Nominal'],
                               item['NumCode'], item['Value']))
        self.dbcursor.executemany('INSERT INTO valute(date, charcode, name, nominal, numcode, value)'
                                  ' VALUES(?,?,?,?,?,?)',values)
        self.conn.commit()
    def select_all_values(self):
        self.dbcursor.execute('SELECT * FROM valute')
        return self.dbcursor.fetchall()
    def select_date_char_value(self, date, charcode):
        date=date.replace('/','.')
        self.dbcursor.execute('SELECT * FROM valute WHERE date=? and charcode=?', (date, charcode))
        return self.dbcursor.fetchone()
    def select_all_date_value(self, date):
        date=date.replace('/','.')
        self.dbcursor.execute('SELECT * FROM valute WHERE date=?',(date,))
        return self.dbcursor.fetchall()
    def del_all_date_value(self, date):
        date=date.replace('/','.')
        self.dbcursor.execute('DELETE FROM valute WHERE date=?', (date,))
        self.conn.commit()


if __name__=='__main__':
    a=DBmanager('valute')
    from cb_requests import req_curr_rate
    b=req_curr_rate('03/10/2013')
    from pprint import pprint
    #a.create_table()
    #a.insert_into(b)
    pprint(a.select_all_values())
    #pprint(a.select_date_char_value('11/05/2017','CAD'))
    #pprint(a.select_all_date_value('03/10/2013'))
    #a.del_all_date_value('03/10/2013')

























