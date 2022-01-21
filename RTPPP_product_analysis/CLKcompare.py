# coding=utf-8
# !/usr/bin/env python
"""
Program: CLKcompare.py
Function: Calculate the precision of GNSS clock file
Author:LZ_CUMT
Version:1.0
Date:2021/12/22
"""
from cmn import *
from math import pow
import time

# CLK结构体
class CLK:
    def __init__(self):
        self.time = 0
        self.sat = 0
        self.sys = "X"
        self.prn = 0
        self.clk = 0.0

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

# 结构体转换为np数组
def clkconvert(clks):
    clk = np.zeros((2880, 148))
    for i in range(len(clks)):
        week, sow = time2gpst(clks[i].time)
        x = int((sow % 86400) / 30)
        y = clks[i].sat
        clk[x, y] = clks[i].clk
    return clk

# 钟差文件读取
def readclk(file):
    clks = []
    f = open(file, "r")
    ln = f.readline()
    while ln:
        if "RINEX VERSION / TYPE" in ln:
            ver = float(ln[:10])
        if "END OF HEADER" in ln:
            break
        ln = f.readline()
    while ln:
        ln = f.readline()
        if ln[0:2] == 'AS' and ln[3:6] != 'C59' and ln[3:6] != 'C60':
            sys = ln[3]
            prn = int(ln[4:6])
            sat = satno(sys, prn)
            if ver == 3.04:
                year = int(ln[13:17])
                mon = int(ln[18:20])
                day = int(ln[21:23])
                hour = int(ln[24:26])
                mini = int(ln[27:29])
                sec = float(ln[30:39])
                clk_single = float(ln[45:64])
            else:
                year = int(ln[8:12])
                mon = int(ln[13:15])
                day = int(ln[16:18])
                hour = int(ln[19:21])
                mini = int(ln[22:24])
                sec = float(ln[25:34])
                clk_single = float(ln[40:59])
            ep = [year, mon, day, hour, mini, sec]
            t = epoch2time(ep)
            clk = CLK()
            clk.time = t
            clk.sys = sys
            clk.prn = prn
            clk.sat = sat
            clk.clk = clk_single
            clks.append(clk)
    all_clk = clkconvert(clks)
    return all_clk

# 双差计算钟差STD和RMS
def clkcompare(diffsat, clks1, clks2):
    satrange = [0, 32, 59, 95, 113, 141]  # G R E C2 C3
    sat_std = np.zeros(148)
    sat_rms = np.zeros(148)
    for i in range(len(satrange) - 1):
        for sat in range(satrange[i], satrange[i + 1]):
            if sat != diffsat[i]:
                ddclks = []
                for k in range(2880):
                    clk11 = clks1[k, sat]
                    clk12 = clks1[k, diffsat[i]]
                    clk21 = clks2[k, sat]
                    clk22 = clks2[k, diffsat[i]]
                    if clk11 == 0 or clk12 == 0 or clk21 == 0 or clk22 == 0:
                        continue
                    sdclk1 = clk11 - clk12
                    sdclk2 = clk21 - clk22
                    ddclk = (sdclk1 - sdclk2) * pow(10, 9)    # s ---> ns
                    ddclks.append(ddclk)
                if ddclks != []:
                    std = list1d_std(ddclks)
                    rms = list1d_rms(ddclks)
                    sat_std[sat] = std
                    sat_rms[sat] = rms
    print("[INFO] Finish compare the clk information!")
    return sat_std, sat_rms

# 把计算结果写入输出文件
def output(file, std, rms, file1, file2):
    fw = open(file, "w")
    head = '% 1st file: {}\n% 2nd file: {}\nSAT      STD        RMS   \n'.format(file1, file2)
    fw.write(head)
    for sat in range(148):
        if std[sat] != 0 and rms[sat] != 0:
            sys, prn = satsys(sat)
            body = '{}{:>02d}  {:11.8f}  {:11.8f}\n'.format(sys, prn, std[sat], rms[sat])
            fw.write(body)
    print("[INFO] Output the results successfully!")

# 核心处理
def process(clkfile1, clkfile2, outputfile, reference):
    init_global()                                             # 全局变量初始化
    diffsat = ref2sat(reference)
    clks1 = readclk(clkfile1)                                 # 钟差文件读取
    print('[INFO] Finish reading the 1st clk file!')
    clks2 = readclk(clkfile2)                                 # 钟差文件读取
    print('[INFO] Finish reading the 2nd clk file!')
    sat_std, sat_rms = clkcompare(diffsat, clks1, clks2)      # 双差计算钟差STD和RMS
    output(outputfile, sat_std, sat_rms, clkfile1, clkfile2)  # 把计算结果写入输出文件


if __name__ == '__main__':
    start = time.perf_counter()
    filepath = r"D:\RT-stream4\test"
    clkfile1 = filepath + "\\" + r'GBM0MGXRAP_20213550000_01D_30S_CLK.CLK'
    clkfile2 = filepath + "\\" + r'casl21892.clk'
    outputfile = clkfile2[:-4] + r'CLKcompare.txt'
    reference = ['G01', 'R01', 'E01', 'C16', 'C36']  # 设置基准卫星
    process(clkfile1, clkfile2, outputfile, reference)
    end = time.perf_counter()
    print("[INFO] The function run time is : %.03f seconds" %(end-start))   # 程序耗时计算
