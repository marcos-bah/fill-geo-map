gis = open("MainStreamFromLidar.txt", 'rb')
matriz = []
i = 0
for lin in gis:
    if(i > 5):
        matriz = [int(x) for x in lin.split()]
        break
    else:
        i += 1

print(matriz)
