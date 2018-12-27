#!/usr/bin/python
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

#import writeinsight3
import writeinsight3new
import i3dtype

# insight3 molecule list uses pixel based x,y,xc,yc
# while Nikon uses real distance based coordinates
pixelSize = 160 # nm per pixel

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
f.close()

channelNames = []
for idx, line in enumerate(lines):
    field = line.split('\t')
    if idx > 0 :
        if(field[0]!='Z Rejected'):
            if(field[0] not in channelNames):
                channelNames.append(field[0])

newlines = []                
fw = open(file_path+"_new.txt", 'w')

for idx, line in enumerate(lines):
    p1["value"] = idx/len(lines)*100
    root.update()
    field = line.split('\t')
    if idx == 0:
        field[0]= 'Cas'+str(len(lines)-1)
    if idx > 0 :
        channelName=field[0]
        if(channelName == 'Z Rejected'):
            field[0] = '0'
        else:
            for ch,name in enumerate(channelNames):
                if channelName == name:
                    field[0] = str(ch+1)
                    break
        #field[0]='1'
        #field[16]='0'
        #field[17]='0'

        x  = float(field[1])/pixelSize
        y  = float(field[2])/pixelSize
        xc = float(field[3])/pixelSize
        yc = float(field[4])/pixelSize
        field[1] = str(x)
        field[2] = str(y)
        field[3] = str(xc)
        field[4] = str(yc)
    newLine =  field[0]+'\t'+field[1]+'\t'+field[2]+'\t'+field[3]+'\t'+field[4]+'\t'+ \
               field[5]+'\t'+field[6]+'\t'+field[7]+'\t'+field[8]+'\t'+field[9]+'\t'+ \
               field[10]+'\t'+field[11]+'\t'+field[12]+'\t'+field[13]+'\t'+field[14]+'\t'+ \
               field[15]+'\t'+field[16]+'\t'+field[17]+'\n'
   
    newlines.append(newLine)

fw.writelines( newlines )
fw.close()

root.withdraw() # use this to hide main window
