from __future__ import annotations
import time
from typing import List, Callable

from world.map import Map


class Simulation:
    """
    Главный класс симуляции.
    Управляет состоянием мира, обработкой каждого хода, визуализацией и логами.
    """

    def __init__(self, world: Map):
        self.world = world  # Игровая карта
        self.turn = 0  # Счётчик ходов
        self.is_running = False  # Флаг для запуска/паузы
        self.init_actions: List[Callable] = []  # Действия при инициализации
        self.turn_actions: List[Callable] = []  # Действия, выполняемые каждый ход

    # ----------------------------
    # Методы управления симуляцией
    # ----------------------------

    def start(self, delay: float = 1.0):
        """Запускает бесконечную симуляцию с задержкой между ходами"""
        self.is_running = True
        print('🚀 Симуляция запущена!\n')
        self.run_init_actions()

        while self.is_running:
            self.next_turn()
            time.sleep(delay)

    def pause(self):
        """Приостанавливает симуляцию"""
        self.is_running = False
        print('⏸️ Симуляция приостановлена')

    # ----------------------------
    # Основной цикл
    # ----------------------------

    def next_turn(self):
        """Выполняет один ход симуляции"""
        self.turn += 1
        log: List[str] = []

        print(f'\n====== ХОД {self.turn} =======')

        # Выполняем все действия, запланированные на каждый ход
        for action in self.turn_actions:
            action(self.world, log)

        # Отображаем текущее состояние карты
        print(self.world.render())

        # Логируем действия
        print('\n📜 Действия за ход:')
        if log:
            for line in log:
                print("  •", line)
        else:
            print('  (Ничего не произошло)')

        # Выводим статистику
        print(f'Всего сущностей: {len(self.world.entities())}')

    # ----------------------------
    # Действия
    # ----------------------------

    def run_init_actions(self):
        """Выполняет все действия, запланированные перед стартом симуляции"""
        for action in self.init_actions:
            action(self.world, [])
        print('✅ Мир инициализирован!')

    def add_init_action(self, action: Callable):
        """Добавляет действие в список инициализаций"""
        self.init_actions.append(action)

    def add_turn_action(self, action: Callable):
        """Добавляет действие, выполняемое каждый ход"""
        self.turn_actions.append(action)