import re

#1. Выделить шестнадцатеричное число #xxxxxx
text = "<font color=#CC0000>"
match = re.search(r"#[\da-fA-F]{6}\b", text)
print(match)

#2. Свойства и методы объекта re.Match
#Две сохраняющие скобки - для атрибута и для значения
match = re.search(r"(\w+)=(#[\da-fA-F]{6})\b", text)
print(match.groups())

#индекс последней группы: match.lastindex

# Позиции начала и конца группы:
# match.start(1)
# match.end(1)

#получить сразу кортеж с начальной и конечной позициями для каждой группы:
#match.span(0)
#match.span(1)

#Для определения первого и последнего индексов, в пределах которых осуществлялась проверка в тексте, служат свойства:
# match.endpos
# match.pos

#Cвойство re возвращает скомпилированное регулярное выражение:
# pattern = match.re

#Свойство string содержит анализируемую строку.
#match.string

# 3. Реализация шаблона для опредления двух именованных групп: key и value
match = re.search(r"(?P<key>\w+)=(?P<value>#[\da-fA-F]{6})\b", text)
#Получение словаря из групп
print(match.groupdict())

# Формирование строки с помощью метода expand
print(match.expand(r"\g<key>:\g<value>"))


#4. Методы re.search, re.finditer и re.findall
"""
re.search(pattern, string, flags)
pattern – регулярное выражение;
string – анализируемая строка;
flags – один или несколько флагов.
"""
text = "<font color=#CC0000 bg=#ffffff>"
match = re.search(r"(?P<key>\w+)=(?P<value>#[\da-fA-F]{6})\b", text)
print(match.groups())

"""
Поиск всех совпадений
re.finditer(pattern, string, flags)
"""
for m in re.finditer(r"(?P<key>\w+)=(?P<value>#[\da-fA-F]{6})\b", text):
    print(m.groups())

"""
Получить лишь список найденных вхождений, групп
re.findall(pattern, string, flags)
"""
match = re.findall(r"(?P<key>\w+)=(?P<value>#[\da-fA-F]{6})\b", text)
print(match)