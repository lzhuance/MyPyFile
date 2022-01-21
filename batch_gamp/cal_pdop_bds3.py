import os
import csv
import numpy as np
#import matplotlib.pyplot as plt
from tkinter import filedialog

F=[]
foldername = filedialog.askdirectory()

f_list = os.listdir(foldername)
for filename in f_list:
    if os.path.splitext(filename)[1] == '.pdop':
        print(foldername+'/'+filename)
        F.append(filename)

filepath = foldername.split('/')
csvfilename=filepath[-2]+'-'+filepath[-1]+'-'+'PDOP.csv'
fs = open(foldername + '/'+csvfilename,'w',newline="")
csv_write=csv.writer(fs)
csv_write.writerow(['STA_NAME','DOY','SUM','G','R','C2','C3','E','J','PDOP'])
fs.close()

for filename in F:
    f = open(foldername + '/' + filename,'r')
    list1 = f.readlines()

    num = len(list1)
    epoch = np.arange(0, num).reshape((num, 1))
    pdop = np.zeros([num, 16], dtype=np.float32)

    for i in range(0, len(list1)):
        list1[i] = list1[i].rstrip('\n')
        if len(list1[i])>0:
            pdop[i] = list1[i].split()
        else:
            pdop[i] = None    

    meansat=np.mean(pdop,0)

    f.close()

    fs = open(foldername + '/'+csvfilename,'a',newline="")
    csv_write=csv.writer(fs)
    csv_write.writerow([filename[0:4],int(filename[4:7]),meansat[8],meansat[9],meansat[10],meansat[11],meansat[12],meansat[13],meansat[14],meansat[15]])
    fs.close()