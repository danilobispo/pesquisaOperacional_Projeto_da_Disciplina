import numpy as np

# Tamanho do vetor de nós clientes (5)
M = 5
# Gera um vetor de nós clientes de tamanho 5
vetor_origem = np.random.randint(low=1, high=20, size=M)
# Salva em um arquivo
np.savetxt("datasets/nodes/nos_clientes_array.txt", vetor_origem, fmt="%d")

# Tamanho do vetor de nós de destino (5)
N = 6
# Gera um vetor de nós servidores de tamanho 5
vetor_servidores = np.random.randint(low=1, high=20, size=N)
# Salva em um arquivo
np.savetxt("datasets/nodes/nos_servidores_array.txt", vetor_servidores, fmt="%d")
