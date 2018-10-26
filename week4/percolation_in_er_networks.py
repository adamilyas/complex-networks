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
import random
import os

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============

###############################################################
# Code that is given to you, and does not need to be modified #
###############################################################


def calculate_loop_edge_fraction(network, visited_nodes, boundary_nodes):
    """ Calculates the number of edges that go from the boundary to already visited nodes
    in addition to the number of edges that is expected if the network would be a tree.
    This number is then divided by the number of edges in total that go from the boundary
    to the visited nodes.

    In the case that the there are zero edges from the boundary to the visited nodes,
    this function returns zero (i.e., in the beginning when the boundary set is the same
    as the visited nodes).

    Parameters
    ----------
    network : networkx.Graph object
    visited_nodes : set object
      The set of nodes that are visited (including the boundary)
    boundary_nodes : set object
      The set of nodes that are in the boundary, i.e., the were visited in the last iteration.

    Returns
    -------
    The fraction described above : float

    """
    if len(visited_nodes) == 1:
        return 0

    edge_count = 0

    for node in boundary_nodes:
        for neighbor in network[node]:
            if neighbor in visited_nodes or neighbor in boundary_nodes:
                edge_count += 1

    if edge_count != 0:
        loop_count = edge_count -len(boundary_nodes)
        assert loop_count >= 0
        return loop_count/float(edge_count)
    else:
        return 0

######################################################
# Starting from here you might need to edit the code #
######################################################


def get_largest_component_size(component_size_distribution):
    """Finds the largest component in the given component size distribution.

    Parameters
    ----------
    component_size_distribution : dict
       The component size distribution. See the function get_component_size_dist

    Returns
    -------
    The largest component size : int
    """
    dist = component_size_distribution
    max_size = max(dist.keys())
    return max_size


def get_susceptibility(component_size_distribution):
    """Calculates the susceptibility (as defined in ex. 4.1e)

    Parameters
    ----------
    component_size_distribution : dict
       The component size distribution. See the function get_component_size_dist

    Returns
    -------
    Susceptibility value : float
    """
    dist = component_size_distribution
    numerator = 0
    denominator = 0
    max_size = -1
    for size in dist:
        freq = dist[size]
        numerator += size**2 * freq
        denominator += size * freq
        
        if size > max_size:
            max_size = size
    
    numerator -= max_size**2
    denominator -= max_size
    
    return numerator/denominator



def get_component_size_dist(net):
    """Calculates the (unnormalised) component size distribution of a network.

    For example, if the input network has 1 component of size 5 nodes and
    3 components of size 10 nodes, then this function will return a dictionary:
    {5:1, 10:3}.

    Parameters
    ----------
    net : networkx.Graph object

    Returns
    -------
    Dictionary where keys are component sizes and values are the number of
    components of that size.
    """
    dist = {}
    
    components = nx.connected_components(net)
    for each_comp in components:
        size = len(each_comp)
        if size in dist:
            dist[size] += 1
        else:
            dist[size] = 1
    
    return dist

def create_er_network(net_size, avg_degree):
    """Creates a realisation of an Erdos-Renyi network.

    Parameters
    ----------
    net_size : int
       Number of nodes in the network.
    avg_degree : float
       The value of edge probability p is set such that this is the
       expected average degree in the network.

    Returns
    -------

    net: a network object

    """
    p = avg_degree / (net_size)# - 1)
    net = nx.fast_gnp_random_graph(n=net_size, p=p)
    return net

def ER_percolation(N, maxk, stepsize=0.1):
    """Builds ER networks with average degrees from 0 to maxk and
       plots the size of the largest connected component and susceptibility
       as a function of the average degree.

    Parameters
    ----------
    N : int
      Number of nodes in the ER network
    maxk : float
      The maximum average degree
    stepsize : float
      The size of the step after which the LCC and susceptibility is calculated.
      I.e., they are plotted at 0, stepsize, 2*stepsize, ..., maxk

    Returns
    -------
    fig : figure handle
    """

    klist = np.arange(0.0, maxk, stepsize)
    giantsize = []
    smallsize = []

    # Loop over the avg degree range
    for k in klist:
        # Generate an ER network with N nodes and avg degree k
        net = create_er_network(N, k)

        # Get the distribution of component sizes
        component_size_dist = get_component_size_dist(net)

        # Galculate the largest component size
        giantsize.append(get_largest_component_size(component_size_dist))

        # Calculate the avg component size for the other components
        smallsize.append(get_susceptibility(component_size_dist))



    # plot the numbers
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)

    ax.plot(klist, giantsize, 'r-')
    ax.set_xlabel('Average Degree') # TODO: label the axis!
    ax.set_ylabel('Largest Component Size') # TODO: label the axis!

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(klist, smallsize, 'k-')
    ax2.set_ylabel('Susceptibility')  # TODO: label the axis!
    ax2.set_xlabel('Average Degree')  # TODO: label the axis!

    fig.suptitle(f'Number of nodes = {N}')
    # plt.show() # uncomment if you want to display the figure on the screen

    return fig


def expand_breadth_first_search(network, visited_nodes, boundary_nodes):
    """Performs one step in a breadth first search and updates the visited nodes
    and boundary nodes sets that are given as parameters accordingly. Here one
    step means that we will find all nodes that are one step further away from
    the starting node. These nodes will form the new boundary.

    Parameters
    ----------
    network : networkx.Graph object
    visited_nodes : set object
      The set of nodes that are visited (including the boundary)
    boundary_nodes : set object
      The set of nodes that are in the boundary, i.e., the were visited in the last iteration.

    Returns
    -------
    Nothing, the visited nodes an boundary nodes are update in place.

    """
    new_boundary = set() # Nodes in the new boundary are added here

    # Go through all the nodes in the boundary, and add their neighbors
    # that are not visited to the new boundary. Remember to update
    # the visited_nodes as you go.
    for node in boundary_nodes:
        for nn in network.neighbors(node):
            if nn not in visited_nodes:
                new_boundary.add(nn)
                visited_nodes.add(nn)

    # Here we replace the old boundary with the new boundary
    boundary_nodes.clear()
    boundary_nodes.update(new_boundary)
    
    # void
    # We return nothing as the results were updated to visited_nodes and boundary_nodes


def ER_breadth_first_search(avg_degree, net_size, number_of_samples,
                            max_depth=15, show_netsize=False):
    """Creates a figure of breadth first search in an ER network.

    Parameters
    ----------
    avg_degree : float
      The expected degree of the nodes in the ER network
    net_size : int
      The number of nodes in the ER network
    number_of_samples : int
       The number of randomly selected starting node for the BFS
    max_depth : int
       The maximum depth of the BFS
    show_netsize : bool
       If True, we will plot the size of the network in the first panel as a dotter horizontal line.

    Returns
    -------
    fig : figure object
    """
    net = create_er_network(net_size, avg_degree)

    # We will count the number of nodes and the loop fraction for each depth and each
    # starting node. That is, we need a 2-dimensional list to save these results.
    # The element node_count[depth][sample_number] gives the number of nodes at the boundary
    # of the BFS at the given depth for given sample number.
    # The code below will create lists of length max_depth where each element is an empty list.
    node_count = [[] for depth in range(max_depth+1)]
    loop_edge_fraction = [[] for depth in range(max_depth+1)]

    # Next we will run the BFS until max_depth for each randomly selected sample
    for _sample_nr in range(number_of_samples):
        # Choose random starting node:
        start_node = random.randint(0, net_size-1)
        # In the beginning we have only visited the start node:
        visited_nodes = set([start_node])
        # The start node is also the only boundary node, see expand_breadth_first_search:
        boundary_nodes = set([start_node])

        for depth in range(max_depth+1):

            number_of_boundary_nodes = len(boundary_nodes)

            fraction_of_loop_edges = calculate_loop_edge_fraction(net,
                                                                  visited_nodes, boundary_nodes)

            # Update the visited nodes and the boundary
            expand_breadth_first_search(net, visited_nodes, boundary_nodes)

            # Saving the results
            node_count[depth].append(number_of_boundary_nodes)
            loop_edge_fraction[depth].append(fraction_of_loop_edges)

    # Averaging over the different starting nodes.
    avg_node_count = list(map(np.mean, node_count))
    avg_loop_edge_fraction = list(map(np.mean, loop_edge_fraction))

    # Calculating the theoretical values, assuming the network is a tree
    avg_node_count_theoretical = []
    for depth in range(max_depth+1):
        # Replace with the formula from 
        # calculate the expected number of nodes at d steps away,  
        #  n_d from a randomly selected node in an ER network
        k = avg_degree
        d = depth
        n = k**d
        avg_node_count_theoretical.append(n)

    #Plotting the results
    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(10,4))


    ax1, ax2 = axes
    plt.suptitle(f'Average degree:{avg_degree} Netsize:{net_size}')

    ax1.semilogy(list(range(max_depth+1)), avg_node_count, "x", label="Simulation")
    ax1.semilogy(list(range(max_depth+1)), avg_node_count_theoretical, label="Theoretical")

    if show_netsize:
        ax1.semilogy([0, max_depth], 2*[net_size], "k--")

    ax1.set_xlabel("Depth") # Set proper axis labels!
    ax1.set_ylabel("Average Node Count") # Set proper axis labels!
    ax1.set_xlim(0, max_depth)
    ax1.legend()


    ax2.plot(list(range(max_depth+1)), avg_loop_edge_fraction, "x", label="Simulation")
    ax2.set_xlabel("Depth") # Set proper axis labels!
    ax2.set_ylabel("Average Loop Edge Fraction") # Set proper axis labels!
    ax2.set_xlim(0, max_depth)
    ax2.set_ylim(0, 1)

    plt.show() # uncomment if you want to display the figure on the screen

    return fig

# =========================== MAIN CODE BELOW ==============================

if __name__ == "__main__":
    a_dir = "./assets"
    if not os.path.isdir(a_dir):
        os.mkdir(a_dir)
    
    #Solution for b)-c):
    fig = ER_breadth_first_search(0.5, 10**4, 10000)
    fig.savefig('./assets/er_breadthfirst_05_10k.pdf')

    fig = ER_breadth_first_search(1, 10**4, 10000)
    fig.savefig('./assets/er_breadthfirst_1_10k.pdf')

    fig = ER_breadth_first_search(2, 10**4, 100, show_netsize=True, max_depth=15)
    fig.savefig('./assets/er_breadthfirst_2_10k.pdf')

    fig = ER_breadth_first_search(0.5, 10**5, 10000)
    fig.savefig('./assets/er_breadthfirst_05_100k.pdf')

    fig = ER_breadth_first_search(1, 10**5, 10000)
    fig.savefig('./assets/er_breadthfirst_1_100k.pdf')

    fig = ER_breadth_first_search(2, 10**5, 100, show_netsize=True, max_depth=15)
    fig.savefig('./assets/er_breadthfirst_2_100k.pdf')

    #Solution for d)-e):
    ER_percolation(10**5, 2.5, 0.05)
    fig.savefig('./assets/er_percolation.pdf')
