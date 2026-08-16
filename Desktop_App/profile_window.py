from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon
CELL_SIZE = 180
CELL_SPACING = 10
BUTTON_IDENTIFIERS = ["1","2","3","0","4","5","6","■","7","8","9","●"]

class Macro_button(QtWidgets.QPushButton):

    def __init__(self, 
                 id, int,
                 identifier: str,
                 identifier_index: int,
                 function_type: str | None = None,
                 cmd: str | None = None,
                 icon: QIcon | None = None,
                 parent= None, 
                 ):
        
        super().__init__(parent)
        self.id = id
        self.identifier = identifier
        self.id_index = identifier_index
        if function is not None:
            self.function = function_type

        if cmd is not None:
            self.cmd = cmd

        if icon is not None:
            self.icon = icon


    def set_functionality(self, function_type: str,cmd: str):
        self.function = function_type
        self.cmd = cmd

    def set_icon(self, icon: QIcon):
        self.icon = icon

    def remove_icon(self):
        self.icon = QIcon()

    def reset_button(self):
        self.function = None
        self.cmd = None
        self.remove_icon()

    


class Profile_window(QtWidgets.QWidget):

    max_nr_layers = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Profile Window")
        self.Base_Layout = QtWidgets.QHBoxLayout(self)

        

        self.Layer_Box = QtWidgets.QWidget(self)
        self.Layer_Box.setMinimumSize(150, 200)
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

        self.Active_Layers = []
        self.Layer_Box.setLayout(QtWidgets.QVBoxLayout())
        self.Layer_selection = QtWidgets.QListWidget(self.Layer_Box)
      
        self.Layer_Box.layout().addWidget(self.Layer_selection)

        
        self.Layer_selection.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.add_Action = QtWidgets.QPushButton("Add Layer", self.Layer_Box)
        self.Layer_Box.layout().addWidget(self.add_Action)
        self.remove_Action = QtWidgets.QPushButton("Remove Layer", self.Layer_Box)
        self.Layer_Box.layout().addWidget(self.remove_Action)
        self.rename_Action = QtWidgets.QPushButton("Rename Layer", self.Layer_Box)
        self.Layer_Box.layout().addWidget(self.rename_Action)

        self.add_Action.clicked.connect(self.add_Layer)
        self.remove_Action.clicked.connect(self.remove_Layer)
        self.rename_Action.clicked.connect(self.rename_Layer)
        

    
    def fill_overview_box(self):
        self.Button_Box = QtWidgets.QWidget(self.overview_box)
        self.Button_Box.setFixedSize((CELL_SIZE+CELL_SPACING) * 4, (CELL_SIZE+CELL_SPACING) * 3)
        self.grid = QtWidgets.QGridLayout(self.Button_Box)
   
        self.grid.setVerticalSpacing(CELL_SPACING)
        self.grid.setHorizontalSpacing(CELL_SPACING)

        for i in range(3):
            for j in range(4):
                button = QtWidgets.QPushButton(f"Button {BUTTON_IDENTIFIERS[(i+1)*j]}", self.Button_Box)
                button.setFixedSize(CELL_SIZE, CELL_SIZE)

                self.grid.addWidget(button, i, j, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        self.Encoder_Box = QtWidgets.QWidget(self)
        self.Encoder_Box.setMinimumSize(20, 20)
        #self.Encoder_Box.setMaximumSize(300, 300)
        self.Encoder_Box.setStyleSheet(
            "background-color: rgb(240, 0, 0);"
            "border: 1px solid gray;"
            "border-radius: 5px;"
        )

        self.OverviewLayout.addWidget(self.Encoder_Box, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.OverviewLayout.addWidget(self.Button_Box, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

    def add_Layer(self):
        if self.Layer_selection.count() == self.max_nr_layers:
            return
        
        self.Layer_selection.addItem("Layer " + str(self.Layer_selection.count() + 1))

        self.Layer_selection.setCurrentRow(self.Layer_selection.count()-1)

        self.Active_Layers.append()

    def remove_Layer(self):
            if self.Layer_selection.count() == 1:
                return
            
            self.Layer_selection.takeItem(self.Layer_selection.currentRow())

    def rename_Layer(self):
            current_item = self.Layer_selection.currentItem()
            new_name, ok = QtWidgets.QInputDialog.getText(
                self, "Rename Layer", "Enter new profile name:", text=current_item.text()
                )
            
            if ok and new_name:
                current_item.setText(new_name)

    
    def load_profile(self):
        return