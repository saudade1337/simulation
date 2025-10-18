from .entity import Entity


class StaticObject(Entity):
    """Абстрактный базовый класс для всех статических объектов мира"""
    pass


class Rock(StaticObject):
    """🪨 Камень - препятствие, блокирует клетку"""
    @property
    def symbol(self) -> str:
        return '🪨'


class Tree(StaticObject):
    """🌳 Дерево - препятствие, блокирует клетку"""
    @property
    def symbol(self) -> str:
        return '🌳'


class Grass(StaticObject):
    """🌿 Трава — ресурс, который поедают травоядные"""
    def __init__(self, pos, nutrition: int = 5):
        super().__init__(pos)
        self.nutrition = nutrition

    @property
    def symbol(self) -> str:
        return '🌿'