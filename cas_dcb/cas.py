# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''
import matplotlib.pyplot as plt
import os
import math

def math_std(prn_all):
    sump = 0
    sumq = 0
    for i in range(len(prn_all)):
        sump += prn_all[i]
    ave = sump /len(prn_all)
    for i in range(len(prn_all)):
        sumq += (prn_all[i]-ave)*(prn_all[i]-ave)
    rms = round(math.sqrt(sumq / len(prn_all)),3)
    return rms

#list = [r'C:\Users\LZ\Desktop\CAS0MGXRAP_20211830000_01D_01D_DCB.BSX',r'C:\Users\LZ\Desktop\CAS0MGXRAP_20211840000_01D_01D_DCB.BSX']
dir = r"D:\paperdata"
results = os.listdir(dir)
list = []
for ele in results:
    if ele[0:3]=='CAS':
        list.append(ele)
C1X_all = []
for file in list[0:31]:
    filepath = dir+'\\'+file
    f = open(filepath)
    ln = f.readline()
    C1X = []
    while ln:
        ln = f.readline()
        if 'DSB' in ln:
            if 'C2I  C6I' in ln and ln[11] == 'C' and ln[15:19] == '    ':
                prn = int(ln[12:14])
                dcb = float(ln[83:91])
                C1X.append([prn,dcb])
    C1X_all.append(C1X)
#print(C1X_all)
prn_list=[]
ax=plt.subplot(111)
for prn in range(19,47):
    prn_all = []
    for i in range(len(C1X_all)):
        for j in range(len(C1X_all[0])):
            if C1X_all[i][j][0] == prn:
                prn_all.append(C1X_all[i][j][1])
    if prn_all != []:
        prn_rms = math_std(prn_all)
        #print('C'+str(prn))
        prn_list.append('C'+str(prn))
    ax.plot(prn_all,'-o')
#plt.ylim([-25, 25])
plt.yticks(fontsize='large')
plt.xticks([0, 5, 10, 15, 20, 25, 30],['182', '187', '192', '197', '202', '207', '212'],fontsize='large')
plt.xlabel('DOY',fontsize='x-large')
plt.ylabel('DCB[ns]',fontsize='x-large')
plt.title('C2I-C6I',fontsize='xx-large')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height])
plt.legend(prn_list, loc='center',bbox_to_anchor=(1.07, 0.5),ncol=1,fontsize='x-small')
plt.savefig(r'C:\Users\LZ\Desktop\C2I-C6I.png', dpi=500)
plt.show()
