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

def calave(std):
    sum = 0
    num = 0
    for i in range(len(std)):
        if i != 26 and i != 27 and std[i] != 0:
            num += 1
            sum += std[i]
    return sum/num

def calbds3ave(std):
    sum1 = 0
    num1 = 0
    sum2 = 0
    num2 = 0
    for i in range(len(std)):
        if i == 17 or i == 18 or i == 19:
            num2 += 1
            sum2 += std[i]
        elif i != 26 and i != 27 and std[i] != 0:
            num1 += 1
            sum1 += std[i]
    if num2 == 0:
        return sum1/num1, 0
    return sum1/num1, sum2/num2

def calbds2ave(std):
    sum1 = 0
    num1 = 0
    sum2 = 0
    num2 = 0
    sum3 = 0
    num3 = 0
    for i in range(len(std)):
        if i ==1 or i == 2 or i == 3 or i == 4 or i == 0:
            num1 += 1
            sum1 += std[i]
        elif i == 11 or i == 10 or i == 13:
            num2 += 1
            sum2 += std[i]
        else:
            num3 += 1
            sum3 += std[i]
    if num1 != 0:
        ave1 = sum1/num1
    else:
        ave1 = 0
    if num2 != 0:
        ave2 = sum2 / num2
    else:
        ave2 = 0
    if num3 != 0:
        ave3 = sum3 / num3
    else:
        ave3 = 0
    return [ave1, ave2, ave3]

def plotclk(std, rms, filepath, ii):
    satrange = sys2range(sys)
    # satrange = [0, 32, 59, 95, 113, 141]  # G R E C2 C3
    for i in range(len(satrange)-1):
        plt.subplot(5, 1, ii + 1)
        listsat = [x for x in range(satrange[i], satrange[i + 1])]
        listsat = deletesat(listsat, sys)
        plot_std = std[listsat]
        if sys == "G":
            mean = calave(std[listsat])
        if sys == "C3":
            mean = calbds3ave(std[listsat])
        if sys == "C2":
            mean = calbds2ave(std[listsat])
        plt.bar(range(len(plot_std)), plot_std)
        listid = listsat2listid(listsat)
        listprn = range(len(listid))
        plt.xticks(listprn, listid, rotation=90)
        plt.xlabel("卫星PRN号", labelpad=2.0)
        if ii == 2:
            plt.ylabel("钟产品误差STD[ns]")
        if sys == "G":
            plt.ylim([0, 0.5])
            plt.yticks([0,0.2,0.4])
            plt.xlim(-1,32)
            plt.text(-0.5,0.4, ac[ii])
            plt.text(2,0.4, "均值: {:4.2f} ns".format(mean))
        elif sys == "C3":
            plt.ylim([0, 5])
            plt.yticks([0,2,4])
            plt.xlim(-1,28)
            plt.text(-0.5, 9/12*5, ac[ii])
            if mean[1] == 0.0:
                plt.text(2, 9/12*5, "均值: MEO: {:4.2f} ns ".format(mean[0]))
            else:
                plt.text(2, 9/12*5, "均值: MEO: {:4.2f} ns IGSO: {:4.2f} ns".format(mean[0],mean[1]))
        elif sys == "C2":
            plt.ylim([0, 5])
            plt.yticks([0,2,4])
            #plt.xlim(-1,28)
            plt.text(-0.5, 4, ac[ii])
            #if mean[0] == 0.0:
            plt.text(1, 4, "均值:")
            if ii ==1:
                plt.text(2, 4, "GEO: {:4.2f} ns IGSO: {:4.2f} ns".format(mean[0],mean[2]))
            elif ii==2:
                plt.text(2, 4, "MEO: {:4.2f} ns ".format(mean[1]))
            else:
                plt.text(2, 4, "GEO: {:4.2f} ns MEO: {:4.2f} ns IGSO: {:4.2f} ns".format(mean[0], mean[1],mean[2]))
            #if mean[1] == 0.0:
            #    plt.text(2, 9/12*5, "均值: MEO: {:4.2f} ns ".format(mean[0]))
            #else:
            #    plt.text(2, 9/12*5, "均值: MEO: {:4.2f} ns IGSO: {:4.2f} ns".format(mean[0],mean[1]))
        plt.gcf().subplots_adjust(bottom=0.2)
    #plt.show()
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
    init_global()
    filepath = r"D:\RT-stream4\test\clk"
    filelist = ["cass21892CLKcompare.txt", "cnes21892CLKcompare.txt", "dlrs21892CLKcompare.txt",\
                "gfzs21892CLKcompare.txt", "whus21892CLKcompare.txt"]

    global ac
    ac = ["CAS","CNES","DLR","GFZ","WHU"]
    sys = "C3"
    png_file = filepath + "\\" + "CLKaccompare" + sys +"4.png"
    fig = plt.subplots(nrows=len(filelist), ncols=1, figsize=(8, 6), sharex=True, sharey=True)
    for i in range(len(filelist)):
        file = filepath + "\\" + filelist[i]
        std, rms = readclkcomp(file)
        plotclk(std, rms, filepath, i)
    plt.subplots_adjust(hspace=0, wspace=0)
    plt.savefig(png_file, dpi=600)
    plt.show()
