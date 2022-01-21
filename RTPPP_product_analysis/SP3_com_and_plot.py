# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""
from SP3compare import *
from plot_orb import *

if __name__ == '__main__':
    start = time.perf_counter()
    filepath = r"D:\RT-stream4\test"
    base_sp3 = filepath + "\\" + r"GBM0MGXRAP_20213550000_01D_05M_ORB.SP3"
    test_sp3 = filepath + "\\" + r"cnet21892.sp3"
    base = readsp3(base_sp3)
    test = readsp3(test_sp3)
    rac_all = compare(base, test)
    stat_rac, sys_rac = statistic_rac(rac_all)
    output = output_rac(filepath, rac_all, stat_rac, sys_rac, base_sp3, test_sp3)
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