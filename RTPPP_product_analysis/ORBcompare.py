# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2021/12/27
"""

from cmn import *
from math import pow
import time

class Sat_RAC:
    def __init__(self):
        self.id = 'X00'
        self.sow = 0.0
        self.r   = 0.0
        self.a   = 0.0
        self.c   = 0.0

# 全局变量初始化
def init_global():
    global NSATGPS
    global NSATGLO
    global NSATGAL
    global NSATBDS
    global NSATQZS
    global NSAT

    NSATGPS = 32
    NSATGLO = 27
    NSATGAL = 36
    NSATBDS = 46
    NSATQZS = 7
    NSAT = NSATGPS + NSATGLO + NSATGAL + NSATBDS + NSATQZS

# 系统sys和prn号转换至卫星号sat
def satno(sys, prn):
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

# 卫星号sat转换至系统sys和prn号
def satsys(sat):
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

# 基准星id转换为卫星号sat
def ref2sat(reference):
    diffsat = []
    for satid in reference:
        sys = satid[0]
        prn = int(satid[1:3])
        sat = satno(sys, prn)
        diffsat.append(sat)
    return diffsat

def scansp3(file):
    f = open(file, "r")
    head = []
    lns = f.readlines()
    for i in range(len(lns)):
        if lns[i][0] == "*":
            head.append(i)
    head.append(len(lns))
    return lns, head

# 轨道文件读取
def readsp3(file):
    lns, head = scansp3(file)
    interval = 300
    num = int(86400 / interval)
    X = np.zeros((num, 148))
    Y = np.zeros((num, 148))
    Z = np.zeros((num, 148))
    S = np.zeros(num)
    for i in range(len(head)-1):
        record = lns[head[i]+1:head[i+1]]
        ln = lns[head[i]]
        year = int(ln[3:7])
        mon = int(ln[8:10])
        day = int(ln[11:13])
        hour = int(ln[14:16])
        mini = int(ln[17:19])
        sec = float(ln[20:31])
        ep = [year, mon, day, hour, mini, sec]
        week, sow = time2gpst(epoch2time(ep))

        index = int((sow%86400)/interval)
        for ln in record:
            if 'P' == ln[0] and ln[1:4] != 'C59' and ln[1:4] != 'C60':
                sys = ln[1]
                prn = int(ln[2:4])
                sat = satno(sys, prn)
                strs = ln.split()
                x = float(strs[1])*1000
                y = float(strs[2])*1000
                z = float(strs[3])*1000
                S[index] = sow
                X[index, sat] = x
                Y[index, sat] = y
                Z[index, sat] = z
    return [X, Y, Z, S]

def xyz2rac(dxyz, pos_xyz, vel_xyz):
    ea = normv3(vel_xyz)
    rc = cross3(pos_xyz, vel_xyz)
    ec = normv3(rc)
    er = cross3(ea, ec)
    A = np.array([[er[0], ea[0], ec[0]], [er[1], ea[1], ec[1]], [er[2], ea[2], ec[2]]])
    drac = np.dot(np.linalg.inv(A), dxyz)
    return drac

def satid(sat):
    sys, prn = satsys(sat)
    return "{}{:0>2d}".format(sys, prn)

# 双差计算钟差STD和RMS
def sp3compare(sp3s1, sp3s2):
    rac_all = []
    #satrange = [0, 32, 59, 95, 113, 141]  # G R E C2 C3
    #sat_std = np.zeros(148)
    #sat_rms = np.zeros(148)
    for i in range(len(sp3s1[0])):
        epoch1 = sp3s1[3][i]
        if i == 0:
            epoch2 = sp3s1[3][i+1]
        else:
            epoch2 = sp3s1[3][i-1]
        for sat in range(148):
            x1 = sp3s1[0][i, sat]
            y1 = sp3s1[1][i, sat]
            z1 = sp3s1[2][i, sat]
            x2 = sp3s2[0][i, sat]
            y2 = sp3s2[1][i, sat]
            z2 = sp3s2[2][i, sat]
            if i == 0:
                x11 = sp3s1[0][i+1, sat]
                y11 = sp3s1[1][i+1, sat]
                z11 = sp3s1[2][i+1, sat]
                x22 = sp3s1[0][i+1, sat]
                y22 = sp3s1[1][i+1, sat]
                z22 = sp3s1[2][i+1, sat]
            else:
                x11 = sp3s1[0][i-1, sat]
                y11 = sp3s1[1][i-1, sat]
                z11 = sp3s1[2][i-1, sat]
                x22 = sp3s1[0][i-1, sat]
                y22 = sp3s1[1][i-1, sat]
                z22 = sp3s1[2][i-1, sat]
            if x1 == 0 or x2 == 0 or x11 == 0 or x22 == 0:
                continue
            dt = epoch1 - epoch2
            pos_xyz = np.array([x1, y1, z1])
            xyz2 = np.array([x11, y11, z11])
            vel_xyz = (pos_xyz - xyz2)/dt
            test_xyz = np.array([x2, y2, z2])
            dxyz = pos_xyz - test_xyz
            drac = xyz2rac(dxyz, pos_xyz, vel_xyz)
            rac = Sat_RAC()
            id = satid(sat)
            # print(id)
            rac.id = id
            rac.sow = epoch1
            rac.r = drac[0]
            rac.a = drac[1]
            rac.c = drac[2]
            rac_all.append(rac)
    return rac_all

def statistic_rac(rac_all):
    sats_id = []
    for i in range(len(rac_all)):
        if rac_all[i].id not in sats_id:
            sats_id.append(rac_all[i].id)

    stat_rac = []
    for sat_id in sats_id:
        rac_single = []
        for i in range(len(rac_all)):
            if sat_id == rac_all[i].id and rac_all[i].r < 100 and rac_all[i].r != 0:
                rac_single.append([rac_all[i].r, rac_all[i].a, rac_all[i].c])
        stat_rac_single = [sat_id]
        for j in range(3):
            summary = 0
            if len(rac_single) != 0:
                for i in range(len(rac_single)):
                    summary += abs(rac_single[i][j])
                stat_rac_single.append(summary / len(rac_single))
        stat_rac.append(stat_rac_single)

    sys_rac = []
    for sys_id in ['G', 'R', 'E', 'C2', 'C3', 'J']:
        sys_single = []
        for i in range(len(rac_all)):
            if rac_all[i].r < 100 and rac_all[i].r != 0:
                if sys_id == rac_all[i].id[0] or (sys_id == 'C3' and rac_all[i].id[0] == "C" and\
                  int(rac_all[i].id[1:]) > 19) or (sys_id == 'C2' and rac_all[i].id[0] == "C" and\
                                                    int(rac_all[i].id[1:]) < 19):
                    sys_single.append([rac_all[i].r, rac_all[i].a, rac_all[i].c])
        sys_rac_single = [sys_id]
        for j in range(3):
            summary = 0
            if len(sys_single) != 0:
                for i in range(len(sys_single)):
                    summary += abs(sys_single[i][j])
                sys_rac_single.append(summary / len(sys_single))
        sys_rac.append(sys_rac_single)

    BDScons = []
    satcon=[[1,2,3,4,5],
            [6,7,8,9,10,13,16],
            [11,12,14],
            [19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,41,42,43,44,45,46],
            [38,39,40]]
    con = ["C2_GEO","C2_IGSO","C2_MEO","C3_MEO","C3_IGSO"]
    for j in range(len(satcon)):
        BDScons_single = []
        for i in range(len(rac_all)):
            if rac_all[i].id[0] != "C":
                continue
            if int(rac_all[i].id[1:]) in satcon[j] and rac_all[i].r < 100:
                BDScons_single.append([rac_all[i].r, rac_all[i].a, rac_all[i].c])
        BDScons_s = [con[j]]
        for k in range(3):
            summary = 0
            if len(BDScons_single) != 0:
                for i in range(len(BDScons_single)):
                    summary += abs(BDScons_single[i][k])
                BDScons_s.append(summary / len(BDScons_single))
        BDScons.append(BDScons_s)


    return stat_rac, sys_rac, BDScons

def output_rac(rac_all, stat_rac, sys_rac, BDScons, file1, file2):
    output1 = file2[:-9] + r"SP3compare_all.log"
    output2 = file2[:-9] + r"SP3compare_satellite.log"
    output3 = file2[:-9] + r"SP3compare_system.log"
    output4 = file2[:-9] + r"SP3compare_BDSconstellation.log"
    head = '% 1st file: {}\n% 2nd file: {}\n'.format(file1, file2)
    f = open(output1, "w")
    f.write(head)
    for i in range(len(rac_all)):
        index = int((rac_all[i].sow%86400)/900)
        ln = "{:5.3f} {:3s} {:10.3f} {:10.3f} {:10.3f} {:3d}\n".format(rac_all[i].sow, rac_all[i].id,\
                                                                       rac_all[i].r, rac_all[i].a, rac_all[i].c, index)
        f.write(ln)
    f = open(output2, "w")
    f.write(head)
    for i in range(len(stat_rac)):
        if len(stat_rac[i]) == 4:
            ln = "{:3s} {:>7.2f} {:>7.2f} {:>7.2f}\n".format(stat_rac[i][0], stat_rac[i][1] * 100, stat_rac[i][2] * 100, \
                                                        stat_rac[i][3] * 100)
            f.write(ln)
    f = open(output3, "w")
    f.write(head)
    for i in range(len(sys_rac)):
        if len(sys_rac[i]) == 4:
            ln = "{:2s} {:>5.2f} {:>5.2f} {:>5.2f}\n".format(sys_rac[i][0], sys_rac[i][1]*100, sys_rac[i][2]*100, \
                                                     sys_rac[i][3]*100)
            f.write(ln)
    f = open(output4, "w")
    f.write(head)
    for i in range(len(BDScons)):
        if len(BDScons[i]) == 4:
            ln = "{:8s} {:>6.2f} {:>6.2f} {:>6.2f}\n".format(BDScons[i][0], BDScons[i][1]*100, BDScons[i][2]*100, \
                                                     BDScons[i][3]*100)
            f.write(ln)
    print("[INFO] Output the results successfully!")
    return [output1, output2, output3]

# 核心处理
def process(sp3file1, sp3file2, outputfile):
    init_global()                                             # 全局变量初始化
    sp3s1 = readsp3(sp3file1)                                 # 钟差文件读取
    print('[INFO] Finish reading the 1st sp3 file!')
    sp3s2 = readsp3(sp3file2)                                 # 钟差文件读取
    print('[INFO] Finish reading the 2nd sp3 file!')
    rac_all = sp3compare(sp3s1, sp3s2)      # 双差计算钟差STD和RMS
    stat_rac, sys_rac, BDScons = statistic_rac(rac_all)
    output = output_rac(rac_all, stat_rac, sys_rac,BDScons, sp3file1, sp3file2)
    return output
    
    
if __name__ == '__main__':
    start = time.perf_counter()
    filepath = r"D:\RT-stream4\test"
    sp3file1 = filepath + "\\" + r'GBM0MGXRAP_20213550000_01D_05M_ORB.SP3'
    sp3file2 = filepath + "\\" + r'cass21892.sp3'
    outputfile = filepath + "\\" + r'sp3compare0.txt'
    process(sp3file1, sp3file2, outputfile)
    end = time.perf_counter()
    print("[INFO] The function run time is : %.03f seconds" %(end-start))   # 程序耗时计算
