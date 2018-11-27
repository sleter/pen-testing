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
        counter = 0
        for i in range(image.size[0]):
            for j in range(image.size[1]):                
                binText += bin(R.getpixel((i, j)))[-self.RC:]
                binText += bin(G.getpixel((i, j)))[-self.GC:]
                binText += bin(B.getpixel((i, j)))[-self.BC:]
                   
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
        self.textLen = len(text)*6
        text = self.text_to_binary(text)
        # print(text)
        # print(self.binary_to_text(text))
        
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if not text:
                    pixels[i, j] = (R.getpixel((i, j)), G.getpixel((i, j)), B.getpixel((i, j)))
                else:
                    redPix = int(bin(R.getpixel((i, j)))[:-self.RC] + text[:self.RC], 2)
                    text = text[self.RC:]
                    greenPix = int(bin(G.getpixel((i, j)))[:-self.GC] + text[:self.GC], 2)
                    text = text[self.GC:]
                    bluePix = int(bin(B.getpixel((i, j)))[:-self.BC] + text[:self.BC], 2)
                    text = text[self.BC:]
                    pixels[i, j] = (redPix, greenPix, bluePix)
                    
        encoded_image.save(pathToSave+'encoded_image.png')

    def text_to_binary(self, text):
        return ''.join(format(ord(x), 'b') for x in text)
    
    def binary_to_text(self, binary):
        pom, text = '', ''
        binary += ' '
        # print("binary:"+binary)
        for i in binary:
            if len(pom) % 6 == 0 and len(pom) != 0:
                text += str(chr(int(str('0b'+pom), 2)))
                # print(text)
                # print(pom)
                pom=i
            else:
                 pom += i
                #  print(pom)
        return text

def main():
    l = LSBSteg(4,4,4)
    input_str = '542 \"0\"123'*100
    l.encode_image('/home/sleter/Pictures/Wallpapers/tvAVMw5.jpg', input_str ,'/home/sleter/Pictures/')
    l.decode_image('/home/sleter/Pictures/encoded_image.png')

if __name__ == '__main__':
    main()