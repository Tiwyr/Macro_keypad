import sys

from PySide6 import QtCore, QtGui, QtWidgets
from BackendProcesses import background_process


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Start Page")
        self.setGeometry(200, 200, 800, 700)
        self.setCentralWidget(MyWidget())

        self.Tray_init()

        # Example background process: this runs every five seconds, even while
        # the window is hidden. Replace background_task with your own work.
        self.background_timer = QtCore.QTimer(self)
        self.background_timer.timeout.connect(self.background_task)
        self.background_timer.start(5_000)


    def Tray_init(self):
                tray_icon = self.style().standardIcon(
                    QtWidgets.QStyle.StandardPixmap.SP_ComputerIcon
                )
                self.tray = QtWidgets.QSystemTrayIcon(tray_icon, self)
                self.tray.setToolTip("Macro Keypad")
        
                tray_menu = QtWidgets.QMenu()
        
                show_action = QtGui.QAction("Show", self)
                show_action.triggered.connect(self.show_from_tray)
                tray_menu.addAction(show_action)
        
                quit_action = QtGui.QAction("Quit", self)
                quit_action.triggered.connect(QtWidgets.QApplication.quit)
                tray_menu.addAction(quit_action)
        
                self.tray.setContextMenu(tray_menu)
                self.tray.activated.connect(self.tray_activated)
                self.tray.show()


    def closeEvent(self, event):
        """Hide the window instead of stopping the application."""
        event.ignore()
        self.hide()
        self.tray.showMessage(
            "Macro Keypad",
            "The application is still running in the background.",
            QtWidgets.QSystemTrayIcon.MessageIcon.Information,
            2_000,
        )

    @QtCore.Slot()
    def show_from_tray(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    @QtCore.Slot(QtWidgets.QSystemTrayIcon.ActivationReason)
    def tray_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self.show_from_tray()

    @QtCore.Slot()
    def background_task(self):
        print("Background task is running")


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        grid = QtWidgets.QGridLayout(self)

        grid.addWidget(QtWidgets.QLabel("Name:"), 0, 0)
        grid.addWidget(QtWidgets.QLineEdit(), 0, 1)

        grid.addWidget(QtWidgets.QLabel("Email:"), 1, 0)
        grid.addWidget(QtWidgets.QLineEdit(), 1, 1)

        save_button = QtWidgets.QPushButton("Save")
        save_button.setFixedSize(120, 40)
        grid.addWidget(
            save_button,
            2,
            1,
            alignment=QtCore.Qt.AlignmentFlag.AlignHCenter,
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
