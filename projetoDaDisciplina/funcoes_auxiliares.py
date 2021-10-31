import numpy as np
import datasets as ds
import funcoes_auxiliares as faux

def loadnfsnetmatrix():
    nsfnet_connect_matrix = np.loadtxt("datasets/nsfnet/nsfnet_graph.txt")
    # print(nsfnet_connect_matrix)
    return nsfnet_connect_matrix


def loadgeant2matrix():
    geant2_connect_matrix = np.loadtxt("datasets/geant2/geant2_graph.txt")
    # print(geant2_connect_matrix)
    return geant2_connect_matrix

def load_random_matrices_from_files(name):
    flow_cost_matrix = []
    matrix_list = []
    for i in range(0, 3):
        flow_cost_matrix.append(np.loadtxt("datasets/%s/connect_matrix_%d_%s.txt" % (name, i, name)))
        matrix_list.append(flow_cost_matrix[i])
        # Debug
        # print("flow_cost_matrix %d: \n" % i, np.array(flow_cost_matrix[i]))
        # print("Dataset atual: connect_matrix_%d_%s.txt" % (name))
    return matrix_list