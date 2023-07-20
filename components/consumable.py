from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.inventory
import components.ai
from components.base_component import BaseComponent
from entity import Actor
from exceptions import Impossible
from input_handers import SingleRangedAttackHandler, AoeRangeedAttackHandler

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


class ConfusionConsumable(Consumable):
    def __init__(self, number_turns: int) -> None:
        self.number_turns = number_turns

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        self.engine.message_log.add_message(
            "Select target location.", color.needs_target
        )
        self.engine.event_handler = SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.map.visible[action.target_xy]:
            raise Impossible("Can't target out of FOV.")
        if not target:
            raise Impossible("You must select an enemy.")
        if target is consumer:
            raise Impossible("You can't use that on yourself.")

        self.engine.message_log.add_message(
            f"You've confused {target.name}.", color.status_effect_applied
        )

        target.ai = components.ai.ConfusedEnemy(
            entity=target, previous_ai=target.ai, turns_remaining=self.number_turns
        )
        self.consume()


class BombConsumable(Consumable):
    def __init__(self, damage: int, radius: int) -> None:
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        self.engine.message_log.add_message(
            "Select target location.", color.needs_target
        )
        self.engine.event_handler = AoeRangeedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.map.visible[target_xy]:
            raise Impossible("Can't target out of FOV")

        targets_hit = False
        for actor in self.engine.map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"You exploded {actor.name} for {self.damage} damage!"
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise Impossible("No targets to be hit here.")

        self.consume()
