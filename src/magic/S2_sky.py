import numpy as np
import matplotlib.pyplot as plt
import glob, os
import sort_nicely as sn

# import jwst pipeline modules
# import jwst
# from jwst.pipeline import Detector1Pipeline, Image2Pipeline, Image3Pipeline # pipeline modules
from jwst import datamodels
from jwst.datamodels import ImageModel, dqflags # Data models and dq values

# import astropy modules
from astropy.visualization import ImageNormalize, ManualInterval, SqrtStretch
from astropy.stats import sigma_clipped_stats
from astropy.io import fits

# import Magic modules
from magic.util import makedirectory
from magic.plots import before_after, show_image

def call(inputdir, outputdir, target_name, filter,
         filetype='*_cal.fits', **kwargs):
    """Subtract sky background from CAL FITS files

    Parameters
    ----------
    inputdir : str
        Input directory where _cal files are loaded
    outputdir : str
        Output directory where _skysub_cal files are saved
    target_name : str
        Name of observed star
    filter : str
        MIRI filter name
    """
    # Create output directory if it doesn't exist
    makedirectory(outputdir)

    # Use the script make_sky to make and subtract off the sky background image.
    skyflat_mean, skyflat_std = make_sky(inputdir, outputdir, **kwargs)

    # Look at cal image before and after sky subtraction
    miri_cal_files = sn.sort_nicely(glob.glob(os.path.join(inputdir, filetype)))
    im1 = ImageModel(miri_cal_files[0])
    vmax1 = np.nanmedian(im1.data)+3*np.nanstd(im1.data)
    miri_skysub_files = sn.sort_nicely(glob.glob(
                                       os.path.join(outputdir,
                                                    '*_skysub_cal.fits')))
    im2 = ImageModel(miri_skysub_files[0])
    vmax2 = np.nanmedian(im2.data)+3*np.nanstd(im2.data)
    title1 = f"Original Image - {target_name} - {filter}"
    title2 = f"Sky-Subtracted Image - {target_name} - {filter}"
    savename = f"{outputdir}/figs/Fig251_{target_name}_{filter}_BeforeAfter.png"
    before_after(im1.data, im2.data, vmax1, vmax2, title1, title2,
                 savename=savename)

    # Look at the created median sky image and write to a file
    drange_cal = [0., vmax1]
    dmap = "afmhot"
    title = f'Median Sky Image - {target_name} - {filter}'
    savename = (f"{outputdir}/figs/Fig252_{target_name}_{filter}_MedianSky.png")
    show_image(skyflat_mean, drange_cal[0], drange_cal[1], dmap=dmap,
               title=title, savename=savename)
    fits.writeto(f'{outputdir}/{filter}_sky.fits', skyflat_mean, overwrite=True)

    return


def make_sky(
    inputdir, outputdir,
    subfiles=None,
    scalebkg=True,
    exclude_sigma=None,
    exclude_delta=None,
    ds9regions=None,
    filetype='*_cal.fits'):
    """
    Make sky background by sigma clipping in image coordinates and subtract it
    from all the input files.

    Parameters
    ----------
    inputdir : str
        Input directory where _cal files are loaded
    outputdir : str
        Output directory where _skysub_cal files are saved
    subfiles : str
        Array of files to subtract sky from. If None, sky will be subracted from all input images. [default=None]
    scalebkg : boolean
        Scale each image by its median to the average value [default=True]
    exclude_sigma : float
        Exclude data above the median bkg + this sigma value from the sky creation
    exclude_delta : float
        Exclude data above the median bkg + this value from sky creation
    ds9regions : ds9 region file
        Exclude pixels inside ds9 regions from sky creation
    """

    files = glob.glob(os.path.join(inputdir, filetype))
    if len(files) == 0:
        print("No files found.")
        return None, None
    # if ds9regions is not None:
    #     ereg = Regions.read(ds9regions, format="ds9")
        # for creg in ereg:
        #     creg.radius *= 0.5

    istack = None
    for k, cfile in enumerate(files):
        print(f"processing {cfile}")
        cdata = datamodels.open(cfile)
        if istack is None:
            isize = cdata.data.shape
            istack = np.empty((isize[0], isize[1], len(files)))
            istackmed = np.empty((len(files)))
        tdata = cdata.data

        # remove all the non imager data
        # bdata = cdata.dq & dqflags.pixel["DO_NOT_USE"] > 0
        # tdata[bdata] = np.NaN

        # if ds9regions is not None:
        #     fits_header, fits_hdulist = cdata.meta.wcs.to_fits()
        #     cwcs = WCS(fits_header)  # <-- "astropy" wcs

        #     pixx = np.arange(isize[1])
        #     pixy = np.arange(isize[0])
        #     imagex, imagey = np.meshgrid(pixx, pixy)
        #     imagera, imagedec = cwcs.wcs_pix2world(imagex, imagey, 0)
        #     # imagera, imagedec = cwcs.pixel_to_world(imagex, imagey, 0)
        #     skycoord = SkyCoord(imagera, imagedec, unit="deg")
        #     for creg in ereg:
        #         inoutimage = creg.contains(skycoord, cwcs)
        #         tdata[inoutimage] = np.NaN
        #     cdata.data = tdata
        #     cdata.write(cfile.replace("cal.fits", "cal_mask.fits"))
        #     # fits.writeto("test.fits", inoutimage * 1., overwrite=True)

        tdata_median = np.nanmedian(tdata)
        if exclude_sigma is not None:
            flux_limit = tdata_median + exclude_sigma*np.nanstd(tdata)
            tdata[tdata > flux_limit] = np.NaN
            print(f"  Excluding data above {flux_limit} counts.")

        if exclude_delta is not None:
            flux_limit = tdata_median + exclude_delta
            tdata[tdata > flux_limit] = np.NaN
            print(f"  Excluding data above {flux_limit} counts.")

        istackmed[k] = np.nanmedian(tdata)
        print(f"  Median sky = {istackmed[k]} counts")

        istack[:, :, k] = tdata

    # adjust the levels to the median
    # allows for data taken at different times with different backgrounds
    ##############################################
    #medsky = np.mean(istackmed)  ########### This is where the combination can be changed between mean or median
    medsky = np.median(istackmed)
    ##############################################

    if scalebkg:
        print("Scaling individual images to median bkg")
        for k in range(len(files)):
            istack[:, :, k] += medsky - istackmed[k]
            print("  ", k, np.nanmedian(istack[:, :, k]))
    else:
        print("Not scaling individual images to median bkg")

    skyflat_mean, skyflat_median, skyflat_std = sigma_clipped_stats(
        istack, sigma_lower=3, sigma_upper=1, axis=2)

    # subtract the sky properly adjusted from the data
    print("Subtracting mean skyflat from data")
    if subfiles is None:
        subfiles = files
    for k, cfile in enumerate(subfiles):
        cdata = datamodels.open(cfile)
        cdata.data -= skyflat_mean
        if scalebkg:
            print("  ", k, medsky - istackmed[k])
            cdata.data += medsky - istackmed[k]
        else:
            print("  ", k)
        ndata = np.isnan(cdata.data)
        #cdata.data[ndata] = 0.0  # This sets all NaNs to 0
        cdata.dq[ndata] = cdata.dq[ndata] & dqflags.pixel["DO_NOT_USE"]
        cfile = cfile.replace(inputdir, outputdir)
        cdata.write(cfile.replace("_cal.fits", "_skysub_cal.fits"))

    return skyflat_mean, skyflat_std

