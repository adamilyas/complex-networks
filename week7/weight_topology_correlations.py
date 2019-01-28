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
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from scipy.stats import binned_statistic

import os
if not os.path.isdir("image_1"):
    os.mkdir("image_1")
if not os.path.isdir("image_2"):
    os.mkdir("image_2")

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============

###############################################################
# Code that is given to you, and does not need to be modified #
###############################################################

def create_linbins(start, end, n_bins):
    """
    Creates a set of linear bins.

    Parameters
    -----------
    start: minimum value of data, int
    end: maximum value of data, int
    n_bins: number of bins, int

    Returns
    --------
    bins: a list of linear bin edges
    """
    bins = np.linspace(start, end, n_bins)
    return bins

def create_logbins(start, end, n_log, n_lin=0):
    """
    Creates a combination of linear and logarithmic bins: n_lin linear bins 
    of width 1 starting from start and n_log logarithmic bins further to
    max.

    Parameters
    -----------
    start: starting point for linear bins, float
    end: maximum value of data, int
    n_log: number of logarithmic bins, int
    n_lin: number of linear bins, int

    Returns
    -------
    bins: a list of bin edges
    """
    if n_lin == 0:
        bins = np.logspace(np.log10(start), np.log10(end), n_log)
    elif n_lin > 0:
        bins = np.array([start + i for i in range(n_lin)] + list(np.logspace(np.log10(start + n_lin), np.log10(end), n_log)))
    return bins
######################################################
# Starting from here you might need to edit the code #
######################################################


def get_link_weights(net):

    """
    Returns a list of link weights in the network.

    Parameters
    -----------
    net: a networkx.Graph() object

    Returns
    --------
    weights: list of link weights in net
    """

    # write a function to get weights of the links
    # Hints:
    # to get the links with their weight data, use net.edges(data=True)
    # to get weight of a single link, use (i, j, data) for each edge,
    # weight = data['weight']
    links = net.edges(data=True)
    weights = []
    for (i, j, data) in links:
        weight = data['weight']
        weights.append(weight)

    return weights

def plot_ccdf(datavecs, labels, xlabel, ylabel, num, path):

    """
    Plots in a single figure the complementary cumulative distributions (1-CDFs)
    of the given data vectors.

    Parameters
    -----------
    datavecs: data vectors to plot, a list of iterables
    labels: labels for the data vectors, list of strings
    styles = styles in which plot the distributions, list of strings
    xlabel: x label for the figure, string
    ylabel: y label for the figure, string
    num: an id of the figure, int or string
    path: path where to save the figure, string
    """
    styles = ['-', '--', '-.']
    fig = plt.figure(num)
    ax = fig.add_subplot(111)
    for datavec, label, style in zip(datavecs,labels, styles):
        #TODO: calculate 1-CDF of datavec and plot it with ax.loglog()
        sorted_datavec = sorted(datavec)
        N = len(sorted_datavec)
        ccdf = np.zeros(N)

        for i, val in enumerate(sorted_datavec):
            for el in sorted_datavec:
                ccdf[i] += (el >= val)
            ccdf[i] /= N
        ax.plot(sorted_datavec, ccdf, style, label=label)     

    ax.set_xscale('log')
    ax.set_yscale('log')        
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc=0)
    ax.grid()
    plt.plot()
    return fig


def get_link_overlap(net):
    """
    Calculates link overlap: 
    O_ij = n_ij / [(k_i - 1) + (k_j - 1) - n_ij]

    Parameters
    -----------
    net: a networkx.Graph() object

    Returns
    --------
    overlaps: list of link overlaps in net
    """

    # TODO: write a function to calculate link neighborhood overlap
    # Hint: for getting common neighbors of two nodes, use
    # set datatype and intersection method

    overlaps = []
    links = net.edges()
    for (i, j) in links:
        n_ij = len([val for val in net.neighbors(i) if val in net.neighbors(j)])
        k_i, k_j = nx.degree(net, i), nx.degree(net, j)

        if n_ij==0:
            overlaps.append(0)
        else:
            overlap = n_ij / (k_i + k_j - 2 - n_ij)
            overlaps.append(overlap)

    return overlaps

# =========================== MAIN CODE BELOW ==============================

if __name__ == '__main__':
    # Loading the network
    #TODO: set correct network path and name
    network_path = './OClinks_w_undir.edg'
    net_name = 'fb_like'
    #TODO: replace with a path where to save the 1-CDF plot
    path = './image_1/ccdfs_' + net_name + '.png'
    #TODO: replace with a base path where to save the average link weight scatter
    # A scale-related suffix will be added to this base path 
    # so the figures will not overwritte
    base_path = '.image_1/s_per_k_vs_k_'
    #TODO: replace with a base path where to save the link neighborhood overlap plot
    save_path_linkneighborhoodplot = './O_vs_w_' + net_name + '.png'
    
    network = nx.read_weighted_edgelist(network_path)

    # First, getting the node degrees and strengths
    degrees = nx.degree(network)
    strengths =  nx.degree(network, weight = 'weight')

    #Now, converting the degree and strength into lists.
    degree_vec = []
    strength_vec = []
    for node in network.nodes():
        degree_vec.append(degrees[node])
        strength_vec.append(strengths[node])

    # Then, computing the weights
    weights = get_link_weights(network)

    # Now let's start solving the exercise.
    # 1a: creating 1-CDF plots
    datavecs = [degree_vec, strength_vec, weights]
    num = 'a)' + net_name # figure identifier

    #TODO: set the correct labels
    labels = ['Degree', 'Strength', 'Weight']
    xlabel = 'Degree, strength or link weight'
    ylabel = '1-CDF'

    fig=plot_ccdf(datavecs, labels, xlabel, ylabel, num, path)
    
    ax = fig.add_subplot(111)
    ax.set_xscale('log')
    ax.set_yscale('log')
    fig.savefig(path)
    print('1-CDF figure saved to ' + path)
    
    # 1b: average link weight per node
    av_weight = degrees = [strength/degree for strength, degree 
                           in zip(strength_vec, degree_vec)]
    #TODO: calculate average link weight per node
    # YOUR CODE HERE

    # Since 1b and 1c solution plots
    # can be drawn in one figure for linear and one figure for logarithmic
    # then, let's plot the scatters and bin averages in one figure
    # creating scatters and adding bin averages on top of them

    n_bins = 50 #TIP: use the number of bins you find reasonable
    min_deg = min(degree_vec)
    max_deg = max(degree_vec)
    linbins = create_linbins(min_deg, max_deg, n_bins)
    logbins = create_logbins(0.5, max_deg, n_bins, n_lin=10)
    num = 'b) ' + net_name + "_"
    alpha = 0.1 # transparency of data points in the scatter

    for bins, scale in zip([linbins, logbins], ['linear', 'log']):
        fig = plt.figure(num + scale)
        ax = fig.add_subplot(111)
        # mean degree value of each degree bin
        degree_bin_means, _, _ = ([], [], [])
        # TODO: use binned_statistic to get mean degree of each bin 
        degree_bin_means, _, _ =binned_statistic(
            x = degree_vec, 
            values=degree_vec, 
            bins=bins,statistic='mean')
        # mean strength value of each degree bin    
        strength_bin_means, _, _ = ([], [], [])
        # TODO: use binned_statistic to get mean strength of each bin)
        strength_bin_means, _, _ =binned_statistic(
            x = degree_vec, 
            values=strength_vec, 
            bins=bins,
            statistic='mean')
        # number of points in each degree bin
        counts, _, _ = ([], [], [])
        # TODO: use binned_statistic to get number of data points
        counts, _, _ = binned_statistic(
            x = degree_vec, 
            values=degree_vec, 
            bins=bins,statistic='count')


        # 1b: plotting all points (scatter)
        ax.scatter(degree_vec, av_weight, marker='o', s=1.5, alpha=alpha)
        # calculating the average weight per bin
        bin_av_weight = strength_bin_means / degree_bin_means

        # 1c: and now, plotting the bin average
        # the marker size is scaled by number of data points in the bin
        ax.scatter(degree_bin_means,
                   bin_av_weight,
                   marker='o',
                   color='g',
                   s=np.sqrt(counts) + 1,
                   label='binned data')
        ax.set_xscale(scale)
        min_max = np.array([min_deg, max_deg])
        ax.set_xlabel('degree k')
        ax.set_ylabel('avg link weight s')
        ax.grid()

        ax.legend(loc='best')
        plt.suptitle('avg. link weight vs. strength:' + net_name)
        save_path = base_path + scale + '_' + net_name + '.png'
        fig.savefig(save_path)
        print('Average link weight scatter saved to ' + save_path)
            
    # 1e: getting link neighborhood overlaps
    overlaps = get_link_overlap(network)

    # creating link neighborhood overlap scatter
    num = 'd) + net_name'
    fig = plt.figure(num)
    ax = fig.add_subplot(111)

    n_bins = 50 #TIP: use the number of bins you find reasonable
    min_w = np.min(weights)
    max_w = np.max(weights)

    linbins = create_linbins(min_w, max_w, n_bins)
    logbins = create_logbins(min_w, max_w, n_bins)

    #TODO: try both linear and logarithmic bins, select the best one
    bins = logbins

    # mean weight value of each weight bin
    weight_bin_means, _, _ = binned_statistic(x = weights, 
                                              values=weights, 
                                              bins=bins,statistic='mean'
                                             )
    #TODO: use binned_statistic to get mean weight of each bin
    # mean link neighborhood overlap of each weight bin
    overlap_bin_means, _, _ = binned_statistic(x = weights, 
                                               values=overlaps, 
                                               bins=bins,statistic='mean'
                                              )
    #TODO: use binned_statistic to get mean overlap of each bin 
    # number of points in each weigth bin
    counts, _, _ =binned_statistic(x = weights, 
                                   values=weights, 
                                   bins=bins,statistic='count'
                                  )
    #TODO: use binned_statistic to get number of data points
    # plotting all points (overlap)
    ax.scatter(weights, overlaps, marker="o", s=1.5, alpha=alpha)
    # plotting bin average, marker size scaled by number of data points in the bin
    ax.scatter(weight_bin_means,
               overlap_bin_means,
               s=np.sqrt(counts) + 2,
               marker='o',
               color='g')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid()
    ax.set_xlabel('link weight')
    ax.set_ylabel('link neighborhood overlap')
    fig.suptitle('Overlap vs. weight:' + net_name)
    fig.savefig(save_path_linkneighborhoodplot)
    print('Link neighborhood overlap scatter saved as ' + save_path_linkneighborhoodplot)