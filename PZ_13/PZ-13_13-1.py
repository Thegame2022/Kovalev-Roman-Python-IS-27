from functools import reduce
#Вычисление среднего арифметического
sz = lambda lst: sum(lst) / len(lst)
#Ввод строк матрицы
def input_matrix():
    return[list(map(int, input(f"Строка {i+1}: ").split())) for i in range(int(input("Количество строк: ")))]
#Рассчет среднего арифметического для нечетных строк
def odd_rows(matrix):
    return list(map(lambda row: sz(row[1]), filter(lambda row: row[0] % 2 == 1,enumerate(matrix, 1))))
#Проверка кода на запуск напрямую
if __name__ == "__main__":
    #Ввод матрицы
    matrix = input_matrix()
    print("Средние значения нечетных строк: ", odd_rows(matrix))