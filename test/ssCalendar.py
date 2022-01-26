import os.path
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image

class ssCalendarClass(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("날짜입력")
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.Calendar = QCalendarWidget()

    def layouts(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.Calendar)
        self.setLayout(self.mainLayout)