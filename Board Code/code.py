import board
import busio
import digitalio
import displayio
from adafruit_st7789 import ST7789
from adafruit_display_text import label
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.handlers.sequences import simple_key_sequence,send_string
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
import terminalio
import fourwire
from midi import Midi
from kmk.modules.layers import Layers
from kmk.modules import Module
from kmk.modules.layer_button import LayerButtonModule







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






encoders.pins = ((board.D1, board.D0, None),(board.MISO, board.D10, None),)
#encoders.pins = ((board.D1, board.D0, None),(board.MISO, board.D10, None),(board.D12, board.D13, None))


TERMINAL = simple_key_sequence(
    [KC.LCMD(KC.LALT(KC.LSFT(KC.T))), KC.LCTRL(KC.U)]
)

GLAD = simple_key_sequence(KC.G(KC.L(KC.A(KC.D))))
GIT = simple_key_sequence([send_string('open https://github.com'), KC.ENTER])
keyboard.debug_enabled = True

keyboard.keymap = [
    # Layer 0
    [KC.A, KC.C],
    # Layer 1
    [KC.B, KC.D],
]


encoders.map = [
    (   # Layer 0 – MACROS
        (KC.VOLD, KC.VOLU, KC.NO),     # encoder 0: ccw, cw, press
        (KC.C, KC.D, KC.NO),
          
    ),

     (   # Layer 0 – MACROS
        (KC.A, KC.B, KC.NO),     # encoder 0: ccw, cw, press
        (KC.C, KC.D, KC.NO),
          
    ),
]

# --- DISPLAY SETUP ---

displayio.release_displays()

spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=None)



tft_bl = digitalio.DigitalInOut(board.A0)
tft_bl.direction = digitalio.Direction.OUTPUT
tft_bl.value = True

while not spi.try_lock():
    pass
spi.configure(baudrate=24_000_000, phase=0, polarity=0)
spi.unlock()

display_bus = fourwire.FourWire(
    spi,
    command=board.A2,
    chip_select=board.A3,
    reset=board.A1,
    baudrate=24_000_000,
)

display = ST7789(
    display_bus,
    width=320,
    height=240,
    rotation=90,
    rowstart=0,
    colstart=0,
)

splash = displayio.Group()
display.root_group = splash

bg_bitmap = displayio.Bitmap(320, 240, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x003300
bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=0, y=0)
splash.append(bg_sprite)

inner_bitmap = displayio.Bitmap(280, 200, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000055
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

text_group = displayio.Group(scale=2, x=40, y=120)
text_area = label.Label(terminalio.FONT, text="Hello KB2040!", color=0xFFFFFF)
text_group.append(text_area)
splash.append(text_group)

# --- KMK-MODUL FÖR DISPLAYEN ---

class DisplayUpdater:
    def __init__(self, layer_pin, text_area):
        self.layer_pin = layer_pin
        self.text_area = text_area

    # KMK kallar denna inför varje matrix-scan
    def before_matrix_scan(self, keyboard):
        if not self.layer_pin.value:   # knapp mot GND
            self.text_area.text = "Button pressed!"
        else:
            self.text_area.text = "Hello KB2040!"

    def after_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        return key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def during_bootup(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

display_updater = DisplayUpdater(layer_pin, text_area)
keyboard.modules.append(display_updater)



layer_button = LayerButtonModule(layer_pin, layers, layer_to_toggle=1)
keyboard.modules.append(layer_button)



if __name__ == "__main__":
    keyboard.go()




