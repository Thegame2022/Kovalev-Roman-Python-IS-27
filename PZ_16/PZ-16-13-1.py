#Создайте класс "Компьютер" с атрибутами "марка", "процессор" и "оперативная
#память". Напишите метод, который выводит информацию о компьютере в формате
#"Марка: марка, Процессор: процессор, Оперативная память: память".
class Computer:
    def __init__(self, brand, processor, ram):
        self.brand = brand  #Марка компьютера
        self.processor = processor  #Процессор
        self.ram = ram  #Оперативная память

    def display_info(self):
        return f"Марка: {self.brand}, Процессор: {self.processor}, Оперативная память: {self.ram}"

comp = Computer("ASUS", "Ryzen 7 5700", "32 ГБ")
print(comp.display_info())