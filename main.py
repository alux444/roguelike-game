import tcod
import copy
import color
import traceback

from engine import Engine
from procgen import generate_dungeon
import entity_factory


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_mobs_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factory.player)
    engine = Engine(player=player)

    engine.map = generate_dungeon(
        max_rooms=max_rooms,
        max_mobs_room=max_mobs_room,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine,
    )

    engine.message_log.add_message("Welcome to the rat dungeon.", color.welcome_text)

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
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            try:
                for event in tcod.event.wait:
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:
                traceback.print_exc
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
    main()
