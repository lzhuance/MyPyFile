# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/01
 '''

from rtkcmn import ymdhms2wksow

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
        self.inf_fbs = []

def readsp3(filepath):
    fp = open(filepath)
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
            week, sow = ymdhms2wksow(year, month, day, hour, mini, sec)
            fEp = Satpos_1ep()
            fEp.week = week
            fEp.sow = sow
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