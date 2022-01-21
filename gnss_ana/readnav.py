# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""

from cmn import *
import math

def SQR(x):
    return ((x)*(x))

def satno(sys, prn):
    NSATGPS = 32
    NSATGLO = 27
    NSATGAL = 36
    NSATBDS = 46
    NSATQZS = 7
    if sys == 'G':
        sat = prn - 1
    elif sys == 'R':
        sat = NSATGPS + prn - 1
    elif sys == 'E':
        sat = NSATGPS + NSATGLO + prn - 1
    elif sys == 'C':
        sat = NSATGPS + NSATGLO + NSATGAL + prn - 1
    elif sys == 'J':
        sat = NSATGPS + NSATGLO + NSATGAL + NSATBDS + prn - 1
    else:
        sat = 0
    return sat

# --------------------广播星历文件读取及卫星位置计算-----------------------------------
# 读取广播星历
# 输出星历结构体
def readbrdc(navfile):
    ephs = []
    gephs = []
    f = open(navfile)
    ln = f.readline()
    while ln:
        if 'RINEX VERSION / TYPE' in ln:
            ver = float(ln[0:9])
        if 'END OF HEADER' in ln:
            break
        ln = f.readline()
    while ln:
        ln = f.readline()
        if len(ln) == 0:
            break
        head = ln.split(' ')
        sys = head[0][0]
        prn = int(head[0][1:3])
        sat = satno(sys, prn)
        year = int(head[1])
        month = int(head[2])
        day = int(head[3])
        hour = int(head[4])
        min = int(head[5])
        sec = float(ln[21:23])
        ep = [year, month, day, hour, min, sec]
        toc = epoch2time(ep)
        if ln[0] == 'R':
            week, tow = time2gpst(toc)
            toc = gpst2time(week, math.floor((tow+450.0)/900.0)*900)
            dow = int(math.floor(tow/86400.0))
            geph = gEph()
            geph.prn = head[0]
            geph.sat = sat
            if ver <= 2.99:
                tod = float(ln[61:80])
            else:
                tod = math.fmod(float(ln[61:80]), 86400.0)
            tof = gpst2time(week, tod+dow*86400.0)
            tof = adjday(tof, toc)
            geph.toe = utc2gpst(toc)
            # print(geph.prn, geph.toe, sow, tow)
            geph.tof = utc2gpst(tof)
            geph.iode = int(math.fmod(tow + 10800.0, 86400.0) / 900.0 + 0.5)
            geph.taun = -float(ln[23:42])
            geph.gamn = float(ln[42:61])
            ln = f.readline()
            geph.pos[0] = float(ln[4:23]) * 1000
            geph.vel[0] = float(ln[23:42]) * 1000
            geph.acc[0] = float(ln[42:61]) * 1000
            geph.svh = int(float(ln[61:80]))
            ln = f.readline()
            geph.pos[1] = float(ln[4:23]) * 1000
            geph.vel[1] = float(ln[23:42]) * 1000
            geph.acc[1] = float(ln[42:61]) * 1000
            geph.frq = int(float(ln[61:80]))
            ln = f.readline()
            geph.pos[2] = float(ln[4:23]) * 1000
            geph.vel[2] = float(ln[23:42]) * 1000
            geph.acc[2] = float(ln[42:61]) * 1000
            geph.age = int(float(ln[61:80]))
            if geph.frq > 128:
                geph.frq -= 256
            gephs.append(geph)
        elif ln[0] == 'S':
            for i in range(3):
                ln = f.readline()
        elif ln[0] == 'I':
            for i in range(7):
                ln = f.readline()
        else:
            eph = Eph()
            eph.prn = head[0]
            eph.sat = sat
            eph.toc = toc
            if sys == 'C':
                eph.toc = bdt2gpst(eph.toc)  # bdt -> gpst
            eph.clk = np.array([float(ln[23:42]), float(ln[42:61]), float(ln[61:80])])

            ln = f.readline()
            eph.iode = int(float(ln[4:23]))
            eph.crs = float(ln[23:42])
            eph.deln = float(ln[42:61])
            eph.M0 = float(ln[61:80])
            ln = f.readline()
            eph.cuc = float(ln[4:23])
            eph.e = float(ln[23:42])
            eph.cus = float(ln[42:61])
            eph.A = SQR(float(ln[61:80]))
            ln = f.readline()
            eph.toes = float(ln[4:23])
            eph.cic = float(ln[23:42])
            eph.OMG0 = float(ln[42:61])
            eph.cis = float(ln[61:80])
            ln = f.readline()
            eph.i0 = float(ln[4:23])
            eph.crc = float(ln[23:42])
            eph.omg = float(ln[42:61])
            eph.OMGd = float(ln[61:80])
            ln = (f.readline()).rstrip()
            eph.idot = float(ln[4:23])
            eph.code = int(float(ln[23:42]))
            eph.week = int(float(ln[42:61]))
            if sys == 'G' or sys == 'J':
                eph.flag = int(float(ln[61:80]))
            ln = (f.readline()).rstrip()
            eph.sva = float(ln[4:23])
            eph.svh = int(float(ln[23:42]))
            eph.tgd[0] = float(ln[42:61])
            if sys == 'G' or sys == 'J':
                eph.iodc = int(float(ln[61:80]))
            else:
                eph.tgd[1] = float(ln[61:80])
            ln = (f.readline()).rstrip()
            ttr = float(ln[4:23])
            if len(ln) > 24:
                # print(head)
                fit = float(ln[23:42])
                if sys == 'G':
                    eph.fit = fit
                elif sys == 'J':
                    if fit == 0.0:
                        eph.fit = 1.0
                    else:
                        eph.fit = 2.0
                elif sys == 'C':
                    eph.iodc = fit
            if sys == 'C':
                eph.toe = bdt2gpst(bdt2time(eph.week, eph.toes))
                eph.ttr = bdt2gpst(bdt2time(eph.week, ttr))
                eph.toe = adjweek(eph.toe, toc)
                eph.ttr = adjweek(eph.ttr, toc)
                eph.iode = math.fmod(eph.toes/720, 240)
                # print(eph.iode)
            else:
                eph.toe = adjweek(gpst2time(eph.week, eph.toes), eph.toc)
                eph.ttr = adjweek(gpst2time(eph.week, ttr), eph.toc)
            ephs.append(eph)
    return ephs, gephs
