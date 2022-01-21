# coding=utf-8
# !/usr/bin/env python
"""
 Program:SP3compare.py
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/01
 """

from cmn import *
from peph import *
import numpy as np

class Sat_RAC:
    def __init__(self):
        self.id = 'X00'
        self.week= 0
        self.sow = 0.0
        self.r   = 0.0
        self.a   = 0.0
        self.c   = 0.0

def rac2dxyz(drac, pos_xyz, vel_xyz):
    dxyz = [0, 0, 0]
    ea = normv3(vel_xyz)
    rc = cross3(pos_xyz, vel_xyz)
    ec = normv3(rc)
    er = cross3(ea, ec)
    for i in range(3):
        dxyz[i] = ea[i] * drac[0] + ec[i] * drac[1] + er[i] * drac[2]
    return dxyz

def xyz2rac(dxyz, pos_xyz, vel_xyz):
    ea = normv3(vel_xyz)
    rc = cross3(pos_xyz, vel_xyz)
    ec = normv3(rc)
    er = cross3(ea, ec)
    A = np.array([[er[0], ea[0], ec[0]], [er[1], ea[1], ec[1]], [er[2], ea[2], ec[2]]])
    drac = np.dot(np.linalg.inv(A), dxyz)
    return drac

def switch(base, test):
    if len(base) < len(test):
        return base, test
    else:
        return test, base

def compare(base1, test1):
    base, test = switch(base1, test1)
    rac_all = []
    for i in range(len(base)):
        epoch1 = base[i].sow
        if i == 0:
            epoch2 = base[i+1].sow
        else:
            epoch2 = base[i-1].sow
        dt = epoch1 - epoch2
        for j in range(len(base[i].inf_fbs)):
            if base[i].inf_fbs[j].x != 0:
                pos_xyz = np.array([base[i].inf_fbs[j].x, base[i].inf_fbs[j].y, base[i].inf_fbs[j].z])
                id = base[i].inf_fbs[j].id
                if i == 0:
                    xyz2 = [base[i+1].inf_fbs[j].x, base[i+1].inf_fbs[j].y, base[i+1].inf_fbs[j].z]
                else:
                    xyz2 = [base[i-1].inf_fbs[j].x, base[i-1].inf_fbs[j].y, base[i-1].inf_fbs[j].z]
                #print(epoch1,i,base[i+1].inf_fbs[j].x)

                test_xyz = []
                #print(len(test[i].inf_fbs))
                for m in range(len(test[i].inf_fbs)):
                    id2 = test[i].inf_fbs[m].id
                    sow2 = test[i].sow
                    if id2 == id and test[i].inf_fbs[m].x != 0 and sow2 == base[i].sow:
                        test_xyz = [test[i].inf_fbs[m].x, test[i].inf_fbs[m].y, test[i].inf_fbs[m].z]
                        break
                if test_xyz == []:
                    continue
                vel_xyz = np.zeros(3)
                dxyz = np.zeros(3)
                for k in range(3):
                    vel_xyz[k] = (pos_xyz[k] - xyz2[k]) / dt
                    if test_xyz != []:
                        dxyz[k] = pos_xyz[k]-test_xyz[k]

                drac = xyz2rac(dxyz, pos_xyz, vel_xyz)
                rac = Sat_RAC()
                rac.id = id
                rac.week = base[i].week
                rac.sow = epoch1
                rac.r = drac[0]
                rac.a = drac[1]
                rac.c = drac[2]
                rac_all.append(rac)
    return rac_all

def statistic_rac(rac_all):
    sats_id = []
    for i in range(len(rac_all)):
        if rac_all[i].id not in sats_id:
            sats_id.append(rac_all[i].id)

    stat_rac = []
    for sat_id in sats_id:
        rac_single = []
        for i in range(len(rac_all)):
            if sat_id == rac_all[i].id and rac_all[i].r < 100 and rac_all[i].r != 0:
                rac_single.append([rac_all[i].r, rac_all[i].a, rac_all[i].c])
        stat_rac_single = [sat_id]
        for j in range(3):
            summary = 0
            if len(rac_single) != 0:
                for i in range(len(rac_single)):
                    summary += abs(rac_single[i][j])
                stat_rac_single.append(summary / len(rac_single))
        stat_rac.append(stat_rac_single)

    sys_rac = []
    for sys_id in ['G', 'R', 'E', 'C2', 'C3', 'J']:
        sys_single = []
        for i in range(len(rac_all)):
            if rac_all[i].r < 100 and rac_all[i].r != 0:
                if sys_id == rac_all[i].id[0] or (sys_id == 'C3' and rac_all[i].id[0] == "C" and\
                  int(rac_all[i].id[1:]) > 19) or (sys_id == 'C2' and rac_all[i].id[0] == "C" and\
                                                    int(rac_all[i].id[1:]) < 19):
                    sys_single.append([rac_all[i].r, rac_all[i].a, rac_all[i].c])
        sys_rac_single = [sys_id]
        for j in range(3):
            summary = 0
            if len(sys_single) != 0:
                for i in range(len(sys_single)):
                    summary += abs(sys_single[i][j])
                sys_rac_single.append(summary / len(sys_single))
        sys_rac.append(sys_rac_single)

    return stat_rac, sys_rac

def output_rac(filepath, rac_all, stat_rac, sys_rac, file1, file2):
    output1 = file2[:-9] + r"SP3compare_all.log"
    output2 = file2[:-9] + r"SP3compare_satellite.log"
    output3 = file2[:-9] + r"SP3compare_system.log"
    head = '% 1st file: {}\n% 2nd file: {}\n'.format(file1, file2)
    f = open(output1, "w")
    f.write(head)
    for i in range(len(rac_all)):
        index = int((rac_all[i].sow%86400)/900)
        ln = "{:4d} {:5.3f} {:3s} {:10.3f} {:10.3f} {:10.3f} {:3d}\n".format(rac_all[i].week, rac_all[i].sow, rac_all[i].id,\
                                                                       rac_all[i].r, rac_all[i].a, rac_all[i].c, index)
        f.write(ln)
    f = open(output2, "w")
    f.write(head)
    for i in range(len(stat_rac)):
        if len(stat_rac[i]) == 4:
            ln = "{:3s} {:>7.2f} {:>7.2f} {:>7.2f}\n".format(stat_rac[i][0], stat_rac[i][1] * 100, stat_rac[i][2] * 100, \
                                                        stat_rac[i][3] * 100)
            f.write(ln)
    f = open(output3, "w")
    f.write(head)
    for i in range(len(sys_rac)):
        if len(sys_rac[i]) == 4:
            ln = "{:2s} {:>5.2f} {:>5.2f} {:>5.2f}\n".format(sys_rac[i][0], sys_rac[i][1]*100, sys_rac[i][2]*100, \
                                                     sys_rac[i][3]*100)
            f.write(ln)
    return [output1, output2, output3]


if __name__ == '__main__':
    filepath = r"D:\RT-stream4\test"
    base_sp3 = filepath + "\\" + r"igr21892.sp3"
    test_sp3 = filepath + "\\" + r"cne21892.sp3"
    base = readsp3(base_sp3)
    test = readsp3(test_sp3)
    rac_all = compare(base, test)
    stat_rac, sys_rac = statistic_rac(rac_all)
    output_rac(filepath, rac_all, stat_rac, sys_rac, base_sp3, test_sp3)
    print("Finish!")