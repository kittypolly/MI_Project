import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):

        super().__init__()

        combolist = ["test1", "test2"]

        combo = QComboBox(self)
        combo.addItems(combolist)


        layout = QHBoxLayout()
        layout.addWidget(combo)


        self.setLayout(layout)

        print(combo.currentText())

        #이제 이걸 텍스트로 받아오는걸 해야돼.



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())