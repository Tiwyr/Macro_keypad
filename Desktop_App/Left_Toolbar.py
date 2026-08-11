from PySide6 import QtCore, QtGui, QtWidgets

class Profile_Toolbar(QtWidgets.QToolBar):

    
    def __init__(self):
        super().__init__()
        self.setMovable(False)
        Top_spacer = QtWidgets.QWidget()
        Top_spacer.setMinimumHeight(50)
        self.addWidget(Top_spacer)
        self.addAction("Top action")

        spacer = QtWidgets.QWidget()
        spacer.setMinimumWidth(80)
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.addWidget(spacer)
        self.bottom_menu_init()
        

       

    def bottom_menu_init(self):
           self.addSeparator()
           self.add_action = self.addAction("Add")
           self.del_action = self.addAction("Delete")
           self.addSeparator()
           self.save_action = self.addAction("Save")
           self.upload_action = self.addAction("Upload")

           upload_button = self.widgetForAction(self.upload_action)
           upload_button.setStyleSheet("""
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
            """)

           self.add_action.triggered.connect(self.AddProfile)
           self.del_action.triggered.connect(self.DeleteProfile)
           self.save_action.triggered.connect(self.SaveProfile)
           self.upload_action.triggered.connect(self.UploadProfile)

    def AddProfile(self):
        Exception(NotImplementedError)

    def SaveProfile(self):
            Exception(NotImplementedError)

    def DeleteProfile(self):
            Exception(NotImplementedError)

    def UploadProfile(self):
                Exception(NotImplementedError)