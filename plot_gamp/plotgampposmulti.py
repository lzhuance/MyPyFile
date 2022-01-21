import os
import csv
import math
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
    if os.path.splitext(filename)[1] == '.pos':
        
        F.append(filename)

filepath = foldername.split('/')

Sat=[' C3','C3 New','   C',' C New','   G','GC2',' GC','GC New']
epoch = np.arange(0,2880).reshape((2880,1))
pos = np.zeros([2880, 15], dtype=np.float32)
covgetime = np.zeros([4], dtype=np.float32)

ylib = np.linspace(-1, 1, 11)
#gamp_pos_file = 'abmf0020.20o.pos'

#fig,ax = plt.figure(2, 1, sharex=True, sharey=True, figsize=(14, 8))
fig,ax = plt.subplots(2, 4, sharex=True, sharey=True,figsize=(8, 4))
Num=0

for filename in F:
    print('*************** Processing the '+str(Num+1)+'th file ***************')
    print(foldername+'/'+filename)
    f = open(foldername + '/' + filename,'r')
    list1 = f.readlines()
    
    for i in range(0, len(list1)):
        #print(list1[i])
        list1[i] = list1[i].rstrip('\n')
        if len(list1[i])>0:
            pos[i] = list1[i].split()
        else:
            pos[i] = None

    ax1=int(Num/4)
    ax2=Num%4
    Num = Num + 1

    ax[ax1, ax2].plot(epoch[0:480] / 60, pos[0:480, 11], color='r')
    ax[ax1, ax2].plot(epoch[0:480] / 60, pos[0:480, 12], color='g')
    ax[ax1, ax2].plot(epoch[0:480] / 60, pos[0:480, 13], color='b')
    ax[ax1,ax2].grid(True, linestyle='--')
    ax[ax1,ax2].axis([0, 4, -0.3, 0.3])
    if Num==5:
        ax[ax1, ax2].set_yticks([ -0.2, -0.1, 0, 0.1, 0.2,0.3])
    else:
        ax[ax1, ax2].set_yticks([ -0.2, -0.1, 0, 0.1, 0.2,0.3])
    if Num==8:
        ax[ax1, ax2].set_xticks([0, 1, 2, 3])
    else:
        ax[ax1, ax2].set_xticks([0, 1, 2, 3])

    #ax[ax1,ax2].set_yticks(ylib)
    ax[ax1,ax2].text(0.6, 0.22, Sat[Num-1], fontsize=12)
    if Num==8:
        ax[ax1,ax2].legend(['E', 'N', 'U'],loc='lower right')
    #plt.title(filepath[-1]+'/'+filename)
    if ax2==0:
        ax[ax1,ax2].set_ylabel('Error[m]')
    if ax1==1:
        ax[ax1,ax2].set_xlabel('Time[h]')
    f.close()

plt.subplots_adjust(wspace=0, hspace=0)

fig.savefig(foldername + '/' + 'pos-static2.tiff', bbox_inches='tight', dpi=400)
plt.show()


