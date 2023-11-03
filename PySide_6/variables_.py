from pathlib import Path

ROOT_DIR = Path(__file__).parent
# Colors
PRIMARY_COLOR = "#1e81b0"
DARKER_PRIMARY_COLOR = "#16658a"
DARKEST_PRIMARY_COLOR = "#115270"

# Sizing
BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 12
TEXT_MARGIN = 15
MINIMUM_WIDTH = 500

QSS = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""
