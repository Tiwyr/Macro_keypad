# ui_display.py

import board
import busio
import digitalio
import displayio
import fourwire
import terminalio
import vectorio
import os
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from kmk.modules import Module
LOGO_SIZE = 55


class DisplayUpdater(Module):
    def __init__(self, layer_text, status_text, accent_palette, icons):
        self.layer_text = layer_text
        self.status_text = status_text
        self.accent_palette = accent_palette
        self.icons = icons
        self._last_state = None

    def _show_layer(self, active_layer):
        for layer_index, layer in enumerate(self.icons):
            for row in layer:
                for icon in row:
                    if icon is not None:
                        icon.hidden = layer_index != active_layer

    def before_matrix_scan(self, keyboard):
        layer1_active = 1 in keyboard.active_layers

        # Only redraw when the keyboard layer changes.
        if layer1_active != self._last_state:
            self._last_state = layer1_active

            if layer1_active:
                self.layer_text.text = "LAYER 1"
                self.status_text.text = "MUTE"
                self.accent_palette[0] = 0xD94A38
                self._show_layer(1)

            else:
                self.layer_text.text = "LAYER 0"
                self.status_text.text = "VOLUME"
                self.accent_palette[0] = 0x1C9A62
                self._show_layer(0)

    def after_matrix_scan(self, keyboard): return
    def process_key(self, keyboard, key, is_pressed, int_coord): return key
    def before_hid_send(self, keyboard): return
    def after_hid_send(self, keyboard): return
    def during_bootup(self, keyboard): return
    def on_powersave_enable(self, keyboard): return
    def on_powersave_disable(self, keyboard): return


def _rectangle(width, height, color, x=0, y=0):
    palette = displayio.Palette(1)
    palette[0] = color
    rect = vectorio.Rectangle(
        pixel_shader=palette,
        width=width,
        height=height,
        x=x,
        y=y,
    )
    return rect, palette


def _make_icon_grid(x = 9, y = 49, square_size = 60, line_thiccness = 2, columns = 4, rows = 3):
    width = square_size*columns + (columns + 1) * line_thiccness
    length = square_size*rows + (rows + 1) * line_thiccness

    icon_coordinates = [
    [(0, 0) for column in range(columns)]
    for row in range(rows)
    ]

    bitmap = displayio.Bitmap(width, length, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF
    palette.make_transparent(0)

    def rect(x1, y1, x2, y2):
        for y in range(y1, y2):
            for x in range(x1, x2):
                bitmap[x, y] = 1

    def v_line(x, y, length , thiccness):
        return rect(x,y,x+thiccness,y+length)
    
    def h_line(x, y, length , thiccness):
        return rect(x,y,x+length,y+thiccness)

    for column in range(columns + 1):
        x_cor = (square_size + line_thiccness)*column
        v_line(x_cor, 0, length, line_thiccness)

        if column < columns:
            for row in range(rows):
                icon_coordinates[row][column] = (x + x_cor + line_thiccness, 0)

    for row in range(rows + 1):
        y_cor = (square_size + line_thiccness)*row
        h_line(0, y_cor, width, line_thiccness)

        if row < rows:
            for column in range(columns):
                old_x, _ = icon_coordinates[row][column]
                icon_coordinates[row][column] = (old_x, y + y_cor + line_thiccness)


    return displayio.TileGrid(bitmap, pixel_shader=palette, x=x, y=y) , icon_coordinates


def _picture_in_cell(path, cell_x, cell_y, cell_size=60):
    bitmap = displayio.OnDiskBitmap(path)
    tile = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

    tile.x = cell_x + max(0, (cell_size - bitmap.width) // 2)
    tile.y = cell_y + max(0, (cell_size - bitmap.height) // 2)

    return tile


def _make_speaker_icon(muted=False):
    bitmap = displayio.Bitmap(36, 36, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFFFFFF
    palette.make_transparent(0)

    def rect(x1, y1, x2, y2):
        for y in range(y1, y2):
            for x in range(x1, x2):
                bitmap[x, y] = 1

    rect(4, 14, 10, 23)
    rect(10, 11, 16, 26)

    for y in range(8, 29):
        width = 1 + abs(18 - y) // 3
        for x in range(16, 22 - width):
            bitmap[x, y] = 1

    if muted:
        for i in range(8, 28):
            bitmap[i, i] = 1
            bitmap[i + 1, i] = 1
            bitmap[35 - i, i] = 1
            bitmap[34 - i, i] = 1
    else:
        for y in range(11, 26):
            bitmap[24 + abs(18 - y) // 3, y] = 1
        for y in range(8, 29):
            bitmap[29 + abs(18 - y) // 4, y] = 1

    return displayio.TileGrid(bitmap, pixel_shader=palette, x=38, y=112)



def folder_has_file_with_keyword(folder, keyword):
    for filename in os.listdir(folder):
        full_path = folder + "/" + filename

        try:
            stat = os.stat(full_path)
            is_file = not (stat[0] & 0x4000)
        except OSError:
            continue

        if is_file and keyword in filename:
            return full_path

    return None


def setup_display(nr_layers):

    
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

    background, _ = _rectangle(320, 240, 0x101418)
    header, _ = _rectangle(320, 30, 0x1F2930)
    accent, accent_palette = _rectangle(320, 8, 0x1C9A62, y=30)
    panel, _ = _rectangle(252, 84, 0x182026, x=34, y=92) #rectangle around volume text
    icon_grid, icon_coordinates = _make_icon_grid(square_size=LOGO_SIZE)

    for row in icon_coordinates:
        print(row)

    
                
   
    icons = [[[None for column in range(4)] for row in range(3)] for layer in range(nr_layers)]
    # icons = [layer,row,column]

    splash.append(background)
    splash.append(header)
    splash.append(accent)
    splash.append(icon_grid)

    
    for layer in range(nr_layers):
        root = "/images/Layer_" + str(layer)
        for row in range(3):
            for column in range(4):
                x_cord = int(icon_coordinates[row][column][0])
                y_cord = int(icon_coordinates[row][column][1])

                index = row * 4 + column + 1
                folder = root + "/" + str(index)
                keyword = str(LOGO_SIZE) + "x" + str(LOGO_SIZE)

                match = folder_has_file_with_keyword(folder, keyword)

                if match != None:
                    icons[layer][row][column] = _picture_in_cell(
                    match,
                    x_cord,
                    y_cord,
                    cell_size= LOGO_SIZE,
                    )
                    splash.append(icons[layer][row][column])

                

   

    layer_text = label.Label(
        terminalio.FONT,
        text="LAYER 0",
        color=0xE8F1F2,
        scale=2,
        x=20,
        y=14,
    )
    status_text = label.Label(
        terminalio.FONT,
        text="VOLUME",
        color=0xFFFFFF,
        scale=3,
        x=92,
        y=136,
    )

    speaker_tile = _make_speaker_icon(False)
    mute_tile = _make_speaker_icon(True)
    mute_tile.hidden = True

    splash.append(layer_text)
    #splash.append(speaker_tile)
    #splash.append(mute_tile)
    #splash.append(status_text)

    return DisplayUpdater(
        layer_text,
        status_text,
        accent_palette,
        icons,
    )
