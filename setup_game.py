from __future__ import annotations

import copy
from typing import Optional

import tcod
import libtcodpy
from tcod.console import Console
import lzma
import pickle
import traceback

import color
from engine import Engine
import entity_factory
import input_handers
from map import GameWorld

background = tcod.image.load("menu_background.png")[:, :, :3]


def new_game() -> Engine:
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factory.player)

    engine = Engine(player=player)

    engine.world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    engine.world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message("Welcome to the rat dungeon", color.welcome_text)
    return engine


def load_game(filename: str) -> Engine:
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handers.BaseEventHandler):
    def on_render(self, console: Console) -> None:
        console.draw_semigraphics(background, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "RAT DUNGEON ADVENTURE",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "by alux444",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play new game", "[C] Continue previous game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return input_handers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handers.PopupMessage(self, "No saved game.")
            except Exception as exc:
                traceback.print_exc()
                return input_handers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return input_handers.MainGameEventHandler(new_game())

        return None
