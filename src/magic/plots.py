import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.constrained_layout.use'] = True

from astropy.visualization import ImageNormalize, ManualInterval, SqrtStretch
from astropy.stats import sigma_clipped_stats
from astropy.io import fits

colors = ['xkcd:bright blue','orange','purple','xkcd:soft green','pink']
fmts = ['-o', '-s', '-^', '-v',
        '--o', '--s', '--^', '--v',
        ':o', ':s', ':^', ':v']
plt.rcParams['figure.constrained_layout.use'] = True

# Helper script to plot before/after BG subtraction
def before_after(data_before, data_after, vmax_before, vmax_after,
                 title_before, title_after, savename=None, fignum=251):
    """Function to generate 2D image from before and after
    background subtraction.

    Parameters
    ----------
    data_before : numpy.ndarray
        Image to be displayed, before BG subtractions
    data_after : numpy.ndarray
        Image to be displayed, after BG subtractions
    vmax_before : float
        Maximum signal value to use for scaling
    vmax_after : float
        Maximum signal value to use for scaling
    title_before : str
        String to use for the plot title
    title_after : str
        String to use for the plot title
    savename : str
        Full path and name used for saving image
    fignum : int
        Figure number
    """

    plt.figure(fignum, figsize=(14,6))
    plt.clf()
    plt.subplot(121)
    plt.title(title_before)
    plt.imshow(data_before, cmap='Greys', origin='lower', vmin=0, vmax=vmax_before)
    plt.ylabel("Pixel Row")
    plt.xlabel("Pixel Column")
    plt.colorbar()
    plt.subplot(122)
    plt.title(title_after)
    plt.imshow(data_after, cmap='Greys', origin='lower', vmin=0, vmax=vmax_after)
    plt.ylabel("Pixel Row")
    plt.xlabel("Pixel Column")
    plt.colorbar()
    if savename:
        plt.savefig(savename, dpi=200)


# Helper script to plot 2D images
def show_image(data_2d, vmin, vmax, xpixel=None, ypixel=None, title=None,
               units="DN", dmap="binary", savename=None, fignum=252):
    """Function to generate a 2D, log-scaled image of the data,
    with an option to highlight a specific pixel (with a red dot).

    Parameters
    ----------
    data_2d : numpy.ndarray
        Image to be displayed
    vmin : float
        Minimum signal value to use for scaling
    vmax : float
        Maximum signal value to use for scaling
    xpixel : int
        X-coordinate of pixel to highlight
    ypixel : int
        Y-coordinate of pixel to highlight
    title : str
        String to use for the plot title
    units : str
        Units of the data. Used for the annotation in the
        color bar
    savename : str
        Full path and name used for saving image
    fignum : int
        Figure number
    """
    norm = ImageNormalize(data_2d,
                          interval=ManualInterval(vmin=vmin, vmax=vmax),
                          stretch=SqrtStretch())

    plt.figure(fignum, figsize=(7.1, 6))
    plt.clf()
    if title:
        plt.title(title)
    plt.imshow(data_2d, origin="lower", norm=norm, cmap=plt.get_cmap(dmap))
    if xpixel and ypixel:
        plt.plot(xpixel, ypixel, marker="o", color="red", label="Selected Pixel")
    plt.colorbar(label=units)
    plt.xlabel("Pixel Column")
    plt.ylabel("Pixel Row")
    if savename:
        plt.savefig(savename, dpi=200)


# Helper script to plot an image and overlay catalog sources
def overlay_catalog(data_2d, catalog, flux_limit=0, vmin=0, vmax=10,
                    title=None, units="MJy/str", dmap="binary",
                    savename=None, fignum=302):
    """Function to generate a 2D image of the data,
    with sources overlaid.

    Parameters
    ----------
    data_2d : numpy.ndarray
        2D image to be displayed
    catalog : astropy.table.Table
        Table of sources
    flux_limit : float
        Minimum signal threshold to overplot sources from catalog.
        Sources below this limit will not be shown on the image.
    vmin : float
        Minimum signal value to use for scaling
    vmax : float
        Maximum signal value to use for scaling
    title : str
        String to use for the plot title
    units : str
        Units of the data. Used for the annotation in the
        color bar
    savename : str
        Full path and name used for saving image
    fignum : int
        Figure number
    """
    norm = ImageNormalize(
        data_2d, interval=ManualInterval(vmin=vmin, vmax=vmax),
        stretch=SqrtStretch())

    plt.figure(fignum, figsize=(7.1, 6))
    plt.clf()
    if title:
        plt.title(title)
    plt.imshow(data_2d, origin="lower", norm=norm, cmap=plt.get_cmap(dmap))

    for row in catalog:
        if row["aper_total_flux"].value > flux_limit:
            plt.plot(
                row["xcentroid"],
                row["ycentroid"],
                marker="o",
                markersize="3",
                color="red",
            )

    plt.xlabel("Pixel column")
    plt.ylabel("Pixel row")
    plt.colorbar(label=units)
    # plt.tight_layout()

    # fig.colorbar(im, label=units)
    # fig.tight_layout()
    # plt.subplots_adjust(left=0.15)

    if savename:
        plt.savefig(savename, dpi=200)


def show_true_colors(pl_colors, filters, target_list, slopes,
                     title=None, savename=None, fignum=401):
    '''
    '''
    f1, f2, f3 = filters

    plt.figure(fignum, figsize=(7.1, 6))
    plt.clf()
    if title:
        plt.title(title)
    for i, target_name in enumerate(target_list):
        plt.errorbar(pl_colors[i,0], pl_colors[i,1],
                     fmt=fmts[i%12], color=colors[i%5],
                     ms=4, zorder=3, label=target_name)
    plt.legend(loc='best', ncol=2)
    plt.xlabel(f"({f1}-{f2})/{f2}")
    plt.ylabel(f"({f3}-{f2})/{f2}")


# def show_true_colors(pl_colors, title=None,
#                     savename=None, fignum=402):
#     '''
#     '''

    plt.figure(402, figsize=(7.1, 6))
    plt.clf()
    if title:
        plt.title(title)
    plt.errorbar(pl_colors[:,0,0], pl_colors[:,1,0], fmt='o', color=colors[0],
             ms=4, zorder=3, label='Aperature 30 Flux')
    plt.errorbar(pl_colors[:,0,1], pl_colors[:,1,1], fmt='s', color=colors[1],
             ms=4, zorder=5, label='Aperature 50 Flux')
    plt.errorbar(pl_colors[:,0,2], pl_colors[:,1,2], fmt='^', color=colors[2],
             ms=4, zorder=7, label='Aperature 70 Flux')
    plt.errorbar(pl_colors[:,0,3], pl_colors[:,1,3], fmt='v', color=colors[3],
             ms=4, zorder=10, label='Aperature 100 Flux')
    plt.legend(loc='best', ncol=2)
    plt.xlabel(f"({f1}-{f2})/{f2}")
    plt.ylabel(f"({f3}-{f2})/{f2}")



    plt.figure(403, figsize=(7.1, 6))
    plt.clf()
    for i, target_name in enumerate(target_list):
        plt.errorbar(slopes[i,1]-slopes[i,0], pl_colors[i,0,3],
                     fmt=fmts[i%12], color=colors[i%5],
                     ms=4, zorder=3, label=target_name)
    plt.legend(loc='best', ncol=2)
    plt.xlabel(f"Slope 2 - Slope 1")
    plt.ylabel(f"({f1}-{f2})/{f2}")

    plt.figure(404, figsize=(7.1, 6))
    plt.clf()
    plt.errorbar(slopes[:,1]-slopes[:,0], pl_colors[:,0,3], fmt='v', color=colors[3],
             ms=4, zorder=10, label='Aperature 100 Flux')
    plt.xlabel(f"Slope 2 - Slope 1")
    plt.ylabel(f"({f1}-{f2})/{f2}")

