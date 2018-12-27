#!/usr/bin/python
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

#import writeinsight3
import writeinsight3new
import i3dtype

root = tk.Tk()

root.title("Progress...")
# 定量进度条
p1 = ttk.Progressbar(root, length=200, mode="determinate", orient=tk.HORIZONTAL)
p1.grid(row=1,column=1)
p1["maximum"] = 100
p1["value"] = 0
 

file_path = filedialog.askopenfilename()
f = open(file_path, 'r')
lines = f.readlines();

channelNames = []
MaxFrameNumber  = 0
for idx, line in enumerate(lines):
    if idx > 0 :
        field = line.split('\t')
        if(field[0]!='Z Rejected'):
            if(field[0] not in channelNames):
                channelNames.append(field[0])
        frameNumber =int(field[12])
        if(frameNumber > MaxFrameNumber):
            MaxFrameNumber = frameNumber

print(channelNames,MaxFrameNumber)

binWriter = writeinsight3new.I3Writer(file_path+".bin",MaxFrameNumber)

for idx, line in enumerate(lines):
    p1["value"] = idx/len(lines)*100
    root.update()
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
        
        c  = 1 # default to 1
        channelName = field[0]
        if(channelName == 'Z Rejected'):
            c = 0
        else:
            for ch,name in enumerate(channelNames):
                if channelName == name:
                    c = ch+1
                    break
        fi = int(field[15])#"valid" for iteration
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

root.withdraw() # use this to hide main window
