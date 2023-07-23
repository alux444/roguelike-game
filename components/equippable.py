from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self, type: EquipmentType, power_bonus: int = 0, defense_bonus: int = 0
    ) -> None:
        self.type = type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus


class Stick(Equippable):
    def __init__(self) -> None:
        super().__init__(type=EquipmentType.WEAPON, power_bonus=2)


class Knife(Equippable):
    def __init__(self) -> None:
        super().__init__(type=EquipmentType.WEAPON, power_bonus=4)


class Shield(Equippable):
    def __init__(self) -> None:
        super().__init__(type=EquipmentType.ARMOR, defense_bonus=2)


class BigShield(Equippable):
    def __init__(self) -> None:
        super().__init__(type=EquipmentType.ARMOR, defense_bonus=4)
