# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""

def obssnr(obss, info):
    snrindex = [[], [], [], [], [], [], []]
    obstype = info.obstypes
    for i in range(len(obstype)):
        for j in range(len(obstype[i])):
            if obstype[i][j][0] == "S":
                snrindex[i].append(j)
    print(info)
    return 0