from miller_rabin_pt import probablyPrime
from fractions import gcd

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
        for i in range(2,1001):
            if probablyPrime(i, accuracy=100) and gcd(phi, i) == 1:
                self.e = i
                break
            else:
                continue
        print("e = {}".format(self.e))
        self.d = None
        for i in range(1,1001):
            if (self.e*i -1) % phi == 0:
                self.d = i
                break
            else:
                continue
        print("d = {}".format(self.d))

    def cipher(self, m):
        print("------------------------cipher")
        return m ** self.e % self.n
    
    def decipher(self, c):
        print("------------------------decipher")
        return c ** self.d % self.n

        
        
        
r = RSA(31, 19)
r.key_generator()
c = r.cipher(8)
print(c)
print(r.decipher(c))
