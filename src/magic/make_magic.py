
import os
from magic import S2_sky, S3_image, S4_trends, util
# from importlib import reload
# reload(S3_image)


mast_dir = '/Users/stevekb1/Documents/data/JWST/WD/MAST'
jwst_dir = '/Users/stevekb1/Documents/data/JWST/WD/JWST-S2'
magic_dir = '/Users/stevekb1/Documents/data/JWST/WD/Magic-2024-07'
filetype = '*_cal.fits'

# Move downloaded files from MAST dir to JWST dir
# files = util.sortMAST(mast_dir, jwst_dir, filetype)

# Get unique list of target names and filters
target_list, filter_list = util.getTargetInfo(jwst_dir, filetype)

# Run Magic Stage 2 (sky BG subtractiong) on all targets and filters
for target_name in target_list:
    for filter in filter_list:
        inputdir = os.path.join(jwst_dir, target_name, filter)
        outputdir_S2 = os.path.join(magic_dir, target_name, filter)
        if os.path.exists(inputdir):
            print(f"Processing target {target_name}, filter {filter}")
            S2_sky.call(inputdir, outputdir_S2, target_name, filter)

# Run Magic Stage 3 (JWST Stage 3 wrapper) on all targets and filters
for target_name in target_list:
    for filter in filter_list:
        outputdir_S3 = os.path.join(magic_dir, target_name, filter)
        if os.path.exists(outputdir_S3):
            print(f"Processing target {target_name}, filter {filter}")
            S3_image.call(outputdir_S3, target_name, filter)

# Run Magic Stage 4 (trends) on all targets and filters
apcorr_file = '/Users/stevekb1/Documents/Analyses/JWST/WD/aperture_correction_tab3.csv'
filters = ['F770W', 'F1800W', 'F2100W']
S4_trends.call(magic_dir, filters, target_list, apcorr_file)






"""
Resources:
https://github.com/spacetelescope/jwebbinar_prep/blob/webbinar6/pointsource_imaging/MIRI_Aperture_Photometry_solution.ipynb
https://photutils.readthedocs.io/en/stable/api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder
https://github.com/STScI-MIRI/Imaging_ExampleNB/blob/main/Pipeline_demo_subtract_imager_background.ipynb
"""



