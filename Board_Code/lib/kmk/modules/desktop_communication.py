# Board_Code/lib/kmk/modules/desktop_communication.py
import usb_cdc
from kmk.modules import Module
import time
from kmk.keys import Key, make_argumented_key

class MessageKey(Key):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.message = message

class DesktopCommunication(Module):
    def __init__(self):
        self.serial = usb_cdc.data
        self.buffer = bytearray()
        self.is_connected = False
        self.time_since_last_ping = 0
        self.timer = time.monotonic()

        make_argumented_key(
        names=("MESSAGE",),
        constructor=MessageKey,
        on_press=self.send_message,
        )

    def send_message(self, key, keyboard, *args):
        if self.serial and self.serial.connected and self.is_connected:
            self.serial.write(
                (key.message + "\n").encode("utf-8")
            )

    def before_matrix_scan(self, keyboard):
        self.check_messages()
        if time.monotonic() > self.time_since_last_ping + 1:
            self.is_connected = False

    def check_messages(self):
        if self.serial and self.serial.in_waiting:
            self.buffer.extend(
                self.serial.read(self.serial.in_waiting)
            )

        while b"\n" in self.buffer:
            message, _, self.buffer = self.buffer.partition(b"\n")
            self.handle_message(message.decode().strip())

    def handle_message(self, message):
        if message == "PING":
            self.is_connected = True
            self.time_since_last_ping = time.monotonic()
            self.serial.write(b"PONG\n")

    def during_bootup(self, keyboard):
        pass

    def after_matrix_scan(self, keyboard):
        pass

    def process_key(self, keyboard, key, is_pressed, int_coord):
        return key

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass