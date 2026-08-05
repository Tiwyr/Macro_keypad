# Custom made macro keyboard
This macro keyboard have 12 individual programmable buttons, one layer button with support up to 4 layers and 3 encoders. Personally I use the encoders to adjust the 3 audio channels in SteelSeries GG Sonar, explaining the encoder logos. However the function is programmable in the desktop app and the logos are easily modifyable in either the STEP file or F3D file for personalization. 

The afformentionedd desktop app serves as both a GUI used to program functions to the buttons and also a backend command executer for some programmable functions that require windows acess. 
<p align="center">
  <img src="images/20260804_154111.jpg" alt="Macro keypad back" width="45%">
  <img src="images/20260804_154054.jpg" alt="Macro keypad front" width="45%">
</p>
<img src="images/0F5D317F-E71B-4517-BB42-9381734777E2.png" alt="Macro keypad" width="800">

## Firmware configuration

### Using the `MACRO:` wrapper

Use the `MACRO:` wrapper when one button should perform several actions, type text, include a delay, or behave differently when pressed, held, and released. Separate each part of a macro with `|`.

The supported macro commands are:

- `TEXT:` types text.
- `TAP:` presses and immediately releases a key or shortcut.
- `PRESS:` holds a key down.
- `RELEASE:` releases a held key.
- `DELAY:` waits for the specified number of milliseconds.

For example, this macro copies, waits 100 milliseconds, and then pastes:

```python
"MACRO:TAP:KC.LCTRL(KC.C)|DELAY:100|TAP:KC.LCTRL(KC.V)"
```

A key action without an explicit event prefix runs when the button is pressed. The optional event prefixes are:

- `ON_PRESS:` runs when the button is pressed.
- `ON_HOLD:` runs while the button is held.
- `ON_RELEASE:` runs when the button is released.

For example:

```python
"MACRO:ON_PRESS:TEXT:start|ON_HOLD:TAP:KC.A|ON_HOLD:DELAY:100|ON_RELEASE:TEXT:end"
```

Simple shortcuts do not require the macro wrapper and can be assigned directly:

```python
"KC.LCTRL(KC.C)"
```
