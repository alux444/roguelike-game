from __future__ import annotations
from typing import Dict, Tuple, Iterator, List, TYPE_CHECKING
from map import GameMap
import entity_factory
import random
import tile_types
import tcod

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

max_items_floor = [(1, 1), (4, 2)]

max_mobs_floor = [(1, 2), (4, 3), (6, 5)]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factory.health_potion, 35), (entity_factory.stick, 10)],
    1: [(entity_factory.confusion_scroll, 10), (entity_factory.shield, 15)],
    2: [(entity_factory.lightning_scroll, 25), (entity_factory.knife, 5)],
    3: [(entity_factory.bomb, 25), (entity_factory.big_shield, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factory.rat, 80)],
    2: [(entity_factory.frog, 15)],
    4: [(entity_factory.frog, 30)],
    6: [(entity_factory.demon_rat, 30)],
    7: [(entity_factory.demon_rat, 40)],
    8: [(entity_factory.demon_frog, 30)],
}


def get_max_val_for_floor(
    weighted_chance_floor: List[Tuple[int, int]], floor: int
) -> int:
    current = 0

    for floor_min, value in weighted_chance_floor:
        if floor_min > floor:
            break
        else:
            current = value

    return current


def get_random_entity(
    weighted_chance_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_mobs: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chance_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_vals = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_vals, k=number_of_mobs
    )

    return chosen_entities


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y

    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def place_entities(room: RectangularRoom, dungeon: GameMap, floor: int) -> None:
    number_of_mobs = random.randint(0, get_max_val_for_floor(max_mobs_floor, floor))
    number_of_items = random.randint(0, get_max_val_for_floor(max_mobs_floor, floor))

    monsters: List[Entity] = get_random_entity(enemy_chances, number_of_mobs, floor)
    items: List[Entity] = get_random_entity(item_chances, number_of_items, floor)

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    engine: Engine,
    map_width,
    map_height,
) -> GameMap:
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other) for other in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            player.place(*new_room.center, dungeon)
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.world.current_floor)

        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_loc = center_of_last_room

        rooms.append(new_room)

    return dungeon
