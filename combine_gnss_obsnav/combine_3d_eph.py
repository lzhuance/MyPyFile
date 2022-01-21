# coding=utf-8
# !/usr/bin/env python
"""
Program:combine_3d_eph.py
Function:
Author:LZ_CUMT
Version:1.0
Date:2021/12/27
"""

def readeph(file):
    f = open(file, "r")
    lines = f.readlines()
    for i in range(len(lines)):
        if "END OF HEADER" in lines[i]:
            break
    return lines[:i+1], lines[i+1:]

def writeeph(filew, head, body):
    fw = open(filew, "w")
    for j in head[1]:
        fw.write(j)
    for i in range(len(body)):
        for j in body[i]:
            fw.write(j)


if __name__ == '__main__':
    filepath = r"C:\Users\LZ\Desktop\rt_test1\SSR"
    filelist = ["BRDM00DLR_S_20213550000_01D_MN.rnx", "BRDM00DLR_S_20213560000_01D_MN.rnx",
                "BRDM00DLR_S_20213570000_01D_MN.rnx"]
    filew = r"brdm3560.21p"
    filewpath = filepath + "//" + filew
    head = []
    body = []
    for i in range(len(filelist)):
        filenav = filepath + "//" + filelist[i]
        head_, body_ = readeph(filenav)
        head.append(head_)
        body.append(body_)
    writeeph(filewpath, head, body)