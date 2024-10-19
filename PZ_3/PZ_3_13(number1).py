# 1. Даны три целых числа: A, B, C. Проверить истинность высказывания: «Хотя бы одно
# из чисел A, B, C положительное»
(lambda a, b, c:
 print('True' if ((a > 0) and (b <= 0) and (c <= 0)) or ((a <= 0) and (b > 0) and (c <= 0)) or
                 ((a <= 0) and (b <= 0) and (c > 0)) else 'False'))(int(input()), int(input()), int(input()))
