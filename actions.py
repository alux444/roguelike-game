from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class MovementAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.map.in_bounds(dest_x, dest_y):
            return  # out of bounds
        if not engine.map.tiles["walkable"][dest_x, dest_y]:
            return  # tile blocked
        if engine.map.get_blocking_entity(dest_x, dest_y):
            return  # blocked by entity

        entity.move(self.dx, self.dy)


class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        target = engine.map.get_blocking_entity(dest_x, dest_y)
        if not target:
            return  # no meleeable target

        print(f"Ouch! - {target.name}")


class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.map.get_blocking_entity(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
