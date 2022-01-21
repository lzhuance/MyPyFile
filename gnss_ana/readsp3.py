# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""
# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/01
 '''

from cmn import *

class Satpos_base_t:
    def __init__(self):
        self.id = 'X00'
        self.csys  = 'X'
        self.prn   = 0
        self.x   = 0.0
        self.y   = 0.0
        self.z   = 0.0

class Satpos_1ep:
    def __init__(self):
        self.week   = 0
        self.sow    = 0.0
        self.time   = 0.0
        self.inf_fbs = []

def readsp3(sp3file):
    fp = open(sp3file)
    f_Eps = []
    ln = fp.readline()
    while ln:
        if '*' == ln[0]:
            year = int(ln[3:7])
            month = int(ln[8:10])
            day = int(ln[11:13])
            hour = int(ln[14:16])
            mini = int(ln[17:19])
            sec = float(ln[21:31])
            t = epoch2time([year, month, day, hour, mini, sec])
            week, sow = time2gpst(t)
            fEp = Satpos_1ep()
            fEp.week = week
            fEp.sow = sow
            fEp.time = t
            while 1:
                ln = fp.readline()
                if not ln:
                    break
                if '*' == ln[0]:
                    break
                if 'P' != ln[0]:
                    continue
                strs = ln.split()

                ss = strs[0][1:]
                ch = ss[0]
                prn = int(strs[0][2:])
                x = float(strs[1])*1000
                y = float(strs[2])*1000
                z = float(strs[3])*1000

                Satp = Satpos_base_t()
                Satp.id = ss
                Satp.sys = ch
                Satp.prn = prn
                Satp.x = x
                Satp.y = y
                Satp.z = z
                fEp.inf_fbs.append(Satp)
            f_Eps.append(fEp)
        else:
            ln = fp.readline()
    fp.close()
    return f_Eps

def findeph(teph, satposs, sp3span):
    i = 0
    j = len(satposs)-1
    while i < j:
        k = floor((i+j)/2)
        if timediff(satposs[k].time, teph) < 0.0:
            i = k+1
        else:
            j = k
    if i <= 0:
        index = 0
    else:
        index = i-1

    NMAX = 11
    i = index-floor(NMAX/2)
    if i<0:
        i = 0
    elif i+NMAX-1 >= len(satposs):
        i = len(satposs) - NMAX
    t = np.zeros(NMAX)
    for j in range(NMAX):
        t[j] = timediff(satposs[i+j].time,teph)
    print(i,time2epoch(teph),t)
    for j in range(NMAX):
        return 0

def satpos_expand(info, satposs):
    sp3span = timediff(satposs[1].time, satposs[0].time)
    nepoch = int(timediff(info.te, info.ts)/info.span) + 1
    for i in range(nepoch):
        teph = info.ts + info.span * i
        satpos = findeph(teph, satposs, sp3span)
        #print("I")
    return 0
