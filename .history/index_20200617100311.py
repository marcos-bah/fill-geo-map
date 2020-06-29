import numpy as np
import pandas as pd

rio_correto = open("MainStreamPixel.txt", 'rb')
rio_errado = open("RioErrado.txt", 'rb')
inter_rios = open("InterRios.txt", 'rb')
mapa_elevacao = open("MapaElevacaoCorreta.txt", 'rb')

noData = -9999
data = 1

dx = (1, 1, 1, 0, -1, -1, -1, 0)
dy = (-1, 0, 1, 1, 1, 0, -1, -1)

black_list = []


def matriz(arq):  # inicializa a matriz
    m = []
    i = 0
    for lin in arq:
        if(i > 5):  # descarta as 5 linhas iniciais
            m.append([float(x) for x in lin.split()])
        else:
            i += 1
    return m  # retorna um array


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
    for i in range(rows):
        for j in range(cols):
            if (m_inter[i, j] == data):
                m_saida.append([float(m_elevacao[i, j]), int(i-1), int(j)])
    return sorted(m_saida)


def carve_point(m_rio_correto, m_refer):
    array = []
    for i in range(len(m_refer)):
        x = int(m_refer[2][i])
        y = int(m_refer[1][i])
        print(x, y)
        for k in range(8):
            print(m_rio_correto[x+dx[k], y+dy[k]])
            if(m_rio_correto[x+dx[k], y+dy[k]] == -9999.0):
                print(x+dx[k], y+dy[k])
                array.append(0)
            else:
                array.append(1)
        return array


# cria os arrays e os transforma em np.array type
matriz_rio_correto = np.array(matriz(rio_correto))
matriz_rio_errado = np.array(matriz(rio_errado))
matriz_inter_rios = np.array(matriz(inter_rios))
matriz_mapa_elevacao = np.array(matriz(mapa_elevacao))

# pega o número de colunas e linhas, é padronizado para todos
rows = matriz_rio_correto.shape[0] - 1
cols = matriz_rio_correto.shape[1] - 1

matriz_elevacao_coodenadas = np.array(
    array_pits(matriz_inter_rios, matriz_mapa_elevacao))
df_matriz_elevacao_coodenadas = pd.DataFrame(matriz_elevacao_coodenadas)

df_matriz_elevacao_coodenadas.to_csv('output/saida-matriz.csv')
