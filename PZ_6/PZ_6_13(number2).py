#Дано число R и список размера N. Найти два соседних элемента списка, сумма
#которых наиболее близка к числу R, и вывести эти элементы в порядке возрастания
#их индексов (определение наиболее близких чисел - то есть такой элемент AK, для
#которого величина |AK - R| является минимальной).
def couple(R, A):
    if len(A) < 2:
        raise ValueError("Список должен содержать хотя бы два элемента")

    closest_pair = (A[0], A[1])  #Инициализируем начальную пару
    min_difference = abs((A[0] + A[1]) - R)

    for i in range(len(A) - 1):
        current_sum = A[i] + A[i + 1]
        difference = abs(current_sum - R)

        if difference < min_difference:
            min_difference = difference
            closest_pair = (A[i], A[i + 1])

    return sorted(closest_pair)

if __name__ == "__main__":
    try:
        #Запрашиваем у пользователя ввод числа R
        R = float(input("Введите число R: "))

        #Запрашиваем у пользователя ввод списка A
        A = list(map(int, input("Введите элементы списка A через пробел: ").split()))

        #Выводим исходный список
        print(f"Исходный список: {A}")

        #Вызываем функцию поиска ближайшей пары
        closest_pair = couple(R, A)

        #Выводим ближайшую пару
        print(f"Ближайшая пара к {R}: {closest_pair}")
    except ValueError as e:
        print(f"Произошла ошибка: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")








