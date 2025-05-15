#В двумерном списке найти максимальный положительный элемент, кратный 4
import random
#Ввод количества строк
n = int(input("Введите количество строк: "))
#Матрица созданная через random
matrix = list(map(lambda _: list(map(lambda _: random.randint(-100, 100), range(3))), range(n)))
#Фильтрация по условию положительно,кратно 4
filtered = list(filter(lambda x: x > 0 and x % 4 == 0, sum(matrix, [])))
#Вывод матрицы
print(matrix)
#Вывод максимального значения после фильтрации
print(max(filtered) if filtered else None)