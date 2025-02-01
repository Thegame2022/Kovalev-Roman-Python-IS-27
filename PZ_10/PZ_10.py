#Книжные магазины предлагают следующие коллекции книг.
#Магистр – Лермонтов, Достоевский, Пушкин, Тютчев
#ДомКниги – Толстой, Грибоедов, Чехов, Пушкин.
#БукМаркет – Пушкин, Достоевский, Маяковский.
#Галерея – Чехов, Тютчев, Пушкин.
#Определить:
#1.в каких магазинах можно одновременно приобрести книги Достоевского и Пушкина.
#2.в ассортимент магазина ДомКниги добавить автора Лермонтов.
#3.какие книги из магазина БукМаркет отсутствуют в магазине Магистр.2
Lermontov = { 'Magistr' }
Dostoevskiy = { 'Magistr', 'BucMarket'}
Pushkin = { 'Magistr', 'DomKnigi', 'BucMarket', 'Galereya'}
Tutchev = { 'Magistr', 'Galereya' }
Tolstoy = { 'DomKnigi' }
Griboedov = { 'DomKnigi' }
Chehov = { 'DomKnigi', 'Galereya' }
Mayakovskiy = { 'BucMarket' }
print(Dostoevskiy&Pushkin)
Lermontov.add('DomKnigi')
print(Lermontov)
BucMarket = { 'Пушкин', 'Достовеский', 'Маяковский'}
Magistr = { 'Лермонтов', 'Достоевский', 'Пушкин', 'Тютчев'}
print(BucMarket-Magistr)