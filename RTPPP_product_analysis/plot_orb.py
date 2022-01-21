# coding=utf-8
# !/usr/bin/env python
"""
Program: plot_orb.py
Function: Plot orbit error on RAC direction with file from SP3compare.py
Author:LZ_CUMT
Version:1.0
Date:2021/12/22
"""
from ORBcompare import *
import matplotlib.pyplot as plt
from matplotlib import rcParams

def readsp3comp(file):
    f = open(file, "r")
    lns = f.readlines()
    rac = np.zeros((148,3))
    for ln in lns:
        if ln[0] != "%" and len(ln) == 28:
            sys = ln[0]
            prn = int(ln[1:3])
            sat = satno(sys, prn)
            rac[sat, 0] = float(ln[5:11])
            rac[sat, 1] = float(ln[13:19])
            rac[sat, 2] = float(ln[21:27])
    return rac

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

def float_range(range1, float):
    range2 = []
    for i in range1:
        range2.append(i+float)
    return range2

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

def plot_rac(rac, outfile):
    satrange = [0, 32, 59, 95, 113, 141]  # G R E C2 C3
    for i in range(len(satrange)-1):
        plt.figure(figsize=(6, 3))
        listsat = [x for x in range(satrange[i], satrange[i+1])]
        listsat = deletesat(listsat, i)
        plot_std_r = rac[listsat, 0]
        plot_std_a = rac[listsat, 1]
        plot_std_c = rac[listsat, 2]
        plt.bar(float_range(range(len(plot_std_a)),-0.3), plot_std_r, width=0.3)
        plt.bar(range(len(plot_std_a)), plot_std_a, width=0.3)
        plt.bar(float_range(range(len(plot_std_a)),0.3), plot_std_c, width=0.3)
        listid = listsat2listid(listsat)
        listprn = range(len(listid))
        # plt.ylim([0,10])
        plt.xticks(listprn, listid, rotation=90)
        plt.xlabel("卫星PRN号", labelpad=2.0)
        plt.ylabel("轨道误差RMS[cm]")
        plt.legend(["R", "A", "C"], fontsize='small', loc='upper right')
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.savefig(outfile + 'ORB'+str(i)+".png", dpi=400)
    plt.show()
    print("[INFO] Finish Plotting!")

if __name__ == '__main__':
    init_global()
    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 12,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)

    filepath = r"D:\RT-stream4\test"
    file = filepath + "\\" + r'SP3compare_satellite.log'
    rac = readsp3comp(file)
    plot_rac(rac, filepath)