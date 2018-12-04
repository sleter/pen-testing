from tkinter import  *
from PIL import Image, ImageOps, ImageTk
import sys, time, PIL
from random import random
import numpy as np

outs = ['out1.png', 'out2.png']

def generate():
    image = Image.open(e1.get())
    # konwersja na czarno białe
    image = image.convert('1')
    # 1->4bit
    out1 = Image.new("1", [dimension * 2 for dimension in image.size])
    out2 = Image.new("1", [dimension * 2 for dimension in image.size])

    for x in range(0, image.size[0], 2):
        for y in range(0, image.size[1], 2):
            sourcepixel = image.getpixel((x, y))
            rand = random()
            if sourcepixel == 0:
                if rand < .5:
                    out1.putpixel((x * 2, y * 2), 255)
                    out1.putpixel((x * 2 + 1, y * 2), 0)
                    out1.putpixel((x * 2, y * 2 + 1), 0)
                    out1.putpixel((x * 2 + 1, y * 2 + 1), 255)
                    
                    out2.putpixel((x * 2, y * 2), 0)
                    out2.putpixel((x * 2 + 1, y * 2), 255)
                    out2.putpixel((x * 2, y * 2 + 1), 255)
                    out2.putpixel((x * 2 + 1, y * 2 + 1), 0)
                else:
                    out1.putpixel((x * 2, y * 2), 0)
                    out1.putpixel((x * 2 + 1, y * 2), 255)
                    out1.putpixel((x * 2, y * 2 + 1), 255)
                    out1.putpixel((x * 2 + 1, y * 2 + 1), 0)
                    
                    out2.putpixel((x * 2, y * 2), 255)
                    out2.putpixel((x * 2 + 1, y * 2), 0)
                    out2.putpixel((x * 2, y * 2 + 1), 0)
                    out2.putpixel((x * 2 + 1, y * 2 + 1), 255)
            elif sourcepixel == 255:
                if rand < .5:
                    out1.putpixel((x * 2, y * 2), 255)
                    out1.putpixel((x * 2 + 1, y * 2), 0)
                    out1.putpixel((x * 2, y * 2 + 1), 0)
                    out1.putpixel((x * 2 + 1, y * 2 + 1), 255)
                    
                    out2.putpixel((x * 2, y * 2), 255)
                    out2.putpixel((x * 2 + 1, y * 2), 0)
                    out2.putpixel((x * 2, y * 2 + 1), 0)
                    out2.putpixel((x * 2 + 1, y * 2 + 1), 255)
                else:
                    out1.putpixel((x * 2, y * 2), 0)
                    out1.putpixel((x * 2 + 1, y * 2), 255)
                    out1.putpixel((x * 2, y * 2 + 1), 255)
                    out1.putpixel((x * 2 + 1, y * 2 + 1), 0)
                    
                    out2.putpixel((x * 2, y * 2), 0)
                    out2.putpixel((x * 2 + 1, y * 2), 255)
                    out2.putpixel((x * 2, y * 2 + 1), 255)
                    out2.putpixel((x * 2 + 1, y * 2 + 1), 0)

    out1.save(outs[0])
    out2.save(outs[1])

    # show_image_encoded()

def show():
    img = Image.open("out1.png")
    img2 = Image.open("out2.png")
    out = Image.new('1', img.size)

    # mergowanie obrazków
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            out.putpixel((x, y), max(img.getpixel((x, y)), img2.getpixel((x, y))))

    # out = 1 - np.asarray(out)
    out.show()
    out.save('out.jpg')

    out=Image.open("out.jpg")
    out=PIL.ImageOps.invert(out)
    out.save('output.jpg')
    

    # show_image_decoded()

def show_image_encoded():
    id = 0
    for i in outs:
        img = ImageTk.PhotoImage(Image.open(i))
        Label(root,image=img).grid(row=4,column=id)
        id += 1
    Label.pack()

def show_image_decoded():
    img = ImageTk.PhotoImage(Image.open('output.png'))
    Label(root,image=img).grid(row=4,column=0)
    Label.pack()

root = Tk()
root.title('Simple visual cryptography')
Label(root, text="Input path:").grid(row=0)
Label(root, text="Output path:").grid(row=1)
v = StringVar()
v2= StringVar()
v.set('/home/sleter/Pictures/test.png')
e1 = Entry(root, textvariable=v, width=100)
v2.set('/home/sleter/Pictures/')
e2 = Entry(root, textvariable=v2, width=100)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
Button(root, text='Close', command=root.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(root, text='Encode',command=generate).grid(row=3, column=1)
Button(root, text='Decode',command=show).grid(row=3, column=2)
root.mainloop()

