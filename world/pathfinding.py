from __future__ import annotations
from collections import deque
from typing import Dict, List, Optional, Tuple

from world.map import Map
from entities.entity import Pos


def bfs_path(world: Map, start: Pos, goal: Pos) -> Optional[List[Pos]]:
    if not world.is_inside(start) or not world.is_inside(goal):
        return None

    queue = deque([start])
    came_from: Dict[Pos, Optional[Pos]] = {start: None}

    # Основной цикл
    while queue:
        current = queue.popleft()

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in world.neighbors(current):
            if neighbor not in came_from and (world.is_empty(neighbor) or neighbor == goal):
                queue.append(neighbor)
                came_from[neighbor] = current

    return None


def reconstruct_path(came_from: Dict[Pos, Optional[Pos]], end: Pos) -> List[Pos]:
    """ Восстанавливает путь от конца к началу, используя словарь came_from"""
    path = [end]
    while came_from[end] is not None:
        end = came_from[end]
        path.append(end)
    path.reverse()
    return path