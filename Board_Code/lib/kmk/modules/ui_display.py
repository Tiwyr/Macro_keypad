# ui_display.py

import board
import busio
import digitalio
import displayio
import fourwire
import terminalio
import vectorio
import os
import time
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from kmk.modules import Module
LOGO_SIZE = 55


class DisplayUpdater(Module):
    def __init__(self, display, layer_text, accent_palette, icons):
        self.display = display
        self.layer_text = layer_text
        self.accent_palette = accent_palette
        self.icons = icons
        self._last_state = None
        self._pending_layer = None
        self._pending_index = 0
        self._update_after = 0
        self._settle_delay = 0.4

        for idx, text in enumerate(layer_text):
            if idx == 0:
                pass
            else:
                text.hidden = True
                  
    

    def _show_layer_text(self, active_layer):
        for text_index, text in enumerate(self.layer_text):
            text.hidden = text_index != active_layer

    def _hide_all_icons(self):
        for layer_index, layer in enumerate(self.icons):
            for row in layer:
                for icon in row:
                    if icon is not None:
                        icon.hidden = True

    def _icon_at_index(self, active_layer, icon_index):
        row = icon_index // 4
        column = icon_index % 4
        return self.icons[active_layer][row][column]

    def _continue_layer_update(self):
        if self._pending_layer is None:
            return

        if self._pending_index < 0:
            if time.monotonic() < self._update_after:
                return

            active_layer = self._pending_layer
            self.display.auto_refresh = False
            self._hide_all_icons()
            self._pending_index = 0
            self.display.refresh()
            self.display.auto_refresh = True

        # Reveal one icon per scan so the keyboard stays responsive.
        while self._pending_index < 12:
            icon = self._icon_at_index(self._pending_layer, self._pending_index)
            self._pending_index += 1

            if icon is not None:
                icon.hidden = False
                return

        self._pending_layer = None

    def before_matrix_scan(self, keyboard):
        accent_colors = [0xD94A38 , 0x1C9A62 , 0x5DADEC, 0xFFA500, 0xFF69B4]
        active_layer = keyboard.active_layers[0]

        # Only redraw when the keyboard layer changes.
        if active_layer != self._last_state:
            self._last_state = active_layer

            self.accent_palette[0] = accent_colors[active_layer]
            self._show_layer_text(active_layer)
            self._pending_layer = active_layer
            self._pending_index = -1
            self._update_after = time.monotonic() + self._settle_delay

        self._continue_layer_update()

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


def _make_icon_grid(x = 45, y = 49, square_size = 60, line_thiccness = 2, columns = 4, rows = 3):
    width = square_size*columns + (columns + 1) * line_thiccness
    length = square_size*rows + (rows + 1) * line_thiccness

    icon_coordinates = [
    [(0, 0) for column in range(columns)]
    for row in range(rows)
    ]

    bitmap = displayio.Bitmap(width, length, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFF0000
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


def make_layer_text(nr_layers, Layer_names):
    text_objects = []

    for object in range(nr_layers):
        if Layer_names[object] == None:
            if object == 0:
                layer_text = label.Label(
                            terminalio.FONT,
                            text="DEFAULT",
                            color=0xE8F1F2,
                            scale=2,
                            x=20,
                            y=14,
                        )

            else:
                layer_text = label.Label(
                        terminalio.FONT,
                        text=f"LAYER {object}",
                        color=0xE8F1F2,
                        scale=2,
                        x=20,
                        y=14,
                    )
        else:
            layer_text = label.Label(
                                    terminalio.FONT,
                                    text=Layer_names[object],
                                    color=0xE8F1F2,
                                    scale=2,
                                    x=20,
                                    y=14,
                                )
        text_objects.append(layer_text)

    return text_objects

def text_icons(nr_layers):
    text_objects = []
    paths = [
        "/images/Layer_Text/Layer_Text_m.bmp",
        "/images/Layer_Text/L1_m.bmp",
        "/images/Layer_Text/L2_m.bmp",
    ]

    for path in paths[:nr_layers]:
        bitmap = displayio.OnDiskBitmap(path)
        tile = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        tile.x = 20
        tile.y = 14
        text_objects.append(tile)
    
      

    return text_objects
     
    




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




def setup_display(nr_layers, Layer_names):

    
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
    icon_grid, icon_coordinates = _make_icon_grid(square_size=LOGO_SIZE)

    
                
   
    icons = [[[None for column in range(4)] for row in range(3)] for layer in range(nr_layers)]
    # icons = [layer,row,column]

    text_objects = make_layer_text(nr_layers, Layer_names)
    #text_objects = text_icons(nr_layers)
        
    

    splash.append(background)
    splash.append(header)

    for text in text_objects:
        splash.append(text)

    splash.append(accent)
    splash.append(icon_grid)
    nr_icons = 0

    
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
                    nr_icons += 1
                    splash.append(icons[layer][row][column])

                

   
    
    
    
   

    return DisplayUpdater(
        display,
        text_objects,
        accent_palette,
        icons,
    )
