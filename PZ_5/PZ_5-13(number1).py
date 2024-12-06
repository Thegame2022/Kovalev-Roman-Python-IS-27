#Найти сумму чисел ряда 1,2,3,...,60 с использованием функции нахождения суммы.
#Использовать локальные переменные.
def sum_of_series(sumber):
    #Проверка на рпавильность введенных данных
    if not isinstance(sumber, int) or sumber < 1:
        raise ValueError("Входное значение должно быть целым числом больше или равным 1.")
    #Локальная переменная для хранения суммы
    total_sum = 0
    #Цикл для суммирования чисел от 1 до n
    for i in range(1, sumber + 1):
        total_sum += i
    return total_sum
try:
    #Задаем sumber
    sumber = 60
    #Вызывае функцию для нахождения суммы чисел от 1 до sumber
    result = sum_of_series(sumber)
    print("Сумма чисел от 1 до", sumber, ":", result)
except ValueError as e:
    print("Ошибка:", e)