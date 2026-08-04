from kmk.keys import KC
from kmk.modules.macros import Macros, Press, Release, Tap , Delay
from kmk.handlers.sequences import simple_key_sequence, send_string
import kmk.extensions.keymap_extras.keymap_swe as swe_keymap


def _decode_key_name(key_name):
    key_name = key_name.strip()

    if key_name.startswith("KC."):
        key_name = key_name[3:]

    return getattr(KC, key_name)


def _decode_key_expression(expression):
    """Decode KC.A or nested expressions such as KC.LCTRL(KC.A)."""
    expression = expression.strip()
    opening_parenthesis = expression.find("(")

    if opening_parenthesis == -1:
        return _decode_key_name(expression)

    if not expression.endswith(")"):
        raise ValueError("Invalid key expression: " + expression)

    wrapper = _decode_key_name(expression[:opening_parenthesis])
    inner_expression = expression[opening_parenthesis + 1:-1].strip()

    if not inner_expression:
        raise ValueError("Empty key expression: " + expression)

    return wrapper(_decode_key_expression(inner_expression))


def _decode_combo(combo_text):
    parts = combo_text.split("+")
    key = _decode_key_expression(parts[-1])

    for index in range(len(parts) - 2, -1, -1):
        modifier = _decode_key_expression(parts[index])
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

def send_string_sv(text):
    seq = []

    for char in text:
        if char in swe_keymap.SV_CHARS:
            seq.append(swe_keymap.SV_CHARS[char])
        elif char.isupper():
            seq.append(KC.LSHIFT(getattr(KC, char)))
        elif char == " ":
            seq.append(KC.SPACE)
        else:
            seq.append(getattr(KC, char.upper()))

    return simple_key_sequence(seq)


def convert_string_sv(text):
    seq = []
    tap_seq = []

    for char in text:
        if char in swe_keymap.SV_CHARS:
            seq.append(swe_keymap.SV_CHARS[char])
        elif char.isupper():
            seq.append(KC.LSHIFT(getattr(KC, char)))
        elif char == " ":
            seq.append(KC.SPACE)
        else:
            seq.append(getattr(KC, char.upper()))

    for char in seq:
        tap_seq.append(Tap(char))

    return tap_seq



def cmd_args(cmd):
    cmd = convert_string_sv(cmd)

    return KC.MACRO(
        Tap(KC.LGUI(KC.R)),
        Delay(300),
        "cmd",
        Tap(KC.ENTER),
        Delay(300),
        *cmd,
        Tap(KC.ENTER),
    )

def launch_app(path):
    path = convert_string_sv(path)

    return KC.MACRO(
        Tap(KC.LGUI(KC.R)),
        Delay(300),
        *path,
        Tap(KC.ENTER),
    )

def open_url(url):
    url = url.strip()
    url = convert_string_sv(url)

    return KC.MACRO(
        Tap(KC.LGUI(KC.R)),
        Delay(300),
        "Chrome",
        Tap(KC.ENTER),
        Delay(300),
        *url,
        Tap(KC.ENTER),
    )
    
def action_to_key(action, naitive_cmd):
    if action is None:
        return KC.NO

    if action.startswith("KC."):
        return _decode_key_expression(action)

    if action.startswith("STRING:"):
        return send_string_sv(action[7:])
    
    if action.startswith("MACRO:"):
        return (decode_macro(action[6:]))
    
    if action.startswith("CMD:"):
        return (cmd_args(action[4:])) #Maybe change CMD,LAUNCH,URL to communicate with the windows app instead.
    
    if action.startswith("LAUNCH:"):
        if naitive_cmd:
            return (launch_app(action[7:]))
        else:
            #Communicate with windows app
            raise NotImplementedError("not supported yet")
    
    if action.startswith("URL:"):
        if naitive_cmd:
            return (open_url(action[4:]))
        else:
            raise NotImplementedError("not supported yet")


    return KC.NO
