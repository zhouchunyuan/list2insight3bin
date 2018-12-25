#!/usr/bin/python
import tkinter as tk
from tkinter import filedialog

import writeinsight3
import i3dtype

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
f = open(file_path, 'r')
binWriter = writeinsight3.I3Writer(file_path+".bin")

for idx, line in enumerate(f):
    if idx > 0 :
        data = i3dtype.createDefaultI3Data(1)
        field = line.split('\t')
        x  = float(field[1])
        y  = float(field[2])
        xc = float(field[3])
        yc = float(field[4])
        h  = float(field[5])
        a  = float(field[6])
        w  = float(field[7])
        phi= float(field[8])
        ax = float(field[9])
        bg = float(field[10])
        i  = float(field[11])
        c  = 1
        fi = 1
        fr = int(field[12])
        tl = int(field[13])
        lk = int(field[14])
        z  = float(field[16])
        zc = float(field[17])
        i3dtype.setI3Field(data, 'x', x)
        i3dtype.setI3Field(data, 'y', y)
        i3dtype.setI3Field(data, 'xc', xc)
        i3dtype.setI3Field(data, 'yc', yc)
        i3dtype.setI3Field(data, 'h', h)
        i3dtype.setI3Field(data, 'a', a)
        i3dtype.setI3Field(data, 'w', w)
        i3dtype.setI3Field(data, 'phi', phi)
        i3dtype.setI3Field(data, 'ax', ax)
        i3dtype.setI3Field(data, 'bg', bg)
        i3dtype.setI3Field(data, 'i', i)
        i3dtype.setI3Field(data, 'c', c)
        i3dtype.setI3Field(data, 'fi', fi)
        i3dtype.setI3Field(data, 'fr', fr)
        i3dtype.setI3Field(data, 'tl', tl)
        i3dtype.setI3Field(data, 'lk', lk)
        i3dtype.setI3Field(data, 'z', z)
        i3dtype.setI3Field(data, 'zc', zc)
        binWriter.addMolecules(data)
binWriter.close()
f.close()
