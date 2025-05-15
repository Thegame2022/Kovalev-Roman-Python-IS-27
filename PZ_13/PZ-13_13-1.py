#Для каждой строки матрицы с нечетным номером найти среднее арифметическое ее
#элементов.
import random
#Ввод количества строк
n = int(input("Введите количество строк: "))
#Матрица созданная через random
matrix = list(map(lambda _: list(map(lambda _: random.randint(1,10), range(3))), range(n)))
#Нахождение среднего значения
averages = list(map(lambda r: sum(r)/len(r), map(lambda x: x[1], filter(lambda i: i[0] % 2 == 0, enumerate(matrix)))))
#Вывод матрицы
print(matrix)
#Вывод среднего арифметического из строк с нечетным номером
print(averages)