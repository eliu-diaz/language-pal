from textual.theme import Theme

INK = "#4A4A4A"  # charcoal
MIST = "#CBCBCB"  # light grey
PAPER = "#FFFFE3"  # cream
SLATE = "#6D8196"  # slate blue

# signal colours: deliberately outside the ink wash harmony so they read as alerts
OCHRE = "#C9873A"  # warning
OXBLOOD = "#A8433A"  # error
SAGE = "#6E8B5B"  # success

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
    warning=OCHRE,
    error=OXBLOOD,
    success=SAGE,
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
    warning=OCHRE,
    error=OXBLOOD,
    success=SAGE,
    dark=False,
    variables=_PALETTE_VARIABLES,
)
