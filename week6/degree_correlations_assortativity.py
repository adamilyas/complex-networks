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
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binned_statistic_2d
from scipy.stats import pearsonr
from colorbar_help import add_colorbar

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============

###############################################################
# Code that is given to you, and does not need to be modified #
###############################################################


def create_scatter(x_degrees, y_degrees, network_title):
    """
    For x_degrees, y_degrees pair, creates and
    saves a scatter of the degrees.

    Parameters
    ----------
    x_degrees: np.array
    y_degrees: np.array
    network_title: str
        a network-referring title (string) for figures

    Returns
    -------
    no output, but scatter plot (as pdf) is saved into the given path
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)

    alpha = 0.5
    ax.plot(x_degrees, y_degrees, 'r', ls='', marker='o', ms=5, alpha=alpha)
    ax.set_xlabel(r'Degree $k$')
    ax.set_ylabel(r'Degree $k$')

    ax.set_title(network_title)

    return fig

def create_heatmap(x_degrees, y_degrees, network_title):
    """
    For x_degrees, y_degrees pair, creates and
    saves a heatmap of the degrees.

    Parameters
    ----------
    x_degrees: np.array
    y_degrees: np.array
    network_title: str
        a network-referring title (string) for figures

    Returns
    -------
    no output, but heatmap figure (as pdf) is saved into the given path
    """
    k_min = np.min((x_degrees, y_degrees))
    k_max = np.max((x_degrees, y_degrees))

    n_bins = k_max-k_min+1
    values = np.zeros(x_degrees.size)

    statistic = binned_statistic_2d(x_degrees,y_degrees, values,
                                    statistic='count', bins=n_bins)[0]

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.imshow(statistic, extent=(k_min-0.5, k_max+0.5, k_min-0.5, k_max+0.5),
              origin='lower', cmap='hot', interpolation='nearest')
    ax.set_title(network_title)
    ax.set_xlabel(r'Degree $k$')
    ax.set_ylabel(r'Degree $k$')
    add_colorbar(statistic, cmap='hot')
    return fig

######################################################
# Starting from here you might need to edit the code #
######################################################


def get_x_and_y_degrees(network):
    """
    For the given network, creates two arrays (x_degrees
    and y_degrees) of the degrees of "start" and "end" nodes of each edge in
    the network. For undirected networks, each edge is considered twice.

    Parameters
    ----------
    network: a NetworkX graph object

    Returns
    -------
    x_degrees: np.array
    y_degrees: np.array
    """
    nodes = nx.nodes(network)
    edges = network.edges()
    N = len(edges)
    
    x_degrees = np.zeros(2 * N)
    y_degrees = np.zeros(2 * N)

    for i, edge in enumerate(edges):
        x_degrees[i] = nx.degree(network, edge[0])
        y_degrees[i] = nx.degree(network, edge[1])

    for j in range(i, i+N):
        x_degrees[j] = y_degrees[j-i]
        y_degrees[j] = x_degrees[j-i]
        
    return x_degrees, y_degrees


def assortativity(x_degrees, y_degrees):
    """
    Calculates assortativity for a network, i.e. Pearson correlation
    coefficient between x_degrees and y_degrees in the network.

    Parameters
    ----------
    x_degrees: np.array
    y_degrees: np.array

    Returns
    -------
    assortativity: float
        the assortativity value of the network as a number
    """
    assortativity = pearsonr(x_degrees, y_degrees)[0]
    return assortativity

def get_nearest_neighbor_degree(network):
    """
    Calculates the average nearest neighbor degree for each node for the given
    list of networks.

    Parameters
    ----------
    network: a NetworkX graph objects

    Returns
    -------
    degrees: list-like
        an array of node degree
    nearest_neighbor_degrees: list-like
        an array of node average nearest neighbor degree in the same order
        as degrees
    """
    nearest_neighbor_degrees = []
    degrees_temp = dict(nx.degree(network))
    minIndex1, minIndex2 = 10, 10
    maxIndex1, maxIndex2 = 0, 0
    nearest_neighbor_degrees_temp = nx.average_neighbor_degree(network)

    for key in degrees_temp:
        value = degrees_temp[key]
        if int(key) < minIndex1:
            minIndex1 = int(key)
        if int(key) > maxIndex1:
            maxIndex1 = int(key)
    for key in nearest_neighbor_degrees_temp:
        value = nearest_neighbor_degrees_temp[key]
        if int(key) < minIndex2:
            minIndex2 = int(key)
        if int(key) > maxIndex2:
            maxIndex2 = int(key)

    degrees = np.zeros((maxIndex1-minIndex1 + 1,))
    nearest_neighbor_degrees = np.zeros((maxIndex2-minIndex2 + 1,))
    for key in degrees_temp:
        value = degrees_temp[key]
        degrees[int(key) - minIndex1] = value
    for key in nearest_neighbor_degrees_temp:
        value = nearest_neighbor_degrees_temp[key]
        nearest_neighbor_degrees[int(key) - minIndex2] = value
    return degrees, nearest_neighbor_degrees

def get_simple_bin_average(x_values, y_values):
    """
    Calculates average of y values within each x bin. The binning used is the
    most simple one: each unique x value is a bin of it's own.

    Parameters
    ----------
    x_values: an array of x values
    y_values: an array of corresponding y values

    Returns
    -------
    bins: an array of unique x values
    bin_average: an array of average y values per each unique x
    """
    bins = x_values
    for i in bins:
        for j in bins:
            if i == j:
                bins = np.delete(bins,j)

    bin_average = np.zeros(len(bins)) # replace
    for i in range(len(bins)):
        denominator = 0
        for k in y_values:
            if k == bins[i]:
                bin_average[i] = bin_average[i] + k
                denominator = denominator + 1
        bin_average[i] = bin_average[i]/denominator
    return bins, bin_average

###############################################################
# Code that is given to you, and does not need to be modified #
###############################################################


def visualize_nearest_neighbor_degree(degrees, nearest_neighbor_degrees, bins, bin_averages,
                                      network_title):
    """
    Visualizes the nearest neighbor degree for each degree as a scatter and
    the mean nearest neighbor degree per degree as a line.

    Parameters
    ----------
    degrees: list-like
        an array of node degrees
    nearest_neighbor_degrees: list-like
        an array of node nearest neighbor degrees in the same order as degrees
    bins: list-like
        unique degree values
    bin_averages: list-like
        the mean nearest neighbor degree per unique degree value
    network_title: str
        network-referring title (string) for figure

    Returns
    -------
    fig : figure object
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(degrees, nearest_neighbor_degrees,
              ls='', marker='.', label=r'$k_{nn}$($k$)')
    ax.loglog(bins, bin_averages,
              color='r', label=r'<$k_{nn}$>($k$)')
    ax.set_title(network_title)
    ax.set_xlabel(r'Degree $k$')
    ax.set_ylabel(r'Average nearest neighbor degree $k_{nn}$')
    ax.legend(loc=0)
    return fig

######################################################
# Starting from here you might need to edit the code #
######################################################


# =========================== MAIN CODE BELOW ==============================

if __name__ == '__main__':
    # YOUR CODE HERE
    #TODO: set network paths and names properly
    # see documentation of the functions where these variables are used
    # for the details of these variables
    network_paths = ['', ''] # replace, example path: '../data/karate_club_network_edge_file.edg'
    network_names = ['', ''] # replace, these are extensions added to figure file names
    network_titles = ['', ''] # replace, used in figure titles
    # network_name and .pdf extension are added after figure_base variables when saving the figures
    scatter_figure_base = '' # replace, where to save the scatterplots, example: '../figs/edge_degree_correlation_scatter_' which contains path (../figs/) and beginning of file name (edge_degree...)
    heatmap_figure_base = '' # replace, where to save the heatmaps
    nearest_neighbor_figure_base = '' # replace, where to save nearest neighbor figures
    # Loop through all networks
    for network_path, network_name, network_title in zip(network_paths, network_names, network_titles):
        network = nx.read_weighted_edgelist(network_path)
        x_degrees, y_degrees = get_x_and_y_degrees(network)

        fig = create_scatter(x_degrees, y_degrees, network_title)
        fig.savefig(scatter_figure_base+network_name+'.pdf')

        fig = create_heatmap(x_degrees, y_degrees, network_title)
        fig.savefig(heatmap_figure_base+network_name+'.pdf')

        # assortativities
        assortativity_own = assortativity(x_degrees, y_degrees)
        assortativity_nx = nx.degree_assortativity_coefficient(network)
        print("Own assortativity for " + network_title + ": " +
              str(assortativity_own))
        print("NetworkX assortativity for " + network_title + ": " +
              str(assortativity_nx))

        # nearest neighbor degrees
        degrees, nearest_neighbor_degrees = get_nearest_neighbor_degree(network)
        unique_degrees, mean_nearest_neighbor_degrees = get_simple_bin_average(degrees,
                                                                               nearest_neighbor_degrees)
        fig = visualize_nearest_neighbor_degree(degrees,
                                                nearest_neighbor_degrees,
                                                unique_degrees,
                                                mean_nearest_neighbor_degrees,
                                                network_title)
        fig.savefig(nearest_neighbor_figure_base + network_name + '.pdf')
    #plt.show()
