
import math
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import filedialog

#tk.withdraw()
filename = filedialog.askopenfilename( filetypes=[('txt', '*.txt'), ('All Files', '*')])

f = open(filename, 'r')

ID=[]
PRN=[]
AZ=[]
EL=[]

ln = f.readline()
while ln:
    ln = f.readline()
    if not ln:
        break
    str = ln.split()
    id = str[2]
    prn = int(str[2][1:3])
    if (str[2][0] == 'R'):
        prn = prn+ 31
    elif (str[2][0] == 'E'):
        prn = prn+ 59
    elif (str[2][0] == 'C'):
        prn = prn+ 95
    az = float(str[3])/180*math.pi
    el = 90 - float(str[4])

    ID.append(id)
    PRN.append(prn)
    AZ.append(az)
    EL.append(el)
f.close()
ax = plt.subplot(111, projection='polar')
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
ax.set_rticks([0,30,60,90])

SATAZ=[]
SATEL=[]
SATID=[]
for i in range(1,146):
    for j in range(0,len(ID)):
        if int(PRN[j])==i:
            az=AZ[j]
            SATAZ.append(az)
            el=EL[j]
            SATEL.append(el)
            id=ID[j]
            SATID.append(id)
    if len(SATAZ)>0:
        if i<=32:
            c = ax.scatter(SATAZ, SATEL,s=1, color='g', marker="o", alpha=0.75)
        elif i<=59:
            c = ax.scatter(SATAZ, SATEL,s=1, color='r', marker=".", alpha=0.75)
        elif i<=95:
            c = ax.scatter(SATAZ, SATEL,s=1, color='g', marker=".", alpha=0.75)
        else:
            c = ax.scatter(SATAZ, SATEL,s=1, color='y', marker=".", alpha=0.75)
        middle=int(len(SATAZ)/1.2)
        ax.text(SATAZ[middle],SATEL[middle],SATID[0],fontsize=12)
        SATAZ = []
        SATEL = []
        SATID = []

ax.yaxis.set_label_position('right')
ax.tick_params('y', labelleft=False)
plt.savefig(filename +'.tiff', dpi=400)
plt.show()
