from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon, QPainter, QPixmap


class Macro_button(QtWidgets.QPushButton):

    def __init__(self,
                 size: int,  
                 id: int,
                 identifier: str,
                 identifier_index: int,
                 function_type: str | None = None,
                 cmd: str | None = None,
                 icon: QPixmap | None = None,
                 parent= None, 
                 ):
        
        super().__init__(parent)
        self.id = id
        self.identifier = identifier
        self.id_index = identifier_index
        self.size_ = size


        self.label = QtWidgets.QLabel(identifier,self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedSize(self.size_,self.size_)

        font = self.font()
        font.setBold(True)
        if self.identifier == "●":
            font.setPointSize(80)
        else:
            font.setPointSize(40)
        self.setFont(font)

       

        if function_type is not None:
            self.function = function_type

        if cmd is not None:
            self.cmd = cmd

        if icon is not None:
            self.set_icon(icon, 0.5)


    def set_functionality(self, function_type: str,cmd: str):
        self.function = function_type
        self.cmd = cmd

 

    def set_icon(self, pixmap: QPixmap, opacity: float) -> None:
        if pixmap.isNull():
            self.remove_icon()
            return

        opacity = max(0.0, min(1.0, opacity))
        target_size = QtCore.QSize(self.size_ - 10, self.size_ - 10)
        scaled_pixmap = pixmap.scaled(
            target_size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

        transparent_pixmap = QPixmap(scaled_pixmap.size())
        transparent_pixmap.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QPainter(transparent_pixmap)
        painter.setOpacity(opacity)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        self.setIcon(QIcon(transparent_pixmap))
        self.setIconSize(target_size)

    def remove_icon(self):
        self.setIcon(QPixmap())

    def show_identifier(self):
        self.label.show()

    def hide_identifier(self):
        self.label.hide()

    

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
                background-color: rgb(45, 45, 45);
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

        font = self.font()
        font.setBold(True)
        font.setPointSize(30)
        self.setFont(font)