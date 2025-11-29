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

keyboard = KMKKeyboard()
encoders = EncoderHandler()

keyboard.modules.append(encoders)

keyboard.row_pins = (board.D3, board.D4)
keyboard.col_pins = (board.D6,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
midi_ext = Midi()

keyboard.extensions.append(midi_ext)
keyboard.extensions.append(MediaKeys())

encoders.pins = ((board.D10, board.MISO, None), (board.D1, board.D0, None),)


TERMINAL = simple_key_sequence(
    [KC.LCMD(KC.LALT(KC.LSFT(KC.T))), KC.LCTRL(KC.U)]
)

GLAD = simple_key_sequence(KC.G(KC.L(KC.A(KC.D))))
GIT = simple_key_sequence([send_string('open https://github.com'), KC.ENTER])

keyboard.keymap = [
    [GIT],
     [KC.B]
]

encoders.map = [
    (   # Layer 0 – MACROS
        (KC.VOLD, KC.VOLU, KC.NO),        # encoder 0: ccw, cw, press
        (KC.RGB_VAD, KC.RGB_VAI, KC.NO),  # encoder 1
    ),
    (   # Layer 1 – RGB CTL
        (KC.RGB_AND, KC.RGB_ANI, KC.NO),
        (KC.RGB_HUD, KC.RGB_HUI, KC.NO),
    ),
    (   # Layer 2 – MIDI
        (KC.VOLD, KC.VOLU, KC.NO),
        (KC.RGB_VAD, KC.RGB_VAI, KC.NO),
    ),
]

# --- DISPLAY SETUP ---

displayio.release_displays()

spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Testpinnar (om du vill)
test_pin = digitalio.DigitalInOut(board.D13)
test_pin.direction = digitalio.Direction.OUTPUT
test_pin.value = True

test_pin2 = digitalio.DigitalInOut(board.D12)
test_pin2.direction = digitalio.Direction.OUTPUT
test_pin2.value = False

# BYT TILL EN FRI PIN (INTE D3/D4/D6)!
layer_pin = digitalio.DigitalInOut(board.D9)
layer_pin.direction = digitalio.Direction.INPUT
layer_pin.pull = digitalio.Pull.UP

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

display_updater = DisplayUpdater(layer_pin, text_area)
keyboard.modules.append(display_updater)

if __name__ == "__main__":
    keyboard.go()

