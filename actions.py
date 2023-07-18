from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING
import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        return self.entity.map.engine

    def perform(self) -> None:
        # must be overridden by action
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int) -> None:
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.engine.map.get_blocking_entity(self.dest_xy[0], self.dest_xy[1])

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.map.get_actor_at(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.map.in_bounds(dest_x, dest_y):
            return  # out of bounds
        if not self.engine.map.tiles["walkable"][dest_x, dest_y]:
            return  # tile blocked
        if self.engine.map.get_blocking_entity(dest_x, dest_y):
            return  # blocked by entity

        self.entity.move(self.dx, self.dy)


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor

        if not target:
            return  # no meleeable target

        damage = self.entity.fighter.power - target.fighter.defense

        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} damage", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class WaitAction(Action):
    def perform(self) -> None:
        pass
