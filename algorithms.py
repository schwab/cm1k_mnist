def generateTemplateData():
    templates =[]
    last = 1
    for i in range(0,218):
        mask = int("{0:b}".format(i))
        mask = mask & 0b0000000011111111
        t = [0,0,0,0,0,0,0,0]
        print i,mask
        for m in range(0,8):
            #print last & mask
            if last & mask:
                t[m] = 255
            mask = mask>>1
        print t
        templates.append(t)

    return templates

