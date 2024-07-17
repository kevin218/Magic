
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits, ascii
from astropy import units as u
import astraeus.xarrayIO as xrio
from sort_nicely import sort_nicely
import pandas as pd
import glob

colors = ['xkcd:bright blue','orange','purple','xkcd:soft green','pink']
plt.rcParams['figure.constrained_layout.use'] = True


def read_tables(dirname):
    '''
    Loads all ECSV files into a list of tables.

    Parameters
    ----------
    dirname : str
        Directory or root path to ECSV files. Search is recursive.

    Returns
    -------
    tables : list
        List of QTable objects, one for each ECSV file.
    '''
    # Look for ECSV files in the given directory
    file_list = []
    for fname in glob.glob(dirname+'/**/*_cat.ecsv', recursive=True):
        file_list.append(fname)
    file_list = sort_nicely(file_list)

    tables = []
    for fname in file_list:
        tables.append(ascii.read(fname, format='ecsv'))
    return tables


def read_fits(dirname, tables, apcorr_file):
    '''
    Reads all i2d FITS file into Xarray dataset.

    Parameters
    ----------
    dirname : str
        Directory path to i2d files.
    tables : list
        List of QTable objects, one for each ECSV file.

    Returns
    -------
    data : Xarray Dataset
        The updated Dataset object with the fits data stored inside.

    '''
    # Look for ECSV files in the given directory
    file_list = []
    for fname in glob.glob(dirname+'/**/*_skysub_i2d.fits', recursive=True):
        file_list.append(fname)
    file_list = sort_nicely(file_list)

    batch = []
    for i,fname in enumerate(file_list):
        data = xrio.makeDataset()
        hdulist = fits.open(fname)
        # Load main and science headers
        data['filename'] = fname
        data.attrs['mhdr'] = hdulist[0].header
        data.attrs['shdr'] = hdulist['SCI', 1].header
        data = get_wd_flux(data, tables[i], apcorr_file)
        batch.append(data)

    # Concatenate all XArray datasets into one dataset
    data = xrio.concat(batch, dim='wavelength')

    return data


def get_wd_flux(data, table, apcorr_file):
    '''
    Determine which source is the WD and return flux (in mJy).

    Parameters
    ----------
    data : Xarray Dataset
        The Dataset object in which the fits data are stored.
    table: ECSV table
        The catalog of targets from JWST Stage 3.

    Returns
    -------
    data : Xarray Dataset
        The updated Dataset object with the fits data stored inside.

    '''
    data['filter'] = str(data.mhdr['FILTER'])
    data['subarray'] = str(data.mhdr['SUBARRAY'])
    data['wavelength'] = float(str(data.filter.values).strip('F').strip('W'))/100
    
    # Compute distance of each identified object from expected target position
    ra = data.mhdr['TARG_RA'] * u.deg
    dec = data.mhdr['TARG_DEC'] * u.deg
    distance = np.sqrt((table['sky_centroid'].ra - ra)**2 + 
                       (table['sky_centroid'].dec - dec)**2)
    # Determine index of nearest object to expected target position
    itarget = np.argsort(distance)[0]
    data['distance'] = distance[itarget].to(u.arcsec).value
    print(f"Distance from expected target position: {data['distance'].values} arcsec in {data['filter'].values}")

    # Determine aperture correction factors for filter/subarray combination
    apcorr30, apcorr50, apcorr70 = get_aper_corr(apcorr_file, data['filter'], data['subarray'])

    # Record flux and uncertainty in mJy for various aperture sizes
    data['aper30_flux'] = table['aper30_flux'][itarget]*1e3*apcorr30
    data['aper30_flux_err'] = table['aper30_flux_err'][itarget]*1e3*apcorr30
    data['aper50_flux'] = table['aper50_flux'][itarget]*1e3*apcorr50
    data['aper50_flux_err'] = table['aper50_flux_err'][itarget]*1e3*apcorr50
    data['aper70_flux'] = table['aper70_flux'][itarget]*1e3*apcorr70
    data['aper70_flux_err'] = table['aper70_flux_err'][itarget]*1e3*apcorr70
    data['aper100_flux'] = table['aper_total_flux'][itarget]*1e3
    data['aper100_flux_err'] = table['aper_total_flux_err'][itarget]*1e3

    return data


def get_aper_corr(apcorr_file, filter, subarray):
    """
    Look up aperature correction factors for given filter and subarray size.
    """
    df = pd.read_csv(apcorr_file)
    subdf = df.loc[(df['FILTER'] == filter) & (df['PUPIL'] == subarray)]
    apcorr30 = subdf.loc[subdf['EEFRACTION'] == 0.3]['APCORR'].values[0]
    apcorr50 = subdf.loc[subdf['EEFRACTION'] == 0.5]['APCORR'].values[0]
    apcorr70 = subdf.loc[subdf['EEFRACTION'] == 0.7]['APCORR'].values[0]
    return apcorr30, apcorr50, apcorr70


def plot_wd_flux(data, model_file, save_file, title=None):
    ''''
    
    Parameters
    ----------
    data : Xarray Dataset
        The Dataset object in which the fits data are stored.
    '''
    # Load model file
    model_wave, model_flux = np.genfromtxt(model_file, unpack=True)
    i5mu = np.argwhere(model_wave > 5)[0]
    ymax = model_flux[i5mu]

    # Find closest wavelength index
    iwave = np.zeros(data.wavelength.size, dtype=int)
    for ii, wave in enumerate(data.wavelength):
        iwave[ii] = np.argwhere(model_wave > wave.values)[0]
    
    # Normalize measured flux by model
    flux = np.array([data.aper30_flux, data.aper50_flux, 
                     data.aper70_flux, data.aper100_flux])
    flux_err = np.array([data.aper30_flux_err, data.aper50_flux_err, 
                         data.aper70_flux_err, data.aper100_flux_err])
    norm_flux = flux/model_flux[np.newaxis,iwave]
    norm_flux_err = flux_err/model_flux[np.newaxis,iwave]

    # Compute infrared excess in %
    planet_flux = (norm_flux-1)*100
    planet_flux_err = norm_flux_err*100

    plt.figure(1)
    plt.clf()
    # Plot absolute flux
    plt.subplot(211)
    plt.title(title, size=12)
    plt.errorbar(data.wavelength, data.aper30_flux, data.aper30_flux_err, fmt='o', 
                 color=colors[0], ms=4, zorder=3, label='Aperature 30 Flux')
    plt.errorbar(data.wavelength, data.aper50_flux, data.aper50_flux_err, fmt='o', 
                 color=colors[2], ms=4, zorder=3, label='Aperature 50 Flux')
    plt.errorbar(data.wavelength, data.aper70_flux, data.aper70_flux_err, fmt='o', 
                 color=colors[3], ms=4, zorder=3, label='Aperature 70 Flux')
    plt.errorbar(data.wavelength, data.aper100_flux, data.aper100_flux_err, fmt='o', 
                 color=colors[4], ms=4, zorder=3, label='Aperature Total Flux')
    plt.plot(model_wave, model_flux, '-', color=colors[1], 
             zorder=1, label='Model')
    plt.legend(loc='upper right')
    plt.xlim(5, 25)
    plt.ylim(0, ymax)
    plt.ylabel("Flux (mJy)")
    # Plot infrared excess
    plt.subplot(212)
    plt.errorbar(data.wavelength, planet_flux[0], planet_flux_err[0], fmt='o', 
                 color=colors[0], ms=4, zorder=3, label='Aperature 30 Flux')
    plt.errorbar(data.wavelength, planet_flux[1], planet_flux_err[1], fmt='o', 
                 color=colors[2], ms=4, zorder=3, label='Aperature 50 Flux')
    plt.errorbar(data.wavelength, planet_flux[2], planet_flux_err[2], fmt='o', 
                 color=colors[3], ms=4, zorder=3, label='Aperature 70 Flux')
    plt.errorbar(data.wavelength, planet_flux[3], planet_flux_err[3], fmt='o', 
                 color=colors[4], ms=4, zorder=3, label='Aperature Total Flux')
    plt.hlines(0, 5, 25, ls='solid', color=colors[1])
    plt.hlines([-3, 3], 5, 25, ls='dotted', color=colors[1], 
               label='3% Abs. Flux Unc.', alpha=0.5)
    plt.legend(loc='best', ncol=2)
    plt.xlim(5, 25)
    ymin = np.min((planet_flux.min()-3*planet_flux_err.max(), -5))
    ymax = np.max((planet_flux.max()+3*planet_flux_err.max(), 5))
    plt.ylim(ymin, ymax)
    plt.ylabel("Infrared Excess (%)")
    plt.xlabel("Wavelength ($\mu m$)")

    plt.savefig(save_file)

    return


