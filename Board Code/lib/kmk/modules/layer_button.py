from kmk.modules import Module
from kmk.keys import KC


class LayerButtonModule(Module):
    """
    A module that toggles a specific layer when a GPIO pin is pressed.
    Works exactly like KC.TG(layer) without sending HID keypresses.
    """

    def __init__(self, pin, layers_module, layer_to_toggle=1):
        self.pin = pin
        self.layers_module = layers_module
        self.prev = True  # startas som "släppt"
        self.layer_to_toggle = layer_to_toggle

        # skapa en fake-key med meta.layer så att Layers-modulen kan hantera togglandet
        class _Meta:
            pass

        class _Key:
            pass

        self.fake_key = _Key()
        self.fake_key.meta = _Meta()
        self.fake_key.meta.layer = layer_to_toggle

    #
    # -------- MODULE HOOKS (KMK kräver dessa) --------
    #

    def before_matrix_scan(self, keyboard):
        """Körs inför varje matrix-scan — perfekt för knappläsning."""
        cur = self.pin.value  # True = släppt, False = nedtryckt

        # kantdetektering: släppt → nedtryckt
        if self.prev and not cur:
            # låt Layers-modulen hantera detta, som KC.TG()
            self.layers_module._tg_pressed(self.fake_key, keyboard)
            print("Active layers:", keyboard.active_layers)

        self.prev = cur

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
