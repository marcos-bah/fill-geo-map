import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
import math as m

noData = -9999
data = 1

dx = (1, 1, 1, 0, -1, -1, -1, 0, 2, 2, 2, 2, 2,
      1, 0, -1, -2, -2, -2, -2, -2, -1, 0, 1)
dy = (-1, 0, 1, 1, 1, 0, -1, -1, -2, -1, 0, 1,
      2, 2, 2, 2, 2, 1, 0, -1, -2, -2, -2, -2)


def matriz(arq):  # inicializa a matriz
    start = ""
    m = []
    i = 0
    for lin in arq:
        if(i > 5):  # descarta as 5 linhas iniciais
            m.append([float(x) for x in lin.split()])
        else:
            start += str(lin).replace("b'", "").replace("\\n'", "\n")
            i += 1
    return m, start  # retorna um array


def array_pits(m_inter, m_elevacao):  # metodo que retorna x, y e z do ponto de conexão
    m_saida = []
    for i in range(rows):
        for j in range(cols):
            if (m_inter[i, j] == data):
                m_saida.append([float(m_elevacao[i, j]), int(i), int(j)])
    return sorted(m_saida)


def point_init(m_inicial):  # retorna o ponto inicial para analise
    for i in range(rows):
        for j in range(cols):
            if (m_inicial[i, j] == data):
                return [i, j]


# metodo para escavar os pontos de conexão
def carve_point(init_point, m_rio_correto, m_refer, lim=3000):
    vizinhos = []
    black_list = []

    n_vizinhos = 0

    ctt = 0

    x, y = init_point

    while(ctt < lim):  # limita a qauntidade de pontos escavados
        # print("Verificando ponto: ", x-1, ',', y)
        for k in range(24):
            if(m_rio_correto[x+dx[k], y+dy[k]] == noData):  # verifica se dado é -9999
                # adiciona 0 e segue a procura pelo vizinho
                vizinhos.append(0)
                pass
            # verifica se vizinho está na black-list e o ignora
            elif([x+dx[k], y+dy[k]] in black_list):
                pass
            else:  # agora se sabe que esse vizinho possui valor 1
                vizinhos.append(1)  # adiciona 1 no vizinho
                n_vizinhos += 1
                # adiciona sua posição na blacklist
                black_list.append([x+dx[k], y+dy[k]])
                x, y = x+dx[k], y+dy[k]  # x e y assume novos valores
                # print("\n")
                # print("__________________________________________________\n")
                # vizinhos.clear()
                # print("Número de Vizinhos", n_vizinhos)
                # print("__________________________________________________\n")
                break
        ctt += 1
        # print(n_vizinhos)
    # print("Lista Negra:", black_list[-1:])
    return np.array(black_list)

# metodo para escavar os pontos de conexão


def carve_point_z(init_point, m_rio_correto, m_refer, lim=2000):
    vizinhos = []
    black_list = []
    z_list = []

    n_vizinhos = 0

    ctt = 0

    x, y = init_point

    while(ctt < lim):  # limita a qauntidade de pontos escavados
        for k in range(24):
            if(m_rio_correto[x+dx[k], y+dy[k]] == noData):  # verifica se dado é -9999
                # adiciona 0 e segue a procura pelo vizinho
                vizinhos.append(0)
                pass
            # verifica se vizinho está na black-list e o ignora
            elif([x+dx[k], y+dy[k]] in black_list):
                pass
            else:  # agora se sabe que esse vizinho possui valor 1
                vizinhos.append(1)  # adiciona 1 no vizinho
                n_vizinhos += 1
                # adiciona sua posição na blacklist
                black_list.append([x+dx[k], y+dy[k]])
                z_list.append(m_rio_correto[x+dx[k], y+dy[k]])
                x, y = x+dx[k], y+dy[k]  # x e y assume novos valores
                vizinhos.clear()
                break
        ctt += 1
    return np.array(z_list)


# trata a matriz referencia para tirar eventuais pontos que não foram mapeados no caminho
def pre_tratamento(m_refeer, m_all):
    m_saida = []
    for i in m_refeer:
        for j in m_all:
            if([i[0], i[1]] == [j[0], j[1]]):
                m_saida.append([i[0], i[1]])
    return m_saida


# usa das matrizes referencia e caminho para traçar a distancia entre dois pontos de referencia
def distancia_referencia(m_refeer, m_all, zero=-1):
    i = 0
    distancia = []
    d = 0
    for j in range(len(m_all)):
        try:
            if([int(m_refeer[i][0]), int(m_refeer[i][1])] == [m_all[j][0], m_all[j][1]]):
                if(d == zero):
                    d = 0
                    i += 1
                else:
                    distancia.append([m_all[j][0], m_all[j][1], d])
                    d = 0
                    i += 1
            else:
                d += 1
        except Exception as err:
            pass

    return np.array(distancia)


def distan_refer_xyz(m_distance_r, m_elev_cood):
    m_saida = []
    for i in m_distance_r:
        for j in m_elev_cood:
            if([i[0], i[1]] == [j[1], j[2]]):
                m_saida.append([j[0], i[0], i[1], i[2]])
    return sorted(m_saida)


def inter_maps(m_map1, m_map2):
    m_saida = np.zeros((rows, cols), dtype=np.float64)
    for i in range(rows):
        for j in range(cols):
            if(m_map1[i][j] == m_map2[i][j] and m_map1[i][j] == data):
                m_saida[i][j] = data
            else:
                m_saida[i][j] = noData
    return m_saida


def pre_tratamento_referencia(m_ref1, m_ref2, m_ref):
    m_saida = []
    for i in m_ref1:
        for j in m_ref2:
            if([i[0], i[1]] == [j[0], j[1]]):
                if(i[2] == 0 or j[2] == 0):
                    m_saida.append(
                        [m_ref[i[0], i[1]], i[0], i[1], i[2], j[2], 0])
                else:
                    m_saida.append(
                        [m_ref[i[0], i[1]], i[0], i[1], i[2], j[2], (i[2]/j[2])])
    return np.array(m_saida)


def pos_matriz(matriz, start, end):
    for i in range(len(matriz)):
        if([matriz[i][0], matriz[i][1]] == [start[0], start[1]]):
            s = i
        if([matriz[i][0], matriz[i][1]] == [end[0], end[1]]):
            e = i
    return s, e


def gen_map(m):
    m_saida = np.zeros((rows, cols), dtype=np.float64)
    k = 0
    for i in range(rows):
        for j in range(cols):
            m_saida[i][j] = noData

    for i in range(len(m)):
        m_saida[int(m[i][0])][int(m[i][1])] = m[i][2]

    return m_saida


def conn_maps(joinMap, m_caminho, elevacao, m_caminho_elevacao):
    '''
        JoinMap possui o X, Y, Z e diferenças entre cada ponto de refrencia
        m_caminho possui todos os caminhos que devem ser preenchidos
        elevacao possui todos os Z do caminho oficial
    '''

    xyz = np.array(joinMap[['X', 'Y', 'Z']])
    r = np.array(joinMap[['D/d']])
    j = 0
    k = 1
    cont_inter = 0
    m_saida = []

    '''
        Preencher Z vazios com corespondencia,
        buscando relação entre caminho e altitude,
        preservando o grafico do Z original
    '''

    s, e = pos_matriz(m_caminho, start=[xyz[0][0], xyz[0][1]], end=[
                      xyz[-1][0], xyz[-1][1]])  # inicializando ponto de coleta
    for i in m_caminho[s:e+1]:
        try:
            # no ponto de conexao o x, y são iguais, então recebe z
            if([i[0], i[1]] == [xyz[j][0], xyz[j][1]]):
                m_saida.append([i[0], i[1], xyz[j][2]])
                j += 1
                k = 1
            else:
                s, e = pos_matriz(m_caminho_elevacao,
                                  xyz[j-1][0:2], xyz[j][0:2])
                elevs = elevacao[s+1:e]
                if(r[j][0] != 0):
                    if(m_saida[-1][2] == elevs[m.trunc(k / r[j][0])]):
                        m_saida.append([i[0], i[1], None])
                    else:
                        m_saida.append(
                            [i[0], i[1], elevs[m.trunc(k / r[j][0])]])
                    k += 1
                else:
                    m_saida.append([i[0], i[1], None])
        except Exception as err:
            m_saida.append([i[0], i[1], None])
            pass

    return np.array(m_saida)


def fill_void(m_conn_maps):  # função trabalha com matriz que possui valores nulos em sua base
    '''
        A função vai preencher os valores vazios que permaneceram
    '''
    ctt = 0
    m_saida = []
    for i in range(len(m_conn_maps)):
        if(m_conn_maps[i][2] == None):  # verifica se é nulo
            # se for, pega o valor anterior não nulo
            start = m_conn_maps[i-1][2]
            if(start == None):  # se for nulo, significa que a função já preencheu ele
                pass
            else:
                # faz uma varredura até o ultimo elemento
                for j in range(i, len(m_conn_maps)):
                    ctt += 1  # contador para o número de valores nulos entre não nulos
                    if(m_conn_maps[j][2] != None):  # até encontrar um não nulo
                        # pega o primeiro não nulo para fazer média
                        end = m_conn_maps[j][2]
                        if(start == end):  # se forem iguais, significa ou erro da matriz Z ou um lago
                            dif = 0
                        else:  # senao faz a média
                            dif = (end-start)/ctt
                        ctt = 0  # reinicia o contador
                        for k in range(i, j):
                            start += dif
                            m_saida.append(
                                [m_conn_maps[k][0], m_conn_maps[k][1], start])
                        break

        else:
            m_saida.append(
                [m_conn_maps[i][0], m_conn_maps[i][1], m_conn_maps[i][2]])

    return np.array(m_saida)


def output(m, start):  # exporta o mapa em txt para lwitura no WhiteBox, com o nome: fill-coordenadas-z.txt
    body = ""
    for i in range(rows):
        for j in range(cols):
            if(m[i][j] == noData):
                body += str(int(m[i][j]))+" "
            else:
                body += str(m[i][j])+" "
        body += "\n"

    arq = open('output/fill-coordenadas-z.txt', 'w+')
    arq.write(start)
    arq.write(body)
    arq.close()


'''
    FIM FUNCOES
'''


# cria os arrays e os transforma em np.array type
start = matriz(open("MainStreamFromLidar.txt", 'rb'))[1]
matriz_rio_correto = np.array(matriz(open("MainStreamFromLidar.txt", 'rb'))[0])
matriz_rio_errado = np.array(
    matriz(open("MapaCaminhoElevacaoCorreta.txt", 'rb'))[0])
matriz_mapa_elevacao = np.array(
    matriz(open("MapaElevacaoCorreta.txt", 'rb'))[0])
matriz_ponto_inicial = np.array(
    matriz(open("PourPointVarredura.txt", 'rb'))[0])

# pega o número de colunas e linhas, é padronizado para todos
rows = matriz_rio_correto.shape[0]
cols = matriz_rio_correto.shape[1]

# MAPA COM CAMINHO CORRETO (X,Y)

'''
   O Codigo é com base no mapa com o x e y coretos, mas elevações Z, erradas
   O código abaixo lerá pegará os valores de conexão de dois rios e pegará sua altitude (Z)
   Ele irá gerar um CSV
   Depois irá criar um caminho, começando pelo ponto inicial até o ultimo ponto de referencia
   Depois ele usa os dados de referencia e distancia e junta em um mesmo array, contendo X, Y, Z e Distancia entre as referencias
'''

matriz_inter_rios = inter_maps(matriz_rio_correto, matriz_rio_errado)

# procura os pontos de interseção e retona a elevação daquele ponto e mais a posição x e y dele
matriz_elevacao_coodenadas = np.array(
    array_pits(matriz_inter_rios, matriz_mapa_elevacao))

# converte para DataFrame Pandas
df_matriz_elevacao_coodenadas = pd.DataFrame(matriz_elevacao_coodenadas)

# gera um arquivo csv para saída
df_matriz_elevacao_coodenadas.to_csv('output/inter-xyz.csv')

# escavando pontos de conexão
caminho = carve_point([10, 752],
                      matriz_rio_correto, matriz_elevacao_coodenadas)
df_caminho = pd.DataFrame(caminho)
df_caminho.to_csv('output/caminho_xy.csv')

# pegando apenas as colunas 1 e 2, elimanando o z
m_reffers = np.delete(matriz_elevacao_coodenadas, (0), axis=1)

# pegando a distancia entre os pontos de referencia
m_distance_referencia = distancia_referencia(
    pre_tratamento(m_reffers, caminho), caminho)

# Array numpy com as cordenadas x, y - a distancia - e o valor Z
distant_refer_xyz = distan_refer_xyz(
    m_distance_referencia, matriz_elevacao_coodenadas)

# Criando DataFrame Pandas para gerar csv
pd_m_distant_refer_xyz = pd.DataFrame(distant_refer_xyz, columns=[
                                      'Z', 'X', 'Y', 'Distancia'])

# gerando CSV
pd_m_distant_refer_xyz.to_csv("output/distancia-referencia-xyz_rio_certo.csv")


# MAPA COM ELEVAÇÂO CORRETA (Z)

'''
    O Código abaixo trabalhará com a matriz de pontos do Mapa com a elevação correta
'''

# escavando pontos de conexão
caminho_rio_errado = carve_point([23, 751],
                                 matriz_rio_errado, matriz_elevacao_coodenadas)
df_caminho_rio_errado = pd.DataFrame(caminho_rio_errado)
df_caminho_rio_errado.to_csv('output/caminho_z.csv')

# pegando a distancia entre os pontos de referencia
m_distance_referencia_rio_errado = distancia_referencia(
    pre_tratamento(m_reffers, caminho_rio_errado), caminho_rio_errado)

# Array numpy com as cordenadas x, y - a distancia - e o valor Z
distant_refer_xyz_rio_errado = distan_refer_xyz(
    m_distance_referencia_rio_errado, matriz_elevacao_coodenadas)

# Criando DataFrame Pandas para gerar csv
pd_m_distant_refer_xyz_rio_errado = pd.DataFrame(distant_refer_xyz_rio_errado, columns=[
    'Z', 'X', 'Y', 'Distancia'])

# gerando CSV
pd_m_distant_refer_xyz_rio_errado.to_csv(
    "output/distancia-referencia-xyz_rio_errado.csv")

# TRABALHANDO COM OS DOIS MAPAS

'''
    O código agora relacionará os dois mapas e resultá em um modelo aproximado do real
'''

pre_tratamento_referencial = pre_tratamento_referencia(
    m_distance_referencia, m_distance_referencia_rio_errado, matriz_mapa_elevacao)

pd_pre_tratamento_referencial = pd.DataFrame(
    pre_tratamento_referencial,  columns=['Z', 'X', 'Y', 'D', 'd', 'D/d'])
pd_pre_tratamento_referencial.to_csv("output/pre_tratamento.csv")

joinMapas = pd.concat([pd_pre_tratamento_referencial[['Z']], pd_pre_tratamento_referencial[['X']], pd_pre_tratamento_referencial[['Y']],
                       pd_pre_tratamento_referencial[['d']], pd_pre_tratamento_referencial['D'], pd_pre_tratamento_referencial['D/d']], axis=1, sort=False)

joinMapas.columns = [
    'Z', 'X', 'Y', 'Distancia Traçado Errado', 'Distancia Correto Errado', 'D/d']

joinMapas.to_csv("output/joinMapas.csv")

'''
    Trabalhando com JoinMaps
'''


m_caminho_elevacao = carve_point_z([23, 751],
                                   matriz_mapa_elevacao, matriz_elevacao_coodenadas)


conn_maps = conn_maps(joinMapas, caminho,
                      m_caminho_elevacao, caminho_rio_errado)

m_fill_void = fill_void(conn_maps)

pd_m_fill_void = pd.DataFrame(m_fill_void)
pd_m_fill_void.to_csv("output/m-fill-void.csv")

pd_conn_maps = pd.DataFrame(conn_maps,
                            columns=["X", "Y", "Z"])
pd_conn_maps.to_csv("output/caminho_elevacao_correta.csv")

'''
    Gerando gráficos de elevação e exportando para WhiteBox
'''

# GERANDO SAIDA PARA LEITURA NO WHITEBOX

output(gen_map(m_fill_void), start)

# DADOS PARA GRAFICOS

m_caminho_elevacao = carve_point_z([23, 751],
                                   matriz_mapa_elevacao, matriz_elevacao_coodenadas)

x = np.linspace(0, len(m_caminho_elevacao)-1, len(m_caminho_elevacao))

xinter = np.linspace(0, len(matriz_elevacao_coodenadas) -
                     1, len(matriz_elevacao_coodenadas))
yinter = matriz_elevacao_coodenadas[:, 0]

xfill_void = np.linspace(0, 1229, 1230)
yfill_void = m_fill_void[:, 2]


# GERANDO GRAFICOS

plt.plot(xfill_void, yfill_void, label='XY Original com Z (CORRETO)')
plt.plot(x, m_caminho_elevacao, label='Z Original (ERRADO)')
plt.plot(8*xinter, yinter, 'o', label='Inter')
plt.xlabel('x pixels')
plt.ylabel('y elevation')
plt.legend()

plt.show()

print("success :)")
