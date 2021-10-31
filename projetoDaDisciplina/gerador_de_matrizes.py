import numpy as np
import funcoes_auxiliares as faux

# Valor min-max
minimum_value = 1
maximum_value = 5
# Loop que gera as 3 matrizes:

nfsnet_connectivity_matrix = faux.loadnfsnetmatrix()
geant2_connectivity_matrix = faux.loadgeant2matrix()

for s in range(0, 2):
    if s == 0:  # Gera matriz do GEANT2
        param = geant2_connectivity_matrix
        name = "geant2"
        print("Tamanho da matriz de conectividade geant2: ", len(param))
    else:
        param = nfsnet_connectivity_matrix
        name = "nsfnet"
        print("Tamanho da matriz de conectividade nfsnet: ", len(param))

    print("A matriz de conectividade é: ", param)
    for k in range(0, 3):
        random_matrix = np.copy(param)
        for i in range(len(param)):
            for j in range(len(param)):
                if param[i][j] == 1:
                    val = np.random.randint(low=minimum_value, high=maximum_value)
                    print(val)
                    random_matrix[i][j] = val

        # Debug
        for i in range(len(param)):
            print('[', end='', sep='')
            for j in range(len(param)):
                print(' %d' % (random_matrix[i][j]), sep=' ', end=' ')
            print("]", sep='', end='\n')
        if name == "geant2":
            np.savetxt('datasets/geant2/connect_matrix_%d_%s.txt' % (k, name), random_matrix, fmt="%d")
        else:
            np.savetxt('datasets/nsfnet/connect_matrix_%d_%s.txt' % (k, name), random_matrix, fmt="%d")
        # print("param agora: ", param)
