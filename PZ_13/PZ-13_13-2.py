from itertools import chain
#Ввод строк матрицы
def input_matrix():
    return[list(map(int, input(f"Строка {i+1}: ").split())) for i in range(int(input("Количество строк: ")))]
#Функция для нахождения положительных элементов кратных 4
def multiple_4(matrix):
    #Фильтрация максимального элемента кратного 4
    filtr_numbers = filter(lambda x: x > 0 and x % 4 == 0, chain.from_iterable(matrix))
    #Преобразование в список для проверки наличия элементов
    filtr_list = list(filtr_numbers)
    #Если в списке есть элементы возвращается максимальный,если нет то None
    return max(filtr_list) if filtr_list else None
def main():
    #Ввод матрицы
    matrix = input_matrix()
    #Вывод матрицы для видимости
    print("\nВведеная матрица:")
    for row in matrix:
        print(row)
    #Поиск максимального элемента кратного 4
    result = multiple_4(matrix)
    #Вывод результата с проверкой
    if result is not None:
        print(f"\nМаксимальный элемент кратный 4: {result}")
    else:
        print("\nВ матрице нет элементов кратных 4")
#Проверка кода на запуск напрямую
if __name__ == "__main__":
    main()