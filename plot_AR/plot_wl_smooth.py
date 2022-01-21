
import os
import math
import matplotlib.pyplot as plt
from tkinter import filedialog
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
        self.snr    = 0.0
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
    for i in range(0,len(Res)):
        s += Res[i]*Res[i]
    return math.sqrt(s/len(Res))

def readstat(filename):
    Multi_stat = []
    path = ""
    filepath = filename.split('/')
    for i in range(0,len(filepath)-1):
        path = path+filepath[i]+'/'
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

def ReadData(data):
    Tow1 = []
    Mw1  = []
    Smw1 = []
    Smwv1= []
    Tow2 = []
    Mw2  = []
    Smw2 = []
    Smwv2= []

    for i in range(0, int(len(data))):
        if data[i].sat == 'G14':
            if data[i].smwv < 100:
                Tow1. append(data[i].tow % 86400 // 30)
                Mw1.  append(data[i].mw)
                Smw1. append(data[i].smw)
                Smwv1.append(data[i].smwv)
        if data[i].sat == 'C34':
            if data[i].smwv < 100:
                Tow2. append(data[i].tow % 86400 // 30)
                Mw2.  append(data[i].mw)
                Smw2. append(data[i].smw)
                Smwv2.append(data[i].smwv)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.scatter(Tow1, Mw1, color='b', s=10, alpha=1)
    plt.scatter(Tow1, Smw1, color='r', s=10, alpha=1)
    plt.xlabel('历元', fontsize='x-large')
    plt.ylabel('宽巷模糊度周数', fontsize='x-large')
    plt.xticks(fontsize='x-large')
    plt.yticks(fontsize='x-large')
    plt.title("G06", fontsize='xx-large')

    plt.subplot(1, 2, 2)
    plt.scatter(Tow2, Mw2, color='b', s=10, alpha=1)
    plt.scatter(Tow2, Smw2, color='r', s=10, alpha=1)
    plt.xlabel('历元', fontsize='x-large')
    plt.legend(["平滑前", "平滑后"], fontsize='x-large')
    plt.xticks(fontsize='x-large')
    plt.yticks(fontsize='x-large')
    plt.title("C34", fontsize='xx-large')

    plt.subplots_adjust(hspace=0)
    plt.savefig(filepath + 'MW.png', dpi=400)
    plt.show()


if __name__ == '__main__':
    # 设置matplotlib使用中文
    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 10.5,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)

    filename = filedialog.askopenfilename(filetypes=[('stat', '*.stat'), ('All Files', '*')])
    data, filepath = readstat(filename)
    ReadData(data)


