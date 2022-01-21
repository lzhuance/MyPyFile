# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""

from ORBcompare import *
from plot_orb import readsp3comp, plot_rac, rcParams

if __name__ == '__main__':
    start = time.perf_counter()
    filepath = r"D:\RT-stream4\test"
    sp3file1 = filepath + "\\" + r'GBM0MGXRAP_20213550000_01D_05M_ORB.SP3'
    sp3file2 = filepath + "\\" + r'cass21892.sp3'
    outputfile = filepath + "\\" + r'sp3compare0.txt'
    output = process(sp3file1, sp3file2, outputfile)
    outfile = output[1][:-4]
    init_global()
    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 12,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)
    rac = readsp3comp(output[1])
    plot_rac(rac, outfile)
    end = time.perf_counter()
    print("[INFO] The function run time is : %.03f seconds" %(end-start))   # 程序耗时计算
