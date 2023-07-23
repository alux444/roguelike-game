from entity import Actor, Item
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

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
    level=Level(lvl_up_base=50),
)

rat = Actor(
    char="R",
    color=(63, 127, 64),
    name="Rat",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

frog = Actor(
    char="F",
    color=(0, 127, 0),
    name="Frog",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
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
