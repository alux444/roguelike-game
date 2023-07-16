from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from map import GameMap
from entity import Entity
from input_handers import EventHandler


class Engine:
    def __init__(
        self,
        event_handler: EventHandler,
        map: GameMap,
        player: Entity,
    ):
        self.event_handler = event_handler
        self.map = map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov()

    def update_fov(self) -> None:
        self.map.visible[:] = compute_fov(
            self.map.tiles["transparent"], (self.player.x, self.player.y), radius=8
        )

        self.map.explored |= self.map.visible

    def render(self, console: Console, context: Context) -> None:
        self.map.render(console)

        context.present(console)

        console.clear()
