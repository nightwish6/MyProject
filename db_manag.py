import sqlite3
"""Класс DBmanager, создан для хранения, обработки и работы с запросами от ЦБ РФ."""
class DBmanager(object):
    def __init__(self, way_db, name_db):
        self.conn=sqlite3.connect(way_db %(name_db))
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
    def create_table_dynamic_rate(self):
        self.dbcursor.execute('CREATE TABLE dynamic_rate (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                              'code txt NOT NULL,'
                              'date txt NOT NULL, '
                              'value int NOT NULL,'
                              'nominal int NOT NULL)')

    def insert_into_table_dynamic_rate(self, data):
        values=list()
        for item in sorted(list(data.keys())):
            if item=='ValCurs': continue
            else: values.append((data['ValCurs']['ID'], item, data[item]['Value'], data[item]['Nominal']))
        self.dbcursor.executemany('INSERT INTO dynamic_rate (code, date, value, nominal)'
                                  ' VALUES(?,?,?,?)', values)
        self.conn.commit()








if __name__=='__main__':
    import yaml
    settings=yaml.load(open('settings.yaml'))
    a=DBmanager(settings['way'],'valute')
    from cb_requests import req_curr_rate, req_dynamic_rate
    #b=req_curr_rate('03/10/2013')
    c = req_dynamic_rate('01/10/2016', '10/10/2016', 'R01235')
    from pprint import pprint
    #a.create_table()
    #a.insert_into(b)
    #pprint(a.select_all_values())
    #pprint(a.select_date_char_value('11/05/2017','CAD'))
    #pprint(a.select_all_date_value('03/10/2013'))
    #a.del_all_date_value('03/10/2013')
    #a.create_table_dynamic_rate()
    #pprint(c)
    #a.insert_into_table_dynamic_rate(c)



























