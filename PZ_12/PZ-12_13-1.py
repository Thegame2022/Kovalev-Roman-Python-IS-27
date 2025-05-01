#1.Проверить есть ли в последовательности целых N чисел число K
import random
numbers = [random.randint(1, 100) for _ in range(10)]
kd = int(input("Введите число:"))
#Функция проверяющая наличие k
kp = lambda seq, k: k in seq
#Применение функции
proverka = kp(numbers, kd)
#Вывд результата в консоль
print(f"Число {kd} присутствует: {proverka}")