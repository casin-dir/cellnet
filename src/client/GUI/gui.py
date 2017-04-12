# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QTextEdit, QLineEdit, QLabel,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def myfunc(self):
        print('asdasdasd')
        text = self.reviewEdit.toPlainText()
        print(text)
        self.lbl.setText(text)




    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        btn = QPushButton('Отправить', self)
        btn.setToolTip('Отправить\nсообщение')
        btn.resize(btn.sizeHint())
        btn.move(200, 350)
        btn.clicked.connect(self.myfunc)

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


#def start_gui():
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

