from __future__ import annotations
import random
from typing import List

from entities.creatures import Creature
from entities.static_objects import Grass
from world.map import Map


def move_all_creatures(world: Map, log: List[str]):
    """Все живые существа делают свой ход"""
    creatures = [e for e in world.entities() if isinstance(e, Creature)]

    for creature in creatures:
        if creature.is_alive:
            creature.make_move(world, log)
        else:
            world.remove_entity(creature)
            log.append(f'☠️ {creature.symbol} умер на {creature.pos}')


def spawn_grass_randomly(world: Map, log: List[str], chance: float = 0.003):
    """Случайно вырастает новая трава"""
    empty_cells = [
        (x, y)
        for x in range(world.width)
        for y in range(world.height)
        if world.is_empty((x, y))
    ]

    for pos in empty_cells:
        if random.random() < chance:
            world.add_entity(Grass(pos))
            log.append(f'🌱 На {pos} выросла новая трава!')


def cleanup_dead(world: Map, log: List[str]):
    """Удаляет все мертвые существа"""
    for entity in list(world.entities()):
        if isinstance(entity, Creature) and not entity.is_alive:
            world.remove_entity(entity)
            log.append(f'💀 {entity.symbol} удалён с карты (мертв)')


def world_statistics(world: Map, log: List[str]):
    """Вывод статистики о мире"""
    total = len(world.entities())
    herbivores = sum(1 for e in world.entities() if e.symbol == '🐄')
    predators = sum(1 for e in world.entities() if e.symbol == '🦁')
    grass = sum(1 for e in world.entities() if e.symbol == '🌿')

    log.append(f"📊 Всего: {total}, 🐄={herbivores}, 🦁={predators}, 🌿={grass}")