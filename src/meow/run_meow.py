

import meow_ql as ql
from importlib import reload
reload(ql)

data_dir = '/Users/stevekb1/Documents/data/JWST/WD'
analysis_dir = '/Users/stevekb1/Documents/Analyses/JWST/WD'
apcorr_file = f'{analysis_dir}/aperture_correction_tab3.csv'

target_name = 'CPD-69-177'
dirname = f'{data_dir}/{target_name}/JWST-S3/'
model_file = f'{analysis_dir}/{target_name}/0310-688.txt'
save_file = f'{analysis_dir}/{target_name}/{target_name}_Flux.png'
tables = ql.read_tables(dirname)
data = ql.read_fits(dirname, tables, apcorr_file)
ql.plot_wd_flux(data, model_file, save_file, title=target_name)

target_name = 'WD1748'
dirname = f'{data_dir}/{target_name}/JWST-S3/'
model_file = f'{analysis_dir}/{target_name}/1748+708.txt'
save_file = f'{analysis_dir}/{target_name}/{target_name}_Flux.png'
tables = ql.read_tables(dirname)
data = ql.read_fits(dirname, tables, apcorr_file)
ql.plot_wd_flux(data, model_file, save_file, title=target_name)

target_name = 'WD2151'
dirname = f'{data_dir}/{target_name}/JWST-S3/'
model_file = f'{analysis_dir}/{target_name}/J2151+5917.txt'
save_file = f'{analysis_dir}/{target_name}/{target_name}_Flux.png'
tables = ql.read_tables(dirname)
data = ql.read_fits(dirname, tables, apcorr_file)
ql.plot_wd_flux(data, model_file, save_file, title=target_name)

"""
ToDO
    Look at tutorial for subtracting BG in Stage 2 outputs
    Implement similar version and rerun Stage 3
"""


"""
https://github.com/spacetelescope/jwebbinar_prep/blob/webbinar6/pointsource_imaging/MIRI_Aperture_Photometry_solution.ipynb
https://photutils.readthedocs.io/en/stable/api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder
https://github.com/STScI-MIRI/Imaging_ExampleNB/blob/main/Pipeline_demo_subtract_imager_background.ipynb
"""
# dirname = os.path.join(rootdir, target_name, 'JWST-S3/')

# print(tables[0].keys())
"""
['label', 'xcentroid', 'ycentroid', 'sky_centroid', 'aper_bkg_flux', 'aper_bkg_flux_err', 'aper30_flux', 'aper30_flux_err', 'aper50_flux', 'aper50_flux_err', 'aper70_flux', 'aper70_flux_err', 'aper_total_flux', 'aper_total_flux_err', 'aper30_abmag', 'aper30_abmag_err', 'aper50_abmag', 'aper50_abmag_err', 'aper70_abmag', 'aper70_abmag_err', 'aper_total_abmag', 'aper_total_abmag_err', 'aper30_vegamag', 'aper30_vegamag_err', 'aper50_vegamag', 'aper50_vegamag_err', 'aper70_vegamag', 'aper70_vegamag_err', 'aper_total_vegamag', 'aper_total_vegamag_err', 'CI_50_30', 'CI_70_50', 'CI_70_30', 'is_extended', 'sharpness', 'roundness', 'nn_label', 'nn_dist', 'isophotal_flux', 'isophotal_flux_err', 'isophotal_abmag', 'isophotal_abmag_err', 'isophotal_vegamag', 'isophotal_vegamag_err', 'isophotal_area', 'semimajor_sigma', 'semiminor_sigma', 'ellipticity', 'orientation', 'sky_orientation', 'sky_bbox_ll', 'sky_bbox_ul', 'sky_bbox_lr', 'sky_bbox_ur']
"""

# data_f770 = xrio.makeDataset()
# file_fits = '/Users/stevekb1/Documents/data/JWST/WD/CPD-69-177/S3-JWST/F770W/jw04403-o016_t016_miri_f770w_i2d.fits'
# data_f770 = ql.read_fits(file_fits, data_f770)
# data_f770 = ql.get_wd_flux(data_f770, table_f770)

# data_f1800 = xrio.makeDataset()
# file_fits = '/Users/stevekb1/Documents/data/JWST/WD/CPD-69-177/S3-JWST/F1800W/jw04403-o016_t016_miri_f1800w_i2d.fits'
# data_f1800 = ql.read_fits(file_fits, data_f1800)
# data_f1800 = ql.get_wd_flux(data_f1800, table_f1800)

# data_f2100 = xrio.makeDataset()
# file_fits = '/Users/stevekb1/Documents/data/JWST/WD/CPD-69-177/S3-JWST/F2100W/jw04403-o016_t016_miri_f2100w_i2d.fits'
# data_f2100 = ql.read_fits(file_fits, data_f2100)
# data_f2100 = ql.get_wd_flux(data_f2100, table_f2100)

# batch = [data_f770, data_f1800, data_f2100]
# data = xrio.concat(batch, dim='wavelength')

