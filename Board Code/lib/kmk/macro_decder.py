from kmk.keys import KC
from kmk.modules.macros import Macros, Press, Release, Tap , Delay
from kmk.handlers.sequences import simple_key_sequence, send_string

def _decode_key_name(key_name):
    key_name = key_name.strip()

    if key_name.startswith("KC."):
        key_name = key_name[3:]

    return getattr(KC, key_name)


def _decode_combo(combo_text):
    parts = combo_text.split("+")
    key = _decode_key_name(parts[-1])

    for index in range(len(parts) - 2, -1, -1):
        modifier = _decode_key_name(parts[index])
        key = modifier(key)

    return key


def _decode_macro_part(part):
    if part.startswith("TEXT:"):
        return part[5:]

    if part.startswith("DELAY:"):
        return Delay(int(part[6:]))

    if part.startswith("TAP:"):
        return Tap(_decode_combo(part[4:]))

    if part.startswith("PRESS:"):
        return Press(_decode_combo(part[6:]))

    if part.startswith("RELEASE:"):
        return Release(_decode_combo(part[8:]))
    

    if part.startswith("KC."):
        return Tap(_decode_combo(part))

    return part


def _split_macro_target(part):
    if part.startswith("ON_PRESS:"):
        return "press", part[9:]

    if part.startswith("ON_HOLD:"):
        return "hold", part[8:]

    if part.startswith("ON_RELEASE:"):
        return "release", part[11:]

    return "press", part


def decode_macro(macro):
    press_cmd = []
    hold_cmd = []
    release_cmd = []

    if not macro:
        return KC.NO

    for part in macro.split("|"):
        part = part.strip()

        if not part:
            continue

        target, command = _split_macro_target(part)
        decoded = _decode_macro_part(command)

        if target == "hold":
            hold_cmd.append(decoded)
        elif target == "release":
            release_cmd.append(decoded)
        else:
            press_cmd.append(decoded)

    if not press_cmd and not hold_cmd and not release_cmd:
        return KC.NO

    return KC.MACRO(
        on_press=tuple(press_cmd) or None,
        on_hold=tuple(hold_cmd) or None,
        on_release=tuple(release_cmd) or None,
    )


def action_to_key(action):
    if action is None:
        return KC.NO

    if action.startswith("KC."):
        return getattr(KC, action[3:])

    if action.startswith("STRING:"):
        return send_string(action[7:])
    
    if action.startswith("MACRO:"):
        return (decode_macro(action[6:]))



    return KC.NO