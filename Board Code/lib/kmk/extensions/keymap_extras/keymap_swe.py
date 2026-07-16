from kmk.keys import KC

# Swedish keyboard layout fixes for common string characters

SV_CHARS = {
    "å": KC.LBRC,
    "ä": KC.QUOT,
    "ö": KC.SCLN,
    "Å": KC.LSFT(KC.LBRC),
    "Ä": KC.LSFT(KC.QUOT),
    "Ö": KC.LSFT(KC.SCLN),

    ":": KC.LSFT(KC.DOT),
    "/": KC.LSFT(KC.N7),
    "?": KC.LSFT(KC.MINS),
    "_": KC.LSFT(KC.SLSH),
    "-": KC.SLSH,
    ".": KC.DOT,
    ",": KC.COMM,
    " ": KC.SPACE,
}