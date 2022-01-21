#!/usr/bin/python
# coding=utf-8

import os
import shutil

'''
遍历文件夹并删除指定文件
Version：1.0
Author:LZ_CUMT
'''

# 遍历文件夹
def listfilepath(dir, siteid):
    results = os.listdir(dir)                                    # 获取当前文件夹下所有文件和文件夹列表，存入results
    for element in results:                                      # 依次循环results中的元素
        elefullpath = dir + '\\' + element                       # 构造该元素的完整路径
        if os.path.isfile(elefullpath):                         # 判断是文件还是文件夹
            if element[0:4] == siteid:
                shutil.copy(elefullpath,'D:\\paperdata')
                #print("delete", element, "in path", dir)
        else:
            listfilepath(elefullpath, siteid)       # 递归循环，直到遍历完所有文件夹
    return


if __name__ == '__main__':
    siteids=[]
    #sitefile='C:\\Users\\LZ\\Desktop\\ccc\\LZ\\site_list'
    #f = open(sitefile)
    #ln = f.readline()
    #while ln:
    #    siteids.append(ln[0:4].lower())
    #    ln = f.readline()
    #f.close()
    siteids = ['krgg',	'ptgg',	'cusv',	'wtzr']
    for siteid in siteids:
        dir = "D:\\paperdata\\2021"
        listfilepath(dir, siteid)
