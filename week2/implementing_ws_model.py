# By Adam

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
import random

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============

def ring(n, m):
    """
    This function creates the basic ring (to be rewired) with n nodes
    in which each node is connected to m nodes on the left and right.

    Parameters
    ----------
    n : int
      Number of nodes
    m : int
      Number of neighbors to connect left and right

    Returns
    -------
    network : graph
             The basic ring before rewiring
    """
    network = nx.Graph()
    span = int(m/2)

    for node in range(n):
        network.add_node(node)

    for node in range(n):
        for reach in range(-1*span, span+1):
            if span != 0:
                neighbour_node = node + reach
                if neighbour_node < 0:
                    neighbour_node = n - neighbour_node
                if neighbour_node >= n:
                    neighbour_node = neighbour_node - n
                network.add_edge(node, neighbour_node)

    return network

def ws(n, m, p):
    """
    This function call the ring() function to make a basic ring and then
    rewires each link with  probability p and also prints the total number of
    links and the number of rewired links.
    Note self-loops are not allowed when rewiring (check that you do not rewire
    the end of a link to the node at its other end!) 

    Parameters
    ----------
    n : int
      Number of nodes
    m : int
      Number of neighbors to connect left and right
    p : float
        Rewiring probability

    Returns
    -------
    network : graph
        The Watts-Strogatz small-world network

    """
    network = ring(n, m)
    all_edges = list(network.edges()) # same as copy
    
    rewired_num = 0 # tracks the number of rewired links
    total_num = len(all_edges) # tracks the total number of links in the network


    
    for edges in all_edges:
        if np.random.rand() < p:
            rewired_num += 1
            # rewire
            u, v = edges
            network.remove_edge(u, v)
            other_node = random.choice(list(nx.non_neighbors(network, u)))
            network.add_edge(u, other_node)
            
    print("total number of links:")
    print(total_num)
    print("number of rewired links:")
    print(rewired_num)
    return network

# =========================== MAIN CODE BELOW ==============================

if __name__ == "__main__":
    np.random.seed(42)
    #visualizing the rings for p = 0 ...
    graph1 = ring(15, 2)
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    nx.draw_circular(graph1)

    figure_filename = 'Small_world_ring.pdf'


    fig1.savefig(figure_filename)
    # or just use plt.show() and save manually

    total_num_edges = len(list(graph1.edges()))
    print("Total number of edges for n = 15, m = 2, p = 0 :")
    print(total_num_edges)
    #... and p = 0.5
    graph2 = ws(100, 2, 0.5)
    fig2 = plt.figure()
    ax = fig2.add_subplot(111)
    nx.draw_circular(graph2, node_size=20)

    figure_filename = './Small_world_rewired.pdf'


    fig2.savefig(figure_filename)
    # or just use plt.show() and save manually

    # Produce the basic ring network and calculate the average clustering
    # coefficient and average shortest path of the network
    basic_ring = ring(1000, 5)

    c_basic = nx.average_clustering(basic_ring)
    l_basic = nx.average_shortest_path_length(basic_ring)

    probability = [0.001*(2**n) for n in range(11)] #[0.001, 0.002, 0.004, ...]
    relative_c = []
    relative_l = []

    for p in probability:
        smallworld = ws(1000, 5, p)

        # gets all connected components; mostly there is just one:
        components = nx.connected_component_subgraphs(smallworld)

        # finds the largest to be used for the average path length:
        largest_component = max(components, key=len)

        c_rewired = nx.average_clustering(smallworld)
        l_rewired = nx.average_shortest_path_length(largest_component)
        print('c_rewired ', c_rewired)
        print('l_rewired ', l_rewired)

        # Update relative_c and relative_l
        relative_c.append( c_rewired / c_basic )
        relative_l.append( l_rewired / l_basic )

    fig3 = plt.figure()
    ax = fig3.add_subplot(111)
    ax.semilogx(probability, relative_c, marker='o', ls='', color='b',
                label='relative average cluster coefficient')
    ax.semilogx(probability, relative_l, marker='o', ls='', color='r',
                label='relative average shortest path')

    plt.ylabel("Logarithmic Axis")
    plt.xlabel("p")

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2),
              ncol=3, fancybox=True, shadow=True)

    figure_filename = 'WS_relative_c_and_l.pdf'


    fig3.savefig(figure_filename)

    # or just use plt.show() and save manually
