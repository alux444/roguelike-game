from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class Level(BaseComponent):
    parent: Actor

    def __init__(
        self,
        current_lvl: int = 1,
        current_xp: int = 0,
        lvl_up_base: int = 0,
        lvl_up_factor: int = 150,
        xp_given: int = 0,
    ) -> None:
        self.current_lvl = current_lvl
        self.current_xp = current_xp
        self.lvl_up_base = lvl_up_base
        self.lvl_up_factor = lvl_up_factor
        self.xp_given = xp_given

    @property
    def xp_to_lvl(self) -> int:
        return self.lvl_up_base + self.current_lvl * self.lvl_up_factor

    @property
    def reqs_lvl_up(self) -> bool:
        return self.current_xp > self.xp_to_lvl

    def add_xp(self, xp: int) -> None:
        if xp == 0 or self.lvl_up_base == 0:
            return

        self.current_xp += xp
        self.engine.message_log.add_message(f"You gained {xp} xp")

        if self.reqs_lvl_up:
            self.engine.message_log.add_message(
                f"You levelled up to {self.current_lvl + 1}!"
            )

    def increase_lvl(self) -> None:
        self.current_xp -= self.xp_to_lvl
        self.current_lvl += 1
