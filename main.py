from __future__ import annotations
import random
from entities.creatures import Herbivore, Predator
from entities.static_objects import Grass
from world.map import Map
from simulation.simulation import Simulation
from simulation.actions import move_all_creatures, spawn_grass_randomly, world_statistics, cleanup_dead


# ----------------------------
# Функция создания тестового мира
# ----------------------------

def create_test_world(width: int = 30, height: int = 30) -> Map:
    """Создаёт карту и заполняет её начальными объектами"""
    world = Map(width, height)

    # Добавляем траву 🌿
    for _ in range(10):
        pos = (random.randint(0, width - 1), random.randint(0, height - 1))
        if world.is_empty(pos):
            world.add_entity(Grass(pos))

    # Добавляем травоядных 🐄
    for _ in range(60):
        pos = (random.randint(0, width - 1), random.randint(0, height - 1))
        if world.is_empty(pos):
            world.add_entity(Herbivore(pos))

    # Добавляем хищников 🦁
    for _ in range(30):
        pos = (random.randint(0, width - 1), random.randint(0, height - 1))
        if world.is_empty(pos):
            world.add_entity(Predator(pos))

    return world


# ----------------------------
# Основной запуск симуляции
# ----------------------------

def main():
    # 1️⃣ Создаём мир
    world = create_test_world()

    # 2️⃣ Создаём симуляцию
    sim = Simulation(world)

    # 3️⃣ Добавляем "правила" — функции, выполняемые каждый ход
    sim.add_turn_action(move_all_creatures)     # все существа делают ход
    sim.add_turn_action(spawn_grass_randomly)  # появляется новая трава
    sim.add_turn_action(cleanup_dead)           # удаляем мертвых
    sim.add_turn_action(world_statistics)       # выводим статистику

    # 4️⃣ Запускаем симуляцию
    sim.start(delay=1.5)  # пауза между ходами


if __name__ == "__main__":
    main()
