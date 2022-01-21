# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''
import os

if __name__ == '__main__':
    foldername = 'D:/paperdata/2021/182/daily'
    f_list = os.listdir(foldername)
    for file in f_list:
        site = file[0:4].upper()
        print(site)
