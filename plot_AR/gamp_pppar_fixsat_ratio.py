import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog


ratio_threshold=2    # Ratio Threshold Set
F = []
foldername = filedialog.askdirectory()
filepath = foldername.split('/')
f_list = os.listdir(foldername)

for filename in f_list:
    if os.path.splitext(filename)[1] == '.fix':
        F.append(filename)

for filename in F:
    f = open(foldername + '/' + filename,'r')
    list1 = f.readlines()
    num=len(list1)
    epoch = np.arange(0, num).reshape((num, 1))
    fixsat = np.zeros([num, 12], dtype=np.float32)

    for i in range(0, num ):
        list1[i] = list1[i].rstrip('\n')
        if len(list1[i])>0:
            fixsat[i] = list1[i].split()
        else:
            fixsat[i] = None

    fig = plt.figure(1)
    ax = fig.add_subplot(1,1,1)
    ax.plot(epoch,fixsat[:,8:11])
    ax.grid(True, linestyle='--')
    plt.title(filepath[-1]+'/'+filename)
    plt.ylabel('Number of Satellites')
    plt.xlabel('Epoch')

    plt.legend(['Valid','WL-fixed','NL-fixed'])

    plt.savefig(foldername+'/'+filename+'.png',dpi=360)
    plt.show()
    plt.close()
    f.close()

    ratiosum = 0
    aa = len(list1)
    epoch = np.arange(0, aa).reshape((aa, 1))
    c = np.ones([aa, 1], dtype=np.float32) * 2
    for i in range(0,num) :
        if fixsat[i,11]>ratio_threshold:
            ratiosum=ratiosum+1
    ratiorate=ratiosum/num
    fig = plt.figure(2)
    ax = fig.add_subplot(1,1,1)
    ax.set_yticks(np.linspace(0, 20, 5))
    ax.axis([0,num,0,20])
    ax.plot(epoch,fixsat[:,11])
    #ax.grid(True, linestyle='--')
    plt.plot(epoch[:aa], c, color='r', linewidth=1.5, linestyle='--')
    plt.title(filepath[-1]+'/'+filename)
    plt.ylabel('Ratio Value')
    plt.xlabel('Epoch')

    #plt.text(2000, 4, 'Ratio>'+str(ratio_threshold)+':'+str(ratiorate)[2:4]+'.'+str(ratiorate)[4]+'%', fontsize=12)

    plt.savefig(foldername+'/'+filename+'.ratio.png',dpi=360)
    plt.show()
    plt.close()
    f.close()