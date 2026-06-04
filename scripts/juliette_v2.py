# Simulating iceberg "Juliette"
# Copy of juliette_v2.ipynb as .py (4 June 2026)

#cd ~/work/tutorials/sources/OpenDrift/openberg_custom_juliette
#run this file from the working directory in terminal using: python3 -m scripts.juliette_v2 

from src.utils import *
from src.utils2 import *
from opendrift.models.openberg import OpenBerg
from opendrift.readers.reader_netCDF_CF_generic import Reader    
import gc

# --- Input data ---
wind_in = ['windglophynrt',] #choose wind input
#oc_in = ['topaz4','topaz5','glophyanfc','glorys'] #choose ocean sea ice and wave input, if nested list of mulitple ocean/sea ice data order by priority!
#oc_in = [[si,oc] for oc in ['topaz4','topaz5','glophyanfc','glorys'] for si in ['nextsimanfc',]] #choose ocean sea ice and wave input, if nested list of mulitple ocean/sea ice data order by priority!
# oc_in = [['topaz6-lowres','topaz5'],['nextsimanfc','topaz5'],['nextsimanfc','topaz6-lowres','topaz5']]
oc_in = [['topaz5','arcmfcwam'],['glophyanfc','arcmfcwam'],['topaz6-lowres','topaz5','arcmfcwam'],['topaz4','arcmfcwam'],['glorys','arcmfcwam']]

# --- Clean up ---
for _ in range(2):
    gc.collect()

# Read and subset tracker data
ds_3day = read_tracker('./input/Osker-X2.csv')['3D']
print(ds_3day.time)

# Dictionary of available environmental input datasets
env = {
    # --- Ocean ---
    'topaz4': 'cmems_mod_arc_phy_my_topaz4_P1D-m',
    'topaz4-ensemble':['https://thredds.met.no/thredds/dodsC/accibergt42/topaz4_be_mem0%s.ncml'%membnr for membnr in [('0'+str(memb)) 
                        if memb<10 else str(memb) for memb in range(1,11)]],
                        #find under:'https://thredds.met.no/thredds/catalog/accibergt42/catalog.html',
    'topaz5': 'cmems_mod_arc_phy_anfc_6km_detided_PT1H-i',
    'topaz5-ensemble': ['https://thredds.met.no/thredds/dodsC/accibergt5/topaz5_be_mem0%s.ncml'%membnr for membnr in [('0'+str(memb)) 
                        if memb<10 else str(memb) for memb in range(1,11)]],                      
                       #find under: https://thredds.met.no/thredds/catalog/accibergt5/catalog.html',
    'topaz6': 'https://thredds.met.no/thredds/dodsC/cmems/topaz6/dataset-topaz6-arc-15min-3km-be.ncml', 
    'topaz6-lowres': 'dataset-topaz6-arc-15min-3km-be',
    'glophyanfc': 'cmems_mod_glo_phy_anfc_0.083deg_PT1H-m', #Global anfc (mercator)
    'glorys': 'cmems_mod_glo_phy_my_0.083deg_P1D-m',
    # --- Sea ice ---
    'nextsimanfc':'cmems_mod_arc_phy_anfc_nextsim_hm',
    'nextsimre':'cmems_mod_arc_phy_my_nextsim_P1D-m',
    # --- Wave ---
    'arcmfcwam':'dataset-wam-arctic-1hr3km-be',
    'arcmfcwamre':'cmems_mod_arc_wav_my_3km_PT1H-i',
    'mfwam':'cmems_mod_glo_wav_anfc_0.083deg_PT3H-i',
    'waverys':'cmems_mod_glo_wav_my_0.2deg_PT3H-i',
    # --- Wind ---
    'windglophyre':'cmems_obs-wind_glo_phy_my_l4_0.125deg_PT1H', #availability; 2007-2026
    'windglophynrt':'cmems_obs-wind_glo_phy_nrt_l4_0.125deg_PT1H', #availability: 2024-2026
    'era5':'../input/era5_juliette.nc'} #Has to be downloaded

#Define index of initial simulation time steps
idx = np.arange(ds_3day.time.size) #here, 3-dayly throughout observed trajectory, ADAPT!
print(idx)

#---Combintaions of inputs
input_l = [(oc if isinstance(oc, list) else [oc]) + [wi]
    for wi in wind_in for oc in oc_in ]
# --- Show configurations ---
print("\nAvailable forcing configurations:")
for i, envinput in enumerate(input_l):
    print(i, envinput)

# --- Simulation definitions ---
ib_duration = 3 #in days, How long every iceberg is simulated after its individual initialisation (iceberg age)
n=10 #number of icebergs released on every initialisation
randspace=np.random.rand(n)

# --- Initial iceberg conditions ---
#---Trajectory information---
lons = ds_3day.lon[idx]
lats = ds_3day.lat[idx]
times = pd.to_datetime(ds_3day.time[idx].values).to_pydatetime().tolist()#[t.values.astype(datetime) for t in ds_3day.time[idx]]
#---Iceberg size---
#iceberg = {'length':150+randspace*100,'width':80+randspace*10, 
 #       'water_form_drag_coef':0.25+randspace*1.25,'wind_form_drag_coef':0.5+randspace*1} #Randomised sizes and coefficients
iceberg = {'length':50+randspace*2000, #meassured and random sizes
       'water_form_drag_coef':0.25+randspace*1.25,'wind_form_drag_coef':0.5+randspace*1} #Randomised sizes and coefficients
#iceberg = {'length':[50,2000,500,1000,2000], 
#       'water_form_drag_coef':0.25+randspace*1.25,'wind_form_drag_coef':0.5+randspace*1} #hardcoded input size
#---Size correction---
iceberg = calc_iceberg_size(iceberg) #this function adds missing iceberg sizes
iceberg['length'][0] = 200 #correct for meassured width
iceberg['width'][0] = 85 #correct for meassured width

# --- Runs simulations
for envinput in input_l: #Loops through the ocean and wind input
    print(f"\nRunning with inputs: {envinput}")
    #---Initialisation---
    o=OpenBerg(loglevel=10,logfile='./results/out_%s.log'%('_'.join(envinput)))
    #---Model configuration---
    o.set_config('drift:max_age_seconds', ib_duration*3600*24) #Terminates simulations  ib_duration seconds after their individual initialisation
    o.set_config('drift:vertical_profile',False)
    o.set_config('drift:stokes_drift',False)
    #---Readers
    for envin in envinput:
        dataset_id = env[envin]
        print(f"Loading dataset: {dataset_id}")
        try:
            if isinstance(dataset_id, str) and dataset_id.endswith('.nc'): #local files, e.g. era5
                ds_env = xr.open_mfdataset(dataset_id)
                reader_env = Reader(
                    ds_env,
                    standard_name_mapping={
                        'u10': 'x_wind',
                        'v10': 'y_wind'})
                o.add_reader(reader_env)
            elif isinstance(dataset_id, list) and 'ensemble' in envin: #list of urls or files, eg. for topaz4 ensemble
                ds_env = xr.open_mfdataset(dataset_id,
                         combine="nested",
                         concat_dim="realization",#should be named "realization" or "ensemble_member"
                         parallel=True,engine="netcdf4", chunks={'time': 10})
                ds_env = ds_env.assign_coords(realization=xr.DataArray(ds_env.realization,dims=("realization",),
                    attrs={"standard_name": "realization","long_name": "ensemble member","axis": "E"}))
                reader_env = Reader(ds_env)
                o.add_reader(reader_env)
            else: o.add_readers_from_list([dataset_id]) 
        except Exception as e:
            print(f"❌ Failed to load {dataset_id}: {e}")
    #---Seed icebergs---
    for lon, lat, time in zip(lons, lats, times): #Loops through initialisations of time-positions
        o.seed_elements(
            lon=lon,
            lat=lat,
            time=time,
            number=n,
            radius=1000,
            **iceberg)
    #---Run---
    oi = o.run(duration=timedelta(days=int(idx.size*ib_duration)), #duration from first initialisation to last termination not equal to ib age!
               outfile='./results/juliette_%s.nc'%('_'.join(envinput)))
    #---Plot map---
    o.plot(fast=True,filename='./results/juliette_map_%s.png'%('_'.join(envinput)))
    #collect left over data
    for _ in range(2):
        gc.collect()
print(oi)

#Some checks
# print('Occuring stati',np.unique(oi.status))
#print('proportion of trajectories that became stranded (at any time)',np.mean(np.any(oi.status==1,axis=1)).values)
#print('proportion of trajectories that are stranded (at the end of simulations)',np.mean(oi.status[:,-1]==1).values)
#print('proportion of trajectories that meltet',np.mean(np.any(oi.status==2,axis=1)).values)
#print('which size do melted trajectories have??',oi.sail[np.any(oi.status==2,axis=1),0].values)
# print('proportion of trajectories that are active (ever)', 
#       np.mean(np.any(oi.status == 0, axis=1)))
# print('proportion of trajectories that are active at the end', 
#       np.mean(oi.status[:, -1] == 0))
# print('proportion of trajectories that melted', 
#       np.mean(np.any(oi.status == 2, axis=1)))

#o.plot_property('sea_surface_wave_significant_height')#,filename='../results/juliette_property.png')
#other usedfull properties to plot: draft, sail, length, width, status, x_Wind

# Regularely do in terminal:
# - processes: ps aux | grep python
# - kill kernels (too many open kernels are a problem): pkill -f ipykernel
# - or check kernels: ps aux | grep ipykernel
# - and kill individual ones: kill -9 2260
# - but then they will restart automatically, instead use taskline-Kernels-Shut down all Kernels! Works only 1 kernel left