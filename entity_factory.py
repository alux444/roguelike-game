from entity import Actor
from components.ai import HostileEnemy
from components.fighter import Fighter

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
)

rat = Actor(
    char="R",
    color=(63, 127, 64),
    name="Rat",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
)

frog = Actor(
    char="F",
    color=(0, 127, 0),
    name="Frog",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
)
