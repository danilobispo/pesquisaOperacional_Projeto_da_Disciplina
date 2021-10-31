from ortools.linear_solver import pywraplp
import numpy as np

# Imports de diretórios do projeto
import datasets.nsfnet.nsfnet as nsfnet
import datasets.geant2.geant2 as geant2
import funcoes_auxiliares as faux

#
#
#
#
#
# Primeira parte do experimento: problema de associação
#
#
#
#
#

solver = pywraplp.Solver('problema de associação', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

# Primeira parte: Handshake entre as duas partes
# Problema de associação entre nós clientes e nós servidores
# Unbalanced assignment problem, pois M != N
# Parametrização
M = 5
N = 6

print("# Primeira parte do experimento: Problema de Associação \n"
      "# Primeira parte: Handshake entre as duas partes \n"
      "# Problema de associação entre nós clientes e nós servidores \n"
      "# Unbalanced assignment problem, já que M != N \n"
      "# Parametrização \n"
      "M = 5 ; N = 6")

# Vetor de nós clientes
clients_array = np.loadtxt("datasets/nodes/nos_clientes_array.txt", dtype=int)
# Vetor de nós servidores
servers_array = np.loadtxt("datasets/nodes/nos_servidores_array.txt", dtype=int)
# Debug
# print("vetor_clientes: ", clients_array)
print("Vetor de nós clientes: ", clients_array)
# print("vetor_servidores: ", servers_array)
print("Vetor de nós servidores: ", servers_array)

# Vetor de custos
# O vetor de input será a concatenação desses dois vetores
# Adicionamos um 0 ao vetor de clientes para igualar ao número de servidores
clients_array = np.concatenate((clients_array, [0]))
subtraction_array = np.reshape((clients_array, servers_array), (2, N))

# Debug
# print("subtraction_array: ", subtraction_array)

# A matriz de custo será o custo de cada nó para cada nó, ela será criada dinamicamente pelas diferenças entre os nós
# Se o custo for negativo, significa que o nó de destino possui mais capacidade
# Já se o custo for positivo, significa que o nó de origem possui menos capacidade
# e.g 14 - 17 = -3 && 17 - 14 = 3
# Acho que vou fazer com matriz de módulo (abs)
# Para otimizar essa relação, é necessária uma relação de minimização (Função objetivo)

# A matriz de custo será inicializada como zeros
cost_matrix = []

# Debug
# print(cost_matrix)

for j in range(N):
    for i in range(N):
        if subtraction_array[0][j] != 0:
            cost_matrix.append(abs(subtraction_array[0][j] - subtraction_array[1][i]))
        else:
            cost_matrix.append(9999)

cost_matrix = np.reshape(cost_matrix, (N, N))
print("Matriz de custo entre os nós de entrada e saída cij: \n", cost_matrix)

# Variáveis de decisão
# Variável com o tamanho NxN da matriz
x = [[solver.NumVar(0, solver.infinity(), "X%d%d" % (i, j)) for j in range(0, N)] for i in range(0, N)]

print("# Variáveis de decisão: \n"
      "# Variável com o tamanho NxN da matriz xij")

# Constraints
# Cada cliente terá um servidor dentre os N.

print("# Constraints \n"
      "# Cada cliente terá um servidor dentre os N.\n"
      "# Cada servidor terá 0 ou 1 cliente dentre os M")

print("# Objective function: \n"
      "# É uma função de minimização, onde queremos o menor custo (menor diferença entre nós de origem e destino)\n"
      "# Ou seja, minimização de xij*cij para i e j pertencentes a M e N")

head = 0
for i in range(N):
    ct = solver.Constraint(1, 1, '%d' % head)
    head = head + 1
    for j in range(N):
        ct.SetCoefficient(x[i][j], 1)

# Cada servidor terá um cliente dentre os M

head = 0
for j in range(0, N):
    ct = solver.Constraint(1, 1, '%d' % head)
    head = head + 1
    for i in range(N):
        ct.SetCoefficient(x[i][j], 1)

# Definição da objective function
objective = solver.Objective()
objective.SetMinimization()
for i in range(0, N):
    for j in range(0, N):
        objective.SetCoefficient(x[i][j], np.array(cost_matrix[i][j]).item())

solver.Solve()
solution_array = []
# Print da solução:
print("----------------------------------Resultado-----------------------------------------")
print('Solucao:')
print('Valor objetivo = %.d' % (solver.Objective().Value() - 9999))
for i in range(N):
    print('[', end='', sep='')
    for j in range(N):
        print(' %.d' % (x[i][j].solution_value()), sep=' ', end=' ')
        if x[i][j].solution_value() != 0 and i != N - 1:  # Se for a última linha, a gente ignora o valor
            solution_array.append([(
                i, j, np.minimum(clients_array[i], servers_array[j])),  # Posições de origem e destino e Valor máximo de
                # download/upload do nó
                x[i][j].solution_value()  # solution value
            ])
    print("]", sep='', end='\n')

# DEBUG
# print(solution_array)

#
#
#
#
#
#
# Fim da primeira parte do experimento
#
#
#
#
#
#
# Início da segunda parte do experimento
#
#
#
#
#

# Segunda parte: Problema de maximização
# Com os nos de entrada e saida definidos, podemos definir os constraints para cada caminho gerado
# Como prometido, as matrizes aleatórias geradas no passo anterior vão ser usadas.
# Serão usados dois grafos de topologias extraídas de https://knowledgedefinednetworking.org/
# São eles: NSFNet e GEANT2
# Vamos criar 3 matrizes aleatórias a partir da matriz de conectividade (não-direcionada) atribuindo custos
# diferentes para cada uma delas (esse passo foi realizado no gerador_de_matrizes.py)
# Em seguida, os nós de source e target serão mapeados por dicionários inventados nas variáveis

print("\n\n# Segunda parte: Problema de maximização\n"
      "# Com os nos de entrada e saida definidos, podemos definir os constraints para cada caminho gerado\n"
      "# As matrizes aleatórias geradas no passo anterior vão ser usadas.\n"
      "# Serão usados dois grafos de topologias extraídas de https://knowledgedefinednetworking.org/\n"
      "# São eles: NSFNet e GEANT2\n"
      "# Vamos criar 3 matrizes aleatórias a partir da matriz de conectividade (não-direcionada) atribuindo custos\n"
      "# diferentes para cada uma delas (esse passo foi realizado no gerador_de_matrizes.py)\n"
      "# Em seguida, os nós de source e target serão mapeados por dicionários inventados nas variáveis\n")

flow_cost_matrix = []
dataSetNSFNet = faux.load_random_matrices_from_files("nsfnet")
dataSetGEANT2 = faux.load_random_matrices_from_files("geant2")

# Como temos 5 nós clientes e isso é fixo, podemos fazer um loop ainda mais interno que vasculha todos os
# nós de origem e destino
for z in range(0, 2):  # Duas topologias diferentes
    if z == 0:
        dataset = np.copy(dataSetNSFNet)
    else:
        dataset = np.copy(dataSetGEANT2)
    for k in range(0, 3):  # Três matrizes diferentes
        print("--------------------------------------- Matriz utilizada: ---------------------------------------------")
        print("datasets/nsfnet/connect_matrix_nsfnet_%d.txt" % k) if z == 0 else \
            print("datasets/geant2/connect_matrix_geant2_%d.txt" % k)
        for t in range(5):  # Para 5 clientes diferentes
            solver = pywraplp.Solver('problema de maximização', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
            # Parâmetros
            # Nó de origem (Source node) e Nó de destino (Target node)
            source_node, target_node, max_value = solution_array[t][0]
            # Debug
            print("----------------------------------------------- Parâmetros------------------------------------------"
                  "\n# Nó de origem (Source node) e Nó de destino (Target node)")
            print("# Valor máximo da função objetivo: ", max_value)
            print("# source_node: ", source_node)
            print("# target_node: ", target_node)

            if z == 0:
                source_node = nsfnet.source_dict[source_node]
                target_node = nsfnet.target_dict[target_node]
            else:
                source_node = geant2.source_dict[source_node]
                target_node = geant2.target_dict[target_node]
            # Debug
            print("nó de origem no grafo: ", source_node)
            print("nó de destino no grafo: ", target_node)


            flow_cost_matrix = np.copy(dataset[k])
            print(flow_cost_matrix)

            # Como a matriz de conectividade é necessariamente quadrada, vamos pegar o size e armazenar em N
            M, N = np.shape(dataset[k])
            # Debug
            # print("Size M: ", M)
            # print("Size N: ", N)

            # Matriz de conectividade máxima
            c = flow_cost_matrix

            # print("c: ", c)

            # Criando a aresta abstrata
            c[target_node][source_node] = max_value

            # Matriz de conectividade mínima (Será 0 no nosso caso)
            b = [[0 for j in range(N)] for i in range(N)]

            # Debug
            # print("Matriz de conectividade máxima: %d\n" % np.array(c))
            # print([[c[i][j] for j in range(N)] for i in range(N)])

            # Restrições
            # Matriz de variáveis numéricas para representar os valores de vazão
            # bij <= xij <= cij para todos os i,j em N tal que i é diferente de T e j é diferente de S
            x_part2 = [[solver.NumVar(b[i][j], c[i][j], "x%d%d" % (i, j)) for j in range(N)] for i in range(N)]

            # Debug
            # print(len(x_part2))

            for i in range(N):
                ct = solver.Constraint(0, 0, str("Divergência do meio do caminho"))
                # Para todos os nós intermediários:
                if i != target_node or i != source_node:
                    for j in range(N):
                        ct.SetCoefficient(x_part2[i][j], 1)
                        ct.SetCoefficient(x_part2[j][i], -1)
                # tudo que sai menos tudo que entra é igual a 0 (igual ao shortest path)
                # Para o nó de entrada: apenas arestas saindo, logo
                # A somatória de tudo que sai do nó de origem menos a aresta abstrata é igual a 0 para i = S
                elif i == source_node:
                    ct.SetCoefficient(x_part2[target_node][source_node], -1)
                # Para o nó de saída: apenas arestas entrando, logo
                # A somatória NEGATIVA de tudo que entra do nó de origem mais a aresta abstrata é igual a 0 para i = T
                elif i == target_node:
                    ct.SetCoefficient(x_part2[target_node][source_node], 1)

            # Função objetivo
            # Maximizar a aresta abstrata ( Max xts )
            objective = solver.Objective()
            objective.SetMaximization()
            objective.SetCoefficient(x_part2[target_node][source_node], 1)

            solver.Solve()

            # Vamos guardar os valores de cada dataset em vetores, a fim de organizá-los em arquivos para visualizar
            # melhor os resultados
            vetor_resultados_nsfnet = []
            vetor_resultados_geant2 = []

            # Para cada dataset, temos a matriz k e o t respectivo com seus (i,j)
            # vetor_resultados_nsfnet[k][t] =


            # Print da solução:
            print("----------------------------------Resultado-----------------------------------------")
            print('Solucao:')
            print('Valor objetivo = %.1f' % (solver.Objective().Value()))
            for i in range(0, N):
                for j in range(0, N):
                    if x_part2[i][j].solution_value() != 0:
                        if i == target_node and j == source_node:
                            c[i][j] = -1.00
                            print('X[%d,%d]=%d de MAX_CAP: %.2f' % (i, j, x_part2[i][j].solution_value(), c[i][j]))
                        else:
                            print('X[%d,%d]=%d de MAX_CAP: %.2f' % (i, j, x_part2[i][j].solution_value(), c[i][j]))
