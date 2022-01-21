# coding=utf-8
# !/usr/bin/env python
"""
Program: plot_clk.py
Function: Plot clock error with file from CLKcompare.py
Author:LZ_CUMT
Version:1.0
Date:2021/12/22
"""
from CLKcompare import *
import matplotlib.pyplot as plt
from matplotlib import rcParams

def readclkcomp(file):
    std = np.zeros(148)
    rms = np.zeros(148)
    f = open(file,"r")
    lns = f.readlines()
    for i in range(3,len(lns)):
        sys = lns[i][0]
        prn = int(lns[i][1:3])
        sat = satno(sys, prn)
        std[sat] = float(lns[i][5:15])
        rms[sat] = float(lns[i][19:29])
    return std, rms

def sat2id(sat):
    sys, prn = satsys(sat)
    id = "{}{:02d}".format(sys,prn)
    return id

def listsat2listid(listsat):
    listid = []
    for sat in listsat:
        listid.append(sat2id(sat))
    return listid

def listsat2listprn(listsat):
    listprn = []
    for sat in listsat:
        sys, prn = satsys(sat)
        if sat >= 113:
            listprn.append(prn - 19)
        else:
            listprn.append(prn - 1)
    return listprn

def deletesat(list, i):
    if i == 1:
        poplist = [27, 26, 25, 16, 11]
    elif i == 2:
        poplist = [35, 34, 32, 29, 28, 23, 22, 20, 17, 16, 10, 6]
    elif i == 3:
        poplist = [18, 17, 15]
    elif i == 4:
        poplist = [31]
        for x in poplist:
            list.pop(x - 19)
            return list
    else:
        return list
    for x in poplist:
        list.pop(x - 1)
    return list

def plotclk(std, rms, filepath):
    satrange = [0, 32, 59, 95, 113, 141]  # G R E C2 C3
    for i in range(len(satrange)-1):
        plt.figure(figsize=(6, 3))
        listsat = [x for x in range(satrange[i], satrange[i + 1])]
        listsat = deletesat(listsat, i)
        plot_std = std[listsat]
        plt.bar(range(len(plot_std)),plot_std)
        listid = listsat2listid(listsat)
        listprn = range(len(listid))
        plt.xticks(listprn, listid, rotation=90)
        plt.xlabel("卫星PRN号", labelpad=2.0)
        plt.ylabel("钟产品误差STD[ns]")
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.savefig(filepath[:-4] + str(i) + ".png", dpi=400)
    plt.show()
    print("[INFO] Finish Plotting!")


if __name__ == '__main__':
    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 12,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)

    filepath = r'D:\RT-stream4\test'
    # filepath = r"C:\Users\LZ\Desktop\Pyfile\RTPPP_product_analysis"
    clkcomp = filepath + "\\"+ r'CLKcompare0.txt'
    init_global()
    std, rms = readclkcomp(clkcomp)
    plotclk(std, rms, filepath)
