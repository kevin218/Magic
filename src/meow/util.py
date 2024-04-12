import numpy as np
import os
import glob

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