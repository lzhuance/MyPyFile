# coding=utf-8
# !/usr/bin/env python
"""
Program: readobs.py
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/08
"""
import time
from cmn import *
import numpy as np

class ObsInfo:
    def __init__(self):
        self.ver = 0
        self.site = ""
        self.approx = []
        self.obstypes = []
        self.freq = []
        self.ts = 0
        self.te = 0
        self.span = 0

class ObsData:
    def __init__(self):
        self.week = 0
        self.sow = 0
        self.time = 0
        self.data = 0
        self.n = 0
        self.P = np.zeros(5)
        self.L = np.zeros(5)
        self.D = np.zeros(5)
        self.S = np.zeros(5)

# GPS  L1  L2  L5
# GLO  L1  L2  L3
# BDS  B1I B2I(B2b) B3I B1C B2a
# GAL  E1  E5a E5b E5  E6
# QZS  L1  L2  L5  L6

def epoch2time(ep):
    year = ep[0]
    mon = ep[1]
    day = ep[2]
    hour = ep[3]
    min = ep[4]
    sec = ep[5]
    doy = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    if year < 1970 or 2099 < year or mon < 1 or 12 < mon:
        return 0
    if year % 4 == 0 and mon >= 3:
        days = int((year - 1970) * 365 + (year - 1969) / 4 + doy[mon-1] + day - 2 + 1)
    else:
        days = int((year - 1970) * 365 + (year - 1969) / 4 + doy[mon-1] + day - 2)
    return days * 86400 + hour * 3600 + min * 60 + sec

def time2gpst(time):
    t0 = epoch2time([1980, 1, 6, 0, 0, 0])
    sec = time - t0
    w = int(sec/(86400 * 7))
    s = sec - w * 86400 * 7
    return w, s

def id2sat(id):
    sys = id[0]
    prn = int(id[1:])
    return satno(sys, prn)

def sys2index(sys):
    sysrange = ["G", "R", "E", "C", "J", "I", "S"]
    for i in range(len(sysrange)):
        if sys == sysrange[i]:
            return i

def findtype(sys, obstypes):
    sysrange = ["G", "R", "E", "C", "J"]
    for i in range(len(sysrange)):
        if sys == sysrange[i]:
            return obstypes[i]

def data2PLDS(obs, info):
    P = np.zeros(5)
    L = np.zeros(5)
    D = np.zeros(5)
    S = np.zeros(5)
    type = "CLDS"
    data = obs.data
    for i in range(len(data)):
        sat = data[0]
        sys, prn = satsys(sat)
        obstype = info.obstypes[sys2index(sys)]
        #for obstype_1 in obstype:
           # if obstype_1


def readobs3(obsfile):
    obss = []
    info = ObsInfo()

    fobs = open(obsfile, "r")
    ln = fobs.readline()
    ver = float(ln[0:10])
    obstypes = [[], [], [], [], [], [], []]
    if ver <= 2.99:
        print("[ERROR] obs file version is 2.xx!")
        exit(0)
    info.ver = ver
    while ln:
        ln = fobs.readline()
        if "MARKER NAME" in ln:
            site = ln[0:4].upper()
            info.site = site
        elif "SYS / # / OBS TYPES" in ln:
            if ln[0] != "":
                sys = ln[0]
                index = sys2index(sys)
                typenum = int(ln[4:6])
                extratype = floor(typenum/13)
                typeline = ln[7:58]
                if extratype > 0:
                    for i in range(extratype):
                        ln1 = fobs.readline()
                        typeline += ln1[7:58]
                typeline.strip()
                obstypes[index] = typeline.split()
                info.obstypes = obstypes
        elif "END OF HEADER" in ln:
            break

    while ln:
        ln = fobs.readline()
        if ln == "":
            break
        if ln[0] == ">":
            obshead = ln.split()
            ep = [int(x) for x in obshead[1:6]] + [float(obshead[6])]
            eof = obshead[7]
            satnum = int(obshead[8])
            time = epoch2time(ep)
            week, sow = time2gpst(time)
            obs = ObsData()
            obs.time = time
            obs.week = week
            obs.sow = sow
            obs_ = []
            for i in range(satnum):
                ln = fobs.readline()
                satid = ln[0:3]
                sys = satid[0]
                prn = int(satid[1:])
                sat = satno(sys, prn)
                if sat == 0:
                    continue
                obstype = obstypes[sys2index(sys)]
                obsbody = (ln[3:-1].rstrip()).ljust(len(obstype) * 16)
                obsnum = int(len(obsbody) / 16)
                obs_1 = [sat]
                for j in range(obsnum):
                    if obsbody[16*j+2:16*j+14].isspace():
                        obs_1.append(0)
                    else:
                        obs_1.append(float(obsbody[16*j+2:16*j+14]))
                obs_.append(obs_1)
                obs.data = obs_
                obs.n = len(obs.data)
            data2PLDS(obs, info)
            obss.append(obs)
    info.ts = obss[0].time
    info.te = obss[-1].time
    info.span = timediff(obss[-1].time, obss[-2].time)
    return obss, info
