from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov
import lzma
import pickle

from render_functions import render_bar, render_names
from message_log import MessageLog
import exceptions

if TYPE_CHECKING:
    from entity import Actor
    from map import GameMap


class Engine:
    map: GameMap

    def __init__(
        self,
        player: Actor,
    ):
        self.player = player
        self.message_log = MessageLog()
        self.mouse_loc = (0, 0)

    def save_as(self, filename: str) -> None:
        # save engine game file
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)

    def handle_mob_event(self) -> None:
        for entity in set(self.map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass

    def update_fov(self) -> None:
        self.map.visible[:] = compute_fov(
            self.map.tiles["transparent"], (self.player.x, self.player.y), radius=8
        )

        self.map.explored |= self.map.visible

    def render(self, console: Console) -> None:
        self.map.render(console)

        self.message_log.render(console=console, x=21, y=42, width=45, height=6)

        render_bar(
            console=console,
            cur_val=self.player.fighter.hp,
            max_val=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names(console=console, engine=self)
