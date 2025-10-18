from __future__ import annotations
from typing import List
import random
from abc import ABC, abstractmethod

from .entity import Entity, Pos
from .static_objects import Grass


class Creature(Entity, ABC):
    """Абстрактный класс для всех живых существ"""
    def __init__(self, pos: Pos, hp: int, speed: int):
        super().__init__(pos)
        self.hp = hp
        self.speed = speed
        self.last_action = 'родился' # Последне действие

    @property
    def is_alive(self) -> bool:
        """Возвращает True, если существо живое"""
        return self.hp > 0

    @abstractmethod
    def make_move(self, world: "Map", log: list[str]):
        """Абстрактный метод, определяющий, что делает существо за один ход"""
        pass


class Herbivore(Creature):
    """🐄 Травоядное - ищет и есть траву"""
    def __init__(self, pos: Pos, hp: int = 10, speed: int = 1):
        super().__init__(pos, hp, speed)

    @property
    def symbol(self) -> str:
        return '🐄'

    def make_move(self, world: "Map", log: List[str]):
        from world.pathfinding import bfs_path  # отложенный импорт, чтобы не было циклических ссылок
        target = world.find_nearest(self.pos, Grass)

        if not target:
            self._random_step(world, log)
            return

        path = bfs_path(world, self.pos, target.pos)
        if not path:
            self._random_step(world, log)
            return

        if len(path) <= 2:
            # стоит рядом с травой — ест
            self.hp += target.nutrition
            world.remove_entity(target)
            log.append(f"🐄 на {self.pos} съел 🌿 на {target.pos} (+{target.nutrition} HP)")
        else:
            new_pos = path[1]
            if world.is_empty(new_pos):
                world.move_entity(self, new_pos)
                log.append(f"🐄 идёт к 🌿: {self.pos} → {new_pos}")
            else:
                self._random_step(world, log)

    def _random_step(self, world: "Map", log: List[str]):
        """Случайное движение, если нет цели."""
        free = [p for p in world.neighbors(self.pos) if world.is_empty(p)]
        if free:
            new = random.choice(free)
            world.move_entity(self, new)
            log.append(f"🐄 блуждает: {self.pos} → {new}")


class Predator(Creature):
    """🦁 Хищник - охотится и атакует травоядных"""
    def __init__(self, pos: Pos, hp: int = 15, speed: int = 1, attack: int = 5):
        super().__init__(pos, hp, speed)
        self.attack = attack

    @property
    def symbol(self) -> str:
        return "🦁"

    def make_move(self, world: "Map", log: List[str]):
        from world.pathfinding import bfs_path

        prey = world.find_nearest(self.pos, Herbivore)
        if not prey:
            self._random_step(world, log)
            return

        path = bfs_path(world, self.pos, prey.pos)
        if not path:
            self._random_step(world, log)
            return

        if len(path) <= 2:
            # атака
            prey.hp -= self.attack
            log.append(f"🦁 атакует 🐄 на {prey.pos} (HP жертвы = {prey.hp})")
            if prey.hp <= 0:
                world.remove_entity(prey)
                log.append(f"🦁 съел 🐄 на {prey.pos}")
        else:
            new_pos = path[1]
            if world.is_empty(new_pos):
                world.move_entity(self, new_pos)
                log.append(f"🦁 движется к 🐄: {self.pos} → {new_pos}")
            else:
                self._random_step(world, log)

    def _random_step(self, world: "Map", log: List[str]):
        """Случайное движение, если нет жертвы."""
        free = [p for p in world.neighbors(self.pos) if world.is_empty(p)]
        if free:
            new = random.choice(free)
            world.move_entity(self, new)
            log.append(f"🦁 блуждает: {self.pos} → {new}")