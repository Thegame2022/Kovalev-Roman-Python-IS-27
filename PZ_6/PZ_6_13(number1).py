#Дан список A размера N. Вывести вначале его элементы с четными номерами (в
#порядке возрастания номеров), а затем — элементы с нечетными номерами (также в
#порядке возрастания номеров): A2, A4, А6, . . ., A1, A3, A5, ... . Условный оператор не
#использовать.
def print_even_and_odd_elements(A):
    try:
        #Проверка на пустой список
        if len(A) == 0:
            raise ValueError("Список пуст.")
        #Получаем элементы с четными индексами
        even_elements = A[1::2]
        #Получаем элементы с нечетными индексами
        odd_elements = A[::2]
        #Объединяем срезы и выводим результат
        result = even_elements + odd_elements
        print("Результирующий список:", result)

    except ValueError as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    try:
        #Запрашиваем ввод элементов для списка A
        B = input("Введите элементы списка A: ")
        #Если цифры введены без пробелов,то обрабатываются как отедльные цифры
        if ' ' not in B:
            A = []
            for num in B:
                A.append(int(num))
        else:
            A = B.split()
            A = list(map(int, A))

        print("Исходный список:", A)

        print_even_and_odd_elements(A)

    except ValueError as e:
        print(f"Произошла ошибка: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")



