import sys
from pprint import pprint
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, qApp, QAction, QTextEdit, QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QCalendarWidget
from PyQt5.QtWidgets import QMessageBox, QErrorMessage
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, QDate

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.composition()

    def composition(self):
        self.setWindowTitle('Central Bank')
        self.setGeometry(10, 10, 500, 500)
        self.setWindowIcon(QIcon('cb.png'))
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
        exitAction = QAction(QIcon('cb.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit the program')
        exitAction.triggered.connect(self.close)
        reqValAction=QAction(QIcon('cb.png'),'Learn the exchange rate', self)
        reqValAction.triggered.connect(self.req_val_act)
        reqValAction.setStatusTip('Request currency rates')
        self.toolbar.addAction(reqValAction)
        self.toolbar.addAction(exitAction)
    def req_val_act(self):
        self.win_1=Windows_1()

class Windows_1(QWidget):
    def __init__(self):
        super().__init__()
        self.composition()

    def composition(self):
        self.setWindowTitle('Central Bank currency rates')
        self.setGeometry(10,10,350,150)
        self.setWindowIcon(QIcon('cb.png'))
        self.date_input()
        self.show()

    def date_input(self):
        self.txtbox1 = QLineEdit(self)
        self.txtbox2 = QLineEdit(self)
        self.txtbox3 = QLineEdit(self)
        self.lab1=QLabel('Date:',self)
        self.lab2=QLabel('dd',self)
        self.lab3=QLabel('mm', self)
        self.lab4= QLabel('yyyy', self)
        self.send_but=QPushButton('Send')
        self.cal_but=QPushButton('Calendar')
        self.save_but=QPushButton('Save data')
        self.exit_but=QPushButton('Exit')
        self.save_but.clicked.connect(self.save_date)
        self.send_but.clicked.connect(self.req_curr_rate)
        self.cal_but.clicked.connect(self.calendar)
        self.exit_but.clicked.connect(self.close)
        self.combo_val=QComboBox(self)
        self.combo_val.addItem('AUD')
        self.combo_val.addItem('AZN')
        self.combo_val.addItem('GBP')
        self.combo_val.addItem('AMD')
        self.combo_val.addItem('BYN')
        self.combo_val.addItem('BGN')
        self.combo_val.addItem('BRL')
        self.combo_val.addItem('HUF')
        self.combo_val.addItem('HKD')
        self.combo_val.addItem('DKK')
        self.combo_val.addItem('USD')
        self.combo_val.addItem('EUR')
        self.combo_val.addItem('INR')
        self.combo_val.addItem('KZT')
        self.combo_val.addItem('CAD')
        self.combo_val.addItem('KGS')
        self.combo_val.addItem('CNY')
        self.combo_val.addItem('MDL')
        self.combo_val.addItem('NOK')
        self.combo_val.addItem('PLN')
        self.combo_val.addItem('RON')
        self.combo_val.addItem('XDR')
        self.combo_val.addItem('SGD')
        self.combo_val.addItem('TJS')
        self.combo_val.addItem('TRY')
        self.combo_val.addItem('TMT')
        self.combo_val.addItem('UZS')
        self.combo_val.addItem('UAH')
        self.combo_val.addItem('CZK')
        self.combo_val.addItem('SEK')
        self.combo_val.addItem('CHF')
        self.combo_val.addItem('ZAR')
        self.combo_val.addItem('KRW')
        self.combo_val.addItem('JPY')
        self.combo_val.activated[str].connect(self.insert_combo_val)
        grid=QGridLayout()
        grid.setSpacing(1)
        grid.addWidget(self.lab1,1,0,1,1)
        grid.addWidget(self.txtbox1,1,1,1,1)
        grid.addWidget(self.lab2,1,2,1,1)
        grid.addWidget(self.txtbox2,1,3,1,1)
        grid.addWidget(self.lab3,1,4,1,1)
        grid.addWidget(self.txtbox3,1,5,1,1)
        grid.addWidget(self.lab4,1,6,1,1)
        grid.addWidget(self.send_but, 1,7,1,1)
        grid.addWidget(self.cal_but,1,8,1,1)
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
        txtbox_value=self.txtbox1.text()+'/'+self.txtbox2.text()+'/'+self.txtbox3.text()
        self.request=req_curr_rate(txtbox_value)
        for key in self.request:
            if key=='ValCurs': continue
            elif self.request[key]['CharCode']==self.combo_val.currentText():
                for values in self.request.values():
                    for value in values:
                        if value=='Date' or value=='name':continue
                        else: self.options[value].setText(str(self.request[key][value]))

    def insert_combo_val(self, combo_val):
        for key in self.request:
            if key =='ValCurs': continue
            elif self.request[key]['CharCode']==combo_val:
                for values in self.request.values():
                    for value in values:
                        if value=='Date' or value=='name':continue
                        else: self.options[value].setText(str(self.request[key][value]))

    def calendar(self):
        self.cal=QCalendarWidget()
        self.cal.setGridVisible(True)
        self.cal.setGeometry(300,300,450,200)
        self.cal.setWindowIcon(QIcon('cb.png'))
        self.cal.setWindowTitle('Calendar')
        self.cal.show()
        self.cal.clicked[QDate].connect(self.show_date)

    def show_date(self):
        self.date = self.cal.selectedDate()
        self.curr_date=self.date.toString('dd/MM/yyyy').split('/')
        self.txtbox1.setText(self.curr_date[0])
        self.txtbox2.setText(self.curr_date[1])
        self.txtbox3.setText(self.curr_date[2])

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
        else:
            if len(self.request.values())<=1:
                self.error_no_data = QErrorMessage(self)
                self.error_no_data.setWindowTitle('No data')
                self.error_no_data.showMessage('No data to save')
            else: self.message_save_data=QMessageBox.information(self, 'Save Data', 'Data saved',
                                           QMessageBox.Ok)










if __name__=='__main__':
    app=QApplication(sys.argv)
    a=Interface()
    sys.exit(app.exec_())


