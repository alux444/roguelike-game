import tcod

from engine import Engine
from procgen import generate_dungeon
from input_handers import EventHandler
from entity import Entity


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(screen_width // 2, screen_height // 2, "@", (255, 255, 255))
    npc = Entity((screen_width // 2) - 5, (screen_height // 2) - 5, "&", (255, 255, 0))
    entities = {npc, player}

    game_map = generate_dungeon(map_width, map_height)
    engine = Engine(
        entities=entities, event_handler=event_handler, map=game_map, player=player
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike Game",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")

        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()
