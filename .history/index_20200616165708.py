gis = open("MainStreamFromLidar.txt", 'rb')
i = 0
for lin in gis:
    if(i > 4):
        print(lin)
        break
    i += 1
