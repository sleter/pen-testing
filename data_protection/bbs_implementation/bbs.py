from miller_rabin_pt import probablyPrime
import random
 
def goodPrime(p):
    return p % 4 == 3 and probablyPrime(p, accuracy=100)
 
def findGoodPrime(numBits=512):
    candidate = 1
    while not goodPrime(candidate):
        candidate = random.getrandbits(numBits)
    return candidate
 
def makeModulus():
    return findGoodPrime() * findGoodPrime()
 
def parity(n):
    return sum(int(x) for x in bin(n)[2:]) % 2
 
class BlumBlumShub(object):
    def __init__(self, seed=None):
        self.modulus = makeModulus()
        self.state = seed if seed is not None else random.randint(2, self.modulus - 1)
        self.state = self.state % self.modulus
 
    def seed(self, seed):
        self.state = seed
 
    def bitstream(self):
        while True:
            yield parity(self.state)
            self.state = pow(self.state, 2, self.modulus)
 
    def bits(self, n=20):
        outputBits = []
        for bit in self.bitstream():
            outputBits.append(bit)
            if len(outputBits) == n:
                break
 
        return outputBits

def frequency_test(lp):
    zero = float(lp.count(0))/float(len(lp))*100.0
    one = float(lp.count(1))/float(len(lp))*100.0
    return zero, one

def double_bit_test(lp):
    from itertools import cycle
    lpCycle = cycle(lp)
    nextElem = next(lpCycle)
    tab_00, tab_01, tab_10, tab_11 = 0, 0, 0, 0
    for _ in range(len(lp)-1):
        thisElem, nextElem = nextElem, next(lpCycle)
        pom = str(thisElem)+str(nextElem)
        if pom == "00":
            tab_00 += 1
        elif pom == "01":
            tab_01 += 1
        elif pom == "10":
            tab_10 += 1
        elif pom == "11":
            tab_11 += 1
    return tab_00, tab_01, tab_10, tab_11

def longest_repetition(lb):
    from itertools import groupby
    count_dups = [sum(1 for _ in group) for _, group in groupby(lb)]
    return max(count_dups)

def poker_test(lb):
    dec_list = []  
    for i in range(0, len(lb), 4):
        binary = str(lb[i]) + str(lb[i+1]) + str(lb[i+2]) + str(lb[i+3])
        to_decimal = int(binary, 2)
        dec_list.append(to_decimal)
    out = []
    for j in range(0,16):
        out.append(dec_list.count(j)) 
    sum_ = [i*i for i in out]
    x = (16.0/5000.0) * float(sum(sum_)) - 5000.0
    return x 

def main():
    bbs = BlumBlumShub()
    out = bbs.bits(n=20000)
    zero_freq, one_freq = frequency_test(out)
    print("1. Frequency test\nzero_freq: "+str(zero_freq)+"\none_freq: "+str(one_freq)+"\n")
    tab_00, tab_01, tab_10, tab_11 = double_bit_test(out)
    print("2. Double bit test\n00: "+str(tab_00)+"\n01: "+str(tab_01)+"\n10: "+str(tab_10)+"\n11: "+str(tab_11)+"\n")
    lr = longest_repetition(out)
    print("3. Longest repetition test: "+str(lr)+"\n")   
    x = poker_test(out)
    print("4. Poker test\nx = "+str(x))


if __name__ == "__main__":
    main()
