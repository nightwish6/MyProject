import sys
from matplotlib import pyplot as plt
from datetime import date, datetime
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from pprint import pprint
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, qApp, QAction, QTextEdit, QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QCalendarWidget
from PyQt5.QtWidgets import QMessageBox, QErrorMessage, QDateEdit, QScrollArea, QScrollBar, QAbstractScrollArea
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from PyQt5.QtCore import QCoreApplication, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.composition()

    def composition(self):
        self.setWindowTitle('Central Bank')
        self.setGeometry(10, 10, 500, 500)
        self.setWindowIcon(QIcon('/home/admin1/GitProject/images/cb.png'))
        self.center()
        self.toolbar()
        self.statusBar()
        self.show()

    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def toolbar(self):
        self.toolbar = self.addToolBar('ToolBar')
        exitAction = QAction(QIcon('/home/admin1/GitProject/images/cb.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit the program')
        exitAction.triggered.connect(self.close)
        reqValAction=QAction(QIcon('/home/admin1/GitProject/images/cb.png'),'Learn the exchange rate', self)
        reqValAction.triggered.connect(self.req_val_act)
        reqValAction.setStatusTip('Request currency rates')
        dynamicRateAction=QAction(QIcon('/home/admin1/GitProject/images/cb.png'),'Learn the course dynamics', self)
        dynamicRateAction.triggered.connect(self.req_val_dynamic)
        dynamicRateAction.setStatusTip('Schedule a change in the exchange rate for the period')
        newsAction=QAction(QIcon('/home/admin1/GitProject/images/cb.png'),'Get news', self)
        newsAction.setStatusTip('Get news from the Central bank')
        newsAction.triggered.connect(self.req_news)
        self.toolbar.addAction(reqValAction)
        self.toolbar.addAction(dynamicRateAction)
        self.toolbar.addAction(newsAction)
        self.toolbar.addAction(exitAction)
    def req_val_act(self):
        self.win_1=Windows_1()
    def req_val_dynamic(self):
        self.win_2=Windows_2()
    def req_news(self):
        from cb_requests import req_news
        from requests import ConnectionError
        try:
            req_News = req_news()
            self.win_4 = Windows_4(req_News)
        except ConnectionError:
            self.error_no_connect = QErrorMessage(self)
            self.error_no_connect.setWindowTitle('Сonnection Error')
            self.error_no_connect.showMessage('No internet connection')


class Windows_1(QWidget):
    def __init__(self):
        super().__init__()
        self.composition()

    def composition(self):
        self.setWindowTitle('Central Bank currency rates')
        self.setGeometry(10,10,350,150)
        self.setWindowIcon(QIcon('/home/admin1/GitProject/images/cb.png'))
        self.date_input()
        self.show()

    def date_input(self):
        self.lab1=QLabel('Date:',self)
        self.send_but=QPushButton('Send')
        self.cal_but=QPushButton('Calendar')
        self.save_but=QPushButton('Save data')
        self.exit_but=QPushButton('Exit')
        self.save_but.clicked.connect(self.save_date)
        self.send_but.clicked.connect(self.req_curr_rate)
        self.cal_but.clicked.connect(self.calendar)
        self.exit_but.clicked.connect(self.close)
        self.data=QDateEdit(self)
        self.data.setDisplayFormat('dd/MM/yyyy')
        self.combo_val=QComboBox(self)
        valutes=['AUD','AZN','GBP','AMD','BYN','BGN','BRL','HUF','HKD','DKK','USD','EUR','INR',
                 'KZT','CAD','KGS','CNY','MDL','NOK','PLN','RON','XDR','SGD','TJS','TRY','TMT',
                 'UZS','UAH','CZK','SEK','CHF','ZAR','KRW','JPY']
        for valute in sorted(valutes):
            self.combo_val.addItem(valute)
        self.combo_val.activated[str].connect(self.insert_combo_val)
        grid=QGridLayout()
        grid.setSpacing(1)
        grid.addWidget(self.lab1,1,0,1,1)
        grid.addWidget(self.data,1,1,1,1)
        grid.addWidget(self.cal_but, 1,2,1,1)
        grid.addWidget(self.send_but,1,3,1,1)
        grid.addWidget(self.combo_val, 3,0)
        options=('CharCode','Name','Nominal','NumCode','Value')
        count=4
        self.options=dict()

        for option in options:
            val_lab=QLabel(option)
            val_edit=QLineEdit(self)
            grid.addWidget(val_lab,count,0)
            grid.addWidget(val_edit,count,1,1,8)
            self.options[option]=val_edit
            count+=1

        grid.addWidget(self.save_but,12,7)
        grid.addWidget(self.exit_but,12,8)
        self.setLayout(grid)

    def req_curr_rate(self):
        from cb_requests import req_curr_rate
        from requests import ConnectionError
        if datetime(int(self.data.text()[6:]), int(self.data.text()[3:5]),
                   int(self.data.text()[0:2]),
                hour=0, minute=0, second=0, microsecond=0, tzinfo=None) > datetime.now():
            self.error_no_data = QErrorMessage(self)
            self.error_no_data.setWindowTitle('No data available')
            self.error_no_data.showMessage('You entered a date that is greater than the current date')
        else:
            try:
                self.request=req_curr_rate(self.data.text())
                for key in self.request:
                    if key=='ValCurs': continue
                    elif self.request[key]['CharCode']==self.combo_val.currentText():
                        for values in self.request.values():
                            for value in values:
                                if value=='Date' or value=='name':continue
                                else: self.options[value].setText(str(self.request[key][value]))
            except ConnectionError:
                self.error_no_connect = QErrorMessage(self)
                self.error_no_connect.setWindowTitle('Сonnection Error')
                self.error_no_connect.showMessage('No internet connection')



    def insert_combo_val(self, combo_val):
        try:
            for key in self.request:
                if key =='ValCurs': continue
                elif self.request[key]['CharCode']==combo_val:
                    for values in self.request.values():
                        for value in values:
                            if value=='Date' or value=='name':continue
                            else: self.options[value].setText(str(self.request[key][value]))
        except AttributeError:
            self.error_no_data = QErrorMessage(self)
            self.error_no_data.setWindowTitle('No data available')
            self.error_no_data.showMessage('You did not send the request')

    def calendar(self):
        self.cal=QCalendarWidget()
        self.cal.setGridVisible(True)
        self.cal.setGeometry(300,300,450,200)
        self.cal.setWindowIcon(QIcon('/home/admin1/GitProject/images/cb.png'))
        self.cal.setWindowTitle('Calendar')
        self.cal.show()
        self.cal.clicked[QDate].connect(self.show_date)

    def show_date(self):
        self.data.setDate(self.cal.selectedDate())

    def save_date(self):
        from db_manag import DBmanager
        from sqlite3 import OperationalError as sqlite3_OperationalError
        self.data_base=DBmanager('valute')

        try: self.data_base.insert_into(self.request)
        except sqlite3_OperationalError:
            self.data_base.create_table()
            self.data_base.insert_into(self.request)
            self.message_save_data = QMessageBox.information(self, 'Save Data', 'Data saved',
                                                             QMessageBox.Ok)
        except AttributeError:
            self.error_no_data=QErrorMessage(self)
            self.error_no_data.setWindowTitle('No data')
            self.error_no_data.showMessage('No data to save')
        else: self.message_save_data=QMessageBox.information(self, 'Save Data', 'Data saved',
                                           QMessageBox.Ok)


class Windows_2(QWidget):
    def __init__(self):
        super().__init__()
        self.composition()

    def composition(self):
        self.setWindowTitle('Central Bank dynamic rates')
        self.setGeometry(10,10,430,30)
        self.setWindowIcon(QIcon('/home/admin1/GitProject/images/cb.png'))
        self.period()
        self.show()

    def period(self):
        self.txt_per_1 = QDateEdit(self)
        self.txt_per_2 = QDateEdit(self)
        self.save_but = QPushButton('Save data')
        self.exit_but = QPushButton('Exit')
        self.txt_per_1.setDisplayFormat('dd/MM/yyyy')
        self.txt_per_2.setDisplayFormat('dd/MM/yyyy')
        self.lab_per = QLabel('Period of time:', self)
        self.lab_code = QLabel('Valute:', self)
        self.send_but = QPushButton('Send')
        self.send_but.clicked.connect(self.req_dynamic_rate)
        self.save_but.clicked.connect(self.save_dynamic)
        self.exit_but.clicked.connect(self.close)
        self.combo_val_code=QComboBox(self)
        self.val_code={'R01500':'Молдавский лей', 'R01235':'Доллар США','R01810':'Южноафриканский рэнд',
                       'R01710':'Туркменский манат','R01670':'Таджикский сомони','R01010':'Австралийский доллар',
                       'R01035':'Фунт стерлингов Соединенного королевства','R01060':'Армянский драм',
                       'R01100':'Болгарский лев','R01115':'Бразильский реал','R01135':'Венгерский форинт',
                       'R01215':'Датская крона','R01239':'Евро','R01270':'Индийская рупия','R01335':'Казахстанский тенге',
                       'R01350':'Канадский доллар','R01370':'Киргизский сом','R01375':'Китайский юань','R01535':'Норвежская крона','R01565':'Польский злотый',
                       'R01585':'Румынский лей','R01589':'СДР (специальные права заимствования)',
                       'R01625':'Сингапурский доллар','R01717':'Узбекский сум','R01720':'Украинская гривна',
                       'R01760':'Чешская крона','R01770':'Шведская крона','R01775':'Швейцарский франк',
                       'R01815':'Вон Республики Корея','R01820':'Японская иена'}
        for key in sorted(list(self.val_code.keys())):
            self.combo_val_code.addItem(self.val_code[key])
        grid = QGridLayout()
        grid.setSpacing(1)
        grid.addWidget(self.lab_per, 1, 0, 1, 1)
        grid.addWidget(self.txt_per_1, 1, 1, 1, 1)
        grid.addWidget(self.txt_per_2, 1, 2, 1, 1)
        grid.addWidget(self.lab_code, 2, 0, 1, 1)
        grid.addWidget(self.combo_val_code, 2, 1, 3, 3)
        grid.addWidget(self.send_but, 1, 3, 1, 1)
        grid.addWidget(self.save_but, 5, 2)
        grid.addWidget(self.exit_but, 5, 3)
        self.setLayout(grid)

    def req_dynamic_rate(self):
        if datetime(int(self.txt_per_1.text()[6:]), int(self.txt_per_1.text()[3:5]),
                   int(self.txt_per_1.text()[0:2]),
                hour=0, minute=0, second=0, microsecond=0, tzinfo=None) > datetime.now() or datetime(int(self.txt_per_2.text()[6:]), int(self.txt_per_2.text()[3:5]),
                     int(self.txt_per_2.text()[0:2]),
                     hour=0, minute=0, second=0, microsecond=0, tzinfo=None) > datetime.now():
            self.error_no_data = QErrorMessage(self)
            self.error_no_data.setWindowTitle('No data available')
            self.error_no_data.showMessage('You entered a date that is greater than the current date')
        elif datetime(int(self.txt_per_1.text()[6:]), int(self.txt_per_1.text()[3:5]),
                   int(self.txt_per_1.text()[0:2])) > datetime(int(self.txt_per_2.text()[6:]), int(self.txt_per_2.text()[3:5]),
                     int(self.txt_per_2.text()[0:2])):
            self.error_no_data = QErrorMessage(self)
            self.error_no_data.setWindowTitle('Error entering date')
            self.error_no_data.showMessage('You entered the first date period, which is greater than the second date you entered')
        else:
            from cb_requests import req_dynamic_rate
            from requests import ConnectionError
            for key in self.val_code.keys():
                if self.combo_val_code.currentText()==str(self.val_code[key]):
                    try:
                        self.dynamic_req=req_dynamic_rate(self.txt_per_1.text(),self.txt_per_2.text(),
                                                       str(key))
                        self.win_3=Windows_3(self.dynamic_req)
                    except ConnectionError:
                        self.error_no_connect = QErrorMessage(self)
                        self.error_no_connect.setWindowTitle('Сonnection Error')
                        self.error_no_connect.showMessage('No internet connection')


    def save_dynamic(self):
        from db_manag import DBmanager
        from sqlite3 import OperationalError as sqlite3_OperationalError
        self.data_base = DBmanager('valute')
        try: self.data_base.insert_into_table_dynamic_rate(self.dynamic_req)
        except sqlite3_OperationalError:
            self.data_base.create_table_dynamic_rate()
            self.data_base.insert_into_table_dynamic_rate(self.dynamic_req)
            self.message_save_data = QMessageBox.information(self, 'Save Data', 'Data saved',
                                                             QMessageBox.Ok)
        except AttributeError:
            self.error_no_data = QErrorMessage(self)
            self.error_no_data.setWindowTitle('No data')
            self.error_no_data.showMessage('No data to save')
        else: self.message_save_data = QMessageBox.information(self, 'Save Data', 'Data saved',
                                           QMessageBox.Ok)


class Windows_3(QWidget):
    def __init__(self, dynamic_data):
        super().__init__()
        self.dynamic_req = dynamic_data
        self.composition()

    def composition(self):
        self.setWindowTitle('Shedule')
        self.setGeometry(10,10,600,430)
        self.setWindowIcon(QIcon('/home/admin1/GitProject/images/cb.png'))
        self.course_schedule()
        grid=QGridLayout()
        grid.addWidget(self.canvas)
        self.setLayout(grid)
        self.show()

    def course_schedule(self):
        self.coordinates = dict()
        for key in self.dynamic_req.keys():
            if key == 'ValCurs':
                continue
            else:
                self.coordinates[key] = self.dynamic_req[key]['Value']

        self.xdates = [date(int(i[6:]), int(i[3:5]), int(i[0:2])) for i in list(self.coordinates.keys())]
        self.xdates.sort()
        self.yvalues = list()
        for dates in self.xdates:
            for key in self.coordinates:
                if dates.strftime('%d.%m.%Y') == str(key):
                    self.yvalues.append(float(self.coordinates[key].replace(',', '.')))
        self.figure = plt.figure()
        self.schedule = self.figure.gca()
        self.schedule.set_title('Course schedule')
        self.schedule.set_xlabel('Dates')
        self.schedule.set_ylabel('Values')
        self.schedule.xaxis.set_major_formatter(
            mdates.DateFormatter('%d/%m/%Y'))
        self.schedule.yaxis.set_major_formatter(
            mtick.FormatStrFormatter('%.2f'))
        self.schedule.plot(self.xdates, self.yvalues, 'r')
        self.figure.autofmt_xdate()
        self.canvas = FigureCanvas(self.figure)



class Windows_4(QWidget):
    def __init__(self, req_News):
        super().__init__()
        self.news = req_News
        self.composition()


    def composition(self):
        self.setWindowTitle('Central Bank News')
        self.setGeometry(10, 10, 270, 650)
        self.setWindowIcon(QIcon('/home/admin1/GitProject/images/cb.png'))
        self.news_input()
        self.show()

    def news_input(self):
        self.lab_all = QLabel('All news:', self)
        self.lab_by_date = QLabel('News by date:', self)
        self.txt_all = QLineEdit(self)
        self.exit_but = QPushButton('Exit')
        self.find_but=QPushButton('Find')
        self.cal_but=QPushButton('Calendar')
        self.cal_but.clicked.connect(self.calendar)
        self.find_but.clicked.connect(self.find_news)
        self.date = QDateEdit(self)
        self.date.setDisplayFormat('dd/MM/yyyy')
        self.scroll_area=QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(2)
        self.scroll_area.setHorizontalScrollBarPolicy(2)
        grid = QGridLayout()
        grid.setSpacing(1)
        grid.addWidget(self.lab_all, 1, 0, 1, 1)
        grid.addWidget(self.txt_all, 1, 1, 1, 1)
        grid.addWidget(self.date, 2, 1, 1, 1)
        grid.addWidget(self.cal_but, 2, 2, 1, 1)
        grid.addWidget(self.find_but, 2, 3, 1, 1)
        grid.addWidget(self.lab_by_date, 2, 0, 1, 1)
        grid.addWidget(self.scroll_area, 3, 0, 1, 6)
        grid.addWidget(self.exit_but, 5, 5, 1, 1)
        self.setLayout(grid)
        self.txt_all.setText(str(len(self.news.keys())))

    def calendar(self):
        self.cal=QCalendarWidget()
        self.cal.setGridVisible(True)
        self.cal.setGeometry(300,300,450,200)
        self.cal.setWindowIcon(QIcon('/home/admin1/GitProject/images/cb.png'))
        self.cal.setWindowTitle('Calendar')
        self.cal.show()
        self.cal.clicked[QDate].connect(self.show_date)

    def show_date(self):
        self.date.setDate(self.cal.selectedDate())

    def find_news(self):
        self.grid_scroll = QGridLayout()
        self.scroll_content = QWidget()
        self.scroll_content.setLayout(self.grid_scroll)
        self.scroll_area.setWidget(self.scroll_content)
        count=1
        for item in self.news.keys():
          if self.date.text().replace('/','.')==str(self.news[item]['Date']):
              vallue=QTextEdit((str(self.news[item]['Title'])))
              self.grid_scroll.addWidget(vallue, count, 0, 1, 1)
              count+=1

























if __name__=='__main__':
    app=QApplication(sys.argv)
    a=Interface()
    sys.exit(app.exec_())


