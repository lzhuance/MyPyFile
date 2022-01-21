# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''
from math import sqrt, floor

# --------------------------Count-------------------------------------
def dot(a, b, n):
    c = 0
    n -= 1
    while n >= 0:
        c += a[n]*b[n]
        n -= 1
    return c

def norm(a, n):
    return sqrt(dot(a, a, n))

def normv3(a):
    r = norm(a, 3)
    if r <= 0.0:
        return 0
    else:
        return np.array([a[0]/r, a[1]/r, a[2]/r])

def cross3(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

# --------------------------Time Convert-------------------------------------
# 年月日转换为儒略日
def ymd2mjd(year, mm, dd):
    if mm <= 2:
        mm += 12
        year -= 1
    mjd = 365.25 * year - 365.25 * year % 1.0 - 679006.0
    mjd += floor(30.6001 * (mm + 1)) + 2.0 - floor(year / 100.0) + floor(year / 400) + dd
    return mjd

# 年月日转换为GPS周及周内天
def ymd2wkdow(year, mm, dd):
    mjd0 = 44243
    mjd = ymd2mjd(year, mm, dd)
    difmjd = mjd-mjd0-1
    week = floor(difmjd / 7)
    dow = floor(difmjd % 7)
    return week, dow

def ymdhms2wksow(year, month, day, hour, min, sec):
    week, dow = ymd2wkdow(year, month, day)
    sow = dow * 86400 + hour * 3600 + min * 60 + sec
    return week, sow
