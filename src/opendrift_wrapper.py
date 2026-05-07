from src.utils import *
from math import ceil

from opendrift.models.oceandrift import OceanDrift


def load_and_run(lon,lat,
    time=datetime.now(timezone.utc).replace(tzinfo=None),
    config=None,
    radius=1000, #in meters
    number=100, #number of seeds
    steps=12, 
    max_speed = 3.0, #Adjust max speed for data lookup approximation (10 m.s-1 by default)
    lonlat_range = None, #If None then automatically computed, otherwised approximated withmax_speed
    loglevel=logging.INFO,
                 
):


    configs={'glo':{'cur':{'service':'arco-geo-series','ref':'cmems_mod_glo_phy_anfc_merged-uv_PT1H-i'},
                     'wav':{'service':'arco-geo-series','ref':'cmems_mod_glo_wav_anfc_0.083deg_PT3H-i'},
                     },
             'ibi':{'cur':{'service':'arco-geo-series','ref':'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m'},
                     'wav':{'service':'arco-geo-series','ref':'cmems_mod_ibi_wav_anfc_0.05deg_PT1H-i'},
                    },
             'nws':{'cur':{'service':'arco-geo-series','ref':'cmems_mod_nws_phy_anfc_0.027deg-2D_PT1H-m'},
                     'wav':{'service':'arco-geo-series','ref':'cmems_mod_nws_wav_anfc_0.05deg_PT1H-i'},
                    },
             'arc':{'cur':{'service':'tds','ref':'https://thredds.met.no/thredds/dodsC/cmems/topaz6/dataset-topaz6-arc-15min-3km-be.ncml'},
                    'wav':{'service':'tds','ref':'https://thredds.met.no/thredds/dodsC/cmems/mywavewam3km/dataset-wam-arctic-1hr3km-be.ncml'},
                    },
            }

    if config is None: config=configs['glo12']
    else:
        try: config=configs[config]
        except KeyError: raise Exception("KeyError: this configuration ({}) does not exist. Existing keys are : {}".format(config,','.join(configs.keys())) )
    
    #Get radius range
    if lonlat_range is None : lonlat_range = ceil((( (steps * max_speed * 3600.) / 110000. ) + (radius/(2.*110000.) ))*100.)/100.

    logging.getLogger('copernicusmarine').setLevel(loglevel)
    o = OceanDrift(loglevel=loglevel)

    for i,var in config.items():

        if var['service'].startswith('arco') or var['service'].startswith('tds'):
            o.add_readers_from_list([var['ref']])
        else : raise Exception("Reader service type not defined")
        
    
    o.seed_elements(lon=lon, lat=lat, radius=radius, number=number,
                    time=time)
    o.run(steps=steps, stop_on_error=True)
    return(o)

