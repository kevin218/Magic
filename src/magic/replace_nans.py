
import numpy as np
# from astropy.io import fits
from jwst import datamodels
from scipy.ndimage import label, center_of_mass
from photutils.psf import PSFPhotometry, IntegratedGaussianPRF
from astropy.modeling.fitting import LevMarLSQFitter

def saturated_stars(input_file, output_file, ext=1, method='gaussian'):
    # Load the data (JWST SCI extension is usually 1)
    # with fits.open(input_file) as hdul:
    #    data = hdul[ext].data.copy()
    with datamodels.open(input_file) as model:
        data = model.data.copy()

        # Find large connected regions of NaNs (saturated cores)
        nan_mask = np.isnan(data)
        labeled_array, num_features = label(nan_mask)
        print(f"Found {num_features} saturated regions to potentially fix.")

        # Iterate through each saturated region
        max_data = np.nanmax(data)
        num_fixed = 0
        for i in range(1, num_features + 1):
            region_mask = (labeled_array == i)
            pixel_count = np.sum(region_mask)
            if pixel_count < 10 or pixel_count > 10000:
                # Skip very small or very large regions that are unlikely to be saturated stars
                continue

            print(f"Processing saturated region {i} with {pixel_count} pixels")
            num_fixed += 1

            if method == 'gaussian':
                data = fit_gaussian(data, region_mask, pixel_count)
            elif method == 'max':
                # Simple max replacement (not recommended for large regions)
                data[region_mask] = max_data

            model.err[region_mask] = max_data
            model.dq[region_mask] = 0

            # plt.figure(1)
            # plt.imshow(sub_data, origin='lower')
            # plt.title(f"Model for region {i}")

            # plt.figure(2)
            # plt.imshow(model_vals, origin='lower')
            # plt.title(f"Model for region {i}")

        # Save fixed file
        # hdul[ext].data = data
        # hdul.writeto(output_file, overwrite=True)
        model.data = data
        model.save(output_file, overwrite=True)
        # fits.writeto(output_file, data, header, overwrite=True)
        print(f"Fixed {num_fixed} regions. Saved to {output_file}")


    def fit_gaussian(data, region_mask, pixel_count):
        # Initialize PSF Model (Using a Gaussian as a proxy for JWST's PSF)
        # For higher precision, could use webbpsf.GriddedPSFModel
        fitter = LevMarLSQFitter()

        # Get centroid of the saturated region
        yc, xc = center_of_mass(region_mask)

        # Define a fitting window around the saturation
        hw = np.sqrt(pixel_count) + 10
        y0, y1 = max(0, int(yc - hw)), min(data.shape[0], int(yc + hw))
        x0, x1 = max(0, int(xc - hw)), min(data.shape[1], int(xc + hw))
        sub_data = np.copy(data[y0:y1, x0:x1])
        bg = np.nanmin(sub_data)
        sub_data -= bg  # Background subtraction for better fitting

        # Fit PSF to the non-NaN pixels in this window
        fit_mask = ~np.isnan(sub_data)
        yy, xx = np.mgrid[y0:y1, x0:x1]

        # Initial guess based on surrounding flux
        psf_model = IntegratedGaussianPRF(sigma=np.sqrt(pixel_count),
                                          flux = np.nansum(sub_data)*10,
                                          x_0 = xc, y_0 = yc)

        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore")
        best_fit = fitter(psf_model, xx[fit_mask], yy[fit_mask], sub_data[fit_mask])

        # 5. Replace NaNs with the fitted model values
        model_vals = best_fit(xx, yy)
        # sub_data[region_mask[y0:y1, x0:x1]] = model_vals[region_mask[y0:y1, x0:x1]]
        data[y0:y1, x0:x1][region_mask[y0:y1, x0:x1]] = model_vals[region_mask[y0:y1, x0:x1]]

        return data
