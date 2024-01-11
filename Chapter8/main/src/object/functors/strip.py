"""
Класс-функтор. Всякий раз, когда будет вызываться экземпляр этого функтора, он будет возвращать полученную строку
с отброшенными значениями, заданными при инициализации
"""

class Strip:
    def __init__(self, characters):
        self.characters = characters

    def __call__(self, string):
        return string.strip(self.characters)

def make_strip_function(characters):
    def strip_function(string):
        return string.strip(characters)
    return strip_function

if __name__ == "__main__":
    import doctest

    doctest.testmod()
