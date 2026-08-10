import sys

from PySide6 import QtCore, QtGui, QtWidgets
from BackendProcesses import BackgroundProcess

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Start Page")
        self.setGeometry(200, 200, 800, 700)
        self.setCentralWidget(MyWidget())

        self.Tray_init()

        self.worker = BackgroundProcess(self)
        self.worker.connection_changed.connect(self.update_connection_status)
        self._last_connection_state = None
        self.update_connection_status(self.worker.connected)

    


    def Tray_init(self):
        tray_icon = self.style().standardIcon(
            QtWidgets.QStyle.StandardPixmap.SP_DesktopIcon
        )
        self.tray = QtWidgets.QSystemTrayIcon(tray_icon, self)
        self.tray.setToolTip("Macro Keypad")

        tray_menu = QtWidgets.QMenu()

        self.status_action = QtGui.QAction("Status: Disconnected", self)
        self.status_action.setEnabled(False)
        tray_menu.addAction(self.status_action)
        tray_menu.addSeparator()

        show_action = QtGui.QAction("Show", self)
        show_action.triggered.connect(self.show_from_tray)
        tray_menu.addAction(show_action)

        quit_action = QtGui.QAction("Quit", self)
        quit_action.triggered.connect(QtWidgets.QApplication.quit)
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self.tray_activated)
        self.tray.show()


    @QtCore.Slot(bool)
    def update_connection_status(self, connected):
        previous_state = self._last_connection_state
        self._last_connection_state = connected

        if connected:
            icon = self.style().standardIcon(
                QtWidgets.QStyle.StandardPixmap.SP_DialogApplyButton
            )
            self.status_action.setText("Status: Connected")
            self.tray.setToolTip("Macro Keypad — Connected")
        else:
            icon = self.style().standardIcon(
                QtWidgets.QStyle.StandardPixmap.SP_MessageBoxWarning
            )
            self.status_action.setText("Status: Disconnected")
            self.tray.setToolTip("Macro Keypad — Disconnected")

        self.tray.setIcon(icon)

        if previous_state is True and not connected:
            self.tray.showMessage(
                "Macro Keypad",
                "The keypad connection was lost.",
                QtWidgets.QSystemTrayIcon.MessageIcon.Warning,
                3_000,
            )


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
