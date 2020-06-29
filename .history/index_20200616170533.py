import numpy as np
import pandas as pd

gis = open("MainStreamFromLidar.txt", 'rb')
matriz = []
i = 0
for lin in gis:
    if(i > 5):
        matriz.append([int(float(x)) for x in lin.split()])
    else:
        i += 1

matriz = np.array(matriz)
matriz = pd.DataFrame(matriz)

print(matriz)
