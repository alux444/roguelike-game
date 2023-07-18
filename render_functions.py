from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod.console import Console
    from engine import Engine
    from map import GameMap


def get_names_at_loc(x: int, y: int, map: GameMap) -> str:
    if not map.in_bounds(x, y) or not map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bar(console: Console, cur_val: int, max_val: int, total_width: int) -> None:
    bar_width = int(float(cur_val) / max_val * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(x=1, y=45, string=f"HP: {cur_val}/{max_val}", fg=color.bar_text)


def render_names(console: Console, engine: Engine) -> None:
    mouse_x, mouse_y = engine.mouse_loc

    names_at_loc = get_names_at_loc(x=mouse_x, y=mouse_y, map=engine.map)

    console.print(x=mouse_x + 1, y=mouse_y - 1, string=names_at_loc)
