import numpy as np
import os
import glob
import shutil
import astropy.io.fits as pf

def makedirectory(outputdir):
    """Creates a directory for the current stage.

    Parameters
    ----------
    outputdir : str
        Output directory where FITS files are saved
    """
    if not os.path.exists(outputdir):
        try:
            os.makedirs(outputdir)
        except (PermissionError, OSError) as e:
            # Raise a more helpful error message so that users know to update
            # topdir in their ecf file
            message = (f'You do not have the permissions to make the folder '
                       f'{outputdir}.')
            raise PermissionError(message) from e
    if not os.path.exists(os.path.join(outputdir, "figs")):
        os.makedirs(os.path.join(outputdir, "figs"))

    return


def sortMAST(mast_dir, data_dir, filetype='_cal.fits'):
    """Sort files downloaded from MAST
    
    Parameters
    ----------
    mast_dir : str
        Input directory where FITS files are currently located
    data_dir : str
        Base directory where FITS files are moved

    Returns
    -------
    target_files : list
        List of files in their final directories
    """

    # Collect list of files ending in filetype
    files = glob.glob(f'{mast_dir}/**/*{filetype}', recursive=True)

    # Move files
    target_files = []
    for filename in files:
        hdr = pf.getheader(filename)
        target_name = hdr['TARGPROP']
        filter = hdr['FILTER']
        target_dir = os.path.join(data_dir, target_name, filter)
        # Create directory
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        target_files.append(shutil.move(filename, target_dir))
    return target_files
