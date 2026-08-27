from pathlib import Path

import string


def flash_to_board(profile_data):

    board_root = Path(find_keypad_drive())
    image_root = board_root / "images"

    config = compile_configFile(profile_data)

    flash_images_to_board(profile_data, image_root)

    with open(board_root / "active_config.py", "w", encoding="utf-8") as file:
             file.write(config)

    



def flash_images_to_board(profile_data, image_root : Path):

    num_layers = len(profile_data["layers"])

    for layer in range(num_layers):
        layer_dir = image_root / f"Layer_{layer}"
        for button in range(12):
            button_dir = layer_dir / f"{button+1}"
            button_image = profile_data["layers"][layer]["buttons"][button]["icon_data"]

            if button_image is not None:
                with open(button_dir / "Picture_55x55.bmp", "wb") as file:
                    file.write(button_image)

            else:
                for path in button_dir.iterdir():
                    if path.is_file():
                        path.unlink()


            

    return


def compile_configFile(profile_data) -> str:
    
    num_layers = len(profile_data["layers"])
    layer_names = [None,None,None,None]
    key_actions_string= ""
    encoder_actions_string = ""

    for layer in range(num_layers):
        layer_names[layer] = f"\"{profile_data["layers"][layer]["name"]}\""

        key_actions_string += "    [ \n"
        for button in range(12):
            button_function = profile_data["layers"][layer]["buttons"][button]["function_type"]
            if button_function is not None:
                button_string = str(button_function) + str(profile_data["layers"][layer]["buttons"][button]["command"])
                key_actions_string += f"        {button_string!r}, \n"

            else:
                key_actions_string += f"        None, \n"

        key_actions_string += "    ], \n"


        encoder_actions_string += """
                 [
                        [
                            "KC.LCTRL(KC.F13)",
                            "KC.LCTRL(KC.F14)",
                            "KC.NO",
                        ],
                        [
                            "KC.LCTRL(KC.F15)",
                            "KC.LCTRL(KC.F16)",
                            "KC.NO",
                        ],
                        [
                            "KC.LCTRL(KC.F17)",
                            "KC.LCTRL(KC.F18)",
                            "KC.NO",
                        ],
                ],
               """


    config = f'''
PROFILE_NAME = "{profile_data["name"]}" 
LAYER_COUNT = {num_layers}
LAYER_NAMES = [{layer_names[0]},{layer_names[1]},{layer_names[2]},{layer_names[3]}]
NAITIVE_CMD = False

KEY_ACTIONS = [
    {key_actions_string}
    ]

ENCODER_ACTIONS = [
    {encoder_actions_string}
]

'''

    
    return config



def find_keypad_drive() -> Path:
    candidates = []

    for letter in string.ascii_uppercase:
        root = Path(f"{letter}:/")

        try:
            boot_info = root / "boot_out.txt"
            keypad_marker = root / "Macro_keyboard_AX73.txt"

            if (
                boot_info.is_file()
                and keypad_marker.is_file()
                and "CircuitPython"
                in boot_info.read_text(errors="ignore")
            ):
                candidates.append(root)
                break

        except OSError:
            continue

    if not candidates:
        raise RuntimeError("The Macro Keypad drive was not found.")

    return candidates[0]