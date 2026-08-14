from PySide6 import QtCore, QtWidgets
CELL_MIN_SIZE = 120
CELL_MAX_SIZE = 200
CELL_SPACING = 10

class Profile_window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Profile Window")
        self.Base_Layout = QtWidgets.QHBoxLayout(self)


        self.Layer_Box = QtWidgets.QWidget(self)
        self.Layer_Box.setMinimumSize(100, 200)
        self.Layer_Box.setMaximumSize(300, 200)
        self.Layer_Box.setObjectName("LayerBox")

        self.Layer_Box.setStyleSheet("""
            QWidget#LayerBox {
                border: 3px solid orange;
                border-radius: 10px;
            }
        """)
        
        
        self.overview_box = QtWidgets.QWidget(self)
        self.OverviewLayout = QtWidgets.QVBoxLayout(self.overview_box)

        self.Base_Layout.addWidget(self.overview_box)
        self.Base_Layout.addWidget(self.Layer_Box)

        self.fill_Layer_box()
        self.fill_overview_box()
        
        
    

        
    def fill_Layer_box(self):

        self.Layer_Box.setLayout(QtWidgets.QVBoxLayout())
        self.Layer_selection = QtWidgets.QListWidget(self.Layer_Box)
      
        self.Layer_Box.layout().addWidget(self.Layer_selection)

        #self.Layer_selection.setMinimumSize(50, 30)
        self.Layer_selection.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.add_Action = QtWidgets.QPushButton("Add Layer", self.Layer_Box)
        self.Layer_Box.layout().addWidget(self.add_Action)
        self.remove_Action = QtWidgets.QPushButton("Remove Layer", self.Layer_Box)
        self.Layer_Box.layout().addWidget(self.remove_Action)
        self.rename_Action = QtWidgets.QPushButton("Rename Layer", self.Layer_Box)
        self.Layer_Box.layout().addWidget(self.rename_Action)
        

    
    def fill_overview_box(self):
        self.Button_Box = QtWidgets.QWidget(self.overview_box)
        self.Button_Box.setMinimumSize((CELL_MIN_SIZE+CELL_SPACING) * 4, (CELL_MIN_SIZE+CELL_SPACING) * 3)
        self.Button_Box.setMaximumSize((CELL_MAX_SIZE+CELL_SPACING) * 4, (CELL_MAX_SIZE+CELL_SPACING) * 3)
        self.grid = QtWidgets.QGridLayout(self.Button_Box)
   
        
        self.grid.setVerticalSpacing(CELL_SPACING)
        self.grid.setHorizontalSpacing(CELL_SPACING)
        for i in range(3):
            for j in range(4):
                button = QtWidgets.QPushButton(f"Button {i*4+j+1}", self.Button_Box)
                button.setMinimumSize(CELL_MIN_SIZE, CELL_MIN_SIZE)
                button.setMaximumSize(CELL_MAX_SIZE,CELL_MAX_SIZE)
                button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
                self.grid.addWidget(button, i, j, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        self.Encoder_Box = QtWidgets.QWidget(self)
        #self.Encoder_Box.setMinimumSize(20, 20)
        #self.Encoder_Box.setMaximumSize(300, 300)
        self.Encoder_Box.setStyleSheet(
            "background-color: rgb(240, 0, 0);"
            "border: 1px solid gray;"
            "border-radius: 5px;"
        )

        self.OverviewLayout.addWidget(self.Encoder_Box, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.OverviewLayout.addWidget(self.Button_Box, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)