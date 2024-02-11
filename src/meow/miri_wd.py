#
# Astropy tools
#
from astropy.coordinates import match_coordinates_sky, SkyCoord
from astropy.io import fits, ascii
from astropy.stats import SigmaClip, sigma_clipped_stats
from astropy.table import Table, Column, vstack
import astropy.units as u
from astropy.visualization import LogStretch, LinearStretch, PercentileInterval, ManualInterval
from astropy.nddata import Cutout2D
#
# Numpy library
#
import numpy as np
#
# Photutils library and tools
#
import photutils
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
from photutils import Background2D, MedianBackground, ModeEstimatorBackground, MMMBackground

# # Mask all nan or inf pixels
# mask = np.full(np.shape(img_F560W.data), False, dtype=bool)
# mask[np.isnan(img_F560W.data)] = True
# mask[~np.isfinite(img_F560W.data)] = True

# sigma_clip = SigmaClip(sigma=3.0, maxiters=10)
# # This is the background estimator -> DAOPHOT MMM algorithm - "mode" = 3*median - 2*mean
# mmm_bkg = MMMBackground()
# # Compute sky background
# sky_F560W = Background2D(img_F560W.data, box_size=(20, 20), filter_size=(30, 30), 
#                          sigma_clip=sigma_clip, bkg_estimator=mmm_bkg, coverage_mask=mask, fill_value=0.0)

# print(r'Median background: {0}'.format(sky_F560W.background_median))
# print(r'RMS background: {0}'.format(sky_F560W.background_rms_median))

# img_F560W_skysub = img_F560W.data - sky_F560W.background

# # 5 times the background rms
# threshold_F560W = 5.0*sky_F560W.background_rms_median

# # Filter-dependent FWHM from the PSF
# fwhm_F560W = filter_fwhm.get(img_F560W.meta.instrument.filter)

# # Create DAOStarFinder instance
# dsf_F560W = photutils.DAOStarFinder(threshold=threshold_F560W, fwhm=fwhm_F560W, exclude_border=True)

# # Run DAOStarFinder on the subtracted image and save the output in a table
# xy_F560W_tmp = dsf_F560W(img_F560W_skysub)

# # Print 10 lines of the table
# # xy_F560W_tmp.pprint_all(max_lines=10)

# # Define the positions
# positions_F560W = np.stack((xy_F560W_tmp['xcentroid'], xy_F560W_tmp['ycentroid']), axis=-1)

# # Retrieve the aperture radii based on the FWHM of the F560W-filter PSF
# # r0 = filter_fwhm.get(img_F560W.meta.instrument.filter)
# # r1 = filter_fwhm.get(img_F560W.meta.instrument.filter)*2.0
# # r2 = filter_fwhm.get(img_F560W.meta.instrument.filter)*3.0
# # aper_radii = [r0, r1, r2]

# # print(r'Aperture radii used:')
# # print(r' r0 = {0:.3f} MIRIM pixel'.format(r0))
# # print(r' r1 = {0:.3f} MIRIM pixel'.format(r1))
# # print(r' r2 = {0:.3f} MIRIM pixel'.format(r2))
# # print('')

# # Define the circular apertures
# circular_apertures = [CircularAperture(positions_F560W, r=r) for r in aper_radii]

# # Run the aperture photometry
# phot_F560W_tmp = aperture_photometry(img_F560W.data*img_F560W.area, circular_apertures, method='exact')

# # Print 10 lines
# # phot_F560W_tmp.pprint_all(max_lines=10)

# # Define the annulus aperture
# annulus_aperture = CircularAnnulus(positions_F560W, r_in=25.0, r_out=35.0)

# # Aperture photometry with r0
# phot_F560W['local_sky_r0'] = local_sky_median_F560W*circular_apertures[0].area
# phot_F560W['aperture_r0_skysub'] = phot_F560W_tmp['aperture_sum_0'] - phot_F560W['local_sky_r0']


