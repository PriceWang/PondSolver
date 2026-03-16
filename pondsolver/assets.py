from __future__ import annotations

from pathlib import Path

from .models import Rect


PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

BOARD_SIZE = 6

SIZE = {
    "bg": Rect(0, 0, 1000, 1624),
    "frame": Rect(90, 249, 910, 1069),
    "fish_nor": Rect(0, 0, 224, 112),
    "block_1_2_nor": Rect(0, 0, 220, 108),
    "block_1_3_nor": Rect(0, 0, 332, 108),
    "block_2_1_nor": Rect(0, 0, 108, 220),
    "block_3_1_nor": Rect(0, 0, 108, 332),
    "btn_reset": Rect(0, 0, 99, 99),
    "btn_solve": Rect(0, 0, 99, 99),
    "btn_exit": Rect(0, 0, 99, 99),
    "btn_home": Rect(0, 0, 99, 99),
    "btn_back": Rect(0, 0, 99, 99),
    "btn_forward": Rect(0, 0, 99, 99),
}

BLOCK_TO_ASSET = {
    ("h", 2, True): "fish_nor",
    ("h", 2, False): "block_1_2_nor",
    ("h", 3, False): "block_1_3_nor",
    ("v", 2, False): "block_2_1_nor",
    ("v", 3, False): "block_3_1_nor",
}

PALETTE_BLOCKS = [
    "fish_nor",
    "block_1_2_nor",
    "block_1_3_nor",
    "block_2_1_nor",
    "block_3_1_nor",
]
