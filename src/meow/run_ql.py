
import os
from meow import util
from meow import quickLook as ql
from importlib import reload
reload(ql)


filetype = '*_cal.fits'
apcorr_file = '/Users/stevekb1/Documents/Analyses/JWST/WD/aperture_correction_tab3.csv'


target_name = 'GD-140'
meow_dir = '/Users/stevekb1/Documents/data/JWST/WD/GD-140/MEOW-2024-07/'
dirname = os.path.join(meow_dir, target_name)
model_file = os.path.join(dirname, '1134+300.txt')
save_file = os.path.join(dirname, f'{target_name}_Flux.png')

tables = ql.read_tables(dirname)
data = ql.read_fits(dirname, tables, apcorr_file)
ql.plot_wd_flux(data, model_file, save_file, title=target_name)


target_name = 'CPD-69-177'
meow_dir = '/Users/stevekb1/Documents/data/JWST/WD/MEOW-2024-07/'
dirname = os.path.join(meow_dir, target_name)
model_file = os.path.join(dirname, '0310-688.txt')
save_file = os.path.join(dirname, f'{target_name}_Flux.png')

tables = ql.read_tables(dirname)
data = ql.read_fits(dirname, tables, apcorr_file)
ql.plot_wd_flux(data, model_file, save_file, title=target_name)


# Get unique list of target names and filters
# target_list, filter_list = util.getTargetInfo(meow_dir, filetype)

# for target_name in target_list:
#     for filter in filter_list:
#         inputdir = os.path.join(meow_dir, target_name, filter)

