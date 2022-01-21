import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import filedialog



def ReadPos():
    filename = filedialog.askopenfilename( filetypes=[('pos', '*.pos'), ('All Files', '*')])
    print(filename)

    #ylib = np.linspace(-1, 1, 11)
    f = open(filename,'r')
    list1 = f.readlines()
    num = len(list1)

    epoch = np.arange(0,num).reshape((num,1))
    pos = np.zeros([num, 15], dtype=np.float32)

    for i in range(0, len(list1)):
        list1[i] = list1[i].rstrip('\n')
        if len(list1[i])>0:
            pos[i] = list1[i].split()
        else:
            pos[i] = None
    f.close()
    return epoch,pos,filename,num

def PoltCompare(epoch, Pos1,Pos2,filename):

    ymax=0.1
    ymin=-0.1
    ylib = np.linspace(ymin,ymax, 5)

    plt.subplots(sharex=True, sharey=True,figsize=(8, 5))

    plt.subplot(311)
    plt.plot(epoch[:], Pos1[:, 12])
    plt.plot(epoch[:], Pos2[:, 12])
    plt.axis([0, 2880,ymin,ymax])
    plt.grid(True, linestyle='--')
    plt.ylabel('E--Error[m]')
    #plt.xlabel('Epoch')
    plt.yticks(ylib)

    plt.subplot(312)
    plt.plot(epoch[:], Pos1[:, 13])
    plt.plot(epoch[:], Pos2[:, 13])
    plt.axis([0, 2880,ymin,ymax])
    plt.grid(True, linestyle='--')
    #plt.xlabel('Epoch')
    plt.ylabel('N--Error[m]')
    plt.yticks(ylib)

    plt.subplot(313)
    plt.plot(epoch[:], Pos1[:, 14])
    plt.plot(epoch[:], Pos2[:, 14])
    plt.axis([0, 2880,ymin,ymax])
    plt.grid(True, linestyle='--')
    plt.yticks(ylib)

    filepath = filename.split('/')

    plt.ylabel('U--Error[m]')
    plt.xlabel('Epoch')

    plt.legend(['1','2'])
    #plt.legend(['Float', 'Fix'])
    #plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(filename+'_compare2.tiff',dpi=400)
    plt.show()
    plt.close()


if __name__ == '__main__':
    Epoch1, Pos1,filename1,num1 = ReadPos()
    Epoch2, Pos2,filename2,num2 = ReadPos()
    PoltCompare(Epoch1,Pos1,Pos2,filename2)