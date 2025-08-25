import numpy as np
import os

# import Magic modules
from magic import quickLook as ql


def call(magic_dir, filters, target_list, apcorr_file, **kwargs):
    """Plot trends for all targets in directory using given filters.

    Parameters
    ----------
    dirname : str
        Root directory with a list of subdirectories, one for each target.
        JWST Stage 3 files should be located somewhere within these subdirectories.
    """
    pl_colors = []
    slopes = []
    for target_name in target_list:
        print(f"Processing target {target_name}")
        dirname = os.path.join(magic_dir, target_name)
        tables = ql.read_tables(dirname)
        data = ql.read_fits(dirname, tables, apcorr_file)
        # pl_color = determineColors(data, filters)
        pl_color, slope = determineColors2(data, filters)
        pl_colors.append(pl_color)
        slopes.append(slope)

    pl_colors = np.transpose(np.array(pl_colors), (0, 2, 1))
    slopes = np.array(slopes)



def determineColors(data, filters):
    """

    """
    # Make sure there are exactly 3 filters
    if len(filters) != 3:
        print("Exactly three filters are required.")
        print(f"Filters given: {filters}")
        return None

    # Select and sort the filters into the correct order
    f1, f2, f3 = filters
    w1 = float(f1.strip('F').strip('W'))/100
    w2 = float(f2.strip('F').strip('W'))/100
    w3 = float(f3.strip('F').strip('W'))/100
    foo = data.sel(wavelength=[w1,w2,w3])

    # Compute color pairs [x, y] for different aperture sizes
    color_30 = (foo.aper30_flux[[0,2]] - foo.aper30_flux[1])/foo.aper30_flux[1]
    color_50 = (foo.aper50_flux[[0,2]] - foo.aper50_flux[1])/foo.aper50_flux[1]
    color_70 = (foo.aper70_flux[[0,2]] - foo.aper70_flux[1])/foo.aper70_flux[1]
    color_100 = (foo.aper100_flux[[0,2]] - foo.aper100_flux[1])/foo.aper100_flux[1]

    pl_color = np.array([color_30.values, color_50.values,
                       color_70.values, color_100.values])
    return pl_color


def determineColors2(data, filters):
    """

    """
    # Make sure there are exactly 3 filters
    if len(filters) != 3:
        print("Exactly three filters are required.")
        print(f"Filters given: {filters}")
        return None

    # Select and sort the filters into the correct order
    f1, f2, f3 = filters
    w1 = float(f1.strip('F').strip('W'))/100
    w2 = float(f2.strip('F').strip('W'))/100
    w3 = float(f3.strip('F').strip('W'))/100
    foo = data.sel(wavelength=[w1,w2,w3])

    # Compute color pairs [x, y] for different aperture sizes
    color_30 = (foo.aper30_flux[[0,2]] - foo.aper30_flux[1])/foo.aper30_flux[1]
    color_50 = (foo.aper50_flux[[0,2]] - foo.aper50_flux[1])/foo.aper50_flux[1]
    color_70 = (foo.aper70_flux[[0,2]] - foo.aper70_flux[1])/foo.aper70_flux[1]
    color_100 = (foo.aper100_flux[[0,2]] - foo.aper100_flux[1])/foo.aper100_flux[1]

    pl_color = np.array([color_30.values, color_50.values,
                        color_70.values, color_100.values])


    log_flux = np.log(foo.aper100_flux)
    log_wave = np.log10((w1, w2, w3))
    slope1 = (log_flux[0]-log_flux[1])/(log_wave[0]-log_wave[1])
    slope2 = (log_flux[2]-log_flux[1])/(log_wave[2]-log_wave[1])
    slope = np.array([slope1.values, slope2.values])

    return pl_color, slope