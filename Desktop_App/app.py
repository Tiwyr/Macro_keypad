from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Start Page")
        self.setGeometry(200,200,800,700)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.text_2 = QtWidgets.QLabel("Hej Värld",
                                             alignment=QtCore.Qt.AlignBottom  | QtCore.Qt.AlignLeft)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text_2)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
        self.button.clicked.connect(self.magiker)

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
    #window = MainWindow()
    #window.show()
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())
