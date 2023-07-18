from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handers import MainGameEventHandler
from render_functions import render_bar

if TYPE_CHECKING:
    from entity import Actor
    from map import GameMap
    from input_handers import EventHandler


class Engine:
    map: GameMap

    def __init__(
        self,
        player: Actor,
    ):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player

    def handle_mob_event(self) -> None:
        for entity in set(self.map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        self.map.visible[:] = compute_fov(
            self.map.tiles["transparent"], (self.player.x, self.player.y), radius=8
        )

        self.map.explored |= self.map.visible

    def render(self, console: Console, context: Context) -> None:
        self.map.render(console)

        render_bar(
            console=console,
            cur_val=self.player.fighter.hp,
            max_val=self.player.fighter.max_hp,
            total_width=20,
        )

        context.present(console)

        console.clear()
