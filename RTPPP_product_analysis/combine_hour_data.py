# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2021/12/23
"""

from cmn import ymdhms2wksow
from math import fmod
from readfile import *

def process(filename, fw):

    lns, head = scanssrc2(filename)
    for i in range(len(head)-1):
        lnhead = lns[head[i]]
        week, sow, type = readssrchead2(lnhead)
        if fmod((sow % 86400), 30) == 0:
            for ln in lns[head[i]:head[i+1]]:
                fw.write(ln)


if __name__ == '__main__':
    filepath = r'D:\RT-stream4'
    acs = ["CAS0", "CNE0", "DLR0", "ESA0", "GFZ0", "GMV0", "WHU0"]
    keylist = [chr(i) for i in range(65, 89)]
    for ac in acs:
        output = filepath + "\\day\\SSRC00" + ac + "3560.21C"
        fw = open(output, "w+")
        for key in keylist:
            # key = "A"
            filename = filepath + "\\hour\\SSRC00" + ac + "356" + key + ".21C"
            print(filename)
            process(filename, fw)