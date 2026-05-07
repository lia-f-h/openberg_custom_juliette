import logging
from math import ceil
from datetime import datetime, timedelta, timezone

from opendrift.models.openberg import OpenBerg
from opendrift.readers.reader_netCDF_CF_generic import Reader
import copernicusmarine


def load_and_run(lon,lat,
    time=datetime.now(timezone.utc),
    config=None,
    radius=1000, #in meters
    number=100, #number of seeds
    steps=12, 
    max_speed = 3.0, #Adjust max speed for data lookup approximation (10 m.s-1 by default)
    lonlat_range = None, #If None then automatically computed, otherwised approximated withmax_speed
    log_level=logging.INFO,
                 
):


    configs={'glo':{'cur':{'service':'arco-geo-series','ref':'cmems_mod_glo_phy_anfc_merged-uv_PT1H-i'}},
             'ibi':{'cur':{'service':'arco-geo-series','ref':'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m'}},
             'nws':{'cur':{'service':'arco-geo-series','ref':'cmems_mod_nws_phy_anfc_0.027deg-2D_PT1H-m'}},
             'arc':{'cur':{'service':'tds','ref':'https://thredds.met.no/thredds/dodsC/cmems/topaz6/dataset-topaz6-arc-15min-3km-be.ncml'}},
            }

    if config is None: config=configs['glo']
    else:
        try: config=configs[config]
        except KeyError: raise ValueError("KeyError: this configuration ({}) does not exist. Existing keys are : {}".format(config,','.join(configs.keys())) )
    
    #Get radius range
    if lonlat_range is None : lonlat_range = ceil((( (steps * max_speed * 3600.) / 110000. ) + (radius/(2.*110000.) ))*100.)/100.

#    copernicusmarine.logging.getLogger().setLevel(loglevel)
    o = OpenBerg(loglevel=log_level)

#    o.set_config('general:seafloor_action', 'none')

    for i,var in config.items():

        if var['service'].startswith('arco'):
     
            ds= copernicusmarine.open_dataset(
                dataset_id = var['ref'],
                minimum_longitude = lon-lonlat_range,
                maximum_longitude = lon+lonlat_range,
                minimum_latitude = lat-lonlat_range,
                maximum_latitude = lat+lonlat_range,
                service = var['service'])
            
            o.add_reader(Reader(ds))
            
        elif var['service'].startswith('tds'):
            o.add_readers_from_list([var['ref']])
        else : raise ValueError("Reader service type not defined")
        
    
    o.seed_elements(lon=lon, lat=lat, radius=radius, number=number,
                    time=time, sail=10,draft=50,length=90,width=40)
    o.run(steps=steps, stop_on_error=True)
    return(o)

