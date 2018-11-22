from miller_rabin_pt import probablyPrime
from fractions import gcd
from itertools import count

class RSA():
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def key_generator(self):
        print("------------------------key_generator")
        self.n = self.p*self.q
        print("n = {}".format(self.n))
        phi = (self.p-1)*(self.q-1)
        print("phi = {}".format(phi))
        self.e=None
        for i in count():
            if probablyPrime(i, accuracy=100) and gcd(phi, i) == 1:
                self.e = i
                break
            else:
                continue
        print("e = {}".format(self.e))
        self.d = None
        for i in count():
            if (self.e*i -1) % phi == 0:
                self.d = i
                break
            else:
                continue
        print("d = {}".format(self.d))

    def cipher(self, m):
        print("------------------------cipher")
        ascii_t = [ord(i) for i in m]
        # return [item ** self.e % self.n for item in ascii_t]
        return [self.power(item, self.e, self.n) for item in ascii_t]
    
    def decipher(self, c):
        print("------------------------decipher")
        # out = [item ** self.d % self.n for item in c]
        out = [self.power(item, self.d, self.n) for item in c]
        return ''.join(chr(i) for i in out)

    def power(self, x, y, p):
        res = 1
        x = x % p
        while (y > 0):
            if ((y & 1) == 1):
                res = (res * x) % p
            y = y >> 1 
            x = (x * x) % p
        return res

r = RSA(100019, 170029)                                             #1031, 2029)
r.key_generator()
input_ =  "12345abcde"*5
print("input = "+input_)
c = r.cipher(input_)
print(c)
print(r.decipher(c))
