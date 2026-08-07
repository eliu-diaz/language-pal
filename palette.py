from textual.theme import Theme

INK = "#4A4A4A"  # charcoal
MIST = "#CBCBCB"  # light grey
PAPER = "#FFFFE3"  # cream
SLATE = "#6D8196"  # slate blue

_PALETTE_VARIABLES = {
    "ink": INK,
    "mist": MIST,
    "paper": PAPER,
    "slate": SLATE,
}

INK_WASH_DARK = Theme(
    name="ink-wash-dark",
    background=INK,
    surface=INK,
    foreground=PAPER,
    primary=SLATE,
    secondary=MIST,
    dark=True,
    variables=_PALETTE_VARIABLES,
)

INK_WASH_LIGHT = Theme(
    name="ink-wash-light",
    background=PAPER,
    surface=PAPER,
    foreground=INK,
    primary=SLATE,
    secondary=INK,
    dark=False,
    variables=_PALETTE_VARIABLES,
)
