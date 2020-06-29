gis = open("MainStreamFromLidar.txt", 'rb')
matriz = []
i = 0
for lin in gis:
    if(i > 5):
        matriz.append([int(x) for x in lin.split()])
    else:
        i += 1

print(matriz)
