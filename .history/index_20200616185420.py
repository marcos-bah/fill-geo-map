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


matriz_rio_correto = np.array(matriz(rio_correto))
matriz_rio_errado = np.array(matriz(rio_errado))
matriz_inter_rios = np.array(matriz(inter_rios))
matriz_mapa_elevacao = np.array(matriz(mapa_elevacao))

rows = matriz_rio_correto.shape[0]
cols = matriz_rio_correto.shape[1]

ctt = 0

for j in range(cols, 0, -1):
    for i in range(rows, 0, -1):
        if(matriz_inter_rios[i, j] == data):
            ctt += 1
            if(ctt % 2 == 0):
                print("Par")
                print([i, j])
                print("Distancia")
                print(search_brother(origem, [i, j], matriz_rio_correto))
            else:
                print("impar")
                origem = [i, j]
                print(origem)
