import numpy as np

def calc_iceberg_size(iceberg_in1):
    '''Correct iceberg size not supplied with empirical relations before seeding iceberg.
    '''
    lengths = iceberg_in1['length']
    if 'length' in iceberg_in1 and 'width' not in iceberg_in1:
        iceberg_in1['width'] = 0.7*lengths*np.exp(-0.00062*length)
    if 'length' in iceberg_in1 and np.logical_or('draft' not in iceberg_in1,'sail' not in iceberg_in1):
        rho_i, rho_w = 900,1027 #kg/m3
        height = np.array(0.3*lengths*np.exp(-0.00062*lengths))
        if np.logical_and('draft' not in iceberg_in1, 'sail' in iceberg_in1): print('Implement')
        elif np.logical_and('draft' not in iceberg_in1, 'sail' not in iceberg_in1): draft = height*(rho_i/rho_w)
        if np.logical_and('sail' not in iceberg_in1, 'draft' not in iceberg_in1): sail = height*(1-rho_i/rho_w) 
        elif np.logical_and('sail' not in iceberg_in1, 'draft' in iceberg_in1): print('Implement')
        iceberg_in1['draft'] = draft
        iceberg_in1['sail'] = sail
    return iceberg_in1

# CHECKS
def check_simulation_results(oi_in, dict_in_in, logger):
    '''
    Checks if icebrg seeding, model configurations and variable reading worked correctly.
    '''
    logger.info('Performing checks..')
    #Checks model configurations
    for c in dict_in_in['config']:
        if 'seed' in c: test = abs(dict_in_in['config'][c]-oi_in[c.split(':')[1]][:,0].values[0])>0.01 #Some configurations can be accessed as dataset variables
        else: test = str(dict_in_in['config'][c])==str(oi_in.attrs['config_'+c]) #Some configurations can be accessed as attributes
        if test==True: print('Checks: ',c,' not defined corretly in the model: ',dict_in_in['config'][c],oi_in.attrs['config_'+c])
    #Checks if iceberg(s) were seeded correctly
    for s in dict_in_in['seed']:
        if s not in ('number','time','radius'): 
            test = np.any(np.abs(dict_in_in['seed'][s]-oi_in[s][:,0].values)>0.01)
            if test==True: print('Checks: ',s,' not seeded correctly, difference: ',np.abs(dict_in_in['seed'][s]-oi_in[s][:,0].values))
    #Checks if input variables were read (if Readers worked)
    #list of mmost important input variables
    v_l = ['x_sea_water_velocity',  'y_sea_water_velocity', 'x_wind', 'y_wind',  'sea_water_temperature', 'sea_water_salinity', 
           'sea_ice_area_fraction','sea_ice_thickness', 'sea_ice_x_velocity', 'sea_ice_y_velocity','sea_surface_wave_stokes_drift_x_velocity', 'sea_surface_wave_stokes_drift_y_velocity',] #'sea_surface_wave_significant_height', 'sea_surface_wave_from_direction',  
    test=np.all(oi_in[v_l] == 0) #checks all variable arrays  at once
    for v in v_l: 
        if test[v]==True: print('Checks: ',v, 'NOT imported!') #print warning if variable all zero
    logger.info('Checks done.')
    return