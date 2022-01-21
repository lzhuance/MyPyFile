# coding=utf-8
# !/usr/bin/env python
"""
Program:
Function:
Author:LZ_CUMT
Version:1.0
Date:2022/01/01
"""


# posmode navsys bds3freq outdir
# gamp_S_G_N_WHU.cfg

def readopt(cfgname):
    opt = cfgname[5:-4].split("_")
    return opt


def process(out_cfg, cfgname):
    out = open(out_cfg, "w")
    opt = readopt(cfgname)
    i = 0
    for ln in ref:
        i += 1
        if "posmode" in ln:
            if opt[0] == "S":
                ln = "posmode             = 7                     %(0:spp  6:ppp_kinematic  7:ppp_static)\n"
            elif opt[0] == "K":
                ln = "posmode             = 6                     %(0:spp  6:ppp_kinematic  7:ppp_static)\n"
        elif "navsys" in ln:
            if opt[1] == "G":
                ln = "navsys              = 1                     %(1:gps  4:glo  5:gps+glo  8:gal  16:qzs  32:bds)\n"
            elif opt[1] == "GC":
                ln = "navsys              = 33                     %(1:gps  4:glo  5:gps+glo  8:gal  16:qzs  32:bds)\n"
        elif "bds3freq" in ln:
            if opt[2] == "O":
                ln = "bds3freq            = 1                     %BDS-3 Frequency Type(1:B1I/B3I/B2b 2:B1C/B2a/B3I (BDS-3 only))\n"
            elif opt[2] == "N":
                ln = "bds3freq            = 2                     %BDS-3 Frequency Type(1:B1I/B3I/B2b 2:B1C/B2a/B3I (BDS-3 only))\n"
        elif "arproduct" in ln:
            if opt[2] == "O":
                ln = "arproduct           = 0                     %(0:off,1:fcb,2:irc_grm,3:irc_gbm,4:osb_gbm,5:osb_whu,6:osb_com,7:osb_sgg,8:osb_cnt,9:upd)\n"
            if opt[2] == "N":
                ln = "arproduct           = 0                     %(0:off,1:fcb,2:irc_grm,3:irc_gbm,4:osb_gbm,5:osb_whu,6:osb_com,7:osb_sgg,8:osb_cnt,9:upd)\n"
        elif "preciseprod" in ln:
            ln = "preciseprod         = {}\n".format(opt[-1].lower())
        elif "outdir" in ln:
            ln = "outdir              = PPP{}\n".format(cfgname[4:-4])
        out.write(ln)

if __name__ == '__main__':
    gampexe = "D:\GNSS_RTPPP\Debug\GNSS_RTPPP.exe"
    path = r"C:\Users\LZ\Desktop\rt_test1"
    batfile = path + "\\gamp.bat"
    ref_cfg = path + "\\gamp.cfg"
    bat = open(batfile, "w")

    cfgnames = ["gamp_S_G_O_WHU.cfg", "gamp_S_GC_O_WHU.cfg", "gamp_S_GC_N_WHU.cfg",
                "gamp_K_G_O_WHU.cfg", "gamp_K_GC_O_WHU.cfg", "gamp_K_GC_N_WHU.cfg",
                "gamp_S_G_O_CAS.cfg", "gamp_S_GC_O_CAS.cfg", "gamp_S_GC_N_CAS.cfg",
                "gamp_K_G_O_CAS.cfg", "gamp_K_GC_O_CAS.cfg", "gamp_K_GC_N_CAS.cfg",
                "gamp_S_G_O_GFZ.cfg", "gamp_S_GC_O_GFZ.cfg", "gamp_S_GC_N_GFZ.cfg",
                "gamp_K_G_O_GFZ.cfg", "gamp_K_GC_O_GFZ.cfg", "gamp_K_GC_N_GFZ.cfg",
                "gamp_S_G_O_CNE.cfg", "gamp_S_GC_O_CNE.cfg", "gamp_S_GC_N_CNE.cfg",
                "gamp_K_G_O_CNE.cfg", "gamp_K_GC_O_CNE.cfg", "gamp_K_GC_N_CNE.cfg",
                "gamp_S_G_O_DLR.cfg", "gamp_S_GC_O_DLR.cfg", "gamp_S_GC_N_DLR.cfg",
                "gamp_K_G_O_DLR.cfg", "gamp_K_GC_O_DLR.cfg", "gamp_K_GC_N_DLR.cfg"]

    # cfgnames = ["gamp_S_G_O_WUM.cfg", "gamp_S_G_O_COD.cfg", "gamp_S_G_O_GBM.cfg"]
    for cfgname in cfgnames:
        out_cfg = path + "\\cfg\\" + cfgname
        ref = open(ref_cfg, "r")
        bat.write(gampexe + " ./cfg/" + cfgname + "\n")
        process(out_cfg, cfgname)
    print("Done!")
