#Дано целое число N (> 1). Вывести наименьшее из целых чисел K, для которых
#сумма 1 + 2 + . . . + K будет больше или равна N, и саму эту сумму.
def find_min_k_and_sum(n):
    k = 0
    total_sum = 0
    # Ищем наименьшее K
    while total_sum < n:
        k += 1
        total_sum += k
    return k, total_sum
while True:  # Начинаем бесконечный цикл
    try:
        # Ввод целого числа N
        N = int(input("Введите целое число N (> 1): "))
        if N <= 1:
            raise ValueError("N должно быть больше 1.")
        # Находим K и сумму
        K, total_sum = find_min_k_and_sum(N)
        # Выводим результаты
        print(f"Наименьшее K: {K}")
        print(f"Сумма 1 + 2 + ... + {K} = {total_sum}")
        break  # Выход из цикла, если все прошло успешно
    except ValueError as e:
        print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")