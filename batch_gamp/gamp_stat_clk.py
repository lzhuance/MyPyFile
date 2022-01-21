# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/05
 '''

import numpy as np
import matplotlib.pyplot as plt

def readstat(filename):
    f = open(filename, 'r')
    ln = f.readline()
    stat = np.zeros([2880, 17], dtype=np.float32)
    epoch = 0
    while ln:
        ln = f.readline()
        if not ln:
            break
        str = ln.split(',')
        if str[0]=="$CLK":
            for i in range(1, len(str)):
                if len(str) > 0:
                    stat[epoch,i] = str[i]
                else:
                    stat[epoch,i] = None
            epoch += 1
    return stat


if __name__ == '__main__':
    file = 'abpo1820.21o.pos.stat'
    file1 = 'C:/Users/LZ/Desktop/2017244/ISB_TC/'+file
    file2 = 'C:/Users/LZ/Desktop/2017244/ISB_RW/'+file
    file3 = 'C:/Users/LZ/Desktop/2017244/ISB_WN/'+file
    stat1 = readstat(file1)
    stat2 = readstat(file2)
    stat3 = readstat(file3)
    isb = np.zeros([2880, 3], dtype=np.float32)

    for i in range(0, 2880):
        sd1 = stat1[i, 10]
        sd2 = stat2[i, 10]
        sd3 = stat3[i, 10]
        # sd1 = stat1[i, 10] - stat1[i, 7]
        # sd2 = stat2[i, 10] - stat2[i, 7]
        # sd3 = stat3[i, 10] - stat3[i, 7]
        if abs(sd1) < 1000:
            isb[i, 0] = sd1 * 0.3
            isb[i, 1] = sd2 * 0.3
            isb[i, 2] = sd3 * 0.3

    plt.plot(range(0,2880), isb)
    plt.legend(['TC', 'RW', 'WN'])
    #plt.axis([0, 2880, 13*0.3, 15*0.3])
    #plt.axis([0, 2880, -1.5, 1.5])
    plt.xlabel('Time[hh:mm]')
    plt.xticks([0, 720, 1440, 2160, 2880],['00:00','06:00','12:00','18:00','00:00'])
    plt.ylabel('Inter-System Bias Delay[ns]')

    plt.savefig(file1+'clk.png', dpi=600)
    plt.show()
