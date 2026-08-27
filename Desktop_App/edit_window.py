from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QIcon, QPixmap
from database import Database
from macro_buttons import Macro_button, Macro_encoder
import subprocess
import sys


ICON_SIZE = 300


class Edit_window(QtWidgets.QSplitter):

    changes_saved = QtCore.Signal()

    def __init__(
        self,
        button: Macro_button,
        parent=None,
        database: Database | None = None,
    ):
        super().__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowType.Window, True)
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)

        self.database = database if database is not None else Database()

        self.setWindowTitle(f"Edit button: {button.identifier}")
        self.temp_cmd = getattr(button, "cmd", None)
        self.temp_function = getattr(button, "function", None)
        self.temp_icon_data = getattr(button, "icon_data", None)
        self.temp_icon = QIcon()
        self.temp_icon_path = ""
        self.original_button = button

        self.setOrientation(QtCore.Qt.Vertical)
        self.setChildrenCollapsible(False)

        self.horizontal_splitter = QtWidgets.QSplitter(
            orientation=QtCore.Qt.Horizontal, parent=self
        )
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

        self.macro_button.setFixedSize(200, 50)
        self.launch_button.setFixedSize(200, 50)
        self.url_button.setFixedSize(200, 50)
        self.default_button.setFixedSize(200, 50)
        self.cmd_button.setFixedSize(200, 50)

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
        Load_action = QtGui.QAction("Load From Library", self)
        Cancel_action = QtGui.QAction("Cancel", self)
        Reset_action = QtGui.QAction("Reset", self)

        self.save_button = QtWidgets.QToolButton()
        self.load_button = QtWidgets.QToolButton()
        self.cancel_button = QtWidgets.QToolButton()
        self.reset_button = QtWidgets.QToolButton()

        self.save_button.setStyleSheet(
                                        """
                            QToolButton {
                                background-color: palette(button);
                                color: palette(button-text);
                                border: 2px solid rgb(255, 140, 0);
                            }
                            """)
        

        self.save_button.setFixedSize(200, 50)
        self.load_button.setFixedSize(200, 50)
        self.cancel_button.setFixedSize(200, 50)
        self.reset_button.setFixedSize(200, 50)

        self.save_button.setDefaultAction(Save_action)
        self.load_button.setDefaultAction(Load_action)
        self.cancel_button.setDefaultAction(Cancel_action)
        self.reset_button.setDefaultAction(Reset_action)

        Save_action.triggered.connect(self.save_func)
        Load_action.triggered.connect(self.load_from_func)
        Cancel_action.triggered.connect(self.cancel_func)
        Reset_action.triggered.connect(self.reset_func)

        self.menu_layout.addWidget(self.save_button)
        self.menu_layout.addWidget(self.load_button)
        self.menu_layout.addWidget(self.reset_button)
        self.menu_layout.addWidget(self.cancel_button)

        self.addWidget(self.menu)

    def icon_menu_init(self):
        self.icon_panel = QtWidgets.QWidget(self.horizontal_splitter)
        self.icon_layout = QtWidgets.QHBoxLayout(self.icon_panel)

        self.backround_menu = QtWidgets.QGroupBox("Icon Backround")
        self.color_selection = QtWidgets.QGroupBox("Select fill in color")
        self.convert_selection = QtWidgets.QGroupBox("Select color conversion")

        backround_menu_layout = QtWidgets.QVBoxLayout(self.backround_menu)
        color_selection_layout = QtWidgets.QVBoxLayout(self.color_selection)
        convert_selection_layout = QtWidgets.QVBoxLayout(self.convert_selection)



        self.FillTransperent = QtWidgets.QCheckBox("Fill Transperent Background")
        self.FillColored = QtWidgets.QCheckBox("Replace Black or White")

        self.Apply_button = QtWidgets.QPushButton("Apply")
        
        self.whiteCheck = QtWidgets.QCheckBox("White")
        self.blackCheck = QtWidgets.QCheckBox("Black")

        self.w2bCheck = QtWidgets.QCheckBox("White to Black")
        self.b2wCheck = QtWidgets.QCheckBox("Black to White")
        
        self.number_box = QtWidgets.QSpinBox()
        self.number_box.setRange(0, 100)
        self.number_box.setValue(10)
        self.number_box.setSingleStep(1)
        self.number_box.setSuffix(" %")




        backround_menu_layout.addWidget(self.FillTransperent)
        backround_menu_layout.addWidget(self.FillColored)
        backround_menu_layout.addWidget(self.color_selection)
        backround_menu_layout.addWidget(self.convert_selection)
        backround_menu_layout.addWidget(self.Apply_button)

        color_selection_layout.addWidget(self.whiteCheck)
        color_selection_layout.addWidget(self.blackCheck)

        convert_selection_layout.addWidget(self.w2bCheck)
        convert_selection_layout.addWidget(self.b2wCheck)
        convert_selection_layout.addWidget(self.number_box)
       


        self.convert_selection.hide()
        self.color_selection.hide()

        self.FillTransperent.checkStateChanged.connect(lambda checked: self.toggle_check(state=checked, button="Trans"))
        self.FillColored.checkStateChanged.connect(lambda checked: self.toggle_check(state=checked, button="Color"))

        self.whiteCheck.checkStateChanged.connect(lambda checked: self.toggle_check(state=checked, button="White"))
        self.blackCheck.checkStateChanged.connect(lambda checked: self.toggle_check(state=checked, button="Black"))

        self.w2bCheck.checkStateChanged.connect(lambda checked: self.toggle_check(state=checked, button="W2B"))
        self.b2wCheck.checkStateChanged.connect(lambda checked: self.toggle_check(state=checked, button="B2W"))

        self.Apply_button.clicked.connect(self.apply_filter)


        self.button = QtWidgets.QPushButton(self.icon_panel)
        self.set_temp_icon(self.temp_icon_data)
        self.button.setIconSize(QtCore.QSize(ICON_SIZE - 10, ICON_SIZE - 10))
        self.button.setFixedSize(ICON_SIZE, ICON_SIZE)

        self.button.clicked.connect(self.select_icon)


        self.icon_layout.addWidget(
            self.button,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        self.icon_layout.addWidget(
                    self.backround_menu,
                    alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
                )

        self.horizontal_splitter.addWidget(self.icon_panel)

    

    # -------------------------------FUNCTION BUTTONS-------------------------------------------------

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

        keypad = bool(modifiers & QtCore.Qt.KeyboardModifier.KeypadModifier)

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
            key_name = sequence.toString(QtGui.QKeySequence.SequenceFormat.NativeText)
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
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select an image",
            "",
            "Programs (*.exe *.com *.scr)",
        )

        if file_path == "":
            return
        
        else:
            self.temp_function = "LAUNCH:"
            self.temp_cmd = file_path
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
            self, "Edit Macro", MACRO_GUIDE + "\n\nEnter Macro logic:", text=current_cmd
        )

        if ok and new_cmd:
            self.temp_function = "MACRO:"
            self.temp_cmd = new_cmd
            self.set_active_function()

    # --------------------------------------MENU BUTTONS--------------------------------------------------

    def save_func(self):
        self.original_button.set_functionality(self.temp_function, self.temp_cmd)
        self.original_button.set_icon(self.temp_icon_data, 0.5)
        self.changes_saved.emit()
        self.close()

    def cancel_func(self):
        self.close()

    def reset_func(self):
        self.temp_function = None
        self.temp_cmd = None
        self.set_temp_icon(None)
        self.set_active_function()

    

    def load_from_func(self):
        available_buttons = self.database.list_configured_buttons()

        if not available_buttons:
            QtWidgets.QMessageBox.information(
                self,
                "No configured buttons",
                "No configured macro buttons have been saved in any profile yet.",
            )
            return

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Copy From Existing Button")
        dialog.resize(750, 450)

        layout = QtWidgets.QVBoxLayout(dialog)
        instructions = QtWidgets.QLabel(
            "Select a configured button to copy its command and icon."
        )
        button_list = QtWidgets.QListWidget(dialog)

        for button_data in available_buttons:
            function_type = button_data["function_type"] or ""
            command = button_data["command"] or ""
            action_text = (function_type + command).replace("\n", " ").strip()

            if not action_text:
                action_text = "[icon only]"
            elif len(action_text) > 90:
                action_text = action_text[:87] + "..."

            icon_marker = "  [icon]" if button_data["has_icon"] else ""
            label = (
                f'{button_data["profile_name"]} / '
                f'{button_data["layer_name"]} / '
                f'Button {button_data["button_index"] + 1} — '
                f"{action_text}{icon_marker}"
            )

            item = QtWidgets.QListWidgetItem(label)
            item.setData(
                QtCore.Qt.ItemDataRole.UserRole,
                button_data["id"],
            )
            button_list.addItem(item)

        button_list.setCurrentRow(0)

        dialog_buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel,
            parent=dialog,
        )
        dialog_buttons.accepted.connect(dialog.accept)
        dialog_buttons.rejected.connect(dialog.reject)
        button_list.itemDoubleClicked.connect(lambda item: dialog.accept())

        layout.addWidget(instructions)
        layout.addWidget(button_list)
        layout.addWidget(dialog_buttons)

        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return

        selected_item = button_list.currentItem()
        if selected_item is None:
            return

        button_id = selected_item.data(QtCore.Qt.ItemDataRole.UserRole)
        loaded_button = self.database.load_button(button_id)

        if loaded_button is None:
            QtWidgets.QMessageBox.warning(
                self,
                "Button no longer available",
                "The selected button was deleted before it could be loaded.",
            )
            return

        self.temp_function = loaded_button["function_type"]
        self.temp_cmd = loaded_button["command"]
        self.set_temp_icon(loaded_button["icon_data"])
        self.set_active_function()

    # ---------------------------------------------------------Icon button---------------------------------------------------------------------------------------------------

    

    def toggle_check(self, state : QtCore.Qt.CheckState, button : str):

        if state == QtCore.Qt.CheckState.Checked:
            if button == "Trans":
                print("Trans checked")
                self.color_selection.show()
                self.FillColored.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.b2wCheck.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.w2bCheck.setCheckState(QtCore.Qt.CheckState.Unchecked)

            elif button == "Color":
                print("Color checked")
                self.convert_selection.show()
                self.FillTransperent.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.blackCheck.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.whiteCheck.setCheckState(QtCore.Qt.CheckState.Unchecked)

            elif button == "White":
                self.blackCheck.setCheckState(QtCore.Qt.CheckState.Unchecked)

            elif button == "Black":
                self.whiteCheck.setCheckState(QtCore.Qt.CheckState.Unchecked)

            elif button == "W2B":
                self.b2wCheck.setCheckState(QtCore.Qt.CheckState.Unchecked)

            elif button == "B2W":
                self.w2bCheck.setCheckState(QtCore.Qt.CheckState.Unchecked)

        else:
            if button == "Trans":
                self.color_selection.hide()

            elif button == "Color":
                self.convert_selection.hide()

        return

    def apply_filter(self):
        self.set_temp_icon(self.convert_icon())

    def set_temp_icon(self, image_data: bytes | None) -> None:
            self.temp_icon_data = image_data
    
            if image_data is None:
                self.temp_icon = QIcon()
                self.button.setIcon(self.temp_icon)
                return
    
            pixmap = QPixmap()
    
            if not pixmap.loadFromData(image_data, "BMP"):
                raise ValueError("Invalid BMP image data")
    
            preview_size = QtCore.QSize(ICON_SIZE - 10, ICON_SIZE - 10)
    
            preview_pixmap = pixmap.scaled(
                preview_size,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
    
            self.temp_icon = QIcon(preview_pixmap)
            self.button.setIcon(self.temp_icon)


    def select_icon(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select an image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.ico *.webp)",
        )

        if file_path == "":
            return

        self.temp_icon_path = file_path
        # image_blob = self.convert_icon()
        # self.set_temp_icon(image_blob)
        self.apply_filter()


    def convert_icon(self):
      size = 55
      keep_aspect = False

      size_text = f"{size}x{size}"
      resize = size_text if keep_aspect else size_text + "!"

      if self.temp_icon_path == "" and self.temp_icon_data is None:
          return None

      elif self.temp_icon_path == "": #Prioritize reading from path if avilable
        path = "-"

      else:
          path = str(self.temp_icon_path)

    
      command = [
     "magick",
     path,
     "-resize",
     resize,
     "-colors",
     "16",
     "-depth",
     "4",
     "-compress",
     "none",
     "BMP3:-",  # Write BMP bytes to stdout
     ]

      if self.FillTransperent.checkState() == QtCore.Qt.CheckState.Checked and (self.whiteCheck.checkState() == QtCore.Qt.CheckState.Checked or self.blackCheck.checkState() == QtCore.Qt.CheckState.Checked):
    
          if self.whiteCheck.checkState() == QtCore.Qt.CheckState.Checked:
              Color = "white"
          else:
              Color = "black"

          command[2:2] = [
                "-background",
                Color,
                "-alpha",
                "remove",
            ]
      
      elif self.FillColored.checkState() == QtCore.Qt.CheckState.Checked and (self.w2bCheck.checkState() == QtCore.Qt.CheckState.Checked or self.b2wCheck.checkState() == QtCore.Qt.CheckState.Checked):
          if self.w2bCheck.checkState() == QtCore.Qt.CheckState.Checked:
              From = "white"
              To = "black"
          else:
              From = "black"
              To = "white"

          fuzz = str(self.number_box.value()) + "%"

          command[2:2] = [
              "-fuzz",
              fuzz,
              "-fill",
              To,
              "-opaque",
              From,


          ]

      result = subprocess.run(
     command,
     input= self.temp_icon_data,
     stdout=subprocess.PIPE,
     stderr=subprocess.PIPE,
     check=True,
     creationflags=(
        subprocess.CREATE_NO_WINDOW
        if sys.platform == "win32"
        else 0
    ),
     )

      return result.stdout
