### Desktop App Guide

## Build App
Open PS in Macro_Keypad/Desktop_App and run:
```
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onedir --windowed --name MacroKeypad --icon="images\app_icon.ico" --add-data="images\app_icon.ico:images" app.py
```

