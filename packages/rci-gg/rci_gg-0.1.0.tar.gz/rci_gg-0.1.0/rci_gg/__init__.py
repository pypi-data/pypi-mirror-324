"""
Библиотека для просмотра кода по ячейкам

Функции: get_imports(), get_cell(topic, task, cell)

help(rci.get_imports)
help(rci.get_cell)

from rci import RCI

rci = RCI()
print(rci.get_imports())  # Должен вывести общий импорт
print(rci.get_cell(1, 1, 0))  # Должен вывести первую ячейку первой задачи

"""

from .core import RCI
