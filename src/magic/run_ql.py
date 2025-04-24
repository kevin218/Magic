
import os
from magic import util
from magic import quickLook as ql
from importlib import reload
reload(ql)


filetype = '*_cal.fits'
apcorr_file = '/Users/stevekb1/Documents/Analyses/JWST/WD/aperture_correction_tab3.csv'



target_name = 'CPD-69-177'
magic_dir = '/Users/stevekb1/Documents/data/JWST/WD/Magic-2024-07/'
dirname = os.path.join(magic_dir, target_name)
model_file = os.path.join(dirname, '0310-688.txt')
save_file = os.path.join(dirname, f'{target_name}_Flux.png')

tables = ql.read_tables(dirname)
data = ql.read_fits(dirname, tables, apcorr_file)
ql.plot_wd_flux(data, model_file, save_file, title=target_name)




# Get unique list of target names and filters
# target_list, filter_list = util.getTargetInfo(magic_dir, filetype)

# for target_name in target_list:
#     for filter in filter_list:
#         inputdir = os.path.join(magic_dir, target_name, filter)

# print(tables[0].keys())
"""
['label', 'xcentroid', 'ycentroid', 'sky_centroid', 'aper_bkg_flux', 'aper_bkg_flux_err', 'aper30_flux', 'aper30_flux_err', 'aper50_flux', 'aper50_flux_err', 'aper70_flux', 'aper70_flux_err', 'aper_total_flux', 'aper_total_flux_err', 'aper30_abmag', 'aper30_abmag_err', 'aper50_abmag', 'aper50_abmag_err', 'aper70_abmag', 'aper70_abmag_err', 'aper_total_abmag', 'aper_total_abmag_err', 'aper30_vegamag', 'aper30_vegamag_err', 'aper50_vegamag', 'aper50_vegamag_err', 'aper70_vegamag', 'aper70_vegamag_err', 'aper_total_vegamag', 'aper_total_vegamag_err', 'CI_50_30', 'CI_70_50', 'CI_70_30', 'is_extended', 'sharpness', 'roundness', 'nn_label', 'nn_dist', 'isophotal_flux', 'isophotal_flux_err', 'isophotal_abmag', 'isophotal_abmag_err', 'isophotal_vegamag', 'isophotal_vegamag_err', 'isophotal_area', 'semimajor_sigma', 'semiminor_sigma', 'ellipticity', 'orientation', 'sky_orientation', 'sky_bbox_ll', 'sky_bbox_ul', 'sky_bbox_lr', 'sky_bbox_ur']
"""
