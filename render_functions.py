from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod.console import Console


def render_bar(console: Console, cur_val: int, max_val: int, total_width: int) -> None:
    bar_width = int(float(cur_val) / max_val * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(x=1, y=45, string=f"HP: {cur_val}/{max_val}", fg=color.bar_text)
