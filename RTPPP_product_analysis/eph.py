# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''

class Eph_base_t:
    def __init__(self):
        self.id = 'X00'
        self.csys  = 'X'
        self.prn   = 0
        self.iode  = 0
        self.iodc  = 0
        self.sva   = 0
        self.svh   = 0
        self.flag  = 0
        self.A     = 0.0

class Eph_1ep:
    def __init__(self):
        self.week   = 0
        self.sow    = 0.0
        self.inf_fbs = []
