import os, textwrap, binascii
from PIL import Image, ImageFont, ImageDraw

class LSBSteg:
    def __init__(self):
        self.textLen = 0

    def decode_image(self, pathToImage):
        image = Image.open(pathToImage)
        R = image.split()[0]
        # G = image.split()[1]
        # B = image.split()[2]
        text = ''
        binText=''
        counter = 1
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if counter == self.textLen:
                    break
                else:                 
                    if counter % 8== 0 and counter != 0:
                        # print(binText)
                        text += self.binary_to_text(binText)
                        binText = ''
                    else:
                        # print(bin(R.getpixel((i, j))))
                        binText += str(bin(R.getpixel((i, j))))[-1]
                    counter+=1
        print(text)

        
    def encode_image(self, pathToImage, text, pathToSave):
        image = Image.open(pathToImage)
        R = image.split()[0]
        G = image.split()[1]
        B = image.split()[2]
        encoded_image = Image.new("RGB", image.size)
        pixels = encoded_image.load()
        text = self.text_to_binary(text)
        self.textLen = len(text)
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if not text or len(text) == 1:
                    pixels[i, j] = (R.getpixel((i, j)), G.getpixel((i, j)), B.getpixel((i, j)))
                else:
                    redPix = int(str(bin(R.getpixel((i, j))))[:-1] + text[0], 2)
                    print(str(bin(R.getpixel((i, j))))[:-1] + text[0])
                    print(bin(R.getpixel((i, j))))
                    # greenPix = int(str(bin(G.getpixel((i, j)))[2:].zfill(8))[:-1] + text[1], 2)
                    # bluePix = int(str(bin(B.getpixel((i, j)))[2:].zfill(8))[:-1] + text[2], 2)
                    pixels[i, j] = (redPix, G.getpixel((i, j)), B.getpixel((i, j)))
                    text = text[1:]
                    
        encoded_image.save(pathToSave+'encoded_image.jpg')

    def text_to_binary(self, text):
        return ''.join(format(ord(x), 'b') for x in text)
    
    def binary_to_text(self, binary):
        # print(str(int('0b'+binary, 2)))
        return str(chr(int('0b'+binary, 2)))



def main():
    l = LSBSteg()
    l.encode_image('/home/sleter/Pictures/Wallpapers/tvAVMw5.jpg', 'abcde', '/home/sleter/Pictures/')
    print(l.decode_image('/home/sleter/Pictures/encoded_image.jpg'))

if __name__ == '__main__':
    main()
    