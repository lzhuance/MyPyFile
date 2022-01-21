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
csvfilename=filepath[-2]+'-'+filepath[-1]+'-'+'SPP Performance.csv'
fs = open(foldername + '/'+csvfilename,'w',newline="")
csv_write=csv.writer(fs)
csv_write.writerow(['SAT_NAME','DAY','E','N','U','3D','Use_Rate'])
fs.close()


covgetime = np.zeros([4], dtype=np.float32)

ylib = np.linspace(-5, 5, 11)
#gamp_pos_file = 'abmf0020.20o.pos' 

Num=0

for filename in F:
    Num=Num+1
    print('*************** Processing the '+str(Num)+'th file ***************')
    print(foldername+'/'+filename)
    f = open(foldername + '/' + filename,'r')
    list1 = f.readlines()
    num = len(list1)
    epoch = np.arange(0, num).reshape((num, 1))
    pos = np.zeros([num, 15], dtype=np.float32)

    for i in range(0, len(list1)):
        #print(list1[i])
        list1[i] = list1[i].rstrip('\n')
        if len(list1[i])>0:
            pos[i] = list1[i].split()
        else:
            pos[i] = None
            
    Square = np.zeros([4])
    N = np.zeros([4])
    RMS = np.zeros([4])
    EPON = np.zeros([4])
    pos_999 = np.nanpercentile(abs(pos[:,11:15]),99.93,axis=0)

    test=1

    for j in range(0,4):
        for i in range(0, len(pos)):
            if pos[i,j+11]!=None:
                if math.isnan(pos[i,j+11])!= True :
                    EPON[j] = EPON[j] + 1
                    if (test):
                        if abs(pos[i,j+11])<pos_999[j]:
                            Square[j]=Square[j]+pos[i,j+11]**2
                            N[j]=N[j]+1
                    else:
                        Square[j] = Square[j] + pos[i, j + 11] ** 2
                        N[j] = N[j] + 1
        if N[j]!=0:
            RMS[j]=math.sqrt(Square[j]/N[j])
    print(N,RMS)
    for j in range(0,4):
        for i in range(0, len(pos)-20):
            nannp=np.isnan(pos[i:i+20,j+11])
            if (np.all(nannp== False)): 
                if (np.all(abs(pos[i:i+20,j+11]) <0.1)):
                    covgetime[j] = (i)/2
                    #print(i, j, covgetime[j])
                    #print(pos[i:i+20,j+11])
                    break
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(epoch,pos[:,11:14])
    ax.grid(True, linestyle='--')
    ax.axis([0, num, -1, 1])
    ax.set_yticks(ylib)

    plt.title(filename[0:4].upper())
    plt.ylabel('Error[m]')
    plt.xlabel('Epoch')

    plt.text(2000, -0.55*5, 'Positioning RMS', fontsize=12)
    plt.text(2000, -0.65*5, 'E :'+ str(RMS[0])[0:5]+'m', fontsize=12)
    plt.text(2000, -0.75*5, 'N :'+ str(RMS[1])[0:5]+'m', fontsize=12)
    plt.text(2000, -0.85*5, 'U :'+ str(RMS[2])[0:5]+'m', fontsize=12)
    plt.text(2000, -0.95*5, '3D:'+ str(RMS[3])[0:5]+'m', fontsize=12)
    
    plt.legend(['E','N','U'])

    plt.savefig(foldername + '/' + filename+'.png',dpi=400)
    plt.close()
    plt.show()
    f.close()
    
    fs = open(foldername + '/'+csvfilename,'a',newline="")
    csv_write=csv.writer(fs)
    csv_write.writerow([filename[0:4],int(filename[4:7]),RMS[0],RMS[1],RMS[2],RMS[3],EPON[0]/2880])
    fs.close()