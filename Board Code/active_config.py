PROFILE_NAME = "Default"
PROFILE_VERSION = 1


LAYER_COUNT = 2
KEY_COUNT = 12
NAITIVE_CMD = True

KEY_ACTIONS = [
    [   "CMD:arg1 arg2 arg3",
        "URL:https://www.youtube.com/",
        "LAUNCH:C:/Program Files/KiCad/10.0/bin/kicad.exe",
        "MACRO:KC.LCTRL + KC.v",
        "MACRO:TEXT:start|ON_HOLD:TAP:KC.A|ON_HOLD:DELAY:100|ON_RELEASE:TEXT:end",
        "KC.VOLU",
        "KC.VOLD",
        "KC.MINS",
        None,
        None,
        None,
        None,
    ],
    [
        "KC.C",
        "KC.A",
        "KC.B",
        "STRING:open https://github.com",
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ],
]

ENCODER_ACTIONS = [
    [
        ["KC.VOLD",
        "KC.VOLU",
        "KC.NO",],

        ["KC.A",
        "KC.B",
        "KC.NO",],

    ],
    [
        ["KC.A",
        "KC.B",
        "KC.NO",],
        ["MACRO:KC.LCTRL + KC.C",
        "MACRO:KC.LCTRL + KC.v",
        "KC.NO",],
    ],

]