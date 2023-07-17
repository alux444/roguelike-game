from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from map import GameMap


class Engine:
    map: GameMap

    def __init__(
        self,
        player: Entity,
    ):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player

    def handle_mob_event(self) -> None:
        for entity in self.map.entities - {self.player}:
            print(f"Hmm... - {entity.name}")

    def update_fov(self) -> None:
        self.map.visible[:] = compute_fov(
            self.map.tiles["transparent"], (self.player.x, self.player.y), radius=8
        )

        self.map.explored |= self.map.visible

    def render(self, console: Console, context: Context) -> None:
        self.map.render(console)

        context.present(console)

        console.clear()
