#1. Для каждой строки матрицы с нечетным номером найти среднее арифметическое ее
#элементов.
from functools import reduce
import random
if __name__ == "__main__":
    rows = min(int(input("Количество строк: ")), 10)
    generated_strings = [[random.randint(1, 100) for _ in range(random.randint(1, 10))]for _ in range(rows)]
    print("\nСгенерированные строки:")
    list(map(lambda i_str: print(f"Строка {i_str[0] + 1}: {', '.join(map(str, i_str[1]))}"),enumerate(generated_strings)))
    averages = list(map(lambda s: reduce(lambda a, b: a + b, s) / len(s),map(lambda i_str: i_str[1],filter(lambda i_str: (i_str[0] + 1) % 2 == 1,enumerate(generated_strings)))))
    print("\nСреднее значение нечетных строк:", averages)