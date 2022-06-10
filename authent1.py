import random as r

class security:
    def __init__(self):
        pass

    def key(self):
        lower1 = "abcdefghijklmnopqrstuvwxyz"
        upper1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        number1 = "0123456789"
        symbols = "@#$*"

        all = lower1 + upper1 + number1 + symbols
        len1 = 10

        key = "".join(r.sample(all, len1))

        return key


obj = security()
# print(type(obj.key()))
