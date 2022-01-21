import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import filedialog

F=[]
#tk.withdraw()
foldername = filedialog.askdirectory()
#filename = filedialog.askopenfilename( filetypes=[('pos', '*.pos'), ('All Files', '*')])
f_list = os.listdir(foldername)
for filename in f_list:
    if os.path.splitext(filename)[1] == '.pdop':
        print(foldername+'/'+filename)
        F.append(filename)

filepath = foldername.split('/')
csvfilename=filepath[-2]+'-'+filepath[-1]+'-'+'PDOP.csv'
fs = open(foldername + '/'+csvfilename,'w',newline="")
csv_write=csv.writer(fs)
csv_write.writerow(['STA_NAME','DOY','SUM','G','R','C','E','J','PDOP'])
fs.close()


#ylib = np.linspace(-1, 1, 11)
#gamp_pos_file = 'abmf0020.20o.pos'

for filename in F:
    f = open(foldername + '/' + filename,'r')
    list1 = f.readlines()

    num = len(list1)
    epoch = np.arange(0, num).reshape((num, 1))
    pdop = np.zeros([num, 15], dtype=np.float32)
    covgetime = np.arange(0, 4)

    for i in range(0, len(list1)):
        #print(list1[i])
        list1[i] = list1[i].rstrip('\n')
        if len(list1[i])>0:
            pdop[i] = list1[i].split()
        else:
            pdop[i] = None    

    meansat=np.mean(pdop,0)
    legendindex=['G','R','C','E','J','PDOP']
    legendadd=[]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(9,15):
        if meansat[i]!=0 :
            ax.plot(epoch,pdop[:,i])
            legendadd.append(legendindex[i-9])
    ax.grid(True, linestyle='--')
    #ax.axis([0, num, 0, max(pdop[:,8])+2])
    #ax.set_yticks(ylib)
    plt.title(filename[0:4].upper())
    #plt.title(filepath[-1]+'/'+filename)
    plt.ylabel('Value')
    plt.xlabel('Epoch')
    plt.legend(legendadd)
    plt.savefig(foldername + '/' + filename+'.png',dpi=400)
    plt.close()
    plt.show()
    f.close()
    
    
    fs = open(foldername + '/'+csvfilename,'a',newline="")
    csv_write=csv.writer(fs)
    csv_write.writerow([filename[0:4],int(filename[4:7]),meansat[8],meansat[9],meansat[10],meansat[11],meansat[12],meansat[13],meansat[14]])
    fs.close()