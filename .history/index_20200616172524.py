import numpy as np
import pandas as pd

gis = open("MainStreamPixel.txt", 'rb')
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

for r in range(matriz.shape[0]):
    for c in range(matriz.shape[1]):
        if(matriz[r, c] == noData):
            pass
        else:
            print(matriz[r, c])
