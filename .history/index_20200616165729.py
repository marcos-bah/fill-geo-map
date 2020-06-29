gis = open("MainStreamFromLidar.txt", 'rb')
i = 0
for lin in gis:
    if(i > 5):
        print(lin)
        break
    else:
        i += 1
