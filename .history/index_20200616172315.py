import numpy as np
import pandas as pd

gis = open("teste.txt", 'rb')
matriz = []

noData = -9999

i = 0
for lin in gis:
    if(i > 5):
        matriz.append([int(float(x)) for x in lin.split()])
    else:
        i += 1

matriz = np.array(matriz)
m = pd.DataFrame(matriz)
print(matriz.shape[0])
print(matriz.shape[1])
for r in range(matriz.shape[0]):
    for c in range(matriz.shape[1]):
        print(r)
        break
    break
