#!/usr/bin/python
# coding=utf-8

import sys
import math
import os


def checkargv():
    if len(sys.argv) != 5:
        print("Usage : python snxsit.py SITENAME YYYY MM DD")
        return 1
    else:
        year = sys.argv[2]
        mm = sys.argv[3]
        dd = sys.argv[4]
        ymd = sys.argv[2] + sys.argv[3] + sys.argv[4]
        if len(ymd) != 8:
            print("ERROR: Bad date format:", ymd)
            print("Date format: YYYY MM DD")
            return 1
        if int(year) < 1980:
            print("ERROR: Input year is wrong $year")
            return 1
        elif int(mm) <= 0 or int(mm) > 12:
            print("ERROR: Input month is wrong : $mm")
            return 1
        elif int(dd) <= 0 or int(dd) > 31:
            print("ERROR: Input day is wrong : $dd")
            return 1


def ymd2mjd(year, mm, dd):
    mjd = 0.0
    if mm <= 2:
        mm += 12
        year -= 1
    mjd = 365.25 * year - 365.25 * year % 1.0 - 679006.0
    mjd += math.floor(30.6001 * (mm + 1)) + 2.0 - math.floor(
        year / 100.0) + math.floor(year / 400) + dd
    return mjd


def ymd2wkdow(year, dd, mm):
    mjd0 = 44243
    mjd = ymd2mjd(year, mm, dd)
    difmjd = mjd - mjd0 - 1
    week = math.floor(difmjd / 7)
    dow = math.floor(difmjd % 7)
    return week, dow


# 根据测站id在snx文件中查找测站精确坐标
def getcrd(siteid, sscfile):
    snxcrd = []
    if sscfile != '':
        f = open(sscfile, encoding='gb18030', errors='ignore')
        ln = f.readline()
        while ln:
            ln = f.readline()
            if not ln:
                print('ERROR: Not find the siteid', siteid)
                break
            if ln[14:18] == siteid:
                snxcrd.append(float(ln[47:68]))
                ln = f.readline()
                snxcrd.append(float(ln[47:68]))
                ln = f.readline()
                snxcrd.append(float(ln[47:68]))
                break
        if snxcrd:
            print('The', siteid, 'sitecrd is', snxcrd)
        f.close()


if __name__ == '__main__':

    if checkargv():
        exit(1)
    site = sys.argv[1].upper()
    year = sys.argv[2]
    yr = sys.argv[2][-2:]
    mm = sys.argv[3]
    dd = sys.argv[4]
    week, dow = ymd2wkdow(int(year), int(mm), int(dd))

    args = "-nv -t 3 --connect-timeout=10 --read-timeout=60"
    url = f" ftp://gssc.esa.int/igs/products/{week}/igs{yr}P{week}.ssc.Z"
    sscfile = f"igs{yr}P{week}.ssc"
    if os.path.isfile(sscfile) == 0:
        os.system("wget " + args + url)
        os.system("gzip -d " + f"igs{yr}P{week}.ssc.Z")
    if os.path.isfile(sscfile) == 0:
        print("ERROR: No", sscfile)
        exit(1)
    getcrd(site, sscfile)
