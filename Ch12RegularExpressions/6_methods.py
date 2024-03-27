"""
Методы re.match, re.split, re.sub, re.subn, re.compile
"""
import re


#1. re.match(pattern, string, flags)
# который определяет совпадение шаблона pattern в начале строки string с учетом флагов flags (если они указаны).
# Он возвращает объект совпадения re.Match, либо значение None, если шаблон не был найден.
#Пусть в строке ожидается номер телефона в формате:
#+7(xxx)xxx-xx-xx

text = "+7(123)456-78-90"
m = re.match(r"\+7\(\d{3}\)\d{3}-\d{2}-\d{2}", text)
print(m)

#2. re.split(pattern, string, flags)
# выполняет разбивку строки string по заданному шаблону pattern.
text = """<point lon="40.8482" lat="52.6274" />
<point lon="40.8559" lat="52.6361" />; <point lon="40.8614" lat="52.651" />
<point lon="40.8676" lat="52.6585" />, <point lon="40.8672" lat="52.6626" />
"""
#Требуется получить множество строк, которые разделяются между собой или переносом строки (\n), или символами ; и ,.
ar = re.split(r"[\n;,]+", text)
print(ar)

#3. re.sub(pattern, repl, string, count, flags)
# -pattern – регулярное выражение;
# -repl – строка или функция для замены найденного выражения;
# -string – анализируемая строка;
# -count – максимальное число замен (если не указано, то неограниченно);
# -flags – набор флагов (по умолчанию не используются).
#Выполняет замену в строке найденных совпадений строкой или результатом работы функции repl и возвращает преобразованную строку.
text = """Москва
Казань
Тверь
Самара
Уфа"""

#Преобразуем в список формата HTML
list = re.sub(r"\s*(\w+)\s*", r"<option>\1</option>\n", text)
print(list)

#Но, кроме строки можно передавать ссылку на функцию, которая должна возвращать строку, подставляемую вместо найденного вхождения.
# Например, добавим тегам option атрибут value:
count = 0
def replFind(m):
    global count
    count += 1
    return f"<option value='{count}'>{m.group(1)}</option>\n"

list2 = re.sub(r"\s*(\w+)\s*", replFind, text)
print(list2)

#4. subn(pattern, repl, string, count, flags)
# Возвращает не только преобразованную строку, но и число произведенных замен
list, total = re.subn(r"\s*(\w+)\s*", r"<option>\1</option>\n", text)
print(list, total)

#5. re.compile(pattern, flags)
#выполняет компиляцию регулярного выражения и возвращает его в виде экземпляра класса Pattern.
count = 0
def replFind(m):
    global count
    count += 1
    return f"<option value='{count}'>{m.group(1)}</option>\n"

rx = re.compile(r"\s*(\w+)\s*")
list, total = rx.subn(r"<option>\1</option>\n", text)
list2 = rx.sub(replFind, text)
print(list, total, list2, sep="\n")