# coding=utf-8
# !/usr/bin/env python
"""
Program:combine_15min_obs.py
Function:
Author:LZ_CUMT
Version:1.0
Date:2021/01/06
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
    for j in head[0]:
        fw.write(j)
    for i in range(len(body)):
        for j in body[i]:
            fw.write(j)


if __name__ == '__main__':
    filepath = r"C:\Users\LZ\Desktop\20220106030222\test"
    filelist = ["USUD00JPN_R_20220010000_15M_01S_MO.cro", "USUD00JPN_R_20220010015_15M_01S_MO.cro",
                "USUD00JPN_R_20220010030_15M_01S_MO.cro", "USUD00JPN_R_20220010045_15M_01S_MO.cro",]
    filew = r"usud001a.22o"
    filewpath = filepath + "//" + filew
    head = []
    body = []
    for i in range(len(filelist)):
        filenav = filepath + "//" + filelist[i]
        head_, body_ = readeph(filenav)
        head.append(head_)
        body.append(body_)
    writeeph(filewpath, head, body)
    print("Finished!")