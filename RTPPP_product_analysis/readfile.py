# coding=utf-8
# !/usr/bin/env python
"""
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/19
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
# -------------------------------------------------------------------------
# --------------------SSR改正信息文件读取-----------------------------------
# 播发间隔标志转换为秒
def interval_to_sec(num):
    interval_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800, 7200, 10800]
    return interval_list[num]

# 遍历ssr改正文件获取所有行列表lns和表头行数列表head_list
def scanssrc(ssrcfile):
    head_list = []
    f = open(ssrcfile)
    lns = f.readlines()
    for i in range(len(lns)):
        if lns[i][0] == '>' and lns[i][2:6] != 'VTEC':
            head_list.append(i)
    return lns, head_list

# 读取ssr改正信息表头
def readssrchead(line):
    head = line.split(' ')
    corr_type = head[1]
    year = int(head[2])
    month = int(head[3])
    day = int(head[4])
    hour = int(head[5])
    min = int(head[6])
    sec = float(head[7])
    interval = interval_to_sec(int(head[8]))
    line_num = int(head[9])
    name = head[10]
    week, sow = ymdhms2wksow(year, month, day, hour, min, sec)
    return week, sow

# 读取BNC输出改正数C文件
# 输出改正信息
def readssrc(ssrcfile):
    lns, head = scanssrc(ssrcfile)
    corrs = []
    for i in range(int(len(head)/4)):
        epoch_corr = corr()
        for ln in lns[head[i*4]:head[i*4+1]]:
            if ln[0] == '>':
                week, sow = readssrchead(ln)
                time = gpst2time(week, sow)
                epoch_corr.week = week
                epoch_corr.sow = sow
                epoch_corr.time = time
            else:
                sys = ln[0]
                prn = int(ln[1:3])
                sat = satno(sys, prn)
                # print(ln)
                epoch_corr.orb[sat] = np.array([float(ln[19:26]), float(ln[30:37]), float(ln[41:48])])
                epoch_corr.dorb[sat] = np.array([float(ln[55:62]), float(ln[66:73]), float(ln[77:84])])
        for ln in lns[head[i*4+1]:head[i*4+2]]:
            if ln[0] != '>':
                epoch_corr.clk[sat] = np.array([float(ln[19:26]), float(ln[30:37]), float(ln[41:48])])
        corrs.append(epoch_corr)
    return corrs

# 遍历ssr改正文件获取所有行列表lns和表头行数列表head_list
def scanssrc2(ssrcfile):
    head_list = []
    f = open(ssrcfile)
    lns = f.readlines()
    for i in range(len(lns)):
        if lns[i][0] == '>':
            head_list.append(i)
    head_list.append(len(lns)+1)
    return lns, head_list

def get_corrtype(s):
    if s == "ORBIT":
        return 1
    elif s == "CLOCK":
        return 2
    elif s == "CODE_BIAS":
        return 3
    elif s == "PHASE_BIAS":
        return 4
    elif s == "VTEC":
        return 5
    else:
        return 0

# 读取ssr改正信息表头
def readssrchead2(line):
    head = line.split(' ')
    corr_type = get_corrtype(head[1])
    year = int(head[2])
    month = int(head[3])
    day = int(head[4])
    hour = int(head[5])
    min = int(head[6])
    sec = float(head[7])
    interval = interval_to_sec(int(head[8]))
    line_num = int(head[9])
    name = head[10]
    week, sow = ymdhms2wksow(year, month, day, hour, min, sec)
    return week, sow, corr_type

def convertcorrs(corrs):
    r = np.zeros((2880, 148))
    a = np.zeros((2880, 148))
    c = np.zeros((2880, 148))
    dr = np.zeros((2880, 148))
    da = np.zeros((2880, 148))
    dc = np.zeros((2880, 148))
    t0 = np.zeros((2880, 148))
    t1 = np.zeros((2880, 148))
    t2 = np.zeros((2880, 148))
    iode = np.zeros((2880, 148))

    for i in range(len(corrs)):
        if math.fmod((corrs[i].sow%86400), 30) == 0:
            index = int((corrs[i].sow%86400)/30)
            # print(math.fmod((corrs[i].sow % 86400), 30), index)
            if corrs[i].r[0] != 0:
                r[index] = corrs[i].r
                a[index] = corrs[i].a
                c[index] = corrs[i].c
                dr[index] = corrs[i].dr
                da[index] = corrs[i].da
                dc[index] = corrs[i].dc
                iode[index] = corrs[i].iode
            if corrs[i].t0[0] != 0:
                t0[index] = corrs[i].t0
                t1[index] = corrs[i].t1
                t2[index] = corrs[i].t2
    return [r, a, c, dr, da, dc, t0, t1, t2, iode]


# 读取BNC输出改正数C文件
# 输出改正信息
def readssrc2(ssrcfile):
    corrs = []
    lns, head = scanssrc2(ssrcfile)
    for i in range(len(head)-1):
        corr1 = Corr()
        for ln in lns[head[i]:head[i+1]]:
            if ln[0] == '>':
                week, sow, type = readssrchead2(ln)
                time = gpst2time(week, sow)
                corr1.time = time
                corr1.week = week
                corr1.sow = sow
                corr1.type = type
            else:
                if type == 1:
                    sys = ln[0]
                    prn = int(ln[1:3])
                    if sys == "C" and prn > 46:
                        continue
                    sat = satno(sys, prn)
                    corr1.iode[sat] = int(ln[11:15])
                    corr1.r[sat] = float(ln[19:26])
                    corr1.a[sat] = float(ln[30:37])
                    corr1.c[sat] = float(ln[41:48])
                    corr1.dr[sat] = float(ln[55:62])
                    corr1.da[sat] = float(ln[66:73])
                    corr1.dc[sat] = float(ln[77:84])
                elif type == 2:
                    sys = ln[0]
                    prn = int(ln[1:3])
                    if sys == "C" and prn > 46:
                        continue
                    sat = satno(sys, prn)
                    corr1.t0[sat] = float(ln[19:26])
                    corr1.t1[sat] = float(ln[30:37])
                    corr1.t2[sat] = float(ln[41:48])
        corrs.append(corr1)
    ssr = convertcorrs(corrs)
    return ssr
# ---------------------------------------------------------

def freq1(sat, freq):
    if sat == "G" and freq == 1:
        return True
    if sat == "R" and freq == 1:
        return True
    if sat == "E" and freq == 1:
        return True
    if sat == "C" and freq == 2:
        return True
    if sat == "J" and freq == 1:
        return True

def freq2(sat, freq):
    if sat == "G" and freq == 2:
        return True
    if sat == "R" and freq == 2:
        return True
    if sat == "E" and freq == 5:
        return True
    if sat == "C" and freq == 6:
        return True
    if sat == "J" and freq == 2:
        return True

def readantex(atxfile):
    pcv = np.zeros((148, 6))
    f = open(atxfile, "r")
    ln = f.readline()
    state = 0
    while ln:
        ln = f.readline()
        if "COMMENT" in ln:
            continue
        if "START OF ANTENNA" in ln:
            state = 1
        if "END OF ANTENNA" in ln:
            state = 0
        if state == 0:
            continue
        if "TYPE / SERIAL NO" in ln:
            satid = ln[20:23]
            if satid == "   ":
                continue
            sys = satid[0]
            prn = int(satid[1:3])
            if prn < 46:
                sat = satno(sys, prn)
            else:
                sat = -1
        if "START OF FREQUENCY" in ln:
            freq = int(ln[4:6])
        if "NORTH / EAST / UP" in ln:
            if freq1(sys, freq) and sat != -1:
                pcv[sat, 0] = float(ln[0:10])*float(1E-3)
                pcv[sat, 1] = float(ln[10:20])*float(1E-3)
                pcv[sat, 2] = float(ln[20:30])*float(1E-3)
            if freq2(sys, freq) and sat != -1:
                pcv[sat, 3] = float(ln[0:10])*float(1E-3)
                pcv[sat, 4] = float(ln[10:20])*float(1E-3)
                pcv[sat, 5] = float(ln[20:30])*float(1E-3)
    f.close()
    return pcv