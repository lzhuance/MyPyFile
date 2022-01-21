#!/usr/bin/python
# coding=utf-8

"""
gnss时间转换库
Version：1.0
Author:LZ_CUMT
"""

from math import floor

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


