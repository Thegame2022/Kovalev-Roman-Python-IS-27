#1. Средствами языка Python сформировать текстовый файл (.txt), содержащий
#последовательность из целых положительных и отрицательных чисел. Сформировать
#новый текстовый файл (.txt) следующего вида, предварительно выполнив требуемую
#обработку элементов:
#Исходные данные:
#Количество элементов:
#Индекс первого максимального элемента:
#Произведение элементов средней трети:
import math
#Создание исходного файла с последовательными положительными и отрицательными числами
with open('input(number1).txt', 'w') as file:
    file.write("1 -1 2 -2 3 -3 4 -4 5 -5 6 -6")
#Чтение данных из файла с его обработкой
with open('input(number1).txt', 'r') as file:
    numbers = list(map(int, file.read().split()))
#Количество элементов
count = len(numbers)
#Индекс первого максимального элемента
max_index = numbers.index(max(numbers))
#Произведение элементов средней трети
third = len(numbers) // 3
middle_third = numbers[third:2*third]
product = math.prod(middle_third)
#Запись результатов в новый файл
with open('output(number1).txt', 'w') as file:
    file.write("Исходные данные: " + ' '.join(map(str, numbers)) + "\n")
    file.write("Количество элементов: " + str(count) + "\n")
    file.write("Индекс первого максимального элемента: " + str(max_index) + "\n")
    file.write("Произведение элементов средней трети: " + str(product) + "\n")


