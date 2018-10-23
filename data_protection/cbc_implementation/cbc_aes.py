from Crypto.Cipher import AES
import time

BITS = ('0', '1')
ASCII_BITS = 8

def display_bits(b):
    """converts list of {0, 1}* to string"""
    return ''.join([BITS[e] for e in b])

def seq_to_bits(seq):
    return [0 if b == '0' else 1 for b in seq]

def pad_bits(bits, pad):
    """pads seq with leading 0s up to length pad"""
    assert len(bits) <= pad
    return [0] * (pad - len(bits)) + bits
        
def convert_to_bits(n):
    """converts an integer `n` to bit array"""
    result = []
    if n == 0:
        return [0]
    while n > 0:
        result = [(n % 2)] + result
        n = n / 2
    return result

def list_to_string(p):
    return ''.join(p)

def string_to_bits(s):
    def chr_to_bit(c):
        return pad_bits(convert_to_bits(ord(c)), ASCII_BITS)
    return [b for group in 
            map(chr_to_bit, s)
            for b in group]

def bits_to_char(b):
    assert len(b) == ASCII_BITS
    value = 0
    for e in b:
        value = (value * 2) + e
    return chr(value)

def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + ASCII_BITS]) 
                    for i in range(0, len(b), ASCII_BITS)])

def pad_bits_append(small, size):
    diff = max(0, size - len(small))
    return small + [0] * diff

#-----------------------------------

def aes_encoder(block, key):
    block = pad_bits_append(block, len(key))
    # the pycrypto library expects the key and block in 8 bit ascii 
    # encoded strings so we have to convert from the bit string
    block = bits_to_string(block)
    key = bits_to_string(key)
    ecb = AES.new(key, AES.MODE_ECB)
    return string_to_bits(ecb.encrypt(block))

def aes_encoder2(block, key):
    block = pad_bits_append(block, len(key))
    # the pycrypto library expects the key and block in 8 bit ascii 
    # encoded strings so we have to convert from the bit string
    block = bits_to_string(block)
    key = bits_to_string(key)
    ecb = AES.new(key, AES.MODE_ECB)
    return string_to_bits(ecb.decrypt(block))

def cipher_block_chaining(plaintext, key, init_vec, block_size, block_enc):
    def xor(x, y):
        return [xx ^ yy for xx, yy in zip(x, y)]
    cipher = []
    xor_in = init_vec
    for i in range(len(plaintext) / block_size+1):
        start = i* block_size
        if start >= len(plaintext):
            break
        end = min(len(plaintext), (i+1)*block_size)
        block = plaintext[start:end]
        input_ = xor(xor_in, block)
        output = block_enc(input_, key)
        xor_in = output
        cipher.extend(output)
    return cipher

def de_cipher_block_chaining(plaintext, key, init_vec, block_size, block_enc):
    def xor(x, y):
        return [xx ^ yy for xx, yy in zip(x, y)]
    cipher = []
    xor_in = init_vec
    for i in range(len(plaintext) / block_size+1):
        start = i* block_size
        if start >= len(plaintext):
            break
        end = min(len(plaintext), (i+1)*block_size)
        block = plaintext[start:end]
        output = block_enc(block, key)
        input_ = xor(xor_in, output)
        xor_in = output
        cipher.extend(input_)
    return cipher


def aes_ecb_encoder(plaintext, key):
    ecb = AES.new(key, AES.MODE_ECB)
    return string_to_bits(ecb.encrypt(plaintext))

def main():
    key = string_to_bits('Ft7*%78jkQ1!9t%3')
    iv = string_to_bits('98tRszyfr&^^%$7D')
    text = "TRALALALA1234567"

    plaintext = string_to_bits(text*100000)

    
    start_time = time.time()
    cipher = cipher_block_chaining(plaintext, key, iv, 128, aes_encoder)
    elapsed_time = time.time() - start_time
    print "CBC time: "+str(elapsed_time)

    start_time = time.time()
    cipher2 = aes_ecb_encoder(bits_to_string(plaintext), bits_to_string(key))
    elapsed_time = time.time() - start_time
    print "ECB time: "+str(elapsed_time)

    # print "input_vec_len: "+str(len(iv))+"\nplaintext_len: "+str(len(plaintext))+"\ncipher_len: "+str(len(cipher))
    # print display_bits(cipher)
    # dc = de_cipher_block_chaining(cipher, key, iv, 128, aes_encoder2)
    # print bits_to_string(dc)
    

if __name__ == "__main__":
    main()