# coding=utf-8
# !/usr/bin/env python

'''
 Program: abmupd file producer (batch process)
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''

import os
from tkinter import filedialog
# class for the ambiguity information
class Sat:
    def __init__(self):
        self.prn = "X00"
        self.ifamb = 0.0
        self.wlamb = 0.0
        self.mjdd = 0
        self.mjdss = 0
        self.mjdse = 0
        self.sigif = 0.0
        self.sigwl = 0.0

# Read the IF and WL ambiguity information from the PRIDE-PPPAR-II solutions and save to the Class Sat
def read_pride(filename):
    Multi_sat = []
    f = open(filename, 'r')
    ln = f.readline()
    while ln:
        ln = f.readline()
        if "END OF HEADER" in ln:
            break
    ln = f.readline()
    while ln:
        ln = f.readline()
        if not ln:
            break
        sat = Sat()
        mjds = float('0' + ln[55:66])
        mjde = float('0' + ln[73:84])
        sat.prn = ln[1:4]
        sat.ifamb = float(ln[16:26])
        sat.wlamb = float(ln[37:48])
        sat.sigif = float(ln[87:93])
        sat.sigwl = float(ln[96:102])
        sat.mjdd = int(ln[50:55])
        sat.mjdss = round(mjds * 86400)
        sat.mjdse = round(mjde * 86400)
        Multi_sat.append(sat)
    f.close()
    return Multi_sat

# output the ambiguity information to the abmupd file
def output(sat, filename, site):
    f = open(filename, 'w')
    for epoch in range(0, 86400, 30):
        for i in range(len(sat)):
            if sat[i].mjdss <= epoch <= sat[i].mjdse:
                item = "   %5d%10.1f %4s %3s%19.3f%19.3f%10.3f\n"%(sat[i].mjdd, epoch,\
                     site, sat[i].prn, sat[i].ifamb, sat[i].wlamb, sat[i].sigwl)
                f.write(item)
    f.close()


if __name__ == '__main__':
    filepath = filedialog.askdirectory()
    # filepath = "C:\\Users\\LZ\\Desktop\\sta"
    for files in os.listdir(filepath):
        if "amb" in files[0:3]:
            filename = filepath + "\\" + files
            print("[INFO] Convert the file :", files)
            site = filename[-4:].upper()
            outputfile = filename[:-16] +"LZ\\" + site + '_ambupd_'+filename[-12:-5]
            Multi_sat = read_pride(filename)
            output(Multi_sat, outputfile, site)
