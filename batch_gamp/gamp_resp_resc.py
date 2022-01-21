
import os
import math
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
from matplotlib import rcParams

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
            stat.snr   = float(str[10])
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

def count(list):
    num = 0
    sum = 0
    sum1 = 0
    sum2 = 0
    for i in range(len(list)):
        if -100 < list[i] < 100:
            num += 1
            sum += list[i]
            sum1 += list[i]*list[i]
    ave = sum/num
    rms = math.sqrt(sum1/num)
    for i in range(len(list)):
        if  -100 < list[i] < 100:
            sum2 += (list[i]-ave)*(list[i]-ave)
    std = math.sqrt(sum2/num)
    return ave, std, rms

def ReadData(data, filepath):
    plt.figure(1, figsize=(7,5.5))

    Respp=[]
    for i in range(0, int(len(data))):
        if data[i].resp < 100:
            Respp.append(data[i].resp)
    avep, stdp, rmsp = count(Respp)
    cc = 'AVE = {:4.2f}m  STD = {:4.2f}m  RMS = {:4.2f}m '.format(avep,stdp,rmsp)
    plt.text(15, 4.5, cc, fontsize='x-large')

    # plt.title("pesudo-range residual")
    plt.axis([0, 2880, -5, 5])
    plt.xlabel('时间[hh:mm]', fontsize='x-large')
    plt.xticks([0, 720, 1440, 2160, 2880],['00:00','06:00','12:00','18:00','00:00'], fontsize='x-large')
    plt.ylabel('伪距残差[m]', fontsize='x-large')
    plt.yticks(fontsize='x-large')
    plt.grid(ls='--')
    prns = []
    Resps = []
    for prn in range(1, 47):
        index = 0
        Tow = []
        Resp = []
        plotsep = [0]
        for i in range(0, int(len(data))):
            if data[i].prn == prn and data[i].resp < 100:
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
                plt.plot(Tow[plotsep[i]+1:plotsep[i+1]], Resp[plotsep[i]+1:plotsep[i+1]], linewidth=0.75)
            prns.append("C"+str(prn))
            Resps.append(rms(Resp))

    plt.savefig(filepath + '.resp.png', dpi=600)

    plt.figure(2, figsize=(7,5))
    plt.axis([0, 2880, -10, 10])
    plt.xlabel('时间[hh:mm]')
    plt.xticks([0, 720, 1440, 2160, 2880],['00:00','06:00','12:00','18:00','00:00'])
    plt.ylabel('相位残差[mm]')
    # plt.title("carrier phase residual")
    plt.grid(ls='--')

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
    plt.savefig(filepath+'.resc.png', dpi=600)
    plt.show()

    width = 0.4
    ind = np.linspace(0.5, len(Resps)-0.5,len(Resps))
    fig = plt.figure(3, figsize=(10, 3.5))
    ax = fig.add_subplot(111)

    # Bar Plot
    ax.bar(ind, Resps, width, color='green')
    # Set the ticks on x-axis
    ax.set_xticks(ind)
    ax.set_xticklabels(prns)
    ax.set_ylabel('Bias[m]')
    ax.set_xlabel('Satellite PRN')
    #ax.set_title("pesudorange residual for single satellite")
    plt.savefig(filepath + '.satresp.png', dpi=600)
    #plt.savefig(filepath + '.resp.png', dpi=600)


    fig = plt.figure(4, figsize=(10, 3.5))
    width = 0.4
    ind = np.linspace(0.5, len(Rescs)-0.5,len(Rescs))
    ax1 = fig.add_subplot(111)
    # Bar Plot
    ax1.bar(ind, Rescs, width, color='green')
    # Set the ticks on x-axis
    ax1.set_xticks(ind)
    ax1.set_xticklabels(prns)
    ax1.set_xlabel('Satellite PRN')
    ax1.set_ylabel('Bias[mm]')
    #ax1.set_title("carrier phase residual for single satellite")
    plt.savefig(filepath + '.satresc.png', dpi=600)
    # plt.show()
    # plt.close()

    return


if __name__ == '__main__':
    filename = filedialog.askopenfilename(filetypes=[('stat', '*.stat'), ('All Files', '*')])
    data, filepath = readstat(filename)

    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 12,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)
    ReadData(data, filepath)



