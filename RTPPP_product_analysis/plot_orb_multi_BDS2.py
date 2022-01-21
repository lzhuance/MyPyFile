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
            rac[sat, 2] = float(ln[20:27])
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
    #satrange = [95, 100]
    satrange = [100, 113]
    list_sat = [[95,96,97,98,99],[100,101,102,103,104,105,106,107,108,110]]
    # satrange = [0, 32, 59, 95, 113, 141]  # G R E C2 C3
    #satrange = [0, 32]  # G R E C2 C3
    for i in range(len(satrange)-1):
        plt.subplot(5, 1, ii+1)
        listsat = list_sat[1]
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
            plt.ylabel("轨道误差RMS[m]")
        #if ii == 2:
            #plt.legend(["R", "A", "C"], fontsize='small', loc='upper right',ncol=3)
            #plt.legend(["R", "A", "C"], fontsize='small', ncol=3)
        #plt.ylim([0, 1000])
        #plt.yticks([0, 400, 800],[0,4,8])
        #plt.text(-0.6, 800, ac[ii])
        plt.ylim([0, 40])
        plt.yticks([0, 10, 20,30])
        #plt.text(-0.6, 800, ac[ii])
        #plt.text(0.2, 800, "GEO")
        #plt.text(1, 800, "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(\
        #    float(mean[0][0]),float(mean[0][1]), float(mean[0][2])))
        """
        if mean1[ii][0] != 0:
            plt.text(0.2, 800,
                     "均值: R={:>4.2f} m  A={:>4.2f} m  C={:>4.2f} m".format(float(mean1[ii][0])/100,
                                                                              float(mean1[ii][1])/100, \
                                                                              float(mean1[ii][2])/100))
        """
        if mean2[ii][0]!=0:
            plt.text(-0.8, 30, "MEO")
            if ii == 3:
                plt.text(0.8, 30,
                         "均值: R={:>6.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean2[ii][0]),
                                                                                  float(mean2[ii][1]), \
                                                                                  float(mean2[ii][2])))
            elif ii == 2:
                plt.text(0.8, 30,"均值: R={:>6.2f} cm  A={:>5.2f} cm  C={:>6.2f} cm".format(float(mean2[ii][0]), float(mean2[ii][1]), \
                                                                                float(mean2[ii][2])))
            else:
                plt.text(0.8, 30,"均值: R={:>6.2f} cm  A={:>6.2f} cm  C={:>6.2f} cm".format(float(mean2[ii][0]), float(mean2[ii][1]), \
                                                                                float(mean2[ii][2])))
        if mean2[ii][3] != 0:
            plt.text(-0.8, 23, "IGSO")
            if ii == 0:
                plt.text(0.8, 23,"均值: R={:>5.2f} cm  A={:>6.2f} cm  C={:>5.2f} cm".format(float(mean2[ii][3]),
                                                                                  float(mean2[ii][4]),
                                                                                  float(mean2[ii][5])))
            elif ii == 1:
                plt.text(0.8, 23,"均值: R={:>5.2f} cm  A={:>6.2f} cm  C={:>6.2f} cm".format(float(mean2[ii][3]),
                                                                                  float(mean2[ii][4]),
                                                                                  float(mean2[ii][5])))
            else:
                plt.text(0.8, 23,
                     "均值: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean2[ii][3]), float(mean2[ii][4]),
                                                                                float(mean2[ii][5])))

        '''
        
        print(mean)
        if len(mean) == 3:
            plt.text(0.2, 23, "IGSO")
            plt.text(1.2, 23, "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[1][0]), float(mean[1][1]), float(mean[1][2])))
       #     plt.text(1.7, 300, "GEO")
        #    plt.text(4, 300, "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[0][0]), float(mean[0][1]), float(mean[0][2])))
            plt.text(0.2, 30, "MEO")
            plt.text(1.2, 30,"mean: R={:>6.2f} cm  A={:>6.2f} cm  C={:>6.2f} cm".format(float(mean[2][0]), float(mean[2][1]),\
                                                                                float(mean[2][2])))
        if ii == 2:
            plt.text(0.2, 30, "MEO")
            plt.text(1.2, 30,
                     "mean: R={:>6.2f} cm  A={:>6.2f} cm  C={:>6.2f} cm".format(float(mean[0][0]), float(mean[0][1]), \
                                                                                float(mean[0][2])))
        if ii == 1:
            plt.text(0.2, 23, "IGSO")
            plt.text(1.2, 23,
                     "mean: R={:>5.2f} cm  A={:>5.2f} cm  C={:>5.2f} cm".format(float(mean[1][0]), float(mean[1][1]),
                                                                                float(mean[1][2])))
        #     plt.text(1.7, 300, "GEO")
        '''
        plt.gcf().subplots_adjust(bottom=0.2)
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
    filelist = ["cassSP3compare_satellite.log", "cnesSP3compare_satellite.log", "dlrsSP3compare_satellite.log",\
                "gfzsSP3compare_satellite.log", "whusSP3compare_satellite.log"]
    filelist2 = ["cassSP3compare_system.log", "cnesSP3compare_system.log", "dlrsSP3compare_system.log",\
                "gfzsSP3compare_system.log", "whusSP3compare_system.log"]
    filelist3 = ["cassSP3compare_BDSconstellation.log", "cnesSP3compare_BDSconstellation.log", "dlrsSP3compare_BDSconstellation.log",\
                "gfzsSP3compare_BDSconstellation.log", "whusSP3compare_BDSconstellation.log"]
    global ac
    ac = ["CAS","CNES","DLR","GFZ","WHU"]
    sys = "C2"
    mean1 = [[102.66,407.95,343.93],[96.08,506.72,366.21],[0,0,0],[262.79,700.61,671.80],[181.18,611.07,421.52]]
    mean2 = [[4.52,7.00,8.80,16.64,5.84,19.90], [0,0,0,9.89,11.32,15.74],[7.40,12.82,7.74,0,0,0],
             [3.67,12.72,10.22,35.56,42.27,55.63], [2.79,6.42,5.08,13.20,15.67,19.25]]
    png_file = filepath + "\\" + "SP3accompare" + sys +"56.png"
    fig = plt.subplots(nrows=len(filelist), ncols=1, figsize=(5, 6), sharex=True, sharey=True)
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