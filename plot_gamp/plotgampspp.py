import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import filedialog

#root=tk()
#root.withdraw()
F=[]
#tk.withdraw()
foldername = filedialog.askdirectory()
#filename = filedialog.askopenfilename( filetypes=[('pos', '*.pos'), ('All Files', '*')])
f_list = os.listdir(foldername)
for filename in f_list:
    if os.path.splitext(filename)[1] == '.pos':
        print(foldername+'/'+filename)
        F.append(filename)


filepath = foldername.split('/')
csvfilename=filepath[-1]+'-'+'poserror.csv'
fs = open(foldername + '/'+csvfilename,'w',newline="")
csv_write=csv.writer(fs)
csv_write.writerow(['staname','E68','N68','U68','3D68','E95','N95','U95','3D95'])
fs.close()

epoch = np.arange(0,2880).reshape((2880,1))
pos = np.zeros([2880, 15], dtype=np.float32)

for filename in F:
#ylib = np.linspace(-1, 1, 11)
    f = open(foldername + '/' + filename,'r')
    list1 = f.readlines()

    for i in range(0, len(list1)):
    #print(list1[i])
        list1[i] = list1[i].rstrip('\n')
        if len(list1[i])>0:
            pos[i] = list1[i].split()
        else:
            pos[i] = None
    
    ylib1=5
    #ylib1=np.nanmax(abs(pos[:,14]),0)+2
    #ylib2=-ylib1
    
    pos_east_68 = np.percentile(abs(pos[:,11:15]),68,axis=0)
    pos_east_95 = np.percentile(abs(pos[:,11:15]),95,axis=0)
    print(pos_east_95 )
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(epoch,pos[:,11:14])
    ax.grid(True, linestyle='--')
    #ax.axis([0, 2880, ylib2, ylib1])
    #ax.set_yticks(ylib)

    filepath = filename.split('/')


    plt.title(filepath[-1])
    plt.ylabel('Error[m]')
    plt.xlabel('Epoch')

    plt.legend(['E','N','U'])

    plt.text(0, ylib1*-0.80, '68% Error: E : '+ str(pos_east_68[0])[0:5]+'m'+' N : '+ str(pos_east_68[1])[0:5]+'m'+' U : '+ str(pos_east_68[2])[0:5]+'m', fontsize=12)
    plt.text(0, ylib1*-0.90, '95% Error: E : '+ str(pos_east_95[0])[0:5]+'m'+' N : '+ str(pos_east_95[1])[0:5]+'m'+' U : '+ str(pos_east_95[2])[0:5]+'m', fontsize=12)

    plt.savefig(foldername + '/' + filename+'.tiff')
    #plt.show()
    f.close()
    
    fs = open(foldername + '/'+csvfilename,'a',newline="")
    csv_write=csv.writer(fs)
    csv_write.writerow([filename[0:4],pos_east_68[0],pos_east_68[1],pos_east_68[2],pos_east_68[3],pos_east_95[0],pos_east_95[1],pos_east_95[2],pos_east_95[3]])
    fs.close()