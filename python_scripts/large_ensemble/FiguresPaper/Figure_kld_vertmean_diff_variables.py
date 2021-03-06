# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 18:45:15 2016

@author:
"""
import sys
sys.path.append('../../../common_python/common_functions/')
sys.path.append('../../../common_python/common_modules/')

import numpy as np
import datetime as dt
import ctl_reader as ctlr
import os
import matplotlib.pyplot as plt
from common_functions import common_functions as cf


import common_plot_functions as cpf
import common_mask_functions as cmf

basedir='/home/ra001011/a03471/data/output_data/'

figname='./Figure_kld_vertmean_diff_variables'

filename='kldistance_mean.grd'

exps=['LE_D1_1km_5min','LE_D1_1km_2min','LE_D1_1km_1min','LE_D1_1km_30sec','LE_D1_1km_30sec_nospinup','LE_D1_1km_1min_4D']

deltat=[300,120,60,30,30,60]

filetype='guesgp'   #analgp , analgz , guesgp , guesgz

plot_variables=['tk','qv','w','dbz']

lat_radar=34.823
lon_radar=135.523
radar_range=50.0e3   #Radar range in meters (to define the radar mask)

init_times = ['20130713050500','20130713050400','20130713050500','20130713050500','20130713050500','20130713050500'] 

sigma_smooth=2.0

#Define initial and end times using datetime module.
#itime = dt.datetime(2013,7,13,5, 5,0)  #Initial time.
etime = dt.datetime(2013,7,13,5,55,0)  #End time.

#=========================================================
#  LOOP OVER FILE TYPES
#=========================================================

parameter = dict()   

ensemble_mean = dict()

for iexp , my_exp in enumerate(exps)   :

  itime = dt.datetime.strptime(init_times[iexp] , '%Y%m%d%H%M%S' )

  delta=dt.timedelta(seconds=deltat[iexp])

  #Compute the total number of times
  ntimes=int( 1 + np.around((etime-itime).seconds / delta.seconds) ) #Total number of times.

  ctl_file = basedir + '/' + my_exp + '/ctl/' + filetype + '.ctl'

  #=========================================================
  #  READ CTL FILE
  #=========================================================

  if iexp == 0  :
 
     ctl_dict = ctlr.read_ctl( ctl_file )

     nx=ctl_dict['nx']
     ny=ctl_dict['nx']
     nlev=ctl_dict['nz']
     nt=int(1)             #Force the number of times to be one.
     ctl_dict['nt']=int(1) #Force the number of times to be one.

     undef=np.float32( ctl_dict['undef'] )

  #=========================================================
  #  READ LAT LON
  #=========================================================
 
  if iexp == 0 :

     latlon_file = basedir + '/' + my_exp + '/latlon/latlon.grd'

     tmp=ctlr.read_data_records(latlon_file,ctl=ctl_dict,records=np.array([0,1]))
     lat=tmp[:,:,1]
     lon=tmp[:,:,0]

     #Exclude areas outside the radar domain.
     radar_mask = cmf.distance_range_mask( lon_radar , lat_radar , radar_range , lon , lat )

  #=========================================================
  #  READ THE DATA
  #=========================================================

  my_file=basedir + '/' + my_exp + '/time_mean/'+ filetype + '/' + '/' + filename

  parameter[my_exp]=ctlr.read_data_grads(my_file,ctl_dict,masked=False)

  print('KLD values')
  print( my_exp )
  for var in parameter[my_exp] :
     print( var )
     print( np.min( parameter[my_exp][var] ) , np.max( parameter[my_exp][var] ) )

  my_file=basedir + '/' + my_exp + '/time_mean/'+ filetype + '/' + '/moment0001_mean.grd'

  ensemble_mean[my_exp]=ctlr.read_data_grads(my_file,ctl_dict,masked=False)
  
  print('State variable values')
  print( my_exp )
  for var in ensemble_mean[my_exp] :
     print( var )
     print( np.min( ensemble_mean[my_exp][var] ) , np.max( ensemble_mean[my_exp][var] ) )

 
 
print(' Finish the loop over experiments ' )    

#=========================================================================================
#Plot the mean KLD and its standard deviation.
#=========================================================================================

nexp = len( exps )

plot_kld_mean = np.zeros( [ nx , ny , nexp ] )
plot_dbz_mean = np.zeros( [ nx , ny , nexp ] )



#Plot time mean of the moments.

#plt.figure(1,figsize=[7,10])
#plt.figure(1)

#Start subplots
ncols = 2
nrows = 2
icoldelta = 1.0/ncols
irowdelta = 1.0/nrows
hmargin=0.0
vmargin=-0.5
hoffset=0.0
voffset=0.0

icol = 0
irow = 0

xtick=[134.5,135,135.5,136,136.5,137]
ytick=[34,34.5,35,35.5]
axesrange=[134.97,136.09,34.36,35.30]
titles = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)']

#Plot time mean of the moments.

import matplotlib
#import matplotlib.cm     as cm
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
#from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs


#for key in kld_time_mean  :

plot_dbz_5min   = np.squeeze( np.nanmax( np.delete( ensemble_mean['LE_D1_1km_5min']['dbz'],4,2),2))
plot_dbz_30sec  = np.squeeze( np.nanmax( np.delete( ensemble_mean['LE_D1_1km_30sec']['dbz'],4,2),2))
plot_dbz_5min[ np.logical_not( radar_mask )  ] = np.nan
plot_dbz_30sec[ np.logical_not( radar_mask )  ] = np.nan


ifig = 0 

fig, axs = plt.subplots( nrows,ncols , subplot_kw=dict(projection=ccrs.PlateCarree() ), figsize=[7,5] , sharex = 'col' , sharey = 'row')

fig.subplots_adjust(wspace=0.0,hspace=0.05,bottom=0.04,left=0.08,right=0.90,top=0.97)

blues=['#001a33','#004d99','#0073e6','#3399ff','#66b3ff','#b3d9ff']
reds =['#ffb3b3','#ff6666','#ff0000','#b30000','#660000','#1a0000']


for ivar,var in enumerate(plot_variables) :

   ifig = icol + ncols*(irow) 

   plot_kld_5min   = np.squeeze( np.nanmean( np.delete( parameter['LE_D1_1km_5min'][var],4,2),2) )
   plot_kld_30sec  = np.squeeze( np.nanmean( np.delete( parameter['LE_D1_1km_30sec'][var],4,2),2) )

   print('Smoothing parameter for var=',var)
   plot_kld_5min=cf.gaussian_filter(field0=plot_kld_5min,dx=1.0,sigma=sigma_smooth,nx=nx,ny=ny,undef=undef)
   plot_kld_30sec=cf.gaussian_filter(field0=plot_kld_30sec,dx=1.0,sigma=sigma_smooth,nx=nx,ny=ny,undef=undef)

   plot_kld_diff = 100 * ( ( plot_kld_30sec - plot_kld_5min ) / plot_kld_5min )

   plot_kld_5min[ np.logical_not( radar_mask )  ] = np.nan
   plot_kld_diff[ np.logical_not( radar_mask )  ] = np.nan


   #Axes limits
   #my_axes = [icoldelta*(icol-1)+hmargin+hoffset,irowdelta*(irow-1)+vmargin+voffset,irowdelta-2*hmargin,icoldelta-2*vmargin]
   ax = axs[irow,icol]  #plt.axes( my_axes , facecolor=None , projection=ccrs.PlateCarree() )
   #The pcolor
   ncolors = 12
   smin=-60
   smax=60
   delta = (smax-smin)/ncolors
   #p=ax.pcolor(lon , lat ,  np.transpose( np.squeeze( plot_kld_5min ) ) ,
   #     transform=ccrs.PlateCarree(),vmin=smin , vmax=smax ,cmap=cpf.cmap_discretize('YlGn',21) )
   my_map = cpf.cmap_discretize('coolwarm',11)
   p=ax.contourf(lon , lat ,  np.transpose( np.squeeze( plot_kld_diff ) ) ,
        transform=ccrs.PlateCarree(),vmin=smin , vmax=smax ,cmap=my_map )
   #m = plt.cm.ScalarMappable(cmap=my_map)
   #m.set_array(np.transpose(plot_kld_diff))
   #m.set_clim(smin,smax)
   #cb=plt.colorbar(m,ax=ax,shrink=0.9,boundaries=np.arange(smin,smax+delta,delta))

   ax.set_extent( axesrange , ccrs.PlateCarree())
   gl=ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                linewidth=1.0, color='k',alpha=0.5, linestyle='--')
   #Grid and ticks
   gl.xlocator=mticker.FixedLocator(xtick)
   gl.ylocator=mticker.FixedLocator(ytick)
   #Coastline plot
   ax.coastlines('10m',linewidth=1.0)
   #Colorbar
   #cb=plt.colorbar(p, ax=ax, orientation='vertical' , shrink=0.9 )
   #cb.ax.tick_params(labelsize=10)
   #Contour map
   clevelsneg = [-100,-40,-20]
   clevelspos = [20,40,100]

   print( np.nanmin( plot_kld_5min ) , np.nanmax( plot_kld_5min ) )
   if ivar == 0  :
      clevs = [2.0,2.2,2.4,2.6,2.8,3.0]
   if ivar == 1  :
      clevs = [2.0,3.0,4.0]
   if ivar == 2  :
      clevs = [2.5,5.0,7.5,10.0]
   if ivar == 3  :
      clevs = [20,40,80,120]


   cpos=ax.contour( lon , lat , 100*np.transpose( plot_kld_5min ) , levels=clevs ,  colors='k',linestyles='solid')
   plt.clabel(cpos, inline=1, fontsize=10,fmt='%1.1f')
 
   #Axes label and title
   if irow == 1   :
      plt.xlabel('Latitude')
   if icol == 1   :
      plt.ylabel('Longitude')
   #ax.set_title(titles[ifig],fontsize = 15)
   ax.text(135.01,35.19,titles[ifig],fontsize=15,color='k',bbox={'facecolor':'white', 'alpha':0.8,'edgecolor':'white'})
   #plt.title(titles[ifig],fontsize = 15)

   if icol == 0  :
      gl.ylabel_style = {'size': 12, 'color': 'k' }
   else          :
      gl.ylabel_style = {'visible': False }
   if irow == 1  :
      gl.xlabel_style = {'size': 12, 'color': 'k' }
   else          :
      gl.xlabel_style = {'visible': False }




   gl.xlabels_top = False
   gl.ylabels_right = False

   icol = icol + 1
   if icol >= ncols   :
      icol = 0
      irow = irow + 1

cbar_ax = fig.add_axes([0.90, 0.05, 0.03, 0.9])
m = plt.cm.ScalarMappable(cmap=my_map)
m.set_array(np.transpose(plot_kld_diff))
m.set_clim(smin,smax)
cb=plt.colorbar(m,cax=cbar_ax,boundaries=np.arange(smin,smax+delta,delta))


#plt.show()
plt.savefig( figname + '.eps' , format='eps' , dpi=300  )
plt.close()


