
import math
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import filedialog

#tk.withdraw()
filename = filedialog.askopenfilename( filetypes=[('txt', '*.txt'), ('All Files', '*')])

f = open(filename, 'r')

ID=[]
SN=[]

ln = f.readline()
while ln:
    ln = f.readline()
    if not ln:
        break
    str = ln.split()

    id = str[2]
    sn = float(str[5])

    ID.append(id)
    SN.append(sn)
f.close()
#ax = plt.subplot(111, projection='polar')
#ax.set_theta_direction(-1)
#ax.set_theta_zero_location('N')
#ax.set_rticks([0,30,60,90])

satnum = 32
if  (ID[0][0] == 'G'):
    satnum = 32
elif(ID[0][0] == 'R'):
    satnum = 27
elif(ID[0][0] == 'E'):
    satnum = 36
elif(ID[0][0] == 'C'):
    satnum = 51
SATID=[]
SATSN=[]
for i in range(1,satnum):
    for j in range(0,len(ID)):
        if int(ID[j][1:3])==i:

            id=ID[j]
            SATID.append(id)
            sn=SN[j]
            SATSN.append(sn)
    #if len(SATAZ)>0:
    #    c = ax.scatter(SATAZ,SATEL,s=1, marker=".",alpha=0.75)
    if len(SATID)>0:
        plt.plot(SATSN,'-o',lw=0.5,markersize=1)
    #ax.text(SATAZ[0],SATEL[0],SATID[0])
        SATID = []
        SATSN = []

#ax.yaxis.set_label_position('right')
#ax.tick_params('y', labelleft=False)
plt.savefig(filename +'.png', dpi=400)
plt.show()