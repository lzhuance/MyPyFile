
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
            Multi_stat.append(stat)
    f.close()
    return Multi_stat, path

def ReadData(data, filepath):
    plt.figure(figsize=(14, 5))
    plt.subplot(121)
    plt.xlabel('Epoch')
    plt.ylabel('m')
    plt.title("pesudo-range residual")
    plt.axis([0, 2800, -10, 10])

    prns = []
    Resps = []
    for prn in range(1, 47):
        index = 0
        Tow = []
        Resp = []
        plotsep = [0]
        for i in range(0, int(len(data))):
            if data[i].prn == prn:
                Tow. append(data[i].tow % 86400 // 30)
                Resp.append(data[i].resp)
                index += 1
        # if Resp:
        #    print("C{:2d}  {:5.4f}m".format(prn, rms(Resp)))
        # plt.scatter(Tow, Resp,s=1,alpha=0.75)
        if index != 0:
            for i in range(0, len(Resp)-1):
                if Tow[i+1]-Tow[i] > 30:
                    plotsep.append(i)
            plotsep.append(len(Resp))
            for i in range(0,len(plotsep)-1):
                plt.plot(Tow[plotsep[i]+1:plotsep[i+1]], Resp[plotsep[i]+1:plotsep[i+1]],linewidth=0.75)
            prns.append("C"+str(prn))
            Resps.append(rms(Resp))
    plt.subplot(122)
    plt.axis([0, 2800, -10, 10])
    plt.xlabel('Epoch')
    plt.ylabel('mm')
    plt.title("carrier phase residual")

    Rescs = []
    for prn in range(1, 47):
        index = 0
        Tow = []
        Resc = []
        plotsep = [0]
        for i in range(0, int(len(data))):
            if data[i].prn == prn:
                Tow.append(data[i].tow % 86400 // 30)
                Resc.append(data[i].resc*100)
                index = index + 1

        if index != 0:
            for i in range(0, len(Resc) - 1):
                if Tow[i + 1] - Tow[i] > 30:
                    plotsep.append(i)
            # if Tow[-1]==2879:
            plotsep.append(len(Resc))
            for i in range(0, len(plotsep) - 1):
                plt.plot(Tow[plotsep[i] + 1:plotsep[i + 1]], Resc[plotsep[i] + 1:plotsep[i + 1]], linewidth=0.75)
            Rescs.append(rms(Resc))
    plt.savefig(filepath+'.res.png', dpi=600)
    # plt.show()

    width = 0.4
    ind = np.linspace(0.5, len(Resps)-0.5,len(Resps))
    fig = plt.figure(2, figsize=(14, 7))
    ax = fig.add_subplot(211)
    # Bar Plot
    ax.bar(ind, Resps, width, color='green')
    # Set the ticks on x-axis
    ax.set_xticks(ind)
    ax.set_xticklabels(prns)
    #ax.set_xlabel('Epoch')
    ax.set_ylabel('m')
    ax.set_title("pesudorange residual for single satellite")
    #plt.savefig(filepath + '.resp.png', dpi=600)

    # fig = plt.figure(3, figsize=(14, 5))
    ax1 = fig.add_subplot(212)
    # Bar Plot
    ax1.bar(ind, Rescs, width, color='green')
    # Set the ticks on x-axis
    ax1.set_xticks(ind)
    ax1.set_xticklabels(prns)
    ax1.set_xlabel('Satellite PRN')
    ax1.set_ylabel('mm')
    ax1.set_title("carrier phase residual for single satellite")
    plt.savefig(filepath + '.satres.png', dpi=600)
    # plt.show()
    # plt.close()

    return


if __name__ == '__main__':
    filename = filedialog.askopenfilename(filetypes=[('stat', '*.stat'), ('All Files', '*')])
    data, filepath = readstat(filename)
    ReadData(data, filepath)



