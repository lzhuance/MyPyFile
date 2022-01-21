import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import filedialog

if __name__ == '__main__':
    F=[]
# tk.withdraw()
# foldername = filedialog.askdirectory()
    filename = filedialog.askopenfilename( filetypes=[('pdop', '*.pdop'), ('All Files', '*')])
    f = open(filename,'r')
    list1 = f.readlines()

    num = len(list1)
    epoch = np.arange(0, num).reshape((num, 1))
    pdop = np.zeros([num, 16], dtype=np.float32)
    covgetime = np.arange(0, 4)

    for i in range(0, len(list1)):
        #print(list1[i])
        list1[i] = list1[i].rstrip('\n')
        if len(list1[i])>0:
            pdop[i] = list1[i].split()
        else:
            pdop[i] = None    

    meansat=np.mean(pdop,0)
    legendindex=['G','R','C','C3','E','J','PDOP']
    legendadd=[]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(9,16):
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
    plt.savefig(filename+'.png',dpi=400)
    plt.show()
    f.close()
