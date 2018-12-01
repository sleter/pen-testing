import os, textwrap, binascii
from PIL import Image, ImageFont, ImageDraw

class LSBSteg:
    def __init__(self, RC, GC, BC):
        self.textLen = 0
        self.RC = RC
        self.GC = GC
        self.BC = BC

    def decode_image(self, pathToImage):
        image = Image.open(pathToImage)
        # image = image.convert('RGB')
        R = image.split()[0]
        G = image.split()[1]
        B = image.split()[2]
        binText=''
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                r = str(bin(R.getpixel((i, j))))[2:]
                g = str(bin(G.getpixel((i, j))))[2:]
                b = str(bin(B.getpixel((i, j))))[2:]
                binText += str(r[-self.RC:])
                binText += str(g[-self.GC:])
                binText += str(b[-self.BC:])
                
        # print(self.textLen)
        binText = binText[:self.textLen]

        # print(binText)
        print(self.binary_to_text(binText))

        
    def encode_image(self, pathToImage, text, pathToSave):
        image = Image.open(pathToImage)
        # image = image.convert('RGB')
        R = image.split()[0]
        G = image.split()[1]
        B = image.split()[2]
        encoded_image = Image.new("RGB", image.size)
        pixels = encoded_image.load()
        self.textLen = len(text)*8
        
        text = self.text_to_binary(text)
        
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if not text:
                    pixels[i, j] = (R.getpixel((i, j)), G.getpixel((i, j)), B.getpixel((i, j)))
                else:
                    redPix = int(bin(R.getpixel((i, j))).zfill(8)[:-self.RC] + text[:self.RC], 2)
                    text = text[self.RC:]
                    greenPix = int(bin(G.getpixel((i, j))).zfill(8)[:-self.GC] + text[:self.GC], 2)
                    text = text[self.GC:]
                    bluePix = int(bin(B.getpixel((i, j))).zfill(8)[:-self.BC] + text[:self.BC], 2)
                    text = text[self.BC:]
                    pixels[i, j] = (redPix, greenPix, bluePix)
                    
        encoded_image.save(pathToSave+'encoded_image.png')

    def text_to_binary(self, text):
        text = ' '.join(format(ord(x), 'b') for x in text)
        text = text.split()
        text = ''.join(x.zfill(8) for x in text)
        return text
    
    def binary_to_text(self, binary):
        pom, text = '', ''
        for i in binary:
            if len(pom) % 8 == 0 and len(pom) != 0:
                text += chr(int(pom, 2))
                # print(pom)
                pom=i
            else:
                 pom += i
                #  print(pom)
        return text

def main():
    l = LSBSteg(1,1,7)
    input_str = 'A5 42\"0c192kz 8T3'*1000
    l.encode_image('/home/sleter/Pictures/andy.png', input_str ,'/home/sleter/Pictures/')
    l.decode_image('/home/sleter/Pictures/encoded_image.png')

if __name__ == '__main__':
    main()