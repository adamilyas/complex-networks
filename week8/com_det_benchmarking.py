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
import numpy as np
from math import log

# This function allows you to use log2(x) later in the code instead of log(x, 2)
log2 = lambda x: log(x, 2)

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============


def get_n_nodes(cmtys):
    """
    Calculates the total number of nodes in a network based on a given partition
    (set of communities).

    INPUT:
    cmtys: partition, communities presented as a dictionary of
    community_label:community where community is a list of nodes in the community

    OUTPUT:
    n: total number of nodes in the network (float)
    """
    n = 0
    for _cmty_label, cmty in cmtys.items():
        n += len(cmty)
    return float(n)

def mutual_information(cmtys1, cmtys2):
    """
    Calculates mutual information between two partitions.

    INPUT:
    cmtys1: partition 1, communities presented as a dictionary of
    community_label:community where community is a list of nodes in the community
    cmtys2: partition 2, communities presented as a dictionary of
    community_label:community where community is a list of nodes in the community

    OUTPUT:
    MI: mutual information between cmtys1 and cmtys2
    """
    MI = 0.0
    N = get_n_nodes(cmtys1)
    assert N == get_n_nodes(cmtys2)
    for c1name, c1nodes in cmtys1.items():
        for c2name, c2nodes in cmtys2.items():
            n1 = len(c1nodes)
            n2 = len(c2nodes)
            n_shared = len(set(c1nodes) & set(c2nodes))
            if n_shared == 0:
                continue
            MI += (n_shared / float(N)) * log2(n_shared * N / float(n1 * n2))
    return MI


def entropy(cmtys):
    """
    Calculates the entropy of a partition.

    INPUT:
    cmtys: partition, communities presented as a dictionary of
    community_label:community where community is a list of nodes in the community

    OUTPUT:
    H: entropy of cmtys
    """
    H = 0.0
    N = get_n_nodes(cmtys)
    for cnodes in cmtys.values():
        n = len(cnodes)
        if n == 0:
            continue
        H += n / N * log2(n / N)
    H = -H
    return H


def vi(cmtys1, cmtys2):
    """
    Calculates variation of information between two partitions. The smaller the
    variation of information is, the more similar are the partitions.

    INPUT:
    cmtys1: partition 1, communities presented as a dictionary of
    community_label:community where community is a list of nodes in the community
    cmtys2: partition 2, communities presented as a dictionary of
    community_label:community where community is a list of nodes in the community

    OUTPUT:
    VI: variation of information
    """
    VI=entropy(cmtys1)+entropy(cmtys2)-2*mutual_information(cmtys1,cmtys2)
    return VI

def load_coms(fname):
    """
    Reads in a community structure to a dictionary.
    In the file corresopnding to fname, each row is expected to contain
    one network module.
    Lines starting with a # are treated as comment lines, and are omitted.

    This is the format provided by Jako when "One line per community" is selected.

    INPUT:
    fname : str
        path to a filename, for example "resultdir/mynet_infomap.txt"

    OUTPUT:
    coms : dict
        coms[i] = list of nodes

    No further sanity checks are performed.
    """
    coms = {}
    with open(fname, "r") as f:
        # comment lines:
        line = f.readline()
        i = 0
        while line:
            if line[0] == "#":
                line = f.readline()
                continue
            com = line.split()
            coms[i] = [int(com_elem) for com_elem in com]
            i += 1
            line = f.readline()
    return coms

# =========================== MAIN CODE BELOW ==============================

if __name__ == "__main__":
    # First step: testing the code:
    test1 = {1:[1, 2, 3, 4, 5, 6, 7, 8, 9], 2:[10, 11, 12]}
    test2 = {1:[1, 2, 3, 4, 5, 6, 7], 2:[8, 9, 10], 3:[11, 12]}

    print(vi(test1, test2))
    
    filenames = [
      'lfr100.cmtys',
      'infomap.cmtys',
      'girvan.cmtys',
      'louvain.cmtys',
      'block.cmtys']

    models = [load_coms(fn) for fn in filenames]

    names =['Ground', 'Infomap', 'Girvan-Newman', 'Louvain', 'Stochastic block model']
    for model1,name1 in zip(models, names):
        for model2,name2 in zip(models, names):
            if model1 == model2:
                continue
            result = round(float(vi(model1, model2)),3)
            print(f"{name1} vs {name2}: {result}")  
