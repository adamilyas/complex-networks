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

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============


###############################################################
# Code that is given to you, and does not need to be modified #
###############################################################

def plot_network_usa(net, xycoords, bg_figname, edges=None, alpha=0.3):
    """
    Plot the network usa.

    Parameters
    ----------
    net : the network to be plotted
    xycoords : dictionary of node_id to coordinates (x,y)
    edges : list of node index tuples (node_i,node_j),
            if None all network edges are plotted.
    alpha : float between 0 and 1, describing the level of
            transparency
    """
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 0.9])
    # ([0, 0, 1, 1])
    img = plt.imread(bg_figname)
    axis_extent = (-6674391.856090588, 4922626.076444283,
                   -2028869.260519173, 4658558.416671531)
    ax.imshow(img, extent=axis_extent)
    ax.set_xlim((axis_extent[0], axis_extent[1]))
    ax.set_ylim((axis_extent[2], axis_extent[3]))
    ax.set_axis_off()
    nx.draw_networkx(net,
                     pos=xycoords,
                     with_labels=False,
                     node_color='k',
                     node_size=5,
                     edge_color='r',
                     alpha=alpha,
                     edgelist=edges)
    return fig, ax
######################################################
# Starting from here you might need to edit the code #
######################################################


# =========================== MAIN CODE BELOW ==============================

if __name__ == '__main__':
    csv_path = './US_airport_id_info.csv'
    network_path = "./aggregated_US_air_traffic_network_undir.edg"
    bg_figname = './US_air_bg.png'

    id_data = np.genfromtxt(csv_path, delimiter=',', dtype=None, names=True)
    xycoords = {}
    for row in id_data:
        xycoords[str(row['id'])] = (row['xcoordviz'], row['ycoordviz'])
    net = nx.read_weighted_edgelist(network_path)
    print(f'No. of nodes: {len(nx.nodes(net))}')
    print(f'No. of edges: {len(nx.edges(net))}')
    print(f'Density: {nx.density(net)}')
    print(f'Diameter: {nx.diameter(net)}')
    print(f'Avg. clustering: {nx.average_clustering(net)}')
    fig = plot_network_usa(net, xycoords, bg_figname)
    min_st = list(nx.minimum_spanning_edges(net))
    fig1 = plot_network_usa(net, xycoords, bg_figname, min_st)
    plt.suptitle("Minimal spanning tree", size=20)

    max_st = list(nx.maximum_spanning_edges(net))
    fig2 = plot_network_usa(net, xycoords, bg_figname, max_st)
    plt.suptitle("Maximal spanning tree", size=20)    
    
    temp_net = net.copy()
    for (u,v,d) in temp_net.edges(data=True):
        d['weight']=-d['weight']#edge['weight']
    edges2 = list(nx.minimum_spanning_edges(temp_net))
    max_st2 = list(nx.maximum_spanning_edges(net))
    fig2 = plot_network_usa(net, xycoords, bg_figname, max_st2)
    plt.suptitle("Maximal spanning tree by negating the weights", size=20)
    
     # for maximal
    max_m = len(max_st)
    edges_max_st = sorted(net.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    plot_network_usa(net, xycoords, bg_figname, edges_max_st[:max_m])
    plt.suptitle(f'Strongest {max_m} links (maximal spanning tree)', size=20)
    
    count = 0
    for e1 in edges_max_st:
        for e2 in max_st:
            if e1 == e2:
                count+=1

    print(f'count: {count}')