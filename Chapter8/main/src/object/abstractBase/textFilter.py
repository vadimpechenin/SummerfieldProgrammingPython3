"""
Реализован абстрактный базовый класс TextFilter- функтор, выполняющего фильтрацию текста
>>> vowel_counter = CharCounter()
>>> vowel_counter("dog fish and cat fish", "aeiou")     # returns: 5
5
>>> vowel_counter("there's too many junk lawsuits suing too many doctors",
...               "aeiouAEIOU")
16
>>> text = "The Title\\n=========\\nThe text\\n"
>>> rle_encoder = RunLengthEncode()
>>> rle = rle_encoder(text)
>>> rle, len(rle), len(text)
(b'The Title\\n\\x00\\t=\\nThe text\\n', 23, 29)
>>> rle_decoder = RunLengthDecode()
>>> string = rle_decoder(rle)
>>> string, len(string), string == text
('The Title\\n=========\\nThe text\\n', 29, True)
>>> text = "=============++++++++++--------------"
>>> rle = rle_encoder(text)
>>> rle, len(rle), len(text)
(b'\\x00\\r=\\x00\\n+\\x00\\x0e-', 9, 37)
>>> rle_decoder(rle) == text
True
"""

import abc


class TextFilter(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def is_transformer(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self):
        raise NotImplementedError()


class CharCounter(TextFilter):
    # не преобразователь, т.к. не изменяет заданный текст. Возвращает количество указанных символов в тексте
    @property
    def is_transformer(self):
        return False

    def __call__(self, text, chars):
        count = 0
        for c in text:
            if c in chars:
                count += 1
        return count


class RunLengthEncode(TextFilter):
    # преобразователь, в строке байтов в кодировке UTF-8 замещает байты 0х00 последовательностью 0х00, 0х01, 0х00,
    # и любые последовательности, содержащие от трех до 255 одинаковых байтов, - последовательностями 0х00, количество, байт.
    @property
    def is_transformer(self):
        return True

    def __call__(self, utf8_string):
        byte = None
        count = 0
        binary = bytearray()
        for b in utf8_string.encode("utf8"):
            if byte is None:
                if b == 0:
                    binary.extend((0, 1, 0))
                else:
                    byte = b
                    count = 1
            else:
                if byte == b:
                    count += 1
                    if count == 255:
                        binary.extend((0, count, b))
                        byte = None
                        count = 0
                else:
                    if count == 1:
                        binary.append(byte)
                    elif count == 2:
                        binary.extend((byte, byte))
                    elif count > 2:
                        binary.extend((0, count, byte))
                    if b == 0:
                        binary.extend((0, 1, 0))
                        byte = None
                        count = 0
                    else:
                        byte = b
                        count = 1
        if count == 1:
            binary.append(byte)
        elif count == 2:
            binary.extend((byte, byte))
        elif count > 2:
            binary.extend((0, count, byte))
        return bytes(binary)


class RunLengthDecode(TextFilter):
    #Принимает строку байтов, созданную классом RunLingthEncode, и возвращает оригинальную строку
    @property
    def is_transformer(self):
        return True

    def __call__(self, rle_bytes):
        binary = bytearray()
        length = None
        for b in rle_bytes:
            if length == 0:
                length = b
            elif length is not None:
                binary.extend([b for x in range(length)])
                length = None
            elif b == 0:
                length = 0
            else:
                binary.append(b)
                length = None
        if length:
            binary.extend([b for x in range(length)])
        return binary.decode("utf8")


if __name__ == "__main__":
    text = "The Story\n=========\n\nOnce upon a time..."
    rle_encoder = RunLengthEncode()
    rle_text = rle_encoder(text)
    rle_decoder = RunLengthDecode()
    original_text = rle_decoder(rle_text)
    assert text == original_text

    import doctest

    doctest.testmod()