# coding=utf-8
# !/usr/bin/env python
"""
Program: plot_position.py
Function: plot the RTMG-APP position file
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""
from plot_pos_error.crd_conv import xyz2enu
from plot_pos_error.read_snx import getcrd
import matplotlib.pyplot as plt


def readpos(posfile, basecrd):
    f = open(posfile, "r")
    lns = f.readlines()
    spppos = []
    ppppos = []
    for i in range(len(lns)):
        posline = lns[i][50:].split()
        sppxyz = [float(x) for x in posline[1:4]]
        pppxyz = [float(x) for x in posline[4:7]]
        spppos.append(xyz2enu(sppxyz, basecrd))
        ppppos.append(xyz2enu(pppxyz, basecrd))
    return spppos, ppppos


def plotpos(pos, iden):
    plt.figure(figsize=(6, 5))
    plt.plot(pos)
    plt.title(iden)
    plt.legend(["E", "N", "U"])
    plt.xlabel("Epoch")
    plt.ylabel("Error[m]")
    plt.xlim((0, len(pos)))
    if iden == "SPP":
        plt.ylim((-5, 5))
    elif iden == "PPP":
        plt.ylim((-1, 1))


def readztd(ztdfile):
    f = open(ztdfile, "r")
    lns = f.readlines()
    ztd = []
    for i in range(len(lns)):
        if i != 0:
            ztd.append(float(lns[i][42:50]))
    return ztd


def plotztd(ztd):
    plt.figure(figsize=(6, 5))
    plt.plot(ztd)
    plt.title("ZTD")
    plt.xlabel("Epoch")
    plt.ylabel("ZTD[m]")
    plt.xlim((0, len(ztd)))
    plt.ylim((0, 4))


if __name__ == '__main__':
    posfile = r"E:\workspace\RTMG_APP_EXE\EXE\RTMG_APPData\Ion_free_RTOutPutFiles\position.txt"
    sscfile = r"D:\GNSS_DATA\rt_test1\igs2189.snx"
    ztdfile = r"E:\workspace\RTMG_APP_EXE\EXE\RTMG_APPData\Ion_free_RTOutPutFiles\ZTDW_Clock.txt"
    siteid = "JFNG"
    basecrd = getcrd(siteid, sscfile)
    spppos, ppppos = readpos(posfile, basecrd)
    plotpos(spppos, "SPP")
    plotpos(ppppos, "PPP")
    ztd = readztd(ztdfile)
    plotztd(ztd)
    plt.show()
