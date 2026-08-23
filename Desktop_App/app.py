import sys

from PySide6 import QtCore, QtGui, QtWidgets
from BackendProcesses import BackgroundProcess
from Left_Toolbar import Profile_Toolbar
from profile_window import Profile_window

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Start Page")
        self.setGeometry(200, 200, 800, 700)
        
        self.toolbar = Profile_Toolbar()
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)
        #Load profiles from data base

        self.setCentralWidget(Profile_window())

        self.Tray_init()


        self.worker = BackgroundProcess(self)
        self.worker.connection_changed.connect(self.update_connection_status)
        self._last_connection_state = None
        self.update_connection_status(self.worker.connected)

        self.setStatusBar(QtWidgets.QStatusBar(self))

        

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
            self.statusBar().showMessage("Connected")
        else:
            icon = self.style().standardIcon(
                QtWidgets.QStyle.StandardPixmap.SP_MessageBoxWarning
            )
            self.status_action.setText("Status: Disconnected")
            self.tray.setToolTip("Macro Keypad — Disconnected")
            self.statusBar().showMessage("Disconnected")

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


        

def set_appTheme(app: QtWidgets.QApplication):
    app.setStyle("Fusion")  # Optional, but respects palettes consistently
    
    palette = app.palette()
    Role = QtGui.QPalette.ColorRole

    palette.setColor(Role.Window, QtGui.QColor(30, 30, 30))
    palette.setColor(Role.WindowText, QtGui.QColor(240, 240, 240))

    palette.setColor(Role.Base, QtGui.QColor(20, 20, 20))
    palette.setColor(Role.AlternateBase, QtGui.QColor(40, 40, 40))
    palette.setColor(Role.Text, QtGui.QColor(240, 240, 240))
    palette.setColor(Role.PlaceholderText, QtGui.QColor(140, 140, 140))

    palette.setColor(Role.Button, QtGui.QColor(45, 45, 45))
    palette.setColor(Role.ButtonText, QtGui.QColor(240, 240, 240))

    palette.setColor(Role.Highlight, QtGui.QColor(40, 110, 190))
    palette.setColor(Role.HighlightedText, QtGui.QColor(255, 255, 255))

    palette.setColor(Role.ToolTipBase, QtGui.QColor(50, 50, 50))
    palette.setColor(Role.ToolTipText, QtGui.QColor(255, 255, 255))

    palette.setColor(Role.Link, QtGui.QColor(80, 160, 255))
    palette.setColor(Role.BrightText, QtGui.QColor(255, 70, 70))

    app.setPalette(palette)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    set_appTheme(app)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

