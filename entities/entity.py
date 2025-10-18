from  __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod


Pos = Tuple[int, int]


class Entity(ABC):
    """Базовый абстрактный метод для всех сущностей мира"""

    def __init__(self, pos: Pos):
        self.pos = pos

    @property
    @abstractmethod
    def symbol(self) -> str:
        """Абстрактное свойство — каждый наследник обязан определить свой символ"""
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(pos={self.pos})'