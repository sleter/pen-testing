from Crypto.Cipher import AES

# additional fuctions

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
    # as mentioned in lecture, simply padding with
    # zeros is not a robust way way of padding
    # as there is no way of knowing the actual length
    # of the file, but this is good enough
    # for the purpose of this exercise
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

def cipher_block_chaining(plaintext, key, init_vec, block_size, block_enc):
    """Return the cbc encoding of `plaintext`
    
    Args:
        plaintext: bits to be encoded
        key: bits used as key for the block encoder
        init_vec: bits used as the initalization vector for 
                  the block encoder
        block_size: size of the block used by `block_enc`
        block_enc: function that encodes a block using `key`
    """
    # Assume `block_enc` takes care of the necessary padding
    # if `plaintext` is not a full block
    
    # return a bit array, something of the form: [0, 1, 1, 1, 0]
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

def main():
    key = string_to_bits('Ft7*%78jkQ1!9t%3')
    iv = string_to_bits('98tRszyfr&^^%$7D')
    plaintext = string_to_bits("TRALALALALALALALA")

    cipher = cipher_block_chaining(plaintext, key, iv, 128, aes_encoder)
    print "input_vec_len: "+str(len(iv))+"\nplaintext_len: "+str(len(plaintext))+"\ncipher_len: "+str(len(cipher))
    print display_bits(cipher)
    

if __name__ == "__main__":
    main()