from typing import Tuple
import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # character
        ("fg", "3B"),  # foreground
        ("bg", "3B"),  # background
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool_),  # True if this tile can be walked over.
        ("transparent", np.bool_),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),
    ]
)

NONETILE = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)


def new_tile(
    *,
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">", (0, 0, 100), (50, 50, 150))),
    light=(ord(">"), (255, 255, 255), (200, 180, 50)),
)
