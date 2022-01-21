#!/usr/bin/python
# coding=utf-8

import os
import math
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np

class Stat:
    def __init__(self):
        self.sat    = 'X00'
        self.sys    = 'X'
        self.prn    = 0
        self.week   = 0
        self.tow    = 0.0
        self.frq    = 0
        self.az     = 0.0
        self.el     = 0.0
        self.resp   = 0.0
        self.resc   = 0.0
        self.vsat   = 0
        self.snr    = 0
        self.fix    = 0
        self.slip   = 0
        self.lock   = 0
        self.outc   = 0
        self.slipc  = 0
        self.rejc   = 0
        self.dgpsx  = 0.0
        self.dgpsp  = 0.0
        self.lam    = 0.0
        self.icbias = 0.0
        self.mw     = 0.0
        self.smw    = 0.0
        self.smwv   = 0.0
        self.BW     = 0.0
        self.B1     = 0.0
        self.NW     = 0
        self.N1     = 0
        self.ifb    = 0

def rms(Res):
    s = 0
    for i in range(0, len(Res)):
        s += Res[i]*Res[i]
    return math.sqrt(s/len(Res))

def readstat(filename):
    Multi_stat = []
    path = ""
    filepath = filename.split('/')
    for i in range(0, len(filepath)-1):
        path = path+filepath[i]+'/'
    path = path+filepath[-1][0:12]
    f = open(filename, 'r')
    ln = f.readline()
    while ln:
        ln = f.readline()
        if not ln:
            break
        str = ln.split(',')
        if str[0]=="$SAT":
            stat = Stat()
            stat.week  = int(str[1])
            stat.tow   = float(str[2])
            stat.sat   = str[3]
            stat.sys   = str[3][0]
            stat.prn   = int(str[3][1:])
            stat.frq   = int(str[4])
            stat.az    = float(str[5])
            stat.el    = float(str[6])
            stat.resp  = float(str[7])
            stat.resc  = float(str[8])
            stat.vsat  = int(str[9])
            stat.snr   = int(str[10])
            stat.fix   = int(str[11])
            stat.slip  = int(str[12])
            stat.lock  = int(str[13])
            stat.outc  = int(str[14])
            stat.slipc = int(str[15])
            stat.rejc  = int(str[16])
            stat.dgpsx = float(str[17])
            stat.dgpsp = float(str[18])
            stat.lam   = float(str[19])
            stat.icbias= float(str[20])
            stat.mw    = float(str[21])
            stat.smw   = float(str[22])
            stat.smwv  = float(str[23])
            stat.BW    = float(str[24])
            stat.B1    = float(str[25])
            stat.NW    = int(str[26])
            stat.N1    = int(str[27])
            stat.ifb   = float(str[28])
            Multi_stat.append(stat)
    f.close()
    return Multi_stat, path

def ReadData(data, filepath):
    # font1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
    plt.figure(figsize=(7, 5))
    plt.xlabel('Time[hh:mm]')
    plt.xticks([0, 720, 1440, 2160, 2880],['00:00','06:00','12:00','18:00','00:00'])
    plt.ylabel('Bias[m]')
    # plt.title("BDS-3 B1C/B2a 接收机钟",fontproperties=font1)
    plt.axis([0, 2880, -25, 25])

    plt.grid(ls='--')

    prns = []
    Resps = []
    for prn in range(1, 47):
        index = 0
        Tow = []
        ifb = []
        plotsep = [0]
        for i in range(0, int(len(data))):
            if data[i].prn == prn:
                Tow. append(data[i].tow % 86400 // 30)
                ifb.append(data[i].ifb)
                index += 1
        # if Resp:
        #    print("C{:2d}  {:5.4f}m".format(prn, rms(Resp)))
        # plt.scatter(Tow, Resp,s=1,alpha=0.75)
        if index != 0:
            for i in range(0, len(ifb)-1):
                if Tow[i+1]-Tow[i] > 30:
                    plotsep.append(i)
            plotsep.append(len(ifb))
            for i in range(0,len(plotsep)-1):
                plt.plot(Tow[plotsep[i]+1:plotsep[i+1]], ifb[plotsep[i]+1:plotsep[i+1]], linewidth=1.5)
            prns.append("C"+str(prn))
            Resps.append(rms(ifb))

    plt.savefig(filepath+'.ifb.png', dpi=600)
    # plt.show()

    return


if __name__ == '__main__':
    filename = filedialog.askopenfilename(filetypes=[('stat', '*.stat'), ('All Files', '*')])
    data, filepath = readstat(filename)
    ReadData(data, filepath)



