#!/usr/bin/python
# coding=utf-8
import os
'''
遍历当前文件下所有o文件，读取头文件信息并存储至site.info
Version：1.0
Author:LZ_CUMT

site.info:
site     ver    G    R    E    C    J    I    S   RecType
abmf    3.04   18   20   20   12   12    4    8   SEPT POLARX5        
abpo    3.04   17   12   15   18   15    0    0   SEPT POLARX5        
acrg    3.04   24   16    8    0    0    0    0   JAVAD TR_G3TH       
aggo    3.04   22   20   20   20    0    4    8   SEPT POLARX5TR      
......
'''


if __name__ == '__main__':
    filepath = r"C:\Users\LZ\Desktop\rt_test1\obs"
    writepath = r"C:\Users\LZ\Desktop\rt_test1\bdssat.info"
    fw = open(writepath,"w")
    #fw.write('site     ver    G    R    E    C    J    I    S   RecType\n')
    for file in os.listdir(filepath):
        f = open(filepath+"\\"+file,encoding='gb18030', errors='ignore')
        lns = f.readlines()
        #c2c3 = 0
        c2 = 0
        c3 = 0
        aa = []
        for i in range(len(lns)):
            if lns[i][0] == ">":
                aa.append(i)
            if len(aa) == 2:
                break
        print(aa)
        for ln in lns[aa[0]+1:aa[1]]:
            if ln[0] == "C":
                prn = int(ln[1:3])
                #c2c3 += 1
                if prn <= 14 or prn == 16:
                    c2 += 1
                elif 19 <= prn <= 46 or prn != 31:
                    c3 += 1
        f.close
        output = "{}{:5d}{:5d}\n".format(file[0:4],c2,c3)
        fw.write(output)