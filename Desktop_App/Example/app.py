from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Start Page")
        self.setGeometry(200,200,800,700)
        widget = MyWidget()
        self.setCentralWidget(widget)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["JA", "YES", "Si", "Hai", "Oui", "Ja", "Da", "Ano", "Igen", "Tak", "Evet", "Sim", "是的", "はい", "예", "כן"]

        self.button = QtWidgets.QPushButton("Är Kalle Gay?")
        self.text = QtWidgets.QLabel("?????",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)


        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    @QtCore.Slot()
    def magiker(self):
        if self.text_2.isVisible():
            self.text_2.hide()
        else:
            self.text_2.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
