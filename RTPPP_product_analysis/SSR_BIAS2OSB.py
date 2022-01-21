# coding=utf-8
# !/usr/bin/env python
"""
Program:SSR_BIAS2OSB
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/02
"""
import matplotlib.pyplot as plt
import numpy as np

def mean(array):
    num = 0
    sum = 0.0
    for i in range(len(array)):
        if array[i] != 0:
            num += 1
            sum += array[i]
    if num == 0:
        return 0
    else:
        return sum/num

def osb_sat_ave(osb):
    osb_ave = np.zeros((7, 148))
    for i in range(7):
        for j in range(148):
            osb_ave[i, j] = mean(osb[i, j, :])
    return osb_ave

def sys2index(sys):
    if sys == "G":
        return 0
    elif sys == "R":
        return 1
    elif sys == "E":
        return 2
    elif sys == "C":
        return 3
    elif sys == "J":
        return 4

def satno(sys, prn):
    NSATGPS = 32
    NSATGLO = 27
    NSATGAL = 36
    NSATBDS = 46
    NSATQZS = 7
    NSAT = NSATGPS + NSATGLO + NSATGAL + NSATBDS + NSATQZS
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

def satsys(sat):
    NSATGPS = 32
    NSATGLO = 27
    NSATGAL = 36
    NSATBDS = 46
    NSATQZS = 7
    NSAT = NSATGPS + NSATGLO + NSATGAL + NSATBDS + NSATQZS
    if sat < 0 or NSAT < sat:
        sys = ''
        prn = 0
    elif sat < NSATGPS:
        sys = 'G'
        prn = sat + 1
    elif sat - NSATGPS < NSATGLO:
        sys = 'R'
        prn = sat - NSATGPS + 1
    elif sat - NSATGPS - NSATGLO < NSATGAL:
        sys = 'E'
        prn = sat - NSATGPS - NSATGLO + 1
    elif sat - NSATGPS - NSATGLO - NSATGAL < NSATBDS:
        sys = 'C'
        prn = sat - NSATGPS - NSATGLO - NSATGAL + 1
    elif sat - NSATGPS - NSATGLO - NSATGAL - NSATBDS < NSATQZS:
        sys = 'J'
        prn = sat - NSATGPS - NSATGLO - NSATGAL - NSATBDS + 1
    else:
        sys = ''
        prn = 0
    return sys, prn

def id2sat(id):
    sys = id[0]
    prn = int(id[1:])
    return satno(sys, prn)

def sat2id(sat):
    sys, prn = satsys(sat)
    return "{}{:02d}".format(sys,prn)

def sat2svn(sat):
    sys, prn = satsys(sat)
    return "{}{:03d}".format(sys,prn)

def getosb(osb_line, obs_type):
    index = -1
    for i in range(len(obs_type)):
        if osb_line == obs_type[i][1:]:
            index = i
    return index

def scanbnc(file):
    f = open(file, "r")
    head = []
    osb_num = []
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        if lines[i][0] != ">":
            continue
        head_info = lines[i].split()
        if head_info[1] == "CODE_BIAS":
            head.append(i)
            osb_num.append(int(head_info[9]))
    return lines, head, osb_num

def readbnc(file):
    lines, head, osb_num = scanbnc(file)
    CLIGHT = 299792458.0
    osb = np.zeros((7, 148, 2880))
    for k in range(len(head)):
        line_range = lines[head[k]+1:head[k]+1+osb_num[k]]
        for line in line_range:
            satid = line[0:3]
            sat = id2sat(satid)
            sys, prn = satsys(sat)
            obs_type = obs_type_all[sys2index(sys)]
            osb_line = line.split()
            for i in range(2, len(osb_line)-1):
                index = getosb(osb_line[i], obs_type)
                if index != -1:
                    osb[index, sat, k] = -float(osb_line[i + 1])*1e9/CLIGHT
    osb_ave = osb_sat_ave(osb)
    return osb_ave

def readosb(file):
    osb = np.zeros(32)
    f = open(file, "r")
    lines = f.readlines()
    for line in lines:
        if "OSB" != line[1:4]:
            continue
        if "C1C" not in line:
            continue
        if "    " != line[15:19]:
            continue
        if "G" in line:
            osb_line = line.split()
            prn = int(osb_line[2][1:3]) - 1
            osb[prn] = float(osb_line[7])
    f.close()
    return osb

def plotosb(osb):
    sat = []
    plt.figure(figsize=(8, 6))
    plt.bar(range(32), osb)
    for i in range(32):
        satid = "G{:02d}".format(i+1)
        sat.append(satid)
    plt.legend(sat, ncol=2)
    # plt.show()

def analysis_osb(rt, pp):
    osb = np.zeros(32)
    for i in range(32):
        osb[i] = rt[0, i] + pp[i]
    plotosb(osb)

def timeinfo(bncfile):
    bncfilelist = bncfile.split("/")
    global year
    global doy
    year = int("20" + bncfilelist[-1][-3:-1])
    doy = int(bncfilelist[-1][-8:-5])

def outfile(osb, file):
    fw = open(file, "w")
    fw.write("* Bias Solution INdependent EXchange Format (Bias-SINEX)\n")
    fw.write("+BIAS / SOLUTION\n")
    fw.write("*BIAS SVN_ PRN STATION__ OBS1 OBS2 BIAS_START____ BIAS_END______ UNIT \
__ESTIMATED_VALUE____ _STD_DEV___ __ESTIMATED_SLOPE____ _STD_DEV___\n")
    for sat in range(148):
        sys, prn = satsys(sat)
        obs_type = obs_type_all[sys2index(sys)]
        for i in range(len(obs_type)):
            osb_single = osb[i, sat]
            if osb_single == 0:
                continue
            type1 = obs_type[i]
            type2 = "   "
            bias = "OSB"
            station = "    "
            prn = sat2id(sat)
            svn = sat2svn(sat)
            std = 0.0
            outbody = " {:4s} {:4s} {:3s} {:9s} {:4s} {:4s} {:4d}:{:3d}:00000 {:4d}:{:3d}:00000 ns   {:>21.4f} {:11.4f}\n"\
                .format(bias, svn, prn, station, type1, type2, year, doy, year, doy+1, osb_single, std)
            fw.write(outbody)
    fw.write("-BIAS / SOLUTION\n")
    fw.close()


if __name__ == '__main__':
    bncfile = r"D:\RT-stream4\day\SSRC00CAS03560.21C"
    osbfile = r"C:\Users\LZ\Desktop\CAS0MGXRAP_20213550000_01D_01D_OSB.BIA"
    out = r"C:\Users\LZ\Desktop\rt_test1\CAS0MGXRAP_20213560000_01D_01D_OSB.BIA"

    global obs_type_all
    obs_type_all = [["C1C", "C1W", "C2W", "C5Q", "C5X"],
                    ["C1C", "C1P", "C2C", "C2P"],
                    ["C1C", "C1X", "C5Q", "C5X"],
                    ["C2I", "C6I", "C1P", "C1X", "C5P", "C5X"],
                    ["C1C", "C2X", "C5Q", "C5X"]]

    rt_osb = readbnc(bncfile)
    # pp_osb = readosb(osbfile)
    # plotosb(rt_osb)
    # analysis_osb(rt_osb, pp_osb)
    # plt.show()
    timeinfo(bncfile)
    outfile(rt_osb, out)
