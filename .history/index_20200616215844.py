import numpy as np
import pandas as pd

rio_correto = open("MainStreamPixel.txt", 'rb')
rio_errado = open("RioErrado.txt", 'rb')
inter_rios = open("InterRios.txt", 'rb')
mapa_elevacao = open("MapaElevacaoCorreta.txt", 'rb')

noData = -9999
data = 1

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


def search_brother(origem, destino, m):
    contador = 0
    v = True
    while(v):
        for i in range(len(dx)):
            r = origem[0]+dx[i]
            c = origem[0]+dy[i]
            if m[r, c] == data:
                contador += 1
                origem[0] += dx[i]
                origem[1] += dy[i]
                if(origem[0]+dx[i], origem[1]+dy[i] == destino):
                    v = False

    return contador


def change_column(m1, m2):
    for i in range(cols):
        for j in range(rows):
            if m1[i, j] > 0:
                for k in range(cols):
                    if(m2[i, k] > 0):
                        pass


def array_pits(m_inter, m_elevacao):
    m_saida = []
    print(m_elevacao.shape)
    print(rows)
    for i in range(rows):
        print(i)
        for j in range(cols):
            if (m_inter[i, j] == data):
                #print(m_elevacao[i, j])
                m_saida.append([m_elevacao[i, j], i, j])
    return sorted(m_saida)


matriz_rio_correto = np.array(matriz(rio_correto))
matriz_rio_errado = np.array(matriz(rio_errado))
matriz_inter_rios = np.array(matriz(inter_rios))
matriz_mapa_elevacao = np.array(matriz(mapa_elevacao))

rows = matriz_rio_correto.shape[0] - 1
cols = matriz_rio_correto.shape[1] - 1

ctt = 0

print(array_pits(matriz_inter_rios, matriz_mapa_elevacao))
