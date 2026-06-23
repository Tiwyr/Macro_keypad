import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.handlers.sequences import simple_key_sequence, send_string
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from midi import Midi
from kmk.modules.layers import Layers
from kmk.modules.layer_button import LayerButtonModule
from kmk.modules.ui_display import setup_display  

NR_LAYERS = 2


keyboard = KMKKeyboard()
encoders = EncoderHandler()
layers = Layers()
midi_ext = Midi()

keyboard.modules.append(layers)
keyboard.modules.append(encoders)
keyboard.extensions.append(midi_ext)

keyboard.row_pins = (board.D3, board.D4)
keyboard.col_pins = (board.D6,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

layer_pin = digitalio.DigitalInOut(board.D9)
layer_pin.direction = digitalio.Direction.INPUT
layer_pin.pull = digitalio.Pull.UP

encoders.pins = (
    (board.D1, board.D0, None),
    (board.MISO, board.D10, None),
)

TERMINAL = simple_key_sequence(
    [KC.LCMD(KC.LALT(KC.LSFT(KC.T))), KC.LCTRL(KC.U)]
)
GLAD = simple_key_sequence(KC.G(KC.L(KC.A(KC.D))))
GIT = simple_key_sequence([send_string('open https://github.com'), KC.ENTER])
keyboard.debug_enabled = True

keyboard.keymap = [
    [KC.A, KC.C],  # layer 0
    [KC.B, KC.D],  # layer 1
]

encoders.map = [
    (
        (KC.VOLD, KC.VOLU, KC.NO),
        (KC.C, KC.D, KC.NO),
    ),
    (
        (KC.A, KC.B, KC.NO),
        (KC.C, KC.D, KC.NO),
    ),
]

# --- DISPLAY SETUP (nu EN rad) ---
display_updater = setup_display(NR_LAYERS)
keyboard.modules.append(display_updater)

# Layer-knapp
layer_button = LayerButtonModule(layer_pin, layers, layer_to_toggle=NR_LAYERS-1)
keyboard.modules.append(layer_button)

if __name__ == "__main__":
    keyboard.go()
