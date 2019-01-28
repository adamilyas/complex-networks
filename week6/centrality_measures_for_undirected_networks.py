# In order to understand how the code works, it is a good idea to check the
# final section of the file that starts with
#   if __name__ == '__main__'
#
# Your task is essentially to replace all the parts marked as TODO or as
# instructed through comments in the functions, as well as the filenames
# and labels in the main part of the code which can be found at the end of
# this file.
#
# The raise command is used to help you out in finding where you still need to
# write your own code. When you successfully modified the code in that part,
# remove the `raise` command.
from __future__ import print_function
import numpy as np
import networkx as nx
import matplotlib.pylab as plt
from matplotlib import gridspec
from colorbar_help import add_colorbar
import pickle

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============

###############################################################
# Code that is given to you, and does not need to be modified #
###############################################################


def create_scatter(x_values, y_values, x_label, y_label, labels, markers):
    """
    Creates a scatter plot of y_values as a function of x_values.

    Parameters
    ----------
    x_values: np.array
    y_values: list of np.arrays
    x_label: string
    y_label: string
        a generic label of the y axis
    labels: list of strings
        labels of scatter plots
    markers: list of strings

    Returns
    -------
    No direct output, saves the scatter plot at given figure_path
    """
    assert x_values.size , 'Bad input x_values for creating a scatter plot'

    fig = plt.figure(figsize=(12,5))

    ax = fig.add_subplot(111)

    for y_val, label, marker in zip(y_values, labels, markers):
        ax.plot(x_values, y_val, ls='', marker=marker, label=label)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid()
    ax.legend(loc=0)

    return fig

def visualize_on_network(network, node_values, coords_path,
                         titles, cmap='YlOrRd',
                         node_size=50, font_size=8, scale=500):
    """
    Creates visualizations of the network with nodes color coded by each of the
    node values sets.

    Parameters
    ----------
    network: networkx.Graph()
    node_values: list of lists
    coords_path: path to a file containing node coordinates
    titles: list of strings
    cmap: string
    node_size: int
    font_size: int
    scale: int
        used to calculate the spring layout for node positions

    Returns
    -------
    No direct output, saves the network visualizations at given path
    """
    assert node_values[0].size, "there should be multiple values per node"

    # This is the grid for 5 pictures
    gs = gridspec.GridSpec(3, 4, width_ratios=(20, 1, 20, 1))
    network_gs_indices = [(0, 0), (0, 2), (1, 0), (1, 2), (2,0)]
    cbar_gs_indices = [(0, 1), (0, 3), (1, 1), (1, 3), (2, 1)]

    # Loading coordinates from the file
    with open(coords_path, 'rb') as f:
        #coords = pickle.load(f, encoding='latin1')
        coords = pickle.load(f, encoding='latin1')

    fig = plt.figure(figsize=(12,5))
        
    # Loop over different value sets
    for node_val, title, network_gs_index, cb_gs_index in zip(node_values,
                                                              titles,
                                                              network_gs_indices,
                                                              cbar_gs_indices):
        # Draw the network figure
        
        ax = plt.subplot(gs[network_gs_index[0], network_gs_index[1]])
        nx.draw(network, pos=coords, node_color=node_val, cmap=cmap,
                node_size=node_size, font_size=font_size)

        # Draw the colorbar (cb)
        cb_ax = plt.subplot(gs[cb_gs_index[0], cb_gs_index[1]])
        add_colorbar(node_val, cb_ax=cb_ax)

        ax.set_title(title)
        
    return fig
######################################################
# Starting from here you might need to edit the code #
######################################################


def get_centrality_measures(network, tol):
    """
    Calculates five centrality measures (degree, betweenness, closeness, and
    eigenvector centrality, and k-shell) for the nodes of the given network.

    Parameters
    ----------
    network: networkx.Graph()
    tol: tolerance parameter for calculating eigenvector centrality

    Returns
    --------
    [degree, betweenness, closeness, eigenvector_centrality, kshell]: list of
    numpy.arrays
    """
    nodes = network.node
    N = len(nodes)

    degrees_temp = nx.degree(network)
    betweenness_temp = nx.betweenness_centrality(network)
    closeness_temp = nx.closeness_centrality(network)
    eigenvector_centrality_temp = nx.eigenvector_centrality(network, tol=tol)
    kshell_temp = nx.core_number(network)

    degrees = np.zeros(N)
    betweenness = np.zeros(N)
    closeness = np.zeros(N)
    eigenvector_centrality = np.zeros(N)
    kshell = np.zeros(N)


    for i, node in enumerate(nodes):
        degrees[i] = degrees_temp[node]
        betweenness[i] = betweenness_temp[node]
        closeness[i] = closeness_temp[node]
        eigenvector_centrality[i] = eigenvector_centrality_temp[node]
        kshell[i] = kshell_temp[node]
    return [degrees, betweenness, closeness, eigenvector_centrality, kshell]


# =========================== MAIN CODE BELOW ==============================

if __name__ == '__main__':

    network_paths = ['./small_ring.edg',
                     './larger_lattice.edg',
                     './small_cayley_tree.edg',
                     './karate_club_network_edge_file.edg']
    coords_paths = ['./small_ring_coords.pkl',
                    './larger_lattice_coords.pkl',
                    './small_cayley_tree_coords.pkl',
                    './karate_club_coords.pkl']
    network_names = ['ring', 'lattice', 'cayley_tree', 'karate']
    x_label = 'Degree k'
    y_label = 'Centrality measure'
    labels = ['betweenness centrality', 'closeness centrality',
              'eigenvector centrality', 'normalized k-shell']
    markers = ['.', 'x', '+', 'o']
    scatter_base_path = './centrality_measures_scatter'
    titles = ['Degree $k$', 'Betweenness centrality',
              'Closeness centrality', 'Eigenvector centrality', '$k$-shell']
    network_base_path = './network_figures'


    fig_index = 0
    tol = 10**-1 # tolerance parameter for calculating eigenvector centrality

    # Loop through all networks
    for (network_path, network_name, coords_path) in zip(network_paths, network_names, coords_paths):
        if network_name == 'karate':
            network = nx.read_weighted_edgelist(network_path)

        else:
            network = nx.read_edgelist(network_path)

        # Calculating centrality measures
        [degree, betweenness, closeness, eigenvector_centrality, kshell] = get_centrality_measures(network, tol)
        kshell_normalized = kshell/float(np.max(kshell)) # normalization for easier visualization

        # Scatter plot
        y_values = [betweenness, closeness, eigenvector_centrality, kshell_normalized]
        scatter_path = scatter_base_path + '_' + network_name + '.png'

        fig = create_scatter(degree, y_values, x_label, y_label, labels, markers)

        fig.savefig(scatter_path)


        # Network figures
        network_figure_path = network_base_path + '_' + network_name + '.png'
        all_cvalues = [degree, betweenness, closeness, eigenvector_centrality, kshell]
        fig=visualize_on_network(network, all_cvalues,
                                 coords_path, titles)

        fig.savefig(network_figure_path)
