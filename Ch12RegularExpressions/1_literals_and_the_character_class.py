import re

text = "Карта map и объект bitmap - это разные вещи"

#1. Простое нахождение подстроки
match = re.findall("map", text)
print(match)

#2. Простое нахождение целого слова
match = re.findall("\\bmap\\b", text)
print(match)
#или
match = re.findall(r"\bmap\b", text)
print(match)

#3. Выделение со скобками
text = "(еда), беда, победа"
match = re.findall(r"\(еда\)", text)
print(match)

#4.Символьный класс
text = "Еда, беду, победа"
match = re.findall(r"[еЕ]д[ау]", text)
print(match)

text = "Еда, беду, 5 победа"
match = re.findall(r"[0123456789]", text)
print(match)
#или
match = re.findall(r"[0-9]", text)
print(match)
#Инвертация поиска (поиск не цифры)
match = re.findall(r"[^0-9]", text)
print(match)
#поиск малых букв
match = re.findall(r"[а-я]", text)
print(match)
#Поиск нескольких диапазонов
match = re.findall(r"[а-яА-Я0-9]", text)
print(match)
#Поиск со скобкой
text = "(еда), еда, победа"
match = re.findall(r"[(]еда[)]", text)
print(match)
"""
Символ              Значение
.                   Соответствует любому символу, кроме символа переноса строки (‘\n’). 
                    Но, если установлен флаг re.DOTALL, то точка соответствует вообще любому символу в тексте. 
                    Однако, если она записана внутри символьного класса [.], то воспринимается как символ точки.

\d                  Соответствует любой цифре, если используется кодировка Юникода. 
                    Если же установлен флаг re.ASCII, то диапазону цифр [0-9].

\D                  Соответствует любому не цифровому символу для Юникода или символьному классу
                    [^0-9] при установленном флаге re.ASCII

\s                  Для Юникода – любой пробельный символ. Для re.ASCII – символьному классу [ \t\n\r\f\v]

\S                  Для Юникода – любой не пробельный символ. Для re.ASCII – символьному классу [^ \t\n\r\f\v]

\w                  Для Юникода – любой символ слова. При флаге re.ASCII – набору символов [a-zA-Z0-9_]

\W                  Для Юникода – любой не символ слова. При флаге re.ASCII – набору символов [^a-zA-Z0-9_]
"""
#Поиск всех символов строки
text = "(еда), еда, победа"
match = re.findall(r".", text)
print('. :' + str(match))
#Поиск только символов слов
match = re.findall(r"\w", text)
print('\w :' + str(match))
#Пустой список из-за юникода
match = re.findall(r"\w", text, re.ASCII)
print('\w + re.ASCII:' + str(match))
#Шестнадцатиричные символы из строки
text = "0xf, 0xa, 0x5"
match = re.findall(r"0x[\da-fA-F]", text)
print('Шеснадцатиричные символы из строки:' + str(match))