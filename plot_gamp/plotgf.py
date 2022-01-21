import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import filedialog


filename = filedialog.askopenfilename(filetypes=[('gf', '*.gf'), ('All Files', '*')])
print(filename)



# ylib = np.linspace(-1, 1, 11)
f = open(filename, 'r')
list1 = f.readlines()
aa=len(list1)
epoch = np.arange(0,aa).reshape((aa, 1))
c = np.ones([ aa,1],dtype=np.float32)*0.05
b = np.ones([ aa,1],dtype=np.float32)*-0.05
pos = np.zeros([aa, 40], dtype=np.float32)

for i in range(0, len(list1)):
    list1[i] = list1[i].rstrip('\n')
    if len(list1[i]) > 0:
        pos[i] = list1[i].split()
    else:
        pos[i] = None
f.close()




for i in range(0,aa):
    #c[i]=cc[i]*2.5
    for j in range(0, 40):
        if pos[i,j]==99999.000:
            pos[i, j] = 0

plt.axis([0, aa, -0.3, 0.3])
plt.plot(epoch[:aa], pos[:aa, 9:])
plt.plot(epoch[:aa],c,color='r',linewidth=1.5,linestyle='--')
plt.plot(epoch[:aa],b,color='r',linewidth=1.5,linestyle='--')
plt.xlabel('Epoch')
plt.savefig('LHAZ GF.tiff', dpi=400)
plt.show()