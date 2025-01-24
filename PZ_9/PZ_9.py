#Организовать словарь 10 русско-английских слов, обеспечивающий "перевод" русского слова на английского.
ruan = {
    "привет": "hello",
    "дом": "house",
    "дерево": "tree",
    "собака": "dog",
    "кошка": "cat",
    "книга": "book",
    "машина": "car",
    "компьютер": "computer",
    "человек": "human",
    "город": "city"
}
while True:
    enter = input("Введите русское слово для перевода: ").strip().lower()
    if enter == 'e':
        break
    if enter in ruan:
        translate = ruan[enter]
        print(f"Перевод слова {enter} - {translate}")
    else:
        print(f"Слово {enter} не найдено")
