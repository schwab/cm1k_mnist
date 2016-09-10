import json
import random

### templates for generating training data for cmk1k
class compression_templates:

    ### Returns a training set for the CM1K allowing it to perform lossy compression of 8 bytes of data to just one
    ### This is useful for converting grey scale images where the only infomration needed is whether a pixel is off or on
    ### for instance, on this pattern loaded on the CM1K will convert [255,255,255,255,0,0,0,0] to 11110000 
    def eightToOneByteCompressionAlgorithm(self):
        templates =[]
        last = 1
        for i in range(0,256):
            mask = int("{0:b}".format(i))
            #data = mask & 0b0000001111111111
            data = i
            t = [0,0,0,0,0,0,0,0]
            t2 = [0,0,0,0,0,0,0,0]
            #print i,mask, data
            for m in range(0,8):
                #print last & mask
                if last & data:
                    t[m] =127 
                    t2[m] = 255
                data = data>>1
            trainData = {"x":t,"y":i}
            templates.append(trainData)
            trainData = {"x":t2,"y":i}
            templates.append(trainData)

        return templates
    def save8to1TrainingSet(self):

        t = self.eightToOneByteCompressionAlgorithm()
        lst =[]
        with open("downsample_keyframes.json",'w') as  f:
            json.dump(t,f)

    def compressionTestData(self,count):
        testRange = range(0,count)
        testSet=[]
        random.seed()
        for t in testRange:
            testBin = 0
            vector =[0,0,0,0,0,0,0,0]
            for b in range(0,8):
                vItem = random.randint(1,10)
                if vItem > 4:
                    testBin = testBin | 1
                    vItem = 255
                else:
                    vItem=0
                testBin = testBin << 1
                vector[b]=vItem
            testBin = testBin >> 1
            testSet.append({"x":vector,'y':testBin,'bStr':"{0:b}".format(testBin)})
        #print testSet
        return testSet

    def testCompression(self,input,bl):
        perfectMatches=0
        totalError=0
        totalTests=0
        for item in input:
            respLevel, result = bl.recVec(item['x'])
            #print 'Expected Cat: ',item['y'],'Actual Cat:',result[0][1],'Dist:',result[0][0]
            if item['y'] == result[0][1]:
                perfectMatches+=1
            else:
                totalError+=abs(item['y'] - result[0][1])

            totalTests+=1
        print  "Tests",totalTests,"Matches",perfectMatches,"TotalError",totalError
    #def testCompressCpuImage(self,img):
    
    def compressCpu(self,indata):
        data=0
        #print indata
        for x in range(0,7):
            if indata[x] > 20:
                data = data + 1
                #print data
            data = data << 1
        return data

    def expandOneByteToPixels(self,indata):
        data = [0,0,0,0,0,0,0,0]
        mask = 1
        for x in range(0,7):
            if indata & mask == 1:
                data[7-x] = 255
                indata = indata >> 1
        return data
    
    # expand a compressed byte array (to b/w image data)
    def expandBytesToPixels(self,data):
        out = []
        for b in data:
            out + self.expandOneByteToPixels(b)
        return out


    def compressCpuBatch(self,inset):
        data = []
        for item in inset:
            data.append(self.compressCpu(item['x']))
        return data
