from __future__ import annotations
from typing import Dict, List, Tuple, Optional, Type, TypeVar

from entities.entity import Entity, Pos


# Универсальный тип для find_nearest
T = TypeVar('T', bound=Entity)


class Map:
    """Класс, представляющий двумерный мир"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Храним сущность как словарь {позиция: объект}
        self._entities: Dict[Pos, Entity] = {}

    # ----------------------------
    # Методы работы с содержимым карты
    # ----------------------------

    def add_entity(self, entity: Entity):
        """Добавляет объект в мир"""
        if entity.pos in self._entities:
            raise ValueError(f'Клетка {entity.pos} уже занята')
        self._entities[entity.pos] = entity

    def remove_entity(self, entity: Entity):
        """Удаляет объект с карты"""
        if entity.pos in self._entities:
            del self._entities[entity.pos]

    def move_entity(self, entity: Entity, new_pos: Pos):
        """Перемещает объект по карте"""
        if not self.is_inside(new_pos):
            return
        if not self.is_empty(new_pos):
            return
        del self._entities[entity.pos]
        entity.pos = new_pos
        self._entities[new_pos] = entity

    # ----------------------------
    # Проверки
    # ----------------------------

    def is_inside(self, pos: Pos) -> bool:
        """Проверяет, находится ли клетка в пределах карты"""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_empty(self, pos: Pos) -> bool:
        """True, если клетка пустая"""
        return pos not in self._entities

    # ----------------------------
    # Доступ к соседям
    # ----------------------------

    def neighbors(self, pos: Pos) -> List[Pos]:
        """Возвращает список соседних координат (вверх, вниз, влево, вправо)"""
        x, y = pos
        candidates = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [p for p in candidates if self.is_inside(p)]

    # ----------------------------
    # Поиск объектов
    # ----------------------------

    def find_nearest(self, start: Pos, target_type: Type[T]) -> Optional[T]:
        """Возвращает ближайший объект заданного типа или None, если ничего не найдено"""
        if not self._entities:
            return None

        sx, sy = start
        nearest_entity = None
        min_dist = float('inf')

        for e in self._entities.values():
            if isinstance(e, target_type):
                ex, ey = e.pos
                dist = abs(sx - ex) + abs(sy - ey)
                if dist < min_dist:
                    min_dist = dist
                    nearest_entity = e

        return nearest_entity

    # ----------------------------
    # Рендер
    # ----------------------------

    def render(self) -> str:
        """Возвращает строковое представление карты"""
        lines = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                entity = self._entities.get((x, y))
                row.append(entity.symbol if entity else '▫️')
            lines.append(''.join(row))
        return '\n'.join(lines)

    # ----------------------------
    # Служебные методы
    # ----------------------------

    def entities(self) -> List[Entity]:
        """Возвращает список объектов"""
        return list(self._entities.values())

    def __repr__(self):
        return f'Map({self.width}x{self.height}, entities={len(self._entities)})'