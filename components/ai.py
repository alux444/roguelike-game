from __future__ import annotations

from typing import List, Tuple

import numpy as np
import tcod

from actions import Action
from components.base_component import BaseComponent


class BaseAi(Action, BaseComponent):
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        # path to target position, if none, return empty list
        cost = np.array(self.entity.map.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.map.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))

        return [(index[0], index[1]) for index in path]
