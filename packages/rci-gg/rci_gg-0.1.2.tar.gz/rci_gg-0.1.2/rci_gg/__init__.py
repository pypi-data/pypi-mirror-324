"""
Библиотека для просмотра кода по ячейкам

from rci import RCI

rci = RCI()
print(rci.get_imports())  # Должен вывести общий импорт
print(rci.get_cell(1, 1, 0))  # Должен вывести первую ячейку первой задачи

help(rci.get_imports)
help(rci.get_cell)

"""

from .core import RCI
