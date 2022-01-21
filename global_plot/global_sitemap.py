

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

mpl.rcParams['font.sans-serif'] = ['Helvetical']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rc('xtick', labelsize=9)
mpl.rc('ytick', labelsize=9)
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
plt.rcParams['savefig.dpi'] = 300

# Load the coordinate of IGS Core & MGEX sites, The CSV files are
# exported from: http://www.igs.org/network
mgex = np.recfromcsv('new-mgex.csv', names=True)
#igs = np.recfromcsv('igs.csv', names=True, encoding='utf-8')
#igs = pd.read_csv('mgex.csv')

fig = plt.figure(figsize=(6.4, 3.2))
# Set projection
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=150))
# Add ocean and land
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE, linewidth=0.1)

# sites = ['ABMF', 'DJIG', 'FAA1', 'HARB',
#          'JFNG', 'KIRU', 'MAYG', 'MGUE',
#          'NNOR', 'NYA2', 'PADO', 'SGOC', 'SGPO', 'TOW2', 'URUM']
#sites = sta_list
#ReciverType=['JAVAD TRE_3','JAVAD TRE_3 DE','SEPT POLARX5','TRIMBLE ALLOY']
#lists = []
#for i in mgex:
#    if i['reciver'] == ReciverType[1]:
#        lists.append(i)

#plot_sites = pd.array(lists)
#plot_sites = pd.array('Site')

# Add MGEX & IGS core sites
ax.plot(mgex['lat'][0:9], mgex['long'][0:9], 'o', color='darkorange',mec='k',mew=0.5, transform=ccrs.Geodetic(), ms=8.0)
ax.plot(mgex['lat'][9:21], mgex['long'][9:21], 'o', color='m',mec='k',mew=0.5, transform=ccrs.Geodetic(), ms=8.0)
ax.plot(mgex['lat'][21:36], mgex['long'][21:36], 'o', color='forestgreen',mec='k',mew=0.5, transform=ccrs.Geodetic(), ms=8.0)
ax.plot(mgex['lat'][36:45], mgex['long'][36:45], 'o', color='royalblue',mec='k', mew=0.5,transform=ccrs.Geodetic(), ms=8.0)

for j in plot_sites:
    plt.text(j['long'], j['lat'], j['site'], transform=ccrs.Geodetic(), FontSize=10)

ax.legend(['JAVAD TRE_3','JAVAD TRE_3 DE','SEPT POLARX5','TRIMBLE ALLOY'],loc='lower left',fontsize=8)

# Plot gridlines
# ax.gridlines(linestyle='--', LineWidth=0.05)
ax.set_global()
ax.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

fig.savefig('sites1.tiff', bbox_inches='tight', dpi=400)
plt.show()
