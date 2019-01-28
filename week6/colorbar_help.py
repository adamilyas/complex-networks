from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np


"""
This file provides the function for plotting the colorbar in case plt.colorbar() fails to
output any colorbar at all.

In your script file, import this module with


import colorbar_help as ch
import networkx as nx
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot(111)

# ....
# do your fancy network stuff
# ....

nx.draw(your_network, node_color=your_node_values, cmap='OrRd')

ch.add_colorbar(your_node_values)
#plt.show()
"""

def add_colorbar(cvalues, cmap='OrRd', cb_ax=None):
    """
    Add colorbar for old versions of matplotlib.
    Use the same cmap as you used for drawing networkx!

    Parameters
    ----------
    cvalues : list-like
        List of values (or e.g. numpy array) that are color
        mapped. In this case thse values should correspond to
        the node-wise values of the
    cmap : matplotlib colormap name, optional
    cb_ax : matplotlib axis object
        an axis object where to put the axis
        not required for basic usage!
    """
    eps = np.maximum(0.0000000001, np.min(cvalues)/1000.)
    vmin = np.min(cvalues) - eps
    vmax = np.max(cvalues)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    scm = mpl.cm.ScalarMappable(norm, cmap)
    scm.set_array(cvalues)
    if cb_ax is None:
        plt.colorbar(scm)
    else:
        try:
            plt.colorbar(cax=cb_ax)
        except:
            mpl.colorbar.ColorbarBase(cb_ax,
                                      cmap=cmap,
                                      norm=norm,
                                      orientation='vertical')
