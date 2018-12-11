import random
from functools import partial
from fractions import gcd

def coeff_tuple(s, x, prime):
    accum = 0
    for coeff in reversed(s):
        accum *= x
        accum += coeff
        accum %= prime
    return accum

def create_shares(_range, shares, prime):
    r = partial(random.SystemRandom().randint, 0)
    secret = [r(prime) for i in range(_range)]
    share_points = [(i, coeff_tuple(secret, i, prime))for i in range(1, shares + 1)]
    return secret[0], share_points

def gcd(a, b):
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a%b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x

def modulo_div(number, d, p):
    return number * gcd(d, p)

def pom(vals, accum=1):  
    for v in vals:
        accum *= v
    return accum

def y_for_x(x, _x, _y, p):
    nums = []  
    d = []
    l = len(_x)
    for i in range(l):
        o = list(_x)
        cur = o.pop(i)
        nums.append(pom(x - i for i in o))
        d.append(pom(cur - i for i in o))
    den = pom(d)
    num = sum([modulo_div(nums[i] * den * _y[i] % p, d[i], p)for i in range(l)])
    out = gcd(den, p) * num
    out = (out+p)%p
    return out

def gimme_secret(shares, prime):
    x, y = zip(*shares) # punkty x i y wielomianu
    return y_for_x(0, x, y, prime)

def main():
    prime = 1523
    secret, shares = create_shares(3, 6, prime)
    print(secret)
    for share in shares:
        print(str(share)+', ')
    print(gimme_secret(shares[:3], prime))

if __name__ == '__main__':
    main()