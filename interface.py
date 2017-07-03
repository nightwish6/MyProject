import sys
from pprint import pprint
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, qApp, QAction, QTextEdit, QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

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
        self.setGeometry(10,10,500,150)
        self.setWindowIcon(QIcon('cb.png'))
        self.date_input()
        self.show()
    def date_input(self):
        self.txtbox1 = QLineEdit(self)
        self.txtbox1.resize(100,20)
        self.lab=QLabel('Date:',self)
        self.send_but=QPushButton('Send')
        self.send_but.clicked.connect(self.req_curr_rate)
        self.combo_val=QComboBox(self)
        self.combo_val.addItem('AUD')
        self.combo_val.addItem('AZN')
        self.combo_val.addItem('GBP')
        self.combo_val.activated[str].connect(self.f)


        grid=QGridLayout()
        grid.setSpacing(1)
        grid.addWidget(self.lab, 1,0)
        grid.addWidget(self.txtbox1, 1,1)
        grid.addWidget(self.send_but, 2,0)
        grid.addWidget(self.combo_val, 3,0)

        options=('CharCode','Name','Nominal','NumCode','Value')
        count=4
        self.options=dict()

        for option in options:
            val_lab=QLabel(option)
            val_edit=QLineEdit(self)
            grid.addWidget(val_lab,count,0)
            grid.addWidget(val_edit,count,1)
            self.options[option]=val_edit
            count+=1

        self.setLayout(grid)
    def req_curr_rate(self):
        from cb_requests import req_curr_rate
        txtbox1_value=self.txtbox1.text()
        self.request=req_curr_rate(txtbox1_value)
        for key in self.request:
            if key=='ValCurs': continue
            elif self.request[key]['CharCode']==self.combo_val.currentText():
                for values in self.request.values():
                    for value in values:
                        if value=='Date' or value=='name':continue
                        else: self.options[value].setText(str(self.request[key][value]))






    def f(self):
        pass




























if __name__=='__main__':
    app=QApplication(sys.argv)
    a=Interface()
    sys.exit(app.exec_())


