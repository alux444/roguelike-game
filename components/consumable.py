from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        raise NotImplementedError()

    def consume(self) -> None:
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        recovered = consumer.fighter.heal(self.amount)

        if recovered > 0:
            self.engine.message_log.add_message(
                f"Yo consume the {self.parent.name}, and recover {recovered} HP.",
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible(f"Your health is full.")


class LightningConsumable(Consumable):
    def __init__(self, damage: int, max_range: int) -> None:
        self.damage = damage
        self.max_range = max_range

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_dist = self.max_range + 1.0

        for actor in self.engine.map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_dist:
                    target = actor
                    closest_dist = distance

        if target:
            self.engine.message_log.add_message(
                f"You zap {target.name} for {self.damage} damage."
            )
            target.fighter.take_damage(self.damage)
            self.consume
        else:
            raise Impossible("No enemies to zap.")
