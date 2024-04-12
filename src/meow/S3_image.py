import numpy as np
import matplotlib.pyplot as plt
import glob
import sort_nicely as sn

# import jwst pipeline modules
from jwst.pipeline import Image3Pipeline # pipeline modules
from jwst.associations.lib.rules_level3_base import DMS_Level3_Base
from jwst.associations import asn_from_list

# import MEOW modules
from meow.util import makedirectory

def call(inputdir, outputdir, target_name, filter, **kwargs):
    """Subtract sky background from CAL FITS files

    Parameters
    ----------
    inputdir : str
        Input directory where _skysub_cal files are loaded
    outputdir : str
        Output directory where _skysub_cal files are saved
    target_name : str
        Name of observed star
    filter : str
        MIRI filter name
    """
    # Create output directory if it doesn't exist
    makedirectory(outputdir)

    # Gather sky subtracted cal files
    miri_skysub_files = sn.sort_nicely(glob.glob(f'{inputdir}/*_skysub_cal.fits'))

    # use asn_from_list to create association table
    miri_asn_name = f'miri_{filter}_stage3_asn_skysub' # name of output asn file
    asn = asn_from_list.asn_from_list(miri_skysub_files, rule=DMS_Level3_Base, product_name=miri_asn_name)

    # dump association table to a .json file for use in image3
    miri_asn_file = f'{outputdir}/{miri_asn_name}.json'
    # miri_asn_file = f'{miri_asn_name}.json'
    with open(miri_asn_file, 'w') as outfile:
        outfile.write(asn.dump()[1])


    # Run calwebb_image3 (or Image3Pipeline) on sky subtracted data using association table.
    cfg = dict() 
    #cfg['tweakreg'] = {}
    #cfg['tweakreg']['abs_refcat'] = 'GAIADR2'
    #cfg['skymatch'] = {'skip' : True} 
    cfg['resample']={}  # set up empty dictionary for multiple parameters to be set per step
    cfg['resample']['rotation'] = None
    cfg['resample']['kernel'] = 'gaussian'
    cfg['outlier_detection'] = {'save_intermediate_results' : True}  # Can set single parameters with this syntax
                        
    output = Image3Pipeline.call(miri_asn_file, steps=cfg, save_results=True)

    return