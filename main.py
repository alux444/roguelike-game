import tcod
import copy

from engine import Engine
from procgen import generate_dungeon
import entity_factory


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 50

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_mobs_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factory.player)
    engine = Engine(player=player)

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        max_mobs_room=max_mobs_room,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine,
    )

    engine.update_fov()

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

            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
