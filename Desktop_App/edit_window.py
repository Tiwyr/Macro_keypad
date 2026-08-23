from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QIcon, QPainter, QPixmap
from macro_buttons import Macro_button, Macro_encoder

ICON_SIZE = 300

class Edit_window(QtWidgets.QSplitter):

    def __init__(self, button: Macro_button, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"Edit button: {button.identifier}")
        try:
            self.temp_cmd = button.cmd
        except:
             self.temp_cmd = None


        try:
            self.temp_function = button.function
        except:
             self.temp_function = None


        try:
            icon =  button.icon()
            self.set_temp_icon(icon=icon)

        except:
             self.temp_icon = None

        self.original_button = button
        
        self.setOrientation(QtCore.Qt.Vertical)
        self.setChildrenCollapsible(False)



        self.horizontal_splitter = QtWidgets.QSplitter(orientation=QtCore.Qt.Horizontal, parent=self)
        self.horizontal_splitter.setChildrenCollapsible(False)



        
        self.function_menu_init()
        self.icon_menu_init()

        self.horizontal_splitter.setStretchFactor(0, 1)
        self.horizontal_splitter.setStretchFactor(1, 1)
        self.horizontal_splitter.setSizes([1, 1])

        self.menu_init()


        self.set_active_function()


    def function_menu_init(self):
        self.function_toolbar = QtWidgets.QWidget(self.horizontal_splitter)
        self.ft_layout = QtWidgets.QVBoxLayout(self.function_toolbar)
        
        Macro_action = QtGui.QAction("Macro", self)
        Launch_action = QtGui.QAction("Launch", self)
        URL_action = QtGui.QAction("URL", self)
        CMD_action = QtGui.QAction("CMD", self)
        Default_action = QtGui.QAction("Default", self)
        


        self.macro_button = QtWidgets.QToolButton()
        self.launch_button = QtWidgets.QToolButton()
        self.url_button = QtWidgets.QToolButton()
        self.default_button = QtWidgets.QToolButton()
        self.cmd_button = QtWidgets.QToolButton()

        self.macro_button.setFixedSize(200,50)
        self.launch_button.setFixedSize(200,50)
        self.url_button.setFixedSize(200,50)
        self.default_button.setFixedSize(200,50)
        self.cmd_button.setFixedSize(200,50)

        self.macro_button.setDefaultAction(Macro_action)
        self.launch_button.setDefaultAction(Launch_action)
        self.url_button.setDefaultAction(URL_action)
        self.default_button.setDefaultAction(Default_action)
        self.cmd_button.setDefaultAction(CMD_action)


        URL_action.triggered.connect(self.edit_URL)
        Macro_action.triggered.connect(self.edit_MACRO)
        Launch_action.triggered.connect(self.edit_Launch)
        CMD_action.triggered.connect(self.edit_CMD)
        Default_action.triggered.connect(self.edit_default)
        
        self.ft_layout.addStretch(1)
        self.ft_layout.addWidget(
            self.macro_button,
            alignment=QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        self.ft_layout.addWidget(
            self.launch_button,
            alignment=QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        self.ft_layout.addWidget(
            self.url_button,
            alignment=QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        self.ft_layout.addWidget(
                    self.cmd_button,
                    alignment=QtCore.Qt.AlignmentFlag.AlignHCenter,
                )
        self.ft_layout.addWidget(
            self.default_button,
            alignment=QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        self.ft_layout.addStretch(1)

        self.horizontal_splitter.addWidget(self.function_toolbar)


    def menu_init(self):
            self.menu = QtWidgets.QWidget(self)
            self.menu_layout = QtWidgets.QHBoxLayout(self.menu)
            
            Save_action = QtGui.QAction("Save", self)
            Save_To_action = QtGui.QAction("Save To Library", self)
            Load_action = QtGui.QAction("Load From Library", self)
            Cancel_action = QtGui.QAction("Cancel", self)
            Reset_action = QtGui.QAction("Reset", self)
            
    
    
            self.save_button = QtWidgets.QToolButton()
            self.save_to_button = QtWidgets.QToolButton()
            self.load_button = QtWidgets.QToolButton()
            self.cancel_button = QtWidgets.QToolButton()
            self.reset_button = QtWidgets.QToolButton()
    
            self.save_button.setFixedSize(200,50)
            self.save_to_button.setFixedSize(200,50)
            self.load_button.setFixedSize(200,50)
            self.cancel_button.setFixedSize(200,50)
            self.reset_button.setFixedSize(200,50)
    
            self.save_button.setDefaultAction(Save_action)
            self.save_to_button.setDefaultAction(Save_To_action)
            self.load_button.setDefaultAction(Load_action)
            self.cancel_button.setDefaultAction(Cancel_action)
            self.reset_button.setDefaultAction(Reset_action)
            
            
            self.menu_layout.addWidget(self.save_button)
            self.menu_layout.addWidget(self.save_to_button)
            self.menu_layout.addWidget(self.load_button)
            self.menu_layout.addWidget(self.cancel_button)
            self.menu_layout.addWidget(self.reset_button)
           
            
            
            self.addWidget(self.menu)

    def icon_menu_init(self):
        self.icon_panel = QtWidgets.QWidget(self.horizontal_splitter)
        self.icon_layout = QtWidgets.QVBoxLayout(self.icon_panel)

        button = QtWidgets.QPushButton(self.icon_panel)
        button.setIcon(self.temp_icon)
        button.setIconSize(QtCore.QSize(ICON_SIZE - 10, ICON_SIZE - 10))
        button.setFixedSize(ICON_SIZE, ICON_SIZE)

        self.icon_layout.addWidget(
            button,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        self.horizontal_splitter.addWidget(self.icon_panel)

    def set_temp_icon(self, icon : QIcon):
         target_size = QtCore.QSize(ICON_SIZE - 10, ICON_SIZE - 10)
         pixmap = icon.pixmap(target_size)
         scaled_pixmap = pixmap.scaled(
                target_size,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
         self.temp_icon = QtGui.QIcon(scaled_pixmap)


    def set_active_function(self):

        active_button_style = """
            QToolButton {
                background-color: rgb(0, 120, 215);
                color: white;
                border-radius: 5px;
            }

            QToolButton:hover {
                background-color: rgb(20, 140, 235);
            }

            QToolButton:pressed {
                background-color: rgb(0, 80, 160);
            }
        """

        self.url_button.setStyleSheet("")
        self.launch_button.setStyleSheet("")
        self.cmd_button.setStyleSheet("")
        self.macro_button.setStyleSheet("")
        self.default_button.setStyleSheet("")

        if self.temp_function == None:
             return
        elif self.temp_function == "URL:":
             self.url_button.setStyleSheet(active_button_style)

        elif self.temp_function == "LAUNCH:":
             self.launch_button.setStyleSheet(active_button_style)

        elif self.temp_function == "CMD:":
                     self.cmd_button.setStyleSheet(active_button_style)

        elif self.temp_function == "MACRO:":
                    self.macro_button.setStyleSheet(active_button_style)

        elif self.temp_function in ("", " "):
                    self.default_button.setStyleSheet(active_button_style)


    @staticmethod
    def _qt_value(value):
         """Return the numeric value of a Qt enum on different PySide6 versions."""
         return value.value if hasattr(value, "value") else int(value)


    @classmethod
    def _key_sequence_to_kmk(cls, sequence: QtGui.QKeySequence) -> str:
         """Convert one recorded Qt shortcut into a nested KMK KC expression."""
         if sequence.isEmpty():
              raise ValueError("Record a key or key combination first.")

         combination = sequence[0]
         key = combination.key()
         modifiers = combination.keyboardModifiers()
         key_value = cls._qt_value(key)

         key_map = {
              QtCore.Qt.Key.Key_Escape: "KC.ESC",
              QtCore.Qt.Key.Key_Tab: "KC.TAB",
              QtCore.Qt.Key.Key_Backspace: "KC.BSPC",
              QtCore.Qt.Key.Key_Return: "KC.ENTER",
              QtCore.Qt.Key.Key_Enter: "KC.ENTER",
              QtCore.Qt.Key.Key_Space: "KC.SPACE",
              QtCore.Qt.Key.Key_Insert: "KC.INS",
              QtCore.Qt.Key.Key_Delete: "KC.DEL",
              QtCore.Qt.Key.Key_Home: "KC.HOME",
              QtCore.Qt.Key.Key_End: "KC.END",
              QtCore.Qt.Key.Key_PageUp: "KC.PGUP",
              QtCore.Qt.Key.Key_PageDown: "KC.PGDN",
              QtCore.Qt.Key.Key_Left: "KC.LEFT",
              QtCore.Qt.Key.Key_Right: "KC.RIGHT",
              QtCore.Qt.Key.Key_Up: "KC.UP",
              QtCore.Qt.Key.Key_Down: "KC.DOWN",
              QtCore.Qt.Key.Key_CapsLock: "KC.CAPS",
              QtCore.Qt.Key.Key_NumLock: "KC.NUMLOCK",
              QtCore.Qt.Key.Key_ScrollLock: "KC.SCROLLLOCK",
              QtCore.Qt.Key.Key_Print: "KC.PSCREEN",
              QtCore.Qt.Key.Key_Pause: "KC.PAUSE",
              QtCore.Qt.Key.Key_Minus: "KC.MINS",
              QtCore.Qt.Key.Key_Equal: "KC.EQL",
              QtCore.Qt.Key.Key_BracketLeft: "KC.LBRC",
              QtCore.Qt.Key.Key_BracketRight: "KC.RBRC",
              QtCore.Qt.Key.Key_Backslash: "KC.BSLS",
              QtCore.Qt.Key.Key_Semicolon: "KC.SCLN",
              QtCore.Qt.Key.Key_Apostrophe: "KC.QUOT",
              QtCore.Qt.Key.Key_QuoteLeft: "KC.GRV",
              QtCore.Qt.Key.Key_Comma: "KC.COMM",
              QtCore.Qt.Key.Key_Period: "KC.DOT",
              QtCore.Qt.Key.Key_Slash: "KC.SLSH",
         }

         keypad = bool(
              modifiers & QtCore.Qt.KeyboardModifier.KeypadModifier
         )

         zero = cls._qt_value(QtCore.Qt.Key.Key_0)
         nine = cls._qt_value(QtCore.Qt.Key.Key_9)
         a_key = cls._qt_value(QtCore.Qt.Key.Key_A)
         z_key = cls._qt_value(QtCore.Qt.Key.Key_Z)
         f1 = cls._qt_value(QtCore.Qt.Key.Key_F1)
         f24 = cls._qt_value(QtCore.Qt.Key.Key_F24)

         if zero <= key_value <= nine:
              digit = chr(key_value)
              base_key = f"KC.KP_{digit}" if keypad else f"KC.N{digit}"
         elif a_key <= key_value <= z_key:
              base_key = f"KC.{chr(key_value)}"
         elif f1 <= key_value <= f24:
              base_key = f"KC.F{key_value - f1 + 1}"
         elif keypad and key == QtCore.Qt.Key.Key_Enter:
              base_key = "KC.KP_ENTER"
         elif keypad and key == QtCore.Qt.Key.Key_Plus:
              base_key = "KC.KP_PLUS"
         elif keypad and key == QtCore.Qt.Key.Key_Minus:
              base_key = "KC.KP_MINUS"
         elif keypad and key == QtCore.Qt.Key.Key_Asterisk:
              base_key = "KC.KP_ASTERISK"
         elif keypad and key == QtCore.Qt.Key.Key_Slash:
              base_key = "KC.KP_SLASH"
         elif keypad and key in (
              QtCore.Qt.Key.Key_Period,
              QtCore.Qt.Key.Key_Comma,
         ):
              base_key = "KC.KP_DOT"
         else:
              base_key = key_map.get(key)

         if base_key is None:
              key_name = sequence.toString(
                   QtGui.QKeySequence.SequenceFormat.NativeText
              )
              raise ValueError(f"The recorded key is not supported yet: {key_name}")

         modifier_keys = []
         if modifiers & QtCore.Qt.KeyboardModifier.ControlModifier:
              modifier_keys.append("KC.LCTRL")
         if modifiers & QtCore.Qt.KeyboardModifier.AltModifier:
              modifier_keys.append("KC.LALT")
         if modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier:
              modifier_keys.append("KC.LSHIFT")
         if modifiers & QtCore.Qt.KeyboardModifier.MetaModifier:
              modifier_keys.append("KC.LGUI")

         command = base_key
         for modifier in reversed(modifier_keys):
              command = f"{modifier}({command})"

         return command


    def edit_default(self):
         dialog = QtWidgets.QDialog(self)
         dialog.setWindowTitle("Record key")

         layout = QtWidgets.QVBoxLayout(dialog)
         instructions = QtWidgets.QLabel(
              "Press one key or shortcut combination.\n"
              "For example: A, F16, Ctrl+C, or Ctrl+Shift+S."
         )
         key_recorder = QtWidgets.QKeySequenceEdit(dialog)
         key_recorder.setMaximumSequenceLength(1)
         key_recorder.setClearButtonEnabled(True)

         buttons = QtWidgets.QDialogButtonBox(
              QtWidgets.QDialogButtonBox.StandardButton.Ok
              | QtWidgets.QDialogButtonBox.StandardButton.Cancel,
              parent=dialog,
         )
         buttons.accepted.connect(dialog.accept)
         buttons.rejected.connect(dialog.reject)

         layout.addWidget(instructions)
         layout.addWidget(key_recorder)
         layout.addWidget(buttons)

         if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
              return

         try:
              new_cmd = self._key_sequence_to_kmk(key_recorder.keySequence())
         except ValueError as error:
              QtWidgets.QMessageBox.warning(self, "Unsupported key", str(error))
              return

         self.temp_function = ""
         self.temp_cmd = new_cmd
         self.set_active_function()



    def edit_URL(self):
          if self.temp_function == "URL:":
                current_url = self.temp_cmd
          else:
                current_url = ""

          new_url, ok = QtWidgets.QInputDialog.getText(
                          self, "Edit URL", "Enter a URL:", text=current_url
                          )

          if ok and new_url:
                self.temp_function = "URL:"
                self.temp_cmd = new_url
                self.set_active_function()

    def edit_Launch(self):
              if self.temp_function == "LAUNCH:":
                    current_path = self.temp_cmd
              else:
                    current_path = ""
    
              new_path, ok = QtWidgets.QInputDialog.getText(
                              self, "Edit Launch", "Enter the path to the program:", text=current_path
                              )
    
              if ok and new_path:
                    self.temp_function = "LAUNCH:"
                    self.temp_cmd = new_path
                    self.set_active_function()


    def edit_CMD(self):
              if self.temp_function == "CMD:":
                    current_cmd = self.temp_cmd
              else:
                    current_cmd = ""
    
              new_cmd, ok = QtWidgets.QInputDialog.getText(
                              self, "Edit CMD", "Enter a Powershell command:", text=current_cmd
                              )
    
              if ok and new_cmd:
                    self.temp_function = "CMD:"
                    self.temp_cmd = new_cmd
                    self.set_active_function()

    def edit_MACRO(self):

                  MACRO_GUIDE = """
                    Construct the macro using actions separated by |.

                    Action types:
                    TEXT:text          Type text
                    TAP:KC.A           Press and release a key
                    PRESS:KC.A         Hold a key down
                    RELEASE:KC.A       Release a held key
                    DELAY:100          Wait in milliseconds

                    Optional event prefixes:
                    ON_PRESS:          Run when the button is pressed
                    ON_HOLD:           Run while the button is held
                    ON_RELEASE:        Run when the button is released

                    If no event is specified, ON_PRESS is used.

                    Shortcut examples:
                    TAP:KC.LCTRL(KC.C)
                    TAP:KC.LCTRL+KC.C

                    Complete example:
                    TEXT:start|ON_HOLD:TAP:KC.A|ON_HOLD:DELAY:100|ON_RELEASE:TEXT:end

                    Do not include MACRO: at the beginning.
                    """
                  
                  if self.temp_function == "MACRO:":
                        current_cmd = self.temp_cmd
                  else:
                        current_cmd = ""
        
                  new_cmd, ok = QtWidgets.QInputDialog.getText(
                                  self, "Edit Macro",MACRO_GUIDE + "\n\nEnter Macro logic:", text=current_cmd
                                  )
        
                  if ok and new_cmd:
                        self.temp_function = "MACRO:"
                        self.temp_cmd = new_cmd
                        self.set_active_function()
