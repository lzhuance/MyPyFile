# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""
import numpy as np

from cmn import *
from math import sqrt, sin, cos, atan2, fmod, tan

# 初始化全局变量
def init_global():
    global CLIGHT
    CLIGHT = 299792458.0
    global omegaEarth
    omegaEarth = float(7292115.1467E-11)

    global eph_sel
    eph_sel = [0, 0, 0, 0, 0]

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
    global NX
    NX = 3 + 4
    global RE_WGS84
    RE_WGS84 = 6378137.0
    global FE_WGS84
    FE_WGS84 = (1.0 / 298.257223563)
    global RE_GLO
    global MU_GPS
    global MU_GLO
    global MU_CMP
    global MU_GAL
    global J2_GLO
    RE_GLO = 6378136.0
    MU_GPS = float(3.9860050E14)
    MU_GLO = float(3.9860044E14)
    MU_GAL = float(3.986004418E14)
    MU_CMP = float(3.986004418E14)
    J2_GLO = float(1.0826257E-3)

    global OMGE_GPS
    global OMGE_GLO
    global OMGE_GAL
    global OMGE_CMP
    OMGE_GPS = float(7.2921151467E-5)
    OMGE_GLO = float(7.292115E-5)
    OMGE_GAL = float(7.2921151467E-5)
    OMGE_CMP = float(7.292115E-5)

    global RTOL_KEPLER
    RTOL_KEPLER = float(1E-13)
    global MAX_ITER_KEPLER
    MAX_ITER_KEPLER = 30

    global SIN_5
    SIN_5 = -0.0871557427476582
    global COS_5
    COS_5 = 0.9961946980917456

    global TSTEP
    TSTEP = 60.0
    global MAXDTOE
    global MAXDTOE_QZS
    global MAXDTOE_GAL
    global MAXDTOE_CMP
    global MAXDTOE_GLO
    MAXDTOE = 7200.0
    MAXDTOE_QZS = 7200.0
    MAXDTOE_GAL = 14400.0
    MAXDTOE_CMP = 21600.0
    MAXDTOE_GLO = 1800.0

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

def setseleph(sys, sel):
    if sys == 'G':
        eph_sel[0] = sel
    elif sys == 'R':
        eph_sel[1] = sel
    elif sys == 'E':
        eph_sel[2] = sel
    elif sys == 'C':
        eph_sel[3] = sel
    elif sys == 'J':
        eph_sel[4] = sel

def getseleph(sys):
    if sys == 'G':
        return eph_sel[0]
    elif sys == 'R':
        return eph_sel[1]
    elif sys == 'E':
        return eph_sel[2]
    elif sys == 'C':
        return eph_sel[3]
    elif sys == 'J':
        return eph_sel[4]

# 选取常规广播星历
def seleph(time, sat, iode, ephs):
    sel = 0
    j = -1
    sys, prn = satsys(sat)
    if sys == 'G':
        tmax = MAXDTOE + 1.0
    elif sys == 'E':
        tmax = MAXDTOE_GAL
    elif sys == 'C':
        tmax = MAXDTOE_CMP + 1.0
    elif sys == 'J':
        tmax = MAXDTOE_QZS + 1.0
    else:
        tmax = MAXDTOE + 1.0
    tmin = tmax + 1.0
    for i in range(len(ephs)):
        if ephs[i].sat != sat:
            continue
        if 0 <= iode != ephs[i].iode:
            continue
        if sys == 'E':
            sel = getseleph('E')
            # if sel == 0 and not(ephs[i].code & (1 << 9)):
            #    continue
            #if sel == 1 and not(ephs[i].code & (1 << 8)):
            #    continue
            #if timediff(ephs[i].toe, time) >= 0.0:
            #    continue
        t = abs(timediff(ephs[i].toe, time))
        if t > tmax:
            continue
        if iode >= 0:
            return ephs[i]
        if t < tmin:
            j = i
            tmin = t
    if iode > 0 or j < 0:
        return 0
    return ephs[j]

# 选取GLONASS广播星历
def selgeph(time, sat, iode, gephs):
    tmax = MAXDTOE_GLO
    tmin = tmax + 1.0
    j = -1
    for i in range(len(gephs)):
        if gephs[i].sat != sat:
            continue
        if 0 <= iode != gephs[i].iode:
            continue
        t = abs(timediff(gephs[i].toe, time))
        if t > tmax:
            continue
        if iode >= 0:
            return gephs[i]
        if t < tmin:
            j = i
            tmin = t
    if iode > 0 or j < 0:
        return 0
    return gephs[j]

# 广播星历卫星钟差
def eph2clk(time, eph):
    t = timediff(time, eph.toc)
    ts = timediff(time, eph.toc)
    for i in range(2):
        t = ts - (eph.clk[0] + eph.clk[1] * t + eph.clk[2] * t * t)
    return eph.clk[0] + eph.clk[1] * t + eph.clk[2] * t * t

# GLONASS广播星历卫星钟差
def geph2clk(time, geph):
    t = timediff(time, geph.toe)
    ts = timediff(time, geph.toe)
    for i in range(2):
        t = ts - (-geph.taun + geph.gamn * t)
    return -geph.taun + geph.gamn * t

# 处理广播星历卫星钟
def ephclk(time, sat, ephs, gephs):
    sys, prn = satsys(sat)
    if sys == 'G' or sys == 'E' or sys == 'C' or sys == 'J':
        eph = seleph(time, sat, -1, ephs)
        if eph == 0:
            return 0
        else:
            dt = eph2clk(time, eph)
    elif sys == 'R':
        geph = selgeph(time, sat, -1, gephs)
        if geph == 0:
            return 0
        else:
            dt = geph2clk(time, geph)
    else:
        return 0
    return dt

# 广播星历计算卫星位置和钟差
def eph2pos(time, eph, rs, dts):
    tk = timediff(time, eph.toe)
    sys, prn = satsys(eph.sat)
    if sys == 'E':
        mu = MU_GAL
        omge = OMGE_GAL
    elif sys == 'C':
        mu = MU_CMP
        omge = OMGE_CMP
    else:
        mu = MU_GPS
        omge = OMGE_GPS
    nn = sqrt(mu/(eph.A * eph.A * eph.A))+eph.deln
    M = eph.M0 + nn*tk
    n = 0
    E = M
    Ek = 0.0
    while n >= 0:
        if abs(E - Ek) > RTOL_KEPLER and n < MAX_ITER_KEPLER:
            Ek = E
            E -= (E - eph.e * sin(E) - M) / (1.0 - eph.e * cos(E))
            n += 1
        else:
            break
    sinE = sin(E)
    cosE = cos(E)
    u = atan2(sqrt(1.0-eph.e*eph.e)*sinE, cosE-eph.e)+eph.omg
    r = eph.A * (1.0 - eph.e * cosE)
    i = eph.i0 + eph.idot * tk
    sin2u = sin(2.0 * u)
    cos2u = cos(2.0 * u)
    u += eph.cus * sin2u + eph.cuc * cos2u
    r += eph.crs * sin2u + eph.crc * cos2u
    i += eph.cis * sin2u + eph.cic * cos2u
    x = r * cos(u)
    y = r * sin(u)
    cosi = cos(i)
    if sys == 'C' and eph.sat < NSATGPS + NSATGLO + NSATGAL + 5:
        O = eph.OMG0+eph.OMGd*tk-omge*eph.toes
        sinO = sin(O)
        cosO = cos(O)
        xg = x*cosO-y*cosi*sinO
        yg = x*sinO+y*cosi*cosO
        zg = y*sin(i)
        sino = sin(omge*tk)
        coso = cos(omge*tk)
        rs[0] = xg*coso+yg*sino*COS_5+zg*sino*SIN_5
        rs[1] = -xg*sino+yg*coso*COS_5+zg*coso*SIN_5
        rs[2] = -yg*SIN_5+zg*COS_5
    else:
        O = eph.OMG0+(eph.OMGd-omge)*tk-omge*eph.toes
        sinO = sin(O)
        cosO = cos(O)
        rs[0] = x*cosO-y*cosi*sinO
        rs[1] = x*sinO+y*cosi*cosO
        rs[2] = y*sin(i)
    """
    calculate satellite velocity from BNC ephemeris.cpp ln380
    v = atan2(sqrt(1.0-eph.e*eph.e)*sinE, cosE-eph.e)
    tanv2 = tan(v/2)
    dEdM = 1/(1-eph.e*cosE)
    dotv = sqrt((1.0+eph.e)/(1.0-eph.e))/cos(E/2)/cos(E/2)/(1+tanv2*tanv2)* dEdM * nn
    dotu = dotv + (-eph.cuc*sin2u+eph.cus*cos2u)*2*dotv
    dotom = eph.OMGd-omegaEarth
    doti = eph.idot + (-eph.cic*sin2u+eph.cis*cos2u)*2*dotv
    dotr = eph.A*eph.e*sinE*dEdM*nn+(-eph.crc*sin2u+eph.crs*cos2u)*2*dotv
    dotx = dotr * cos(u) - r * sin(u) * dotu
    doty = dotr * sin(u) + r * cos(u) * dotu
    rs[3] = cosO*dotx-cosi*sinO*doty-x*sinO*dotom-y*cosi*cosO*dotom+y*y*sin(i)*sinO*dotom
    rs[4] = sinO*dotx-cosi*cosO*doty-x*cosO*dotom-y*cosi*sinO*dotom+y*y*sin(i)*cosO*dotom
    rs[5] = sin(i)*doty+y*cosi*doti
    """
    tc = timediff(time, eph.toc)
    dts[0] = eph.clk[0] + eph.clk[1] * tc + eph.clk[2] * tc * tc
    # dts[0] -= 2.0 * sqrt(mu * eph.A)*eph.e * sinE / SQR(CLIGHT)  # 相对论效应(钟差生成时无需考虑，定位时才需考虑)
    return rs, dts

# glonass orbit differential equations
def dep(x, xdot, acc):
    r2 = dot(x, x, 3)
    r3 = r2 * sqrt(r2)
    omg2 = SQR(OMGE_GLO)
    if r2 <= 0.0:
        for i in range(6):
            xdot[i] = 0
        return xdot
    a = 1.5*J2_GLO*MU_GLO*SQR(RE_GLO)/r2/r3
    b = 5.0*x[2]*x[2]/r2
    c = -MU_GLO/r3-a*(1.0-b)
    xdot[0] = x[3]
    xdot[1] = x[4]
    xdot[2] = x[5]
    xdot[3] = (c+omg2)*x[0]+2.0*OMGE_GLO*x[4]+acc[0]
    xdot[4] = (c+omg2)*x[1]-2.0*OMGE_GLO*x[3]+acc[1]
    xdot[5] = (c-2.0*a)*x[2]+acc[2]

# glonass position and velocity by numerical integration
def glorbit(t, x, acc):
    k1 = np.zeros(6)
    k2 = np.zeros(6)
    k3 = np.zeros(6)
    k4 = np.zeros(6)
    w = np.zeros(6)
    dep(x, k1, acc)
    for i in range(6):
        w[i] = x[i]+k1[i]*t/2.0
    dep(x, k2, acc)
    for i in range(6):
        w[i] = x[i]+k2[i]*t/2.0
    dep(x, k3, acc)
    for i in range(6):
        w[i] = x[i]+k3[i]*t
    dep(x, k4, acc)
    for i in range(6):
        x[i] += (k1[i]+2.0*k2[i]+2.0*k3[i]+k4[i])*t/6.0
    return x

# glonass广播星历计算卫星位置和钟差
def geph2pos(time, geph, rs, dts):
    x = np.zeros(6)
    t = timediff(time, geph.toe)
    dts[0] = -geph.taun + geph.gamn * t
    for i in range(3):
        x[i] = geph.pos[i]
        x[i+3] = geph.vel[i]
    if t < 0.0:
        tt = -TSTEP
    else:
        tt = TSTEP
    while abs(t) > float(1E-9):
        if abs(t) < TSTEP:
            tt = t
        x = glorbit(tt, x, geph.acc)
        t -= tt
    for i in range(3):
        rs[i] = x[i]
    return rs, dts

# 由广播星历计算卫星位置速度和钟差钟漂
def ephpos(time, teph, sat, ephs, gephs, iode, rs, dts):
    tt = 0.001
    sys, prn = satsys(sat)
    if sys == 'G' or sys == 'E' or sys == 'C' or sys == 'J':
        eph = seleph(teph, sat, iode, ephs)
        # if sat == 0:
        #    print(time2epoch(eph.toc), eph.prn)
        if eph == 0:
            return rs, dts
        else:
            rs, dts = eph2pos(time, eph, rs, dts)
            time = timeadd(time, tt)
            rst = np.zeros(6)
            dtst = np.zeros(2)
            rst, dtst = eph2pos(time, eph, rst, dtst)
    elif sys == 'R':
        geph = selgeph(teph, sat, iode, gephs)
        if geph == 0:
            return rs, dts
        else:
            rs, dts = geph2pos(time, geph, rs, dts)
            rst = np.zeros(6)
            dtst = np.zeros(2)
            time = timeadd(time, tt)
            rst, dtst = geph2pos(time, geph, rst, dtst)
    else:
        return rs, dts
    for i in range(3):
        rs[i + 3] = (rst[i] - rs[i]) / tt
    dts[1] = (dtst[0] - dts[0]) / tt
    if sys == 'C' and sat < NSATGPS + NSATGLO + NSATGAL + 5:
        omge = float(7.2921151467E-5)
        rs[4] += -omge * rs[1]
        rs[5] += omge * rs[0]
    return rs, dts

# 选取合适的SSR改正信息
def selcorr(time, corrs):
    for i in range(len(corrs)):
        t = timediff(time, corrs[i].time)
        if abs(t) < 5:
            break
    return corrs[i]

# 加入SSR改正的卫星位置计算
def satpos_ssr(time, teph, sat, ephs, gephs, ssr, opt, rs, dts):
    deph = np.zeros(3)
    t1 = timediff(time, teph)
    t2 = timediff(time, teph)
    t1 -= 5 / 2
    t2 -= 5 / 2
    week, sow = time2gpst(teph)
    index = int((sow%86400)/30)
    if ssr[0][index, sat] == 0:
        return rs, dts
    for i in range(3):
        deph[i] = ssr[i][index, sat] + ssr[i+3][index, sat] * t1
    dclk = ssr[6][index, sat] + ssr[7][index, sat]*t2 + ssr[8][index, sat]*t2*t2
    iode = ssr[9][index, sat]
    #print(sat,ssr[0][index, sat],ssr[1][index, sat],ssr[2][index, sat],ssr[3][index, sat],ssr[4][index, sat],\
    #      ssr[5][index, sat],ssr[6][index, sat],ssr[7][index, sat],ssr[8][index, sat])
    rs, dts = ephpos(time, teph, sat, ephs, gephs, iode, rs, dts)
    if rs[0] == 0 and dts[0] == 0:
        return rs, dts
    sys, prn = satsys(sat)
    if sys == 'G' or sys == 'E' or sys == 'C' or sys == 'J':
        eph = seleph(teph, sat, iode, ephs)
        if eph == 0:
            return rs, dts
        tc = timediff(time, eph.toc)
        dts[0] = eph.clk[0] + eph.clk[1] * tc + eph.clk[2] * tc * tc
        dts[1] = eph.clk[1] + 2.0 * eph.clk[2] * tc
        # dts[0] -= 2.0*dot(rs[0:3], rs[3:6], 3)/CLIGHT/CLIGHT    # 相对论效应(钟差生成时无需考虑，定位时才需考虑)
    ea = normv3(rs[3:6])
    rc = cross3(rs[0:3], rs[3:6])
    ec = normv3(rc)
    er = cross3(ea, ec)
    dant = [0, 0, 0]
    #dant = satantoff(time, rs, sat, pcv)
    if opt != 0:
        for i in range(3):
            rs[i] += -(er[i] * deph[0] + ea[i] * deph[1] + ec[i] * deph[2]) + dant[i]
    else:
        for i in range(3):
            rs[i] += -(er[i] * deph[0] + ea[i] * deph[1] + ec[i] * deph[2])
    dts[0] += dclk / CLIGHT
    return rs, dts

#def peph2pos(time, sat, ephs, gephs, ssr, opt, rs, dts):


# 计算time历元下的卫星sat的位置和钟差并存储至rs和dts
def satpos(time, teph, sat, ephs, gephs, ssr, rs, dts, ephmode):
    if ephmode == 'BRDC':
        return ephpos(time, teph, sat, ephs, gephs, -1, rs, dts)
    elif ephmode == 'SSRA':   # 待添加ATX文件天线相位中心改正模块
        return satpos_ssr(time, teph, sat, ephs, gephs, ssr, 1, rs, dts)
    elif ephmode == 'SSRC':
        return satpos_ssr(time, teph, sat, ephs, gephs, ssr, 0, rs, dts)
    #elif ephmode == 'PREC':
    #    return peph2pos(time, sat, ephs, gephs, ssr, 0, rs, dts)
    else:
        return rs, dts

# 计算teph历元下的卫星位置和钟差并存储至rss和dtss
def satposss(teph, obs, n, ephs, gephs, ssr, ephmode):
    #rss = np.zeros((NSAT, 6))
    #dtss = np.zeros((NSAT, 2))
    rss = np.zeros((n, 6))
    dtss = np.zeros((n, 2))

    for i in range(len(obs.data)):
        sat = obs.data[i][0]
        sys, prn = satsys(sat)
        rs = np.zeros(6)
        dts = np.zeros(2)
        time = timeadd(teph, 0)
        # dt = ephclk(time, sat, ephs, gephs)
        # time = timeadd(time, -dt)
        rs, dts = satpos(time, teph, sat, ephs, gephs, ssr, rs, dts, ephmode)
        if rs[0] != 0:
            rss[i] = rs
        if dts[0] != 0:
            dtss[i] = dts
    return rss, dtss

def geodist(rrs, rrr):
    if norm(rrs, 3) < RE_WGS84:
        return 0
    e = rrs[0:3] - rrr
    r = norm(e, 3)
    for i in range(3):
        e[i] /= r
    return e, r + OMGE_GPS *(rrs[0]*rrr[1]-rrs[1]*rrr[0])/CLIGHT

def rescode(x, obs, n, rs):
    rr = x[0:3]
    dtr = x[3]
    pos = ecef2pos(rr)
    for i in range(n):
        time = obs.time
        sat = obs.obs[i][0]
        sys, prn = satsys(sat)
        if i < n-1 and sat == obs.obs[i+1][0]:
            continue
        e, r = geodist(rs[i], rr)
        return 0

def estpos(obs, n, ephs, gephs, rs):
    x = np.zeros(NX)
    dx = np.zeros(NX)
    Q = np.zeros((NX, NX))
    v = np.zeros((n+4, 1))
    H = np.zeros((NX, n+4))
    var = np.zeros((n+4, 1))
    MAXITR = 10
    for i in range(MAXITR):
        nv = rescode(x, obs, n, rs)
        if nv < NX:
            break
        for j in range(nv):
            sig = sqrt(var[j])
            v[j] /= sig
            for k in range(NX):
                H[k+j*NX] /= sig
        #lsq(H,v,NX,nv,dx,Q)

    return 0

def spp(obss, ephs, gephs, info):
    init_global()
    for i in range(len(obss)):
        obs = obss[i]
        teph = obs.time
        n = obs.n
        rss, dtss = satposss(teph, obs, n, ephs, gephs, 0, 'BRDC')
        #estpos(obs, n, ephs, gephs, rss)
        print(time2epoch(teph))
    return 0