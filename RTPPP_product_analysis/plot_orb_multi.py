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

def readsys(file, sys):
    f = open(file)
    lns = f.readlines()
    for ln in lns:
        if ln[0] != "%" and sys in ln:
            mean = ln.split()
    return mean[1:]

def readbdssys(file, sys):
    f = open(file)
    lns = f.readlines()
    bdmean = []
    for ln in lns:
        if ln[0] != "%" and sys in ln:
            mean = ln.split()
            bdmean.append(mean[1:])
    return bdmean

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

def deletesat(list, sys):
    if sys == "R":
        poplist = [27, 26, 25, 16, 11]
    elif sys == "E":
        poplist = [35, 34, 32, 29, 28, 23, 22, 20, 17, 16, 10, 6]
    elif sys == "C2":
        poplist = [18, 17, 15]
    elif sys == "C3":
        poplist = [31]
        for x in poplist:
            list.pop(x - 19)
            return list
    else:
        return list
    for x in poplist:
        list.pop(x - 1)
    return list

def sys2range(sys):
    syss = ["G", "R", "E", "C2", "C3"]
    satrange = [0, 32, 59, 95, 113, 141]  # G R E C2 C3
    for i in range(len(syss)):
        if sys == syss[i]:
            return satrange[i:i+2]

def plot_rac(rac, outfile, ii, mean, sys):
    satrange = sys2range(sys)
    # satrange = [0, 32, 59, 95, 113, 141]  # G R E C2 C3
    #satrange = [0, 32]  # G R E C2 C3
    for i in range(len(satrange)-1):
        #plt.figure(figsize=(6, 3))
        plt.subplot(5, 1, ii + 1)
        listsat = [x for x in range(satrange[i], satrange[i+1])]
        listsat = deletesat(listsat, sys)
        plot_std_r = rac[listsat, 0]
        plot_std_a = rac[listsat, 1]
        plot_std_c = rac[listsat, 2]
        plt.bar(float_range(range(len(plot_std_a)),-0.3), plot_std_r, width=0.3)
        plt.bar(range(len(plot_std_a)), plot_std_a, width=0.3)
        plt.bar(float_range(range(len(plot_std_a)),0.3), plot_std_c, width=0.3)
        listid = listsat2listid(listsat)
        listprn = range(len(listid))
        plt.xticks(listprn, listid, rotation=90)
        plt.xlabel("卫星PRN号", labelpad=3.0)
        if ii == 2:
            plt.ylabel("轨道误差RMS[cm]")
        if ii == 0:
            plt.legend(["R", "A", "C"], fontsize='small', loc='upper right',ncol=3)
        if sys == "G":
            plt.ylim([0, 15])
            plt.xlim([-1, 32])
            plt.yticks([0, 5, 10])
            plt.text(-0.5, 12, ac[ii])
            #plt.text(3, 11, "mean: R={:4.2f} A={:4.2f} C={:4.2f}".format(mean[0], mean[1], mean[2]))
            plt.text(2, 12, "均值: R = {} cm  A = {} cm  C = {} cm".format(mean[0], mean[1], mean[2]))
        elif sys == "C3":
            plt.ylim([0, 20])
            plt.xlim([-1, 28])
            plt.yticks([0, 5, 10,15])
            plt.text(-0.5, 16.2, ac[ii])
            #plt.text(3, 11, "mean: R={:4.2f} A={:4.2f} C={:4.2f}".format(mean[0], mean[1], mean[2]))
            plt.text(1.7, 16.2, "MEO")
            plt.text(4, 16.7, "均值: R={:>6.2f} cm  A={:>6.2f} cm  C={:>6.2f} cm".format(float(mean[0][0]), float(mean[0][1]), float(mean[0][2])))
            if len(mean) != 1:
                plt.text(1.7, 12.5, "IGSO")
                plt.text(4, 12.5, "均值: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[1][0]), float(mean[1][1]), float(mean[1][2])))
        elif sys == "C2":
            plt.ylim([0, 800])
            plt.xlim([-1, 6])
            #plt.yticks([0, 5, 10,15])
            plt.text(-0.5, 400, ac[ii])
            #plt.text(3, 11, "mean: R={:4.2f} A={:4.2f} C={:4.2f}".format(mean[0], mean[1], mean[2]))
            print(mean)
            if len(mean) == 3:
                plt.text(1.7, 400, "IGSO")
                plt.text(4, 400, "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[1][0]), float(mean[1][1]), float(mean[1][2])))
                plt.text(1.7, 300, "GEO")
                plt.text(4, 300, "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[0][0]), float(mean[0][1]), float(mean[0][2])))
                plt.text(1.7, 500, "MEO")
                plt.text(4, 500,"mean: R={:>6.2f} cm  A={:>6.2f} cm  C={:>6.2f} cm".format(float(mean[2][0]), float(mean[2][1]),
                                                                            float(mean[2][2])))
            elif len(mean) == 2:
                plt.text(1.7, 400, "IGSO")
                plt.text(4, 400, "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[1][0]),
                                                                                            float(mean[1][1]),
                                                                                            float(mean[1][2])))
                plt.text(1.7, 300, "GEO")
                plt.text(4, 300, "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[0][0]),
                                                                                            float(mean[0][1]),
                                                                                            float(mean[0][2])))
            elif len(mean) == 1:
                plt.text(1.7, 500, "MEO")
                plt.text(4, 500, "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[0][0]), float(mean[0][1]), float(mean[0][2])))

        plt.gcf().subplots_adjust(bottom=0.2)
        # plt.grid(ls="--")
        # plt.savefig(outfile + 'ORB'+str(i)+".png", dpi=400)
    #plt.show()
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

    filepath = r"D:\RT-stream4\test\sp3"
    filelist = ["casaSP3compare_satellite.log", "cneaSP3compare_satellite.log", "dlraSP3compare_satellite.log",\
                "gfzaSP3compare_satellite.log", "whuaSP3compare_satellite.log"]
    filelist2 = ["casaSP3compare_system.log", "cneaSP3compare_system.log", "dlraSP3compare_system.log",\
                "gfzaSP3compare_system.log", "whuaSP3compare_system.log"]
    filelist3 = ["casaSP3compare_BDSconstellation.log", "cneaSP3compare_BDSconstellation.log", "dlraSP3compare_BDSconstellation.log",\
                "gfzaSP3compare_BDSconstellation.log", "whuaSP3compare_BDSconstellation.log"]
    global ac
    ac = ["CAS","CNES","DLR","GFZ","WHU"]
    sys = "C3"
    png_file = filepath + "\\" + "SP3accompare" + sys +"2.png"
    fig = plt.subplots(nrows=len(filelist), ncols=1, figsize=(8, 6), sharex=True, sharey=True)
    for i in range(len(filelist)):
        file = filepath + "\\" + filelist[i]
        if sys == "C2" or sys == "C3":
            file2 = filepath + "\\" + filelist3[i]
            mean = readbdssys(file2, sys)
        else:
            file2 = filepath + "\\" + filelist2[i]
            mean = readsys(file2, sys)
        rac = readsp3comp(file)

        plot_rac(rac, filepath, i, mean, sys)
    plt.subplots_adjust(hspace=0, wspace=0)
    plt.savefig(png_file, dpi=600)
    plt.show()