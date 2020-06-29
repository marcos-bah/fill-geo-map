gis = open("MainStreamFromLidar.txt", 'rb')
i = 0
for lin in gis:
    if(i < 6):
        i += 1
        pass
    print(lin)
    break
