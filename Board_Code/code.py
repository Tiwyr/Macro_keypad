import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.macros import Macros
from midi import Midi
from kmk.modules.layers import Layers
from kmk.modules.layer_button import LayerButtonModule
from kmk.modules.ui_display import setup_display  
import active_config
from lib.kmk.macro_decder import action_to_key
import kmk.extensions.keymap_extras.keymap_swe
from kmk.modules.desktop_communication import DesktopCommunication



MAX_NR_LAYERS = 4

NR_LAYERS = active_config.LAYER_COUNT
LAYER_NAMES = active_config.LAYER_NAMES

if NR_LAYERS > MAX_NR_LAYERS:
    NR_LAYERS = MAX_NR_LAYERS

key_actions = active_config.KEY_ACTIONS
encoder_actions = active_config.ENCODER_ACTIONS


keyboard = KMKKeyboard()
encoders = EncoderHandler()
encoders.divisor = 2
layers = Layers()
midi_ext = Midi()
macros = Macros()

keyboard.modules.append(macros)
keyboard.modules.append(layers)
keyboard.modules.append(encoders)
keyboard.extensions.append(midi_ext)
keyboard.extensions.append(MediaKeys())

keyboard.row_pins = (board.D5, board.D4, board.D3)
keyboard.col_pins = (board.D9,board.D8, board.D10, board.MISO)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

layer_pin = digitalio.DigitalInOut(board.D0)
layer_pin.direction = digitalio.Direction.INPUT
layer_pin.pull = digitalio.Pull.UP

encoders.pins = (
    (board.D12, board.D13, None),
    (board.D2, board.D1, None),
    (board.D7, board.D6, None),
)


keyboard.debug_enabled = False

keyboard.keymap = [
    [action_to_key(action, active_config.NAITIVE_CMD) for action in layer]
    for layer in key_actions
]

encoders.map = [
    [[action_to_key(action, active_config.NAITIVE_CMD) for action in encoder] for encoder in layer]
    for layer in encoder_actions
]


# --- DISPLAY SETUP ---
display_updater = setup_display(NR_LAYERS, LAYER_NAMES)

# Layer-knapp
layer_button = LayerButtonModule(layer_pin, layers, layer_count=NR_LAYERS)
keyboard.modules.append(layer_button)
keyboard.modules.append(display_updater)

desktop_communication = DesktopCommunication()
keyboard.modules.append(desktop_communication)

if __name__ == "__main__":
    keyboard.go()
