import numpy as np
import pandas as pd

rio_correto = open("MainStreamPixel.txt", 'rb')
rio_errado = open("RioErrado.txt", 'rb')
inter_rios = open("InterRios.txt", 'rb')
mapa_elevacao = open("MapaElevacaoCorreta.txt", 'rb')

noData = -9999

dx = (-1, 0, 1, 1, 1, 0, -1, 0, 0)
dy = (1, 1, 1, 0, -1 - 1, -1, 0, 0)


def matriz(arq):
    m = []
    i = 0
    for lin in arq:
        if(i > 5):
            m.append([int(float(x)) for x in lin.split()])
        else:
            i += 1
    return m


def search_brother(origem, destino, brother, m):
    m[pos]


matriz_rio_correto = np.array(matriz(rio_correto))
matriz_rio_errado = np.array(matriz(rio_errado))
matriz_inter_rios = np.array(matriz(inter_rios))
matriz_mapa_elevacao = np.array(matriz(mapa_elevacao))

for r in range(matriz_rio_correto.shape[0]):
    for c in range(matriz_rio_correto.shape[1]):
        if(matriz_rio_correto[r, c] == noData):
            pass
        else:
            pass
