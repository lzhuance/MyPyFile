# coding=utf-8
# !/usr/bin/env python
"""
Program:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""
import global_var

def global_init():
    global_var.set_value('CLIGHT',299792458.0)


if __name__ == '__main__':
    global_var._init()
    global_init()
    print(global_var.get_value('CLIGHT'))