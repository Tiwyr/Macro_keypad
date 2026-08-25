import sys

from PySide6 import QtCore, QtGui, QtWidgets
from BackendProcesses import BackgroundProcess
from Left_Toolbar import Profile_Toolbar
from profile_window import Profile_window
import database

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Start Page")
        self.setGeometry(200, 200, 800, 700)

        self.DB = database.Database()
        self.DB_profiles = self.DB.list_profiles()

        
        
        self.toolbar = Profile_Toolbar()
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

        if not self.DB_profiles:
                    self.DB.create_profile("Profile 1")
                    self.DB_profiles = self.DB.list_profiles()

        

        self.toolbar.load_profiles(self.DB_profiles)
        
        #Load profiles from data base
        self.profile_window = Profile_window()
        self.setCentralWidget(self.profile_window)

        self.toolbar.active_profile_signal.connect(self.change_profile)
        self.toolbar.confirmed_delete_profile_signal.connect(self.delete_profile)
        self.toolbar.confirmed_renamed_profile_signal.connect(self.rename_profile)
        self.toolbar.added_profile_signal.connect(self.add_profile)
        self.toolbar.save_action.triggered.connect(self.save_profile_to_DB)


        self.Tray_init()
        self.toolbar.set_active_profile(0)

    
        
        self.worker = BackgroundProcess(self)
        self.worker.connection_changed.connect(self.update_connection_status)
        self._last_connection_state = None
        self.update_connection_status(self.worker.connected)

        self.setStatusBar(QtWidgets.QStatusBar(self))

    @QtCore.Slot(str)
    def change_profile(self, profile_name):
        if self.profile_window.is_changed:
             answer = QtWidgets.QMessageBox.question(
                  self,
                  "Confirm save",
                  "The profile has been modified do you want to save?",
             (
                QtWidgets.QMessageBox.StandardButton.Save
                | QtWidgets.QMessageBox.StandardButton.No
                ),
                QtWidgets.QMessageBox.StandardButton.No,
            )

             if answer == QtWidgets.QMessageBox.StandardButton.Save:
                self.save_profile_to_DB()
             else:
                pass
             
        print(f"Load profile {profile_name}")
        profile_data = self.DB.load_profile(self.id_from_name(profile_name))
        self.profile_window.load_profile(profile_data=profile_data)
        self.current_profile_id = profile_data["id"]

    def delete_profile(self, profile_name):
         self.DB.delete_profile(self.current_profile_id)
         self.DB_profiles = self.DB.list_profiles()

    def add_profile(self, profile_name):
         self.DB.create_profile(profile_name)
         self.DB_profiles = self.DB.list_profiles()

    def rename_profile(self, new_name):
             self.DB.rename_profile(self.current_profile_id,new_name)
             self.DB_profiles = self.DB.list_profiles()

    def save_profile_to_DB(self):

        for layer_id in self.profile_window.removed_layer_ids:
             self.DB.delete_layer(layer_id)
        
        layers = self.profile_window.overview_box
        for layer_index in range(layers.count()):
            layer_widget = layers.widget(layer_index)

            if layer_widget.Layer_id is None:
                 generated_id = self.DB.add_layer(self.current_profile_id, layer_widget.name)
                 layer_widget.Layer_id = generated_id

            else:
                 self.DB.rename_layer(layer_widget.Layer_id, layer_widget.name)

            for i in range(3):
                for j in range(4):
                        button = layer_widget.grid.itemAtPosition(i,j).widget()
                        self.DB.update_button( layer_widget.Layer_id,
                                               button.id_index,
                                               button.function,
                                               button.cmd,
                                               button.icon_data
                                               )
        return 
        

    def id_from_name(self, profile_name):
        for profile in self.DB_profiles:
                      if profile["name"] == profile_name:
                           return profile["id"]


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
