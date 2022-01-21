# coding=utf-8
# !/usr/bin/env python
"""
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/16
 """
from math import floor, sqrt, fmod, pi, fabs, atan, atan2
import numpy as np

# GPS/Galileo/BDS广播星历结构体
class Eph:
    def __init__(self):
        self.week = 0
        self.sow = 0
        self.prn = 'X00'
        self.sat = 0
        self.pos = 0
        self.clk = np.zeros(3)
        self.iode = 0
        self.iodc = 0
        self.sva = 0
        self.svh = 0
        self.toe = 0
        self.toes = 0
        self.tof = 0
        self.ttr = 0
        self.sqrtA = 0
        self.e = 0
        self.i0 = 0
        self.OMG0 = 0
        self.omg = 0
        self.M0 = 0
        self.deln = 0
        self.OMGd = 0
        self.idot = 0
        self.crc = 0
        self.crs = 0
        self.cuc = 0
        self.cus = 0
        self.cic = 0
        self.cis = 0
        self.fit = 0
        self.f0 = 0
        self.f1 = 0
        self.f2 = 0
        self.tgd = np.zeros(2)
        self.codeflag = 0

# GLONASS广播星历结构体
class gEph:
    def __init__(self):
        self.sat = 0
        self.taun = 0
        self.tod = 0
        self.gamn = 0
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.acc = np.zeros(3)
        self.svh = 0
        self.frq = 0
        self.age = 0
        self.toe = 0
        self.tof = 0

# SSR改正信息结构体
class corr:
    def __init__(self):
        self.time = 0
        self.week = 0
        self.sow = 0
        self.orb = np.zeros((150, 3))
        self.dorb = np.zeros((150, 3))
        self.clk = np.zeros((150, 3))
        self.pbia = 0
        self.lbia = 0

# SSR改正信息结构体
class Corr:
    def __init__(self):
        self.time = 0
        self.week = 0
        self.sow = 0
        self.r = np.zeros(148)
        self.a = np.zeros(148)
        self.c = np.zeros(148)
        self.dr = np.zeros(148)
        self.da = np.zeros(148)
        self.dc = np.zeros(148)
        self.t0 = np.zeros(148)
        self.t1 = np.zeros(148)
        self.t2 = np.zeros(148)
        self.iode = np.zeros(148)


def SQR(x):
    return ((x)*(x))

# ---------------- ecef2rac Convert -------------------------------------
def dot(a, b, n):
    c = 0.0
    n -= 1
    while n >= 0:
        c += a[n] * b[n]
        n -= 1
    return c

def norm(a, n):
    return sqrt(dot(a, a, n))

def normv3(a):
    r = norm(a, 3)
    if r < 0.0:
        return 0
    else:
        return np.array([a[0]/r, a[1]/r, a[2]/r])

def cross3(a, b):
    return np.array([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

# ------------------  时间转换  ---------------------
# 年月日转换为儒略日
def ymd2mjd(year, mm, dd):
    if mm <= 2:
        mm += 12
        year -= 1
    mjd = 365.25 * year - 365.25 * year % 1.0 - 679006.0
    mjd += floor(30.6001 * (mm + 1)) + 2.0 - floor(year / 100.0) + floor(year / 400) + dd
    return mjd

# 年月日转换为GPS周及周内天
def ymd2wkdow(year, mm, dd):
    mjd0 = 44243
    mjd = ymd2mjd(year, mm, dd)
    difmjd = mjd - mjd0 - 1
    week = floor(difmjd / 7)
    dow = floor(difmjd % 7)
    return week, dow

# 年月日时分秒转换为GPS周及周内秒
def ymdhms2wksow(year, month, day, hour, min, sec):
    week, dow = ymd2wkdow(year, month, day)
    sow = dow * 86400 + hour * 3600 + min * 60 + sec
    return week, sow

# ----------------Time Convent from RTKLib--------------------------------------------------
# epoch 年月日时分秒表示时间
# time 计算机时间[单累计秒值]    起始时刻：[1970, 1, 1, 0, 0, 0]
# gpst GPS时[gps周+周内秒]      起始时刻：[1980, 1, 6, 0, 0, 0]
# bdt  BDS时[bds周+周内秒]      起始时刻：[2006, 1, 1, 0, 0, 0]

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

def gpst2time(week, sec):
    t = epoch2time([1980, 1, 6, 0, 0, 0])
    if abs(sec) > float(1E9):
        sec = 0
    return t + 86400 * 7 * week + sec

def time2gpst(time):
    t0 = epoch2time([1980, 1, 6, 0, 0, 0])
    sec = time - t0
    w = int(sec/(86400 * 7))
    s = sec - w * 86400 * 7
    return w, s

def timeadd(time, sec):
    return time + sec

def timediff(time1, time2):
    return time1 - time2

def adjweek(t, t0):
    tt = timediff(t, t0)
    if tt < -302400.0:
        return timeadd(t, 604800.0)
    elif tt > 302400.0:
        return timeadd(t, -604800.0)
    else:
        return t

def adjday(t, t0):
    tt = timediff(t, t0)
    if tt < -43200.0:
        return timeadd(t, 86400.0)
    elif tt > 43200.0:
        return timeadd(t, -86400.0)
    else:
        return t

def init_leaps():
    leaps = np.array([[2017, 1, 1, 0, 0, 0, -18],
        [2015, 7, 1, 0, 0, 0, -17],
        [2012, 7, 1, 0, 0, 0, -16],
        [2009, 1, 1, 0, 0, 0, -15],
        [2006, 1, 1, 0, 0, 0, -14],
        [1999, 1, 1, 0, 0, 0, -13],
        [1997, 7, 1, 0, 0, 0, -12],
        [1996, 1, 1, 0, 0, 0, -11],
        [1994, 7, 1, 0, 0, 0, -10],
        [1993, 7, 1, 0, 0, 0, -9],
        [1992, 7, 1, 0, 0, 0, -8],
        [1991, 1, 1, 0, 0, 0, -7],
        [1990, 1, 1, 0, 0, 0, -6],
        [1988, 1, 1, 0, 0, 0, -5],
        [1985, 7, 1, 0, 0, 0, -4],
        [1983, 7, 1, 0, 0, 0, -3],
        [1982, 7, 1, 0, 0, 0, -2],
        [1981, 7, 1, 0, 0, 0, -1]])
    return leaps

def time2sec(time):
    ep = time2epoch(time)
    sec = ep[3]*3600+ep[4]*60+ep[5]
    ep[3] = ep[4] = ep[5] = 0.0
    day = epoch2time(ep)
    return day, sec

def utc2gmst(t, ut1_utc):
    ep2000 = [2000, 1, 1, 12, 0, 0]
    tut = timeadd(t,ut1_utc)
    tut0, ut = time2sec(tut)
    t1 = timediff(tut0, epoch2time(ep2000))/86400.0/36525.0
    t2 = t1*t1
    t3 = t2*t1
    gmst0 = 24110.54841 + 8640184.812866 * t1 + 0.093104 * t2 - float(6.2E-6) * t3
    gmst = gmst0 + 1.002737909350795 * ut
    return fmod(gmst,86400.0)*pi/43200.0

def utc2gpst(t):
    leaps = init_leaps()
    for i in range(len(leaps)):
        if timediff(t, epoch2time(leaps[i][0:6])) >= 0.0:
            return timeadd(t, -leaps[i][6])
    return t

def gpst2utc(t):
    leaps = init_leaps()
    for i in range(len(leaps)):
        tu = timeadd(t, leaps[i][6])
        if timediff(tu, epoch2time(leaps[i][0:6])) >= 0.0:
            return tu
    return t

def bdt2time(week, sec):
    t = epoch2time([2006, 1, 1, 0, 0, 0])
    if abs(sec) > float(1E9):
        sec = 0.0
    return t + 86400 * 7 * week + sec

def bdt2gpst(t):
    return timeadd(t, 14.0)

def time2epoch(t):
    ep = [0, 0, 0, 0, 0, 0]
    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31,
           31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # of days in a month

    days = int(floor(t) / 86400)
    sec = t - days * 86400
    day = days % 1461
    mon = 0
    for mon in range(48):
        if day >= mday[mon]:
            day -= mday[mon]
        else:
            break
    ep[0] = floor(1970 + floor(days/1461) * 4 + mon / 12)
    ep[1] = mon % 12 + 1
    ep[2] = day + 1
    ep[3] = int(sec / 3600)
    ep[4] = int(sec % 3600 / 60)
    ep[5] = sec % 60
    return ep

def yd2epoch(year, doy):
    doys = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    mon = 1
    for mon in range(1, 13):
        if doys[mon-1] <= doy < doys[mon]:
            break
    day = doy - doys[mon-1] + 1
    return [year, mon, day, 0, 0, 0]

# ---------------------------------------------------

# --------------------- 统计 -------------------------

# 一维列表求均值
def list1d_ave(list):
    sump = 0
    for i in range(len(list)):
        sump += list[i]
    return sump/len(list)

# 一维列表求STD
def list1d_std(list):
    ave = list1d_ave(list)
    sump = 0
    for i in range(len(list)):
        sump += (list[i]-ave) * (list[i]-ave)
    return sqrt(sump / len(list))

# 一维列表求RMS
def list1d_rms(list):
    sump = 0
    for i in range(len(list)):
        sump += list[i] * list[i]
    return sqrt(sump/len(list))

# 二维列表求RMS
# 待补充
def list2d_rms(list, axis):
    rms = []
    if axis == 0:   # 行
        sump = np.zeros(len(list))
        for i in range(len(list)):
            for j in range(len(list[i])):
                sump[i] = list[i][j] * list[i][j]
            rms.append(sqrt(sump[i]/len(list[i])))
    return rms
# ---------------------------------------------------

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

def satid2sat(id):
    sys = id[0]
    prn = int(id[1:])
    return satno(sys,prn)

def deletesat(list):
    poplist = ["C31", "C18", "C17", "C15", "C08", "C02"]
    #poplist = [125, 112, 111, 109, 96]
    poplist2 = []
    for x in poplist:
        sat = satid2sat(x)
        for i in range(len(list)):
            if sat == list[i]:
                poplist2.append(i)
    for x in poplist2:
        list.pop(x)
    return list

def ecef2pos(r):
    pos = np.zeros(3)
    FE_WGS84 = (1.0/298.257223563)
    RE_WGS84 = 6378137.0
    e2 = FE_WGS84 * (2.0 - FE_WGS84)
    r2 = dot(r, r, 2)
    v = RE_WGS84
    z = r[2]
    zk = 0.0
    while fabs(z-zk) >= 1E-4:
        zk = z
        sinp = z / sqrt(r2+z * z)
        v = RE_WGS84 / sqrt(1.0-e2 * sinp * sinp)
        z = r[2] + v * e2 * sinp
    if r2 > 1e-12:
        pos[0] = atan(z / sqrt(r2))
        pos[1] = atan2(r[1], r[0])
    else:
        if r[2] > 0.0:
            pos[0] = pi / 2.0
        else:
            pos[0] = -pi / 2.0
        pos[1] = 0.0
    pos[2] = sqrt(r2 + z * z) - v
    return pos

