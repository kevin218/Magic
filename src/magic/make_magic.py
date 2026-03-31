
import os
from magic import S2_sky, S3_image, S4_trends, util

"""
Resources:
https://github.com/spacetelescope/jwebbinar_prep/blob/webbinar6/pointsource_imaging/MIRI_Aperture_Photometry_solution.ipynb
https://photutils.readthedocs.io/en/stable/api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder
https://github.com/STScI-MIRI/Imaging_ExampleNB/blob/main/Pipeline_demo_subtract_imager_background.ipynb
"""

# Location of files downloaded from MAST
mast_dir = '/Users/stevekb1/Documents/data/JWST/WD/MAST'
# Location of files after sorting by target and filter
jwst_dir = '/Users/stevekb1/Documents/data/JWST/WD/JWST-S2'
# Output location when making Magic
magic_dir = '/Users/stevekb1/Documents/data/JWST/WD/Magic-2024-07'
# Stage 2 file type (should normally be *_cal.fits)
filetype = '*_cal.fits'

# Move and sort downloaded files from MAST dir to JWST dir
# Comment out this line if reprocessing data that has already been sorted
files = util.sortMAST(mast_dir, jwst_dir, filetype)

# Get unique list of target names and filters
# Target names include the observation number for unique identification
target_list, filter_list = util.getTargetInfo(jwst_dir, filetype)

# Run Magic Stage 2 (sky BG subtraction) on all targets and filters
S2_sky.batch_call(jwst_dir, magic_dir, target_list, filter_list)

# Run Magic Stage 3 (JWST Stage 3 wrapper) on all targets and filters
S3_image.batch_call(magic_dir, target_list, filter_list)

# Run Magic Stage 4 (trends) on all targets and filters
# This code is experimental and not necessary for the standard workflow
# apcorr_file = './aperture_correction_tab3.csv'
# filters = ['F770W', 'F1800W', 'F2100W']
# S4_trends.call(magic_dir, filters, target_list, apcorr_file)








