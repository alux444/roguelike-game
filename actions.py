from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING
import color
from entity import Actor
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine

    def perform(self) -> None:
        # must be overridden by action
        raise NotImplementedError()


class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ) -> None:
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.map.get_actor_at(*self.target_xy)

    def perform(self) -> None:
        if self.item.consumable:
            self.item.consumable.activate(self)


class PickupAction(Action):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Full inventory.")

                self.engine.map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up {item.name}")
                return

        raise exceptions.Impossible("Nothing to pick up.")


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


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item) -> None:
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.map.in_bounds(dest_x, dest_y):
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.map.tiles["walkable"][dest_x, dest_y]:
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.map.get_blocking_entity(dest_x, dest_y):
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor

        if not target:
            raise exceptions.Impossible("Nothing to attack.")

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


class DescendAction(Action):
    def perform(self) -> None:
        if (self.entity.x, self.entity.y) == self.engine.map.downstairs_loc:
            self.engine.world.generate_floor()
            self.engine.message_log.add_message(
                "You descended to the next level.", color.descend
            )
        else:
            raise exceptions.Impossible("No stairs here.")
