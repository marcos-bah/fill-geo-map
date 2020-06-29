gis = open("MainStreamFromLidar.txt", 'rb')
i = 0
for lin in gis:
    if(i > 6):
        print(lin)
        break
    i += 1
