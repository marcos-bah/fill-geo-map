gis = open("MainStreamFromLidar.txt", 'rb')
i = 0
for lin in gis:
    if(i < 5):
        i += 1
        pass
    print(lin)
