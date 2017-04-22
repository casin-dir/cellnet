# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QTextEdit, QLineEdit, QLabel,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.btn = None
        self.initUI()


    def myfunc(self, text='%%%'):

        # text = self.reviewEdit.toPlainText()
        # print(text)
        self.lbl.setText(text)


    def add_button_listener(self, func):

        def callback_out(is_error, mes):
            print('Call callback OUT')
            print('Status ' + str(is_error))
            print('Message ' + str(mes))


        def send_data():
            text = self.reviewEdit.toPlainText()
            func(text,callback_out)
        self.btn.clicked.connect(send_data)

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.btn = QPushButton('Отправить', self)
        self.btn.setToolTip('Отправить\nсообщение')
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(200, 350)


        self.lbl = QLabel(self)
        self.lbl.move(100, 300)
        self.lbl.setText('asdasdadsdsasda')

        self.reviewEdit = QTextEdit(self)
        self.reviewEdit.resize(250,200)
        self.reviewEdit.move(10,10)


        self.resize(300, 400)
        self.setWindowTitle('CellNet')
        self.setWindowTitle('Center')
        self.show()


def start_gui():
    app = QApplication(sys.argv)
    ex = Example()
    return [app, ex]
    # sys.exit(app.exec_())
    # return ex

