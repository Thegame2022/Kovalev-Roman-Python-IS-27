#Создайте базовый класс "Человек" со свойствами "имя", "возраст" и "пол". От этого
#класса унаследуйте классы "Мужчина" и "Женщина" и добавьте в них свойства,
#связанные с социальным положением (например, "семейное положение",
#"количество детей" и т.д.).
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

class Man(Person):
    def __init__(self, name, age, marital_status=None, children=0):
        super().__init__(name, age, gender="мужской")
        self.marital_status = marital_status #Семейное положение
        self.children = children #Количество детей

class Woman(Person):
    def __init__(self, name, age, marital_status=None, children=0):
        super().__init__(name, age, gender="женский")
        self.marital_status = marital_status #Семейное положение
        self.children = children #Количество детей

man = Man("Иван", 30, "женат", 2)
print(f"Имя: {man.name}, Возраст: {man.age}, Пол: {man.gender}, Статус: {man.marital_status}, Дети: {man.children}")

woman = Woman("Мария", 28, "не замужем", 1)
print(f"Имя: {woman.name}, Возраст: {woman.age}, Пол: {woman.gender}, Статус: {woman.marital_status}, Дети: {woman.children}")