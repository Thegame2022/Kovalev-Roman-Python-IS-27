#2. В двумерном списке найти максимальный положительный элемент, кратный 4.
from itertools import chain
from random import randint
matrix = [[randint(-50, 50) for _ in range(3)] for _ in range(3)]
print("Сгенерированная матрица:")
print('\n'.join(' '.join(f"{num:3}" for num in row) for row in matrix))
result = (max(filter(lambda x: x > 0 and x % 4 == 0,chain.from_iterable(matrix))) if any(x > 0 and x % 4 == 0 for row in matrix for x in row) else None)
print("\nМаксимальный положительный элемент кратный 4:", result)