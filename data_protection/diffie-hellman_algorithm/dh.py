from miller_rabin_pt import probablyPrime
from math import gcd
import random

class DH:
    def __init__(self):
        self.n = self.findPrime()
        self.g = random.choice(self.primitiveRoots(self.n))
        print("Diffie-hellman algorithm\n------------------\nn = {}\ng = {}\n------------------".format(self.n, self.g))

    def proceed(self, x, y):
        print("INPUT ---->     Osoba A: x = {}\n\t\tOsoba B: y = {}\n------------------".format(x, y))
        # osoba A
        self.X = self.power(self.g, x, self.n)
        print("Osoba A: X = {}\n------------------".format(self.X))
        # osoba B
        self.Y = self.power(self.g, y, self.n)
        print("Osoba B: Y = {}\n------------------".format(self.Y))
        # osoba A
        self.kA = self.power(self.Y, x, self.n)
        print("Osoba A: k= {}\n------------------".format(self.kA))
        # osoba B
        self.kB = self.power(self.X, y, self.n)
        print("Osoba B: k = {}\n------------------".format(self.kB))

    def findPrime(self, n=random.randint(1000, 9999)):
        while(True):
            if(probablyPrime(n, accuracy=100)): return n
            else: n+=1

    # https://stackoverflow.com/questions/40190849/efficient-finding-primitive-roots-modulo-n-using-python
    def primitiveRoots(self, modulo):
        coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}
        return [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo) for powers in range(1, modulo)}]

    def power(self, x, y, p):
        res = 1
        x = x % p
        while (y > 0):
            if ((y & 1) == 1):
                res = (res * x) % p
            y = y >> 1 
            x = (x * x) % p
        return res
    
dh = DH()
dh.proceed(1337, 2420) # two integers (users input)
