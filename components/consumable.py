from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
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


class HealingConsumable(Consumable):
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def active(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        recovered = consumer.fighter.heal(self.amount)

        if recovered > 0:
            self.engine.message_log.add_message(
                f"Yo consume the {self.parent.name}, and recover {recovered} HP.",
                color.health_recovered,
            )
        else:
            raise Impossible(f"Your health is full.")
