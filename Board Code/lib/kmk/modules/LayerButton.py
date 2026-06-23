from kmk.modules import Module
from kmk.keys import KC


class LayerButtonModule(Module):
    def __init__(self, pin, layers_module, layer_to_toggle=1):
        self.pin = pin
        self.layers_module = layers_module
        self.prev = True
        self.layer_to_toggle = layer_to_toggle

      
        class _Meta:
            pass
        class _Key:
            pass

        self.fake_key = _Key()
        self.fake_key.meta = _Meta()
        self.fake_key.meta.layer = layer_to_toggle

    def before_matrix_scan(self, keyboard):
        cur = self.pin.value  # True = släppt (pull-up), False = nedtryckt

        # kant: tidigare släppt, nu nedtryckt
        if self.prev and not cur:
            # Låt Layers-modulen göra exakt samma som KC.TG(layer_to_toggle)
            self.layers_module._tg_pressed(self.fake_key, keyboard)
            print("Active layers:", keyboard.active_layers)

        self.prev = cur

    # ---- tomma stubbar som KMK vill ha ----
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