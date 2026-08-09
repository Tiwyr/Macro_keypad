# Board_Code/lib/kmk/modules/desktop_communication.py
import usb_cdc
from kmk.modules import Module


class DesktopCommunication(Module):
    def __init__(self):
        self.serial = usb_cdc.data
        self.buffer = bytearray()

    def before_matrix_scan(self, keyboard):
        self.check_messages()

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