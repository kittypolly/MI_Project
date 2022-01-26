from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setItemDelegate(MyDelegate(self))
        self.setCentralWidget(self.tree)

        itemWidget = QTreeWidgetItem()
        itemWidget.setFlags(itemWidget.flags() | Qt.ItemIsEditable)
        itemWidget.setText(0, "very Small Text Edit")
        self.tree.addTopLevelItem(itemWidget)

        itemWidget2 = QTreeWidgetItem()
        itemWidget2.setFlags(itemWidget.flags() | Qt.ItemIsEditable)
        itemWidget2.setText(0, """very Small Text Edit\n
        very Small Text Edit\n
        very Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Editvery Small Text Edit""")
        self.tree.addTopLevelItem(itemWidget2)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MyMainWindow()
    ui.show()
    sys.exit(app.exec_())