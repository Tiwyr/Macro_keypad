from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton
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

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        grid = QGridLayout(self)

        grid.addWidget(QLabel("Name:"), 0, 0)
        grid.addWidget(QLineEdit(),     0, 1)

        grid.addWidget(QLabel("Email:"), 1, 0)
        grid.addWidget(QLineEdit(),      1, 1)
        saveButton = QPushButton("Save")
        saveButton.setFixedSize(120, 40) 
        grid.addWidget(saveButton, 2, 1, alignment=QtCore.Qt.AlignHCenter)
        


       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
