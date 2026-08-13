from PySide6 import QtCore, QtWidgets


class Profile_Toolbar(QtWidgets.QToolBar):
    active_profile_signal = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

        self.setMovable(False)
        self.setWindowTitle("Profiles Menu")
        self.toggleViewAction().setVisible(False)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

        top_spacer = QtWidgets.QWidget()
        top_spacer.setMinimumHeight(5)
        self.addWidget(top_spacer)

        self.profile_list = QtWidgets.QListWidget()
        self.profile_list.setMinimumHeight(100)
        self.profile_list.setSizePolicy(
                    QtWidgets.QSizePolicy.Policy.Preferred,
                    QtWidgets.QSizePolicy.Policy.Expanding,
                )
        self.profile_list.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.profile_list.currentRowChanged.connect(self.set_active_profile)
        self.addWidget(self.profile_list)

        self.bottom_menu_init()

    @property
    def active_profile(self):
        """Return the currently selected profile item, or None."""
        return self.profile_list.currentItem()

    def bottom_menu_init(self):
        self.addSeparator()
        self.add_action = self.addAction("Add")
        self.rename_action = self.addAction("Rename")
        self.del_action = self.addAction("Delete")
        self.addSeparator()
        self.save_action = self.addAction("Save")
        self.upload_action = self.addAction("Upload")

        upload_button = self.widgetForAction(self.upload_action)
        upload_button.setStyleSheet(
            """
            QToolButton {
                background-color: rgb(40, 120, 220);
                color: white;
                padding: 6px;
                border-radius: 4px;
            }

            QToolButton:hover {
                background-color: rgb(60, 145, 245);
            }

            QToolButton:pressed {
                background-color: rgb(25, 90, 175);
            }
            """
        )

        # QAction.triggered emits a bool. The lambdas intentionally discard it.
        self.add_action.triggered.connect(
            lambda checked=False: self.AddProfile()
        )
        self.del_action.triggered.connect(
            lambda checked=False: self.DeleteProfile()
        )
        self.save_action.triggered.connect(
            lambda checked=False: self.SaveProfile()
        )
        self.upload_action.triggered.connect(
            lambda checked=False: self.UploadProfile()
        )
        self.rename_action.triggered.connect(
            lambda checked=False: self.RenameProfile()
        )

    def AddProfile(self, name=None):
        if name is None:
            name = f"Profile {self.profile_list.count() + 1}"

        self.profile_list.addItem(name)
        self.profile_list.setCurrentRow(self.profile_list.count() - 1)

    def RenameProfile(self):
        current_item = self.profile_list.currentItem()
        if current_item is None:
            return

        new_name, ok = QtWidgets.QInputDialog.getText(
            self, "Rename Profile", "Enter new profile name:", text=current_item.text()
        )
        if ok and new_name:
            current_item.setText(new_name)

    def SaveProfile(self):
        pass

    def DeleteProfile(self):
        if self.profile_list.count() <= 1:
            print("Cannot delete the last profile.")
            return

        selected_row = self.profile_list.currentRow()
        if selected_row < 0:
            return
        
        confirm_deletion = QtWidgets.QMessageBox.question(
            self, "Confirm Deletion", "Are you sure you want to delete this profile?"
        )
        if confirm_deletion == QtWidgets.QMessageBox.No:
            return
        
        self.profile_list.takeItem(selected_row)
        # Keep the nearest remaining profile selected.
        next_row = min(selected_row, self.profile_list.count() - 1)
        self.profile_list.setCurrentRow(next_row)

    def UploadProfile(self):
        pass

    @QtCore.Slot(int)
    def set_active_profile(self, row):
        if row < 0:
            return

        profile_item = self.profile_list.item(row)
        print(f"Setting active profile: {profile_item.text()}")
        self.active_profile_signal.emit(profile_item.text())

    def load_profiles(self, profiles):
        for profile_name in profiles:
            self.AddProfile(profile_name)
