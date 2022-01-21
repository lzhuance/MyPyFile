
import os
import math
import matplotlib.pyplot as plt
from tkinter import filedialog


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
    s=0
    for i in range(0,len(Res)):
        s+=Res[i]*Res[i]
    return math.sqrt(s/len(Res))

def readstat(filename):
    Multi_stat = []
    path=""
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
    return Multi_stat,path

def ReadData(data):
    Tow = []

    Mw  = []
    Smw = []
    Smwv= []

    ResWl = []
    ResNl = []

    #figprn=2
    #for i in range(int(len(data)/2),int(len(data))):
    #for i in range(0, int(len(data)/2)):
    for prn in range(1, 33):
        for i in range(0, int(len(data))):
            if data[i].prn==prn:
                if data[i].smwv<100 :
                    Tow. append(data[i].tow % 86400 // 30)
                    Mw.  append(data[i].mw)
                    Smw. append(data[i].smw)
                    Smwv.append(data[i].smwv)

                    ResWl.append(data[i].NW-data[i].BW)
                    ResNl.append(data[i].N1-data[i].B1)
    return Tow, Mw, Smw, Smwv, ResWl, ResNl

def PlotResDis(ResWl,ResNl,filepath):
    plt.figure(figsize=(10, 5))

    plt.subplot(121)
    plt.hist(ResWl,30,(-0.3,0.3),density=True)
    plt.title("WL Residual Distrbution")
    plt.text(-0.3,3,'RMS:%.4f cycles'%(rms(ResWl)),fontsize=12)

    plt.subplot(122)
    plt.hist(ResNl,30,(-0.3,0.3),density=True)
    plt.title("NL Residual Distrbution")
    plt.text(-0.3, 5, 'RMS:%.4f cycles' % (rms(ResNl)), fontsize=12)

    plt.savefig(filepath+'ResDis.tiff',dpi=360)
    plt.show()

    return

def PlotMW(Tow,Mw,Smw,Smwv,filepath):
    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plt.scatter(Tow, Mw,  color='b',s=4, alpha = 0.75)
    plt.scatter(Tow, Smw, color='r',s=4, alpha = 0.75)
    plt.ylabel('cycle')
    plt.title("MW and Smoothed MW")
    plt.legend(["MW","Smoothed MW"])

    plt.subplot(122)
    plt.scatter(Tow, Smwv, color='g',s=4 ,alpha = 0.75)
    plt.ylabel('cycle^2')
    plt.title("Smoothed MW variance")
    plt.savefig(filepath+'MW.tiff',dpi=360)
    plt.show()

def PlotRes(Tow,ResWl, ResNl, filepath):
    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plt.scatter(Tow, ResWl,color='g',s=4,alpha=0.75)
    plt.ylabel('cycle')
    plt.title("WL residual")

    plt.subplot(122)
    plt.scatter(Tow, ResNl,color='g',s=4,alpha=0.75)
    plt.ylabel('cycle')
    plt.title("NL residual")

    plt.savefig(filepath+'Res.tiff',dpi=360)
    plt.show()

    return



if __name__ == '__main__':
    filename = filedialog.askopenfilename(filetypes=[('stat', '*.stat'), ('All Files', '*')])
    data,filepath = readstat(filename)
    Tow,Mw,Smw,Smwv,ResWl,ResNl=ReadData(data)
    #PlotResDis(ResWl, ResNl,filepath)
    PlotMW(Tow, Mw, Smw, Smwv, filepath)
    #PlotRes(Tow,ResWl, ResNl, filepath)



