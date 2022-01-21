# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""
from CLKcompare import *
from plot_clk import *

if __name__ == '__main__':
    start = time.perf_counter()
    filepath = r"C:\Users\LZ\Desktop\rt_test1"
    clkfile1 = filepath + "\\" + r'gbm21893.clk'
    clkfile2 = filepath + "\\" + r'whu21893.clk'
    outputfile = clkfile2[:-4] + 'CLKcompare.txt'
    reference = ['G01', 'R01', 'E01', 'C14', 'C37']  # 设置基准卫星
    process(clkfile1, clkfile2, outputfile, reference)
    init_global()
    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 12,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)
    std, rms = readclkcomp(outputfile)
    plotclk(std, rms, outputfile)
    end = time.perf_counter()
    print("[INFO] The function run time is : %.03f seconds" %(end-start))   # 程序耗时计算