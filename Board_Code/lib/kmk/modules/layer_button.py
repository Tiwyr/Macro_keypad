import time

from kmk.modules import Module


class LayerButtonModule(Module):
    def __init__(self, pin, layers_module, layer_count=1):
        self.pin = pin
        self.layers_module = layers_module
        self.prev = True
        self.last_press_time = 0
        self.repeat_delay = 0.35
        self.current_layer = 0
        self.layer_count = layer_count

    def _make_fake_key(self, current_layer):
        class _Key:
            pass

        fake_key = _Key()
        fake_key.layer = current_layer
        return fake_key

    def _next_layer(self, keyboard):
        self.current_layer += 1

        if self.current_layer >= self.layer_count:
            self.current_layer = 0

        fake_key = self._make_fake_key(self.current_layer)
        self.layers_module._to_pressed(fake_key, keyboard)

    def before_matrix_scan(self, keyboard):
        cur = self.pin.value
        now = time.monotonic()

        if cur:
            self.prev = True
            return

        if self.prev or now - self.last_press_time >= self.repeat_delay:
            self.last_press_time = now
            self._next_layer(keyboard)

        self.prev = False

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
