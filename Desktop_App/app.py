from PySide6.QtWidgets import QApplication, QMainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Start Page")
        self.setGeometry(200,200,800,700)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
