from PyQt5.QtGui import *
from PyQt5.QtCore import *

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

class MyDelegate(QStyledItemDelegate):

    def sizeHint(self, option, index):
        default = QStyledItemDelegate.sizeHint(self, option, index)
        return QSize(default.width(), default.height() + 12)

    def createEditor(self, parent, option, index):
        editor = QTextEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(text)

    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.toPlainText()))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MyMainWindow()
    ui.show()
    sys.exit(app.exec_())