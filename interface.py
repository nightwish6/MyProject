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
import webbrowser
import yaml

"""Класс Interface, создает основное окно приложения с Toolbar для работы с
API Центрального банка РФ
"""
class Interface(QMainWindow):
    """При создании экземпляра класса, в __init__ мы передаем настройки из файла settings.yaml,
    путь к базе данных и путь к Images для иконок.    
    """
    def __init__(self, settings_way_db, settings_panel=None, set_tool1=None,
                 set_tool2=None,
                 set_tool3=None,
                 set_tool4=None):
        super().__init__() #Возвращаем родительский объект Interface с классом
        self.settings_way_db=settings_way_db
        self.settings_panel=settings_panel
        self.set_tool1=set_tool1
        self.set_tool2=set_tool2
        self.set_tool3=set_tool3
        self.set_tool4=set_tool4
        self.composition() #Вызываем конструктор для создания основных компонентов класса
    """Фу-ия composition, является конструктором для главного окна приложения
    """
    def composition(self):
        self.setWindowTitle('Central Bank')
        self.setGeometry(10, 10, 500, 500) #Задаем размеры окна
        self.setWindowIcon(QIcon(self.settings_panel))
        self.center()#Основное окно приложения будет располгаться точно по центру экрана
        self.toolbar()#Конструируем тулбар
        self.statusBar()#Конструируем статусбар
        self.cent_wid=QTextEdit()
        self.setCentralWidget(self.cent_wid)#Центральный виджет основного окна
        self.show()
    """Фу-ия center позволяет разместить основное окно нашего приложения точно по
    центру экрана
    """
    def center(self):
        qr=self.frameGeometry()#Получаем прямоугольник определяющий геометрию главного окна
        cp=QDesktopWidget().availableGeometry().center()#Получем разрешение экрана нашего монитора
        qr.moveCenter(cp)#Получаем центральную точку
        self.move(qr.topLeft())#Двигаем левый верхний угол окна приложения в верхний левый угол qr
    """Фу-ия toolbar является конструктром для панели инструментов главного окна
    приложения 
    """
    def toolbar(self):
        self.toolbar = self.addToolBar('ToolBar')#Создаем основные элементы панели инструментов
        exitAction = QAction(QIcon(self.set_tool1), 'Exit', self)#Создаем экземпляры классов QAction (иконки)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit the program')
        exitAction.triggered.connect(self.close)#Задаем сигнал события за каждой иконкой к определенной функции
        reqValAction=QAction(QIcon(self.set_tool2),'Learn the exchange rate', self)
        reqValAction.triggered.connect(self.req_val_act)
        reqValAction.setStatusTip('Request currency rates')#При наведении курсора мыши, в статус баре появляется соответствующая запись
        dynamicRateAction=QAction(QIcon(self.set_tool3),'Learn the course dynamics', self)
        dynamicRateAction.triggered.connect(self.req_val_dynamic)
        dynamicRateAction.setStatusTip('Schedule a change in the exchange rate for the period')
        newsAction=QAction(QIcon(self.set_tool4),'Get news', self)
        newsAction.setStatusTip('Get news from the Central bank')
        newsAction.triggered.connect(self.req_news)
        self.toolbar.addAction(reqValAction)#Добавляем наши созданные элементы на панель инструментов
        self.toolbar.addAction(dynamicRateAction)
        self.toolbar.addAction(newsAction)
        self.toolbar.addAction(exitAction)
    """Фу-ии req_val_act и req_val_dynamic создают экземпляры классов Windows_1 и Windows_2
    """
    def req_val_act(self):
        self.win_1=Windows_1(self.settings_way_db, self.settings_panel)
    def req_val_dynamic(self):
        self.win_2=Windows_2(self.settings_way_db, self.settings_panel)
    """Фу-ия req_news отправляет запрос базе данных ЦБ РФ, получает обработанные данные в виде
    словаря, создает эземпляр класса Windows_4 и передает словарь в качестве аргумента
    """
    def req_news(self):
        from cb_requests import req_news
        from requests import ConnectionError
        try:
            req_News = req_news() #Обработка исключения, при отправке запроса, в случае отсутствия подключения к интернету, появится окно с ошибкой
            self.win_4 = Windows_4(req_News, self.settings_panel)
        except ConnectionError:
            self.error_no_connect = QErrorMessage(self)
            self.error_no_connect.setWindowTitle('Сonnection Error')
            self.error_no_connect.showMessage('No internet connection')
"""Класс Windows_1, создает окно, которое позволяет нам узнать информацию по курсу любой
валюты, на любое число
"""
class Windows_1(QWidget):
    def __init__(self, settings_way_db, settings_panel=None):
        super().__init__()
        self.settings_way_db=settings_way_db
        self.settings_panel=settings_panel
        self.composition()

    def composition(self):
        self.setWindowTitle('Central Bank currency rates')
        self.setGeometry(10,10,350,150)
        self.setWindowIcon(QIcon(self.settings_panel))
        self.date_input()#Конструируем основные компоненты окна
        self.show()
    """Фу-ия date_input является конструктором для основных элементов окна экземпляров 
    класса Windows_1
    """
    def date_input(self):
        self.lab1=QLabel('Date:',self)
        self.send_but=QPushButton('Send')
        self.cal_but=QPushButton('Calendar')
        self.save_but=QPushButton('Save data')
        self.exit_but=QPushButton('Exit')
        self.save_but.clicked.connect(self.save_date)#При нажатии на кнопки, будет идти сигнал для вызова заданной функции
        self.send_but.clicked.connect(self.req_curr_rate)
        self.cal_but.clicked.connect(self.calendar)
        self.exit_but.clicked.connect(self.close)
        self.data=QDateEdit(self)#Создаем экземпляр класса виджета QDateEdit для окна ввода даты
        self.data.setDisplayFormat('dd/MM/yyyy')
        self.combo_val=QComboBox(self)#Создаем виджет выпадающего списка
        valutes=['AUD','AZN','GBP','AMD','BYN','BGN','BRL','HUF','HKD','DKK','USD','EUR','INR',
                 'KZT','CAD','KGS','CNY','MDL','NOK','PLN','RON','XDR','SGD','TJS','TRY','TMT',
                 'UZS','UAH','CZK','SEK','CHF','ZAR','KRW','JPY']
        for valute in sorted(valutes):
            self.combo_val.addItem(valute)
        self.combo_val.activated[str].connect(self.insert_combo_val)#Закрепляем за каждым элементом списка сигнал для активации заданной функции
        grid=QGridLayout()#Создаем сетку для точного размещения элементов
        grid.setSpacing(1)#Расстояние между элементами в сетке
        grid.addWidget(self.lab1,1,0,1,1)#Добавляем эелементы с позиционированием
        grid.addWidget(self.data,1,1,1,1)
        grid.addWidget(self.cal_but, 1,2,1,1)
        grid.addWidget(self.send_but,1,3,1,1)
        grid.addWidget(self.combo_val, 3,0)
        options=('CharCode','Name','Nominal','NumCode','Value')
        count=4
        self.options=dict()#Создаем словарь для размещения в нем ссылок на объеты экземпляров класса QTextEdit

        for option in options:
            val_lab=QLabel(option)
            val_edit=QLineEdit(self)
            grid.addWidget(val_lab,count,0)
            grid.addWidget(val_edit,count,1,1,8)
            self.options[option]=val_edit
            count+=1

        grid.addWidget(self.save_but,12,7)
        grid.addWidget(self.exit_but,12,8)
        self.setLayout(grid)#Прикрепляем нашу сетку к экземпляру класса Windows_1
    """Фу-ия req_curr_rate отправляет запрос базе данных ЦБ, полученные данные отображает
    в экземплярах класса QTextEdit, ссылки на объекты берет из словаря self.options
    """
    def req_curr_rate(self):
        from cb_requests import req_curr_rate
        from requests import ConnectionError
        if datetime(int(self.data.text()[6:]), int(self.data.text()[3:5]),
                   int(self.data.text()[0:2]),
                hour=0, minute=0, second=0, microsecond=0, tzinfo=None) > datetime.now():#Перед отправкой запроса идет сравнение времени, если введенная дата больше текущей, то выскочит сообщение об ошибке
            self.error_no_data = QErrorMessage(self)
            self.error_no_data.setWindowTitle('No data available')
            self.error_no_data.showMessage('You entered a date that is greater than the current date')
        else:
            try:
                self.request=req_curr_rate(self.data.text())#Обработка исключения, если при отправке запроса, появется ConnectionError, то появится окно с ошибкой
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
    """Фу-ия insert_combo_val получает сигнал от каждого элемента выпадающего списка и
    заполняет объекты словаря self.options полученными данными от запроса в ЦБ РФ
    """
    def insert_combo_val(self, combo_val):
        try:
            for key in self.request: #Обработка исключения, в случае если запрос не был отправлен
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
    """Фу-ия calendar, создает экземпляр класса QCalendarWidget
    """
    def calendar(self):
        self.cal=QCalendarWidget()
        self.cal.setGridVisible(True)#Видимая сетка на календаре
        self.cal.setGeometry(300,300,450,200)
        self.cal.setWindowIcon(QIcon(self.settings_panel))
        self.cal.setWindowTitle('Calendar')
        self.cal.show()
        self.cal.clicked[QDate].connect(self.show_date)#При нажатии на дату передает сигнал заданной функции
    """Фу-ия show_date устанавливает выбранную дату в поле вывода даты  
    """
    def show_date(self):
        self.data.setDate(self.cal.selectedDate())
    """Фу-ия save_date сохраняет полученные данные из базы данных ЦБ РФ, в собственную
    базу данных 'Valute', при отсутсвии базы данных создает новую
    """
    def save_date(self):
        from db_manag import DBmanager
        from sqlite3 import OperationalError as sqlite3_OperationalError
        self.data_base=DBmanager(self.settings_way_db,'valute')#Подключаемся или создаем экземпляр класса DBManager, передаем путь к базе данных из settings.yaml в качестве аргумента

        try: self.data_base.insert_into(self.request)#Сохранеям данные в базу данных 'Valute'
        except sqlite3_OperationalError:
            self.data_base.create_table()#Обработка исключения, в случае отсутсвия бд 'Valute', создаем новую базу данных
            self.data_base.insert_into(self.request)
            self.message_save_data = QMessageBox.information(self, 'Save Data', 'Data saved',
                                                             QMessageBox.Ok)
        except AttributeError:
            self.error_no_data=QErrorMessage(self)
            self.error_no_data.setWindowTitle('No data')
            self.error_no_data.showMessage('No data to save')
        else: self.message_save_data=QMessageBox.information(self, 'Save Data', 'Data saved',
                                           QMessageBox.Ok)

"""Класс Windows_2, создает окно, которое позволяет нам построить график изменения курса валюты
за определенный период
"""
class Windows_2(QWidget):
    def __init__(self, settings_way_db, settings_panel=None):
        super().__init__()
        self.settings_way_db=settings_way_db
        self.settings_panel=settings_panel
        self.composition()

    def composition(self):
        self.setWindowTitle('Central Bank dynamic rates')
        self.setGeometry(10,10,430,30)
        self.setWindowIcon(QIcon(self.settings_panel))
        self.period()#Конструктор основных компонентов окна
        self.show()

    """Фу-ия period является конструктором для основных элементов окна экземпляров 
        класса Windows_2
    """
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
    """Фу-ия req_dynamic_rate отправляет запрос в базу данных ЦБ РФ, а полученные данные
    передает создаваемому экземпляру класса Windows_3, который строит сам график изменения
    курса валюты
    """
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
                        self.win_3=Windows_3(self.dynamic_req, self.settings_panel)
                    except ConnectionError:
                        self.error_no_connect = QErrorMessage(self)
                        self.error_no_connect.setWindowTitle('Сonnection Error')
                        self.error_no_connect.showMessage('No internet connection')

    """Фу-ия save_dynamic сохраняет полученные данные из базы данных ЦБ РФ, в собственную
        базу данных 'Valute', при отсутсвии базы данных создает новую
    """
    def save_dynamic(self):
        from db_manag import DBmanager
        from sqlite3 import OperationalError as sqlite3_OperationalError
        self.data_base = DBmanager(self.settings_way_db, 'valute')
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

"""Класс Windows_3, создает окно, которое отображает построенный график, на основании полученных
данных из запроса в ЦБ, используется библиотека matplotlib
"""

class Windows_3(QWidget):
    def __init__(self, dynamic_data, settings_panel=None):
        super().__init__()
        self.dynamic_req = dynamic_data
        self.settings_panel = settings_panel
        self.composition()

    def composition(self):
        self.setWindowTitle('Shedule')
        self.setGeometry(10,10,600,430)
        self.setWindowIcon(QIcon(self.settings_panel))
        self.course_schedule()
        grid=QGridLayout()
        grid.addWidget(self.canvas)
        self.setLayout(grid)
        self.show()
    """Фу-ия course_schedule строит непосредственно сам график
    """
    def course_schedule(self):
        self.coordinates = dict()
        for key in self.dynamic_req.keys():
            if key == 'ValCurs':
                continue
            else:
                self.coordinates[key] = self.dynamic_req[key]['Value']

        self.xdates = [date(int(i[6:]), int(i[3:5]), int(i[0:2])) for i in list(self.coordinates.keys())]#Преобразуем данные (дата) для оси Х
        self.xdates.sort()
        self.yvalues = list()
        for dates in self.xdates:
            for key in self.coordinates:
                if dates.strftime('%d.%m.%Y') == str(key):
                    self.yvalues.append(float(self.coordinates[key].replace(',', '.')))#Данные для оси Y
        self.figure = plt.figure()#Берем Фрейм для графика
        self.schedule = self.figure.gca()#Шаблон для построения графика
        self.schedule.set_title('Course schedule')#Редактируем
        self.schedule.set_xlabel('Dates')
        self.schedule.set_ylabel('Values')
        self.schedule.xaxis.set_major_formatter(
            mdates.DateFormatter('%d/%m/%Y'))
        self.schedule.yaxis.set_major_formatter(
            mtick.FormatStrFormatter('%.2f'))
        self.schedule.plot(self.xdates, self.yvalues, 'r')
        self.figure.autofmt_xdate()#Автомормат даты на оси X
        self.canvas = FigureCanvas(self.figure)#Интеграция matplotlib с PyQT5, чтобы график был встроен в виджет Pyqt5

"""Класс Windows_4 позволяет построить окно для отображения новостей с сервера ЦБ РФ
"""

class Windows_4(QWidget):
    def __init__(self, req_News, settings_panel=None):
        super().__init__()
        self.news = req_News
        self.settings_panel=settings_panel
        self.composition()

    def composition(self):
        self.setWindowTitle('Central Bank News')
        self.setGeometry(10, 10, 270, 650)
        self.setWindowIcon(QIcon(self.settings_panel))
        self.news_input()
        self.show()

    """Фу-ия news_input является конструктором для основных элементов окна экземпляров 
        класса Windows_4
    """
    def news_input(self):
        self.lab_all = QLabel('All news:', self)
        self.lab_search = QLabel('Search:', self)
        self.lab_by_date = QLabel('News by date:', self)
        self.txt_all = QLineEdit(self)
        self.txt_search = QLineEdit(self)
        self.exit_but = QPushButton('Exit')
        self.find_but = QPushButton('Find')
        self.find_but2 = QPushButton('Find')
        self.cal_but= QPushButton('Calendar')
        self.cal_but.clicked.connect(self.calendar)
        self.find_but.clicked.connect(self.find_news)
        self.find_but2.clicked.connect(self.find_by_words)
        self.exit_but.clicked.connect(self.close)
        self.date = QDateEdit(self)
        self.date.setDisplayFormat('dd/MM/yyyy')
        self.scroll_area=QScrollArea()#Создаем обект с горизонтальной и вертикальной полосой прокрутки
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(2)#Вертикальная и горизонтальная полоса прокрутки будут вседа видны
        self.scroll_area.setHorizontalScrollBarPolicy(2)
        grid = QGridLayout()
        grid.setSpacing(1)
        grid.addWidget(self.lab_all, 1, 0, 1, 1)
        grid.addWidget(self.txt_all, 1, 1, 1, 1)
        grid.addWidget(self.date, 2, 1, 1, 1)
        grid.addWidget(self.cal_but, 2, 2, 1, 1)
        grid.addWidget(self.find_but, 2, 3, 1, 1)
        grid.addWidget(self.lab_by_date, 2, 0, 1, 1)
        grid.addWidget(self.lab_search, 3, 0, 1, 1)
        grid.addWidget(self.txt_search, 3, 1, 1, 2)
        grid.addWidget(self.find_but2, 3, 3, 1, 1)
        grid.addWidget(self.scroll_area, 4, 0, 1, 6)
        grid.addWidget(self.exit_but, 5, 5, 1, 1)
        self.setLayout(grid)
        self.txt_all.setText(str(len(self.news.keys())))

    def calendar(self):
        self.cal=QCalendarWidget()
        self.cal.setGridVisible(True)
        self.cal.setGeometry(300,300,450,200)
        self.cal.setWindowIcon(QIcon(self.settings_panel))
        self.cal.setWindowTitle('Calendar')
        self.cal.show()
        self.cal.clicked[QDate].connect(self.show_date)

    def show_date(self):
        self.date.setDate(self.cal.selectedDate())
    """Фу-ия find_news динамически создает объекты: поля вывода текста и кнопки для переноса
    на сайт ЦБ для просмотра новости, на основании полученных данных с сервера ЦБ РФ
    """
    def find_news(self):
        if datetime(int(self.date.text()[6:]), int(self.date.text()[3:5]),
                    int(self.date.text()[0:2]),
                    hour=0, minute=0, second=0, microsecond=0, tzinfo=None) > datetime.now():
            self.error_no_data = QErrorMessage(self)
            self.error_no_data.setWindowTitle('No data available')
            self.error_no_data.showMessage('You entered a date that is greater than the current date')
        else:
            self.grid_scroll = QGridLayout()#Создаем сетку внутри области прокрутки
            self.scroll_content = QWidget()
            self.scroll_content.setLayout(self.grid_scroll)
            self.scroll_area.setWidget(self.scroll_content)
            self.but_and_url = dict()
            count = 2
            for item in self.news.keys():
                if self.date.text().replace('/', '.') == str(self.news[item]['Date']):
                    self.vallue = QTextEdit((str(self.news[item]['Title'])))
                    self.button = QPushButton('Send')
                    self.url = str(self.news[item]['Url'])
                    self.button.clicked.connect(self.open_url)
                    self.grid_scroll.addWidget(self.vallue, count, 0, 1, 1)
                    count += 1
                    self.grid_scroll.addWidget(self.button, count, 0, 1, 1)
                    count += 1
                    self.but_and_url[self.button] = self.url
    """Фу-ия open_url при нажтии на кнопку под новостью, переносит на сайт ЦБ для просмотра 
    """
    def open_url(self):
        sendler=self.sender()
        webbrowser.open_new('http://www.cbr.ru'+self.but_and_url[sendler])
    """Фу-ия find_by_words позволяет осуществить поиск по полученным новостям, отобрать
    и отобразить те (также динамически создавая виджеты), которые нас интересуют
    """
    def find_by_words(self):
        if self.txt_search.text()=='':
            self.error_no_data = QErrorMessage(self)
            self.error_no_data.setWindowTitle('Unsuccessful search')
            self.error_no_data.showMessage('You must enter a word')
        else:
            self.grid_scroll = QGridLayout()
            self.scroll_content = QWidget()
            self.scroll_content.setLayout(self.grid_scroll)
            self.scroll_area.setWidget(self.scroll_content)
            self.but_and_url = dict()
            count = 2
            for item in self.news.keys():
                if self.txt_search.text() in self.news[item]['Title']:
                    self.vallue = QTextEdit((str(self.news[item]['Title'])))
                    self.button = QPushButton('Send')
                    self.url = str(self.news[item]['Url'])
                    self.button.clicked.connect(self.open_url)
                    self.grid_scroll.addWidget(self.vallue, count, 0, 1, 1)
                    count += 1
                    self.grid_scroll.addWidget(self.button, count, 0, 1, 1)
                    count += 1
                    self.but_and_url[self.button] = self.url
            if len(self.but_and_url.keys())==0:
                self.error_no_data = QErrorMessage(self)
                self.error_no_data.setWindowTitle('Unsuccessful search')
                self.error_no_data.showMessage('Nothing found on your request')




if __name__=='__main__':
    settings = yaml.load(open('settings.yaml'))
    app=QApplication(sys.argv)#Каждое приложение должно создаватьобъект приложения QApplication. Параметр sys.argv это список аргументов командной строки
    a=Interface(settings['way'],settings['panel'],settings['toolbar']['exit'],
                settings['toolbar']['dollar'],
                settings['toolbar']['dynamic'],
                settings['toolbar']['news'])
    sys.exit(app.exec_())#Полностью заканчиваем цикл нашего приложения


