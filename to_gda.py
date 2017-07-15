__author__ = 'lisette.espin'

#############################################################################
# DEPENDENCIES
#############################################################################
import sys
import os
from scipy.io import loadmat
import networkx as nx
import numpy as np
import pandas as pd

#############################################################################
# CONSTANTS
#############################################################################

MISSINGVALUECODE = '?'

#############################################################################
# FUNCTIONS
#############################################################################

def load_mat(fn,classname,missingvaluecode):
    obj = loadmat(fn)
    graph = nx.from_scipy_sparse_matrix(obj['A'])
    # renaming nodes
    mapping = {n:'node{}'.format(n + 1) for n in graph.nodes()}
    graph = nx.relabel_nodes(graph, mapping)
    # attributes
    attribute_names = ['status', 'gender', 'major', '2major', 'dorm', 'year', 'highschool']
    nodes = pd.DataFrame(np.array(obj['local_info']), index=graph.nodes(), columns=attribute_names)
    nodes.index.name = 'Name'
    # missing values as ?
    nodes.replace(missingvaluecode,MISSINGVALUECODE,inplace=True)
    # class goes as last column
    cols = list(attribute_names)
    del(cols[cols.index(classname)])
    cols.append(classname)
    nodes = nodes[cols]
    # removing nodes with missing values in class
    try:
        toremove = nodes[nodes[classname] == '?'].index
        nodes = nodes.drop(toremove)
        graph.remove_nodes_from(toremove.values)
    except:
        pass
    # removing singletons
    toremove = [n for n in graph.nodes() if graph.degree(n)==0]
    graph.remove_nodes_from(toremove)
    print(nx.info(graph))
    return nodes,graph

def write_nodes(nodes,classname,networkfn,output):
    fn = networkfn.split('/')[-1].split('.')[0]
    fn = os.path.join(output,'{}-{}-nodes.gda'.format(fn,classname))
    nodes.to_csv(fn,header=True)

def write_edges(graph,classname,networkfn,output):
    fn = networkfn.split('/')[-1].split('.')[0]
    fn = os.path.join(output, '{}-{}-edges.gda'.format(fn,classname))
    edges = ['link{},{}'.format(edge_id+1,node) for edge_id, edge in enumerate(graph.edges()) for node in edge]
    with open(fn,'w') as f:
        f.write('link,entity\n')
        f.write('\n'.join(edges))

#############################################################################
# MAIN
#############################################################################
if __name__ == '__main__':
    fn = sys.argv[1]
    classname = sys.argv[2]
    missingvaluecode = sys.argv[3]
    output = sys.argv[4]
    nodes = None
    graph = None

    if os.path.exists(fn):
        ext = fn.endswith('.mat')
        if ext:
            nodes,graph = load_mat(fn,classname,missingvaluecode)
        else:
            print('{} NOT supported.'.format(ext))

        if nodes is not None and graph is not None:
            print('graph succesfully loaded!')
            write_nodes(nodes,classname,fn,output)
            print('nodes saved!')
            write_edges(graph,classname,fn,output)
            print('edges saved!')