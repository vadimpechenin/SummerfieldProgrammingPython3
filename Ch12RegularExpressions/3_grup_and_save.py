import re

#Просто выделяем ключи и данные
text = "lat = 5, lon = 7, a = 10"

match = re.findall(r"\w+\s*=\s*\d+", text)
print("проcто выделялем ключ + значение: \n" + str(match))

#Учет только ключей lat и lon
#В лоб
match = re.findall(r"lat\s*=\s*\d+|lon\s*=\s*\d+", text)
print("выделяем только ключ + значение с определенными ключами в лоб: \n" + str(match))

#Группирующие скобки
match = re.findall(r"(?:lat|lon)\s*=\s*\d+", text)
print("выделяем только ключ + значение с использованием группировки и ?:(не сохраняющие): \n" + str(match))

match = re.findall(r"(lat|lon)\s*=\s*\d+", text)
print("выделяем только ключ с использованием группировки и (сохраняющими скобками): \n" + str(match))

match = re.findall(r"((lat|lon)\s*=\s*\d+)", text)
print("выделяем ключ + значение и ключи с использованием двойных сохраняющих скобок: \n" + str(match))

match = re.findall(r"(lat|lon)\s*=\s*(\d+)", text)
print("выделяем и сохраняем отдельно ключи и значения: \n" + str(match))

#Выделение атрибута src у тэга img
text = "<p>Картинка <img src='bg.jpg'> в тексте</p>"
match = re.findall(r"<img\s+[^>]*src=[\"'](.+?)[\"']", text)
print("выделяем тэг img: \n" + str(match))

text = "<p>Картинка <img src='bg.jpg'> в тексте</p>"
match = re.findall(r"<img\s+[^>]*src=([\"'])(.+?)\1", text)
print("выделяем тэг img, /1 - поставить значение 1-й сохраняющей скобки (): \n" + str(match))

#Назначение имен сохранающей скобки
#(?P<name>...)   обращение - (?P=name)
match = re.findall(r"(<img)\s+[^>]*src=(?P<q>[\"'])(.+?)(?P=q)", text)
print("выделяем тэг img, использование обращения по имени группирующей скобки: \n" + str(match))
