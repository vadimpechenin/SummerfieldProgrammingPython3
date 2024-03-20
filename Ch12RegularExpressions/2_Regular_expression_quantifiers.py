"""
В общем виде квантификаторы записываются (без пробелов):
{m,n}

где m – минимальное число совпадений с выражением; n – максимальное число совпадений с выражением.

"""

import re

text = "Google, Gooogle, Goooooogle"
match = re.findall(r"o{2,5}", text)

print(match)

#квантификатор находит наиболее длинные последовательности. Про такой режим еще говорят, что он жадный или мажорный.
# В противоположность ему есть другой, минорный режим работы. В этом случае ищутся последовательности минимальной длины,
# удовлетворяющие шаблону.
match = re.findall(r"o{2,5}?", text)
print(match)

"""
Квантификаторы можно записывать и в кратких формах, например:

{m} – повторение выражения ровно m раз (эквивалент {m,m});
{m,} – повторения от m и более раз;
{, n} – повторения не более n раз.
"""
text = "Google, Gooogle, Goooooogle"
match = re.findall(r"Go{2,}gle", text)
print(match)

text = "Google, Gooogle, Goooooogle"
match = re.findall(r"Go{,4}gle", text)
print(match)

#Выделение телефонного номера с первой цифрой 8 и следующими 10 цифрами
phone = "89123456789"
match = re.findall(r"8\d{10}", phone)
print(match)

"""
Для квантификаторов {0,} и {1,} существуют специальные символы:

? – от нуля до одного (аналог {0,1});
* – от нуля и до «бесконечности» (в действительности, большого числа – от 32767), соответствует квантификатору {0,};
+ – от единицы и до «бесконечности» (также большого числа – от 32767), соответствует квантификатору {1,}.
"""

text = "стеклянный, стекляный"
match = re.findall(r"стеклянн?ый", text)
print(match)

#Парсинг по ключам и значениям, получение списка
text = "author=Пушкин А.С.; title = Евгений Онегин; price =200; year= 2001"
match = re.findall(r"\w+\s*=\s*[^;]+", text)
print(match)

#Сразу выделяем в виде кортежей
match = re.findall(r"(\w+)\s*=\s*([^;]+)", text)
print(match)

# Выделить фрагмент с тегом <img …>.
text = "Картинка <img src='bg.jpg'> в тексте</p>"
#решение с минорным квантификатором
match = re.findall(r"<img.*?>", text)
print(match)
#Решение с указанием символьного класса
match = re.findall(r"<img[^>]*>", text)
print(match)
text = "<p>Картинка <img alt='картинка' src='bg.jpg'> в тексте</p>"
match = re.findall(r"<img\s+[^>]*?src\s*=\s*[^>]*>", text)
print(match)