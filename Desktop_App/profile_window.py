from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon
CELL_SIZE = 180
CELL_SPACING = 10
BUTTON_IDENTIFIERS = ["7","8","9","●","4","5","6","■","1","2","3","0"]

class Macro_button(QtWidgets.QPushButton):

    def __init__(self, 
                 id: int,
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
        self.setText(identifier)
        self.id_index = identifier_index

        if function_type is not None:
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

class Macro_encoder(QtWidgets.QPushButton):
    def __init__(self, 
                id: int,
                identifier: str,
                identifier_index: int,
                function_type: str | None = None,
                cmd: str | None = None,
                parent= None, 
                ):
        
        super().__init__(parent)
        self.id = id
        self.identifier = identifier
        self.setText(identifier)
        self.id_index = identifier_index

        if function_type is not None:
            self.function = function_type

        if cmd is not None:
            self.cmd = cmd

        self.setFixedSize(120,120)

        self.setStyleSheet("""
            QPushButton {
                background-color: rgb(40, 120, 220);
                color: white;
                border: none;
                border-radius: 60px;
            }

            QPushButton:hover {
                background-color: rgb(60, 145, 245);
            }

            QPushButton:pressed {
                background-color: rgb(25, 90, 175);
            }
        """)



class Layer(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.Button_Box = QtWidgets.QWidget(self)
        self.Button_Box.setFixedSize((CELL_SIZE+CELL_SPACING) * 4, (CELL_SIZE+CELL_SPACING) * 3)
        self.grid = QtWidgets.QGridLayout(self.Button_Box)
    
        self.grid.setVerticalSpacing(CELL_SPACING)
        self.grid.setHorizontalSpacing(CELL_SPACING)

        for i in range(3):
            for j in range(4):
                button = Macro_button(id=5, identifier=BUTTON_IDENTIFIERS[i*4+j], identifier_index=(i*4+j), parent=self.Button_Box)
                button.setFixedSize(CELL_SIZE, CELL_SIZE)

                self.grid.addWidget(button, i, j, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        self.Encoder_Box = QtWidgets.QWidget(self)
        self.Encoder_Box_Layout = QtWidgets.QVBoxLayout(self.Encoder_Box)
        self.Encoder_Box.setFixedSize(350, 600)
        self.Encoder_Box.setObjectName("EncoderBox")
        
        self.Encoder_Box.setStyleSheet("""
            QWidget#EncoderBox {
                border: 3px solid orange;
                border-radius: 10px;
            }
        """)

        
        self.layout.addWidget(self.Button_Box, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.Encoder_Box, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Encoder_Box_Layout.addWidget(Macro_encoder(id=2,identifier="E1",identifier_index=1), alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

class Profile_window(QtWidgets.QWidget):

    max_nr_layers = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Profile Window")
        self.Base_Layout = QtWidgets.QVBoxLayout(self)

        self.Box_adjustment_box = QtWidgets.QWidget(self)
        self.Box_adjustment_box_layout = QtWidgets.QHBoxLayout(self.Box_adjustment_box)
        #self.Box_adjustment_box_layout.setContentsMargins(0, 0, 0, 0)
        #self.Box_adjustment_box_layout.setSpacing(0)
        self.Horizontal_spacer = QtWidgets.QWidget(self.Box_adjustment_box)
        self.Horizontal_spacer.setFixedWidth(1)
        


        self.Layer_Box = QtWidgets.QWidget(self.Box_adjustment_box)
        self.Layer_Box.setMinimumSize((CELL_SIZE+CELL_SPACING) * 4, 200)
        self.Layer_Box.setMaximumSize((CELL_SIZE+CELL_SPACING) * 4, 300)
        self.Layer_Box.setObjectName("LayerBox")

        self.Layer_Box.setStyleSheet("""
            QWidget#LayerBox {
                border: 3px solid orange;
                border-radius: 10px;
            }
        """)
        self.Box_adjustment_box_layout.addWidget(self.Layer_Box , alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Box_adjustment_box_layout.addWidget(self.Horizontal_spacer, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        
        
        self.overview_box = QtWidgets.QStackedWidget(self)

        self.Base_Layout.addWidget(self.Box_adjustment_box)
        self.Base_Layout.addWidget(self.overview_box)
        

        self.fill_Layer_box()

        self.Layer_selection.currentRowChanged.connect(self.display_layer)
        
        
        
    
    def display_layer(self):
        self.overview_box.setCurrentIndex(self.Layer_selection.currentRow())
        
        
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

        self.add_Layer()
        

    

    def add_Layer(self):
        if self.Layer_selection.count() == self.max_nr_layers:
            return
        
        self.Layer_selection.addItem("Layer " + str(self.Layer_selection.count() + 1))

        self.Layer_selection.setCurrentRow(self.Layer_selection.count()-1)
        
        self.overview_box.addWidget(Layer())

        

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