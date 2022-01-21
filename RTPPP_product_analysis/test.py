# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/19
 '''
from eph2sp3 import *
from readfile import *
import time

def output_satno():
    f = open(r'satno.txt','w')
    init_global()
    for sat in range(150):
        sys, prn = satsys(sat)
        output = '{:3d}  {}{:2d}\n'.format(sat,sys,prn)
        f.write(output)

def process():
    #ssrcfile =r"D:\RT-stream4\SSRC00CAS0355A.21C"
    #rac, clk = readssrc2(ssrcfile)
    atxfile = "igs14.atx"
    pcv = readantex(atxfile)
    print(pcv)

if __name__ == '__main__':
    start = time.perf_counter()
    process()
    end = time.perf_counter()
    print("The function run time is : %.03f seconds" %(end-start))