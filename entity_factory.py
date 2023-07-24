from entity import Actor, Item
import components.equippable
from components.consumable import (
    HealingConsumable,
    LightningConsumable,
    ConfusionConsumable,
    BombConsumable,
)
from components.ai import HostileEnemy
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment


player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, base_defense=2, base_power=5),
    inventory=Inventory(capacity=26),
    level=Level(lvl_up_base=50),
    equipment=Equipment(),
)

rat = Actor(
    char="R",
    color=(63, 127, 64),
    name="Rat",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    equipment=Equipment(),
)

frog = Actor(
    char="F",
    color=(0, 127, 0),
    name="Frog",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    equipment=Equipment(),
)

demon_rat = Actor(
    char="R",
    color=(255, 0, 0),
    name="Demon Rat",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=25, base_defense=2, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    equipment=Equipment(),
)

demon_frog = Actor(
    char="F",
    color=(255, 0, 0),
    name="Demon Frog",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, base_defense=2, base_power=6),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    equipment=Equipment(),
)

health_potion = Item(
    char="+",
    color=(127, 0, 255),
    name="Health Pot",
    consumable=HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char="Z",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=LightningConsumable(damage=20, max_range=5),
)

confusion_scroll = Item(
    char="C",
    color=(206, 63, 255),
    name="Confusion Scroll",
    consumable=ConfusionConsumable(number_turns=10),
)

bomb = Item(
    char="B",
    color=(255, 0, 0),
    name="Bomb",
    consumable=BombConsumable(damage=12, radius=3),
)

stick = Item(
    char="/",
    color=(0, 191, 255),
    name="Stick",
    equippable=components.equippable.Stick(),
)
knife = Item(
    char="/",
    color=(0, 191, 255),
    name="Knife",
    equippable=components.equippable.Knife(),
)
shield = Item(
    char="o",
    color=(0, 191, 255),
    name="Shield",
    equippable=components.equippable.Shield(),
)
big_shield = Item(
    char="o",
    color=(0, 191, 255),
    name="Big Shield",
    equippable=components.equippable.BigShield(),
)
