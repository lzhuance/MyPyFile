#!/usr/bin/python
# coding=utf-8

import os

'''
遍历文件夹并删除指定文件
Version：1.0
Author:LZ_CUMT
'''

# 遍历文件夹
def listfilepath(dir, siteids):
    results = os.listdir(dir)                                    # 获取当前文件夹下所有文件和文件夹列表，存入results
    for element in results:                                      # 依次循环results中的元素
        elefullpath = dir + '\\' + element                       # 构造该元素的完整路径
        if os.path.isfile(elefullpath):                         # 判断是文件还是文件夹
            flag = 0
            for siteid in siteids:
                if element[0:4] == siteid:
                    flag = flag+1
            if flag == 0:
                os.remove(elefullpath)
                print("delete", element, "in path", dir)
        else:
            listfilepath(elefullpath, siteids)       # 递归循环，直到遍历完所有文件夹
    return


if __name__ == '__main__':
    siteids = ['abpo','cusv','dgar','djig','gamg','harb','iisc','kiru','mal2','mchl','met3','metg','mizu','mobs',\
               'nrmg','ptgg','seyg','sgoc','sod3','spt0','wtzr','yar2']
    # for siteid in siteids:
    dir = 'D:/ifb2'
    listfilepath(dir, siteids)
