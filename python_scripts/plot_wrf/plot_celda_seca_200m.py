#Este script plotea el empuje y sus componentes en un corte vertical.
#Las funciones estan pensadas para leer un diccionario (wrf_data) que contiene todos los datos necesarios.
#Cada funcion va agregando nuevas variables a ese diccionario.

#Las funciones buscan reducir el tiempo y no repetir calculos inecesariamente, por eso se fijan si el calculo ya esta hecho.
#Pero tambien esta la opcion de setear force=True para repetir el calulo a la fuerza.

import wrf_module as wrf
import wrf_plot   as wrfp
import numpy as np
import os


exp_path = '/home/jruiz/datosalertar1/SIMULACIONES_CYM_2017/celda_seca_200m/'    #Carpeta base del experimento.

data_path = exp_path + '/run/'                                                       #Carpeta donde estan los datos.

plot_path = exp_path + '/figuras/'                                                   #Carpeta donde se generan las figuras.
os.makedirs(plot_path,exist_ok=True)


wrf_data = wrf.get_data_vslice( data_path , slice_type='vy' , slice_index = 80 , force=False ) 

wrf_data = wrf.get_moment_equation( wrf_data , force=False )

wrf_data = wrf.get_termo_equation( wrf_data , force=False )

wrf_data = wrf.get_water_equation( wrf_data , force=False )

wrf_data = wrf.get_ppert_equation(  wrf_data , force=False )


wrfp.plot_momentum_equation_v( wrf_data , plot_path )

wrfp.plot_termo_equation_v( wrf_data , plot_path )

wrfp.plot_vapor_equation_v( wrf_data , plot_path )

#wrfp.plot_water_equation_v( wrf_data , plot_path )

wrfp.plot_ppert_equation_v( wrf_data , plot_path )
