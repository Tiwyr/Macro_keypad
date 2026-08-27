PROFILE_NAME = "Default"


LAYER_COUNT = 3

LAYER_NAMES = [None,None,None,None]

NAITIVE_CMD = False

KEY_ACTIONS = [
    [
        "KC.LSHIFT(KC.LALT(KC.P))",
        "MACRO:TAP:KC.LCTRL+KC.K|TAP:KC.V",
        "LAUNCH:C:/Program Files/KiCad/10.0/bin/kicad.exe",
        "URL:https://www.youtube.com/",
        "CMD:Start-Process explorer.exe -ArgumentList 'C:/Users/tiast/Documents/Macro_keypad/Desktop_App'",
        "KC.F",
        "KC.G",
        "KC.H",
        "KC.I",
        "KC.J",
        "KC.K",
        "KC.L",
    ],
    [
        "KC.A",
        "KC.B",
        "KC.C",
        "KC.D",
        "KC.E",
        "KC.F",
        "KC.G",
        "KC.H",
        "KC.I",
        "KC.J",
        "KC.K",
        "KC.L",
    ],
    [
        "KC.A",
        "KC.B",
        "KC.C",
        "KC.D",
        "KC.E",
        "KC.F",
        "KC.G",
        "KC.H",
        "KC.I",
        "KC.J",
        "KC.K",
        "KC.L",
    ],
    [
        "CMD:arg1 arg2 arg3",
        "URL:https://www.youtube.com/",
        "LAUNCH:C:/Program Files/KiCad/10.0/bin/kicad.exe",
        "MACRO:TAP:KC.LCTRL+KC.V",
        "MACRO:TEXT:start|ON_HOLD:TAP:KC.A|ON_HOLD:DELAY:100|ON_RELEASE:TEXT:end",
        "KC.VOLU",
        "KC.VOLD",
        "KC.MINS",
        None,
        None,
        None,
        None,
    ],
]

# Media
# Game
# Chat

ENCODER_ACTIONS = [
    [
        [
            "KC.LCTRL(KC.F13)",
            "KC.LCTRL(KC.F14)",
            "KC.NO",
        ],
        [
            "KC.LCTRL(KC.F15)",
            "MACRO:KC.LCTRL(KC.F16)",
            "KC.NO",
        ],
        [
            "KC.LCTRL(KC.F17)",
            "KC.LCTRL(KC.F18)",
            "KC.NO",
        ],
    ],
    [
        [
            "KC.LCTRL(KC.F13)",
            "KC.LCTRL(KC.F14)",
            "KC.NO",
        ],
        [
            "KC.LCTRL(KC.F15)",
            "MACRO:KC.LCTRL(KC.F16)",
            "KC.NO",
        ],
        [
            "KC.LCTRL(KC.F17)",
            "KC.LCTRL(KC.F18)",
            "KC.NO",
        ],
    ],
    [
            [
                "KC.LCTRL(KC.F13)",
                "KC.LCTRL(KC.F14)",
                "KC.NO",
            ],
            [
                "KC.LCTRL(KC.F15)",
                "MACRO:KC.LCTRL(KC.F16)",
                "KC.NO",
            ],
            [
                "KC.LCTRL(KC.F17)",
                "KC.LCTRL(KC.F18)",
                "KC.NO",
            ],
        ],
    [
            [
                "KC.LCTRL(KC.F13)",
                "KC.LCTRL(KC.F14)",
                "KC.NO",
            ],
            [
                "KC.LCTRL(KC.F15)",
                "MACRO:KC.LCTRL(KC.F16)",
                "KC.NO",
            ],
            [
                "KC.LCTRL(KC.F17)",
                "KC.LCTRL(KC.F18)",
                "KC.NO",
            ],
        ],
    [
            [
                "KC.LCTRL(KC.F13)",
                "KC.LCTRL(KC.F14)",
                "KC.NO",
            ],
            [
                "KC.LCTRL(KC.F15)",
                "MACRO:KC.LCTRL(KC.F16)",
                "KC.NO",
            ],
            [
                "KC.LCTRL(KC.F17)",
                "KC.LCTRL(KC.F18)",
                "KC.NO",
            ],
        ],
]
