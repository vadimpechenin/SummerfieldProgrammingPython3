import math

def main():
    #1. Простой способ выполнить выражение
    x = eval("(2 ** 31) - 1") # x== 2147483647
    print(x)
    #2. Создание функции динамически
    code = '''
def area_of_sphere(r):
    return 4 * math.pi * r ** 2
    '''
    context = {}
    context["math"] = math
    exec(code, context) #Создание объекта-функции area_of_sphere в словаре context
    area_of_sphere = context["area_of_sphere"]
    area = area_of_sphere(5) #314.1592653589793
    print(area)

main()