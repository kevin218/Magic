import glob, os
from astropy.io import ascii

# import jwst pipeline modules
from jwst.pipeline import Image3Pipeline # pipeline modules
from jwst import datamodels
from jwst.associations.lib.rules_level3_base import DMS_Level3_Base
from jwst.associations import asn_from_list

# import Magic modules
from magic.plots import show_image, overlay_catalog
import magic.sort_nicely as sn

def call(outputdir, target_name, filter, **kwargs):
    """Run JWST Stage 3 pipeline and plot results.

    Parameters
    ----------
    outputdir : str
        Input/output directory where _skysub_cal files are loaded
    target_name : str
        Name of observed star
    filter : str
        MIRI filter name
    """
    # Change directory to location of files because the JWST pipeline
    # only outputs results into the current working directory
    cwd = os.getcwd()
    os.chdir(outputdir)

    # Gather sky subtracted cal files
    miri_skysub_files = sn.sort_nicely(
        glob.glob(f'{outputdir}/*_skysub_cal.fits'))

    # Ase asn_from_list to create association table
    miri_asn_name = f'{outputdir}/miri_{filter}_stage3_asn_skysub'
    asn = asn_from_list.asn_from_list(miri_skysub_files,
                                      rule=DMS_Level3_Base,
                                      product_name=miri_asn_name)

    # Dump association table to a .json file for use in image3
    miri_asn_file = f'{miri_asn_name}.json'
    with open(miri_asn_file, 'w') as outfile:
        outfile.write(asn.dump()[1])

    # Run calwebb_image3 (or Image3Pipeline) on sky subtracted data
    # using association table
    cfg = dict()
    #cfg['tweakreg'] = {}
    #cfg['tweakreg']['abs_refcat'] = 'GAIADR2'
    #cfg['skymatch'] = {'skip' : True}
    cfg['resample']={}
    cfg['resample']['rotation'] = None
    cfg['resample']['kernel'] = 'gaussian'
    cfg['outlier_detection'] = {'save_intermediate_results' : False}
    output = Image3Pipeline.call(miri_asn_file, steps=cfg, save_results=True)

    # Look at the resulting mosaic image
    miri_mosaic_file =  miri_asn_name + '_i2d.fits'
    miri_mosaic = datamodels.open(miri_mosaic_file)
    vmin, vmax = [0,10]
    dmap = "afmhot"
    flux_limit = 5e-7
    title = f"Mosaic Image - {target_name} - {filter}"
    savename = f"{outputdir}/figs/Fig301_{target_name}_{filter}_Mosaic.png"
    show_image(miri_mosaic.data, vmin=vmin, vmax=vmax, dmap=dmap,
               title=title, units="MJy/str", savename=savename, fignum=301)

    # Look at mosaic data and sources found with source_catalog
    miri_catalog_file = miri_asn_name + '_cat.ecsv'
    # Read in the source catalog
    miri_source_cat = ascii.read(miri_catalog_file)
    # Show the catalog sources on the mosaic
    title = f"Mosaic With Source Catalog - {target_name} - {filter}"
    savename = f"{outputdir}/figs/Fig302_{target_name}_{filter}_SourceCatalog.png"
    overlay_catalog(miri_mosaic.data, miri_source_cat,
                    flux_limit=flux_limit, vmin=vmin, vmax=vmax,
                    title=title, dmap="Greys", savename=savename)

    # Change directory back
    os.chdir(cwd)
    return