# coding=utf-8
# !/usr/bin/env python
"""
Program:
Author:LZ_CUMT
Version:1.0
Date:2021/12/21
"""

from cmn import time2epoch, time2gpst, deletesat

# 卫星号sat转换至系统sys和prn号
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

# 将时间信息写入sp3头文件
def sp3head(fp, time):
    ep = time2epoch(time)
    weeks, sows = time2gpst(time)
    # weeke, sowe = time2gpst(timeadd(time, 86400))
    heads = [
    "#dP{:4d} {:2d} {:2d} {:2d} {:2d} {:11.8f}      96   u+U IGb14 FIT  LIU\n".format(ep[0], ep[1], ep[2], ep[3], \
                                                                                      ep[4], ep[5]),
    "## {:4d} {:6d}.00000000   900.00000000 59396 0.0000000000000\n".format(weeks, sows),
    "+  122   G01G02G03G04G05G06G07G08G09G10G11G12G13G14G15G16G17\n",
    "+        G18G19G20G21G22G23G24G25G26G27G28G29G30G31G32R01R02\n",
    "+        R03R04R05R07R08R09R11R12R13R14R15R16R17R18R19R20R21\n",
    "+        R22R24E01E02E03E04E05E07E08E09E11E12E13E14E15E18E19\n",
    "+        E21E24E25E26E27E30E31E33E36C02C03C04C05C06C07C08C09\n",
    "+        C10C11C12C13C14C16C19C20C21C22C23C24C25C26C27C28C29\n",
    "+        C30C32C33C34C35C36C37C38C39C40C41C42C43C44C45C46J01\n",
    "+        J02J03J07 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "%c M  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n",
    "%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n",
    "%f  1.2500000  1.025000000  0.00000000000  0.000000000000000\n",
    "%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n",
    "%i    0    0    0    0      0      0      0      0         0\n",
    "%i    0    0    0    0      0      0      0      0         0\n",
    "/* PCV:IGS14_2163 OL/AL:FES2004  NONE     YN CLK:CoN ORB:CoN\n",
    "/*\n",
    "/*\n"]
    for head in heads:
        fp.write(head)

# 将时间信息写入sp3头文件
def sp3head2(fp, time):
    ep = time2epoch(time)
    weeks, sows = time2gpst(time)
    # weeke, sowe = time2gpst(timeadd(time, 86400))
    heads = [
    "#dP{:4d} {:2d} {:2d} {:2d} {:2d} {:11.8f}      96   u+U IGb14 FIT  LIU\n".format(ep[0], ep[1], ep[2], ep[3], \
                                                                                      ep[4], ep[5]),
    "## {:4d} {:6d}.00000000   900.00000000 59396 0.0000000000000\n".format(weeks, sows),
    "+   32   G01G02G03G04G05G06G07G08G09G10G11G12G13G14G15G16G17\n",
    "+        G18G19G20G21G22G23G24G25G26G27G28G29G30G31G32 00 00\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "%c G  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n",
    "%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n",
    "%f  1.2500000  1.025000000  0.00000000000  0.000000000000000\n",
    "%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n",
    "%i    0    0    0    0      0      0      0      0         0\n",
    "%i    0    0    0    0      0      0      0      0         0\n",
    "/* PCV:IGS14_2163 OL/AL:FES2004  NONE     YN CLK:CoN ORB:CoN\n",
    "/*\n",
    "/*\n"]
    for head in heads:
        fp.write(head)

# 将时间信息写入sp3头文件
def sp3head3(fp, time):
    ep = time2epoch(time)
    weeks, sows = time2gpst(time)
    # weeke, sowe = time2gpst(timeadd(time, 86400))
    heads = [
    "#dP{:4d} {:2d} {:2d} {:2d} {:2d} {:11.8f}      96   u+U IGb14 FIT  LIU\n".format(ep[0], ep[1], ep[2], ep[3], \
                                                                                      ep[4], ep[5]),
    "## {:4d} {:6d}.00000000   900.00000000 59396 0.0000000000000\n".format(weeks, sows),
    "+   74   G01G02G03G04G05G06G07G08G09G10G11G12G13G14G15G16G17\n",
    "+        G18G19G20G21G22G23G24G25G26G27G28G29G30G31G32C01C02\n",
    "++       C03C04C05C06C07C08C09C10C11C12C13C14C16C19C20C21C22\n",
    "++       C23C24C25C26C27C28C29C30C32C33C34C35C36C37C38C39C40\n",
    "++       C41C42C43C44C45C46  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "++         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0\n",
    "%c G  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n",
    "%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc\n",
    "%f  1.2500000  1.025000000  0.00000000000  0.000000000000000\n",
    "%f  0.0000000  0.000000000  0.00000000000  0.000000000000000\n",
    "%i    0    0    0    0      0      0      0      0         0\n",
    "%i    0    0    0    0      0      0      0      0         0\n",
    "/* PCV:IGS14_2163 OL/AL:FES2004  NONE     YN CLK:CoN ORB:CoN\n",
    "/*\n",
    "/*\n"]
    for head in heads:
        fp.write(head)


# 将结果写入sp3文件体
def sp3body(rss, dtss, time, fp):
    ep = time2epoch(time)
    header = '*  {:4d} {:2d} {:2d} {:2d} {:2d} {:11.8f}\n'.format(ep[0], ep[1], ep[2], ep[3], ep[4], ep[5])
    fp.write(header)
    satlist = [x for x in range(32)] + [x for x in range(95, 141)]
    deletesat(satlist)
    for sat in satlist:
        sys, prn = satsys(sat)
        if rss[sat][0] != 0:
            x = rss[sat][0] / 1000
            y = rss[sat][1] / 1000
            z = rss[sat][2] / 1000
            t = dtss[sat][0] * 1000000
        else:
            x = 999999.999999
            y = 999999.999999
            z = 999999.999999
            t = 999999.999999
        body = 'P{:s}{:0>2d} {:13.6f} {:13.6f} {:13.6f} {:13.6f}                    \n'.format(sys, prn, x, y, z, t)
        fp.write(body)

# 将时间信息写入clk头文件
def clkhead(fp, time):
    ep = time2epoch(time)
    heads = ["     3.00           C                                       RINEX VERSION / TYPE\n",
             "                                                            END OF HEADER\n"]
    for head in heads:
        fp.write(head)

def clkbody(dtss, time, fp):
    ep = time2epoch(time)
    for sat in range(148):
        sys, prn = satsys(sat)
        if dtss[sat][0] != 0:
            body = 'AS {:s}{:0>2d}  {:4d} {:2d} {:2d} {:2d} {:2d} {:9.6f}  1{:>22.12E}\n'.format(sys, prn,\
                    ep[0], ep[1], ep[2], ep[3], ep[4], ep[5], dtss[sat][0])
            fp.write(body)