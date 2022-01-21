#!/usr/bin/python
# coding=utf-8
import os
'''
遍历当前文件下所有o文件，读取头文件信息并存储至site.info
Version：1.0
Author:LZ_CUMT   
......
'''


if __name__ == '__main__':
    filepath="C:\\Users\\LZ\\Desktop\\ccc\\LZ"
    writepath = 'C:\\Users\\LZ\\Desktop\\ccc\\LZ\\site_list'
    fw = open(writepath,"w")
    for file in os.listdir(filepath):
        output="{}\n".format(file[0:4])
        fw.write(output)