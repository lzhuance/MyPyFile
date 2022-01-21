import os
import math
import numpy as np
import matplotlib as mpl
#from mpl_toolkits.basemap import Basemap
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

mpl.rcParams['font.sans-serif'] = ['Helvetical']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rc('xtick', labelsize=9)
mpl.rc('ytick', labelsize=9)
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
plt.rcParams['savefig.dpi'] = 400


fig = plt.figure(figsize=(5, 2))
# Set projection
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=150))
# Add ocean and land
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE, linewidth=0.1)

cm=plt.get_cmap('RdBu_r')
data = pd.read_csv('imp.csv')
sc=plt.scatter(data['Lat']-150, data['Long'], c=data['Imp'],cmap=cm,zorder=40,s=60)
cbar = plt.colorbar(sc)
cbar.set_ticks([-.4,-.2,-.1, 0,.1,.2,.3, .4])
cbar.set_ticklabels(['-40%', '-20%', '-10%','0', '10%', '20%', '30%', '40%'])

ax.set_global()
ax.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

#plt.colorbar(sc)
fig.savefig('static-sitesimp2.tiff', bbox_inches='tight', dpi=400)
plt.show()