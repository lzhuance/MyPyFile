# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""
import time
from readnav import *
from readobs import *
from readsp3 import *
from spp import *
from obssnr import *

def process():
    obsfile = r"D:\GNSS_DATA\rt_test1\zamb3560.21o"
    navfile = r"D:\GNSS_DATA\rt_test1\brdm3560.21p"
    sp3file = r"D:\GNSS_DATA\rt_test1\gbm21893.sp3"
    ephs, gephs = readbrdc(navfile)
    obss, info = readobs3(obsfile)
    # satposs = readsp3(sp3file)
    # satpos_expand(info, satposs)
    # spp(obss, ephs, gephs, info)
    obssnr(obss, info)


if __name__ == '__main__':
    start = time.perf_counter()
    process()
    end = time.perf_counter()
    print("[INFO] The function run time is : %.03f seconds" %(end-start))   # 程序耗时计算