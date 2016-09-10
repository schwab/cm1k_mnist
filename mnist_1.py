##
## Train and test the BrainCard on the MNIST data card
##
##
import time
import Braincard
import json
from constants import *
from loader import MNIST
from algorithms import compression_templates

# Perform BrainCard training and testing on the MNIST image set
class brain_learn:
    Braincard.connect(500000);
    inputlen=750;
    trvec=None	
    trvecRed=None
    train_labels =None
    ncount=0
    ca=None
    minif=2
    
    ### Load the raw MNIST training data into training arrays	
    def loadMnist(self):
		m = MNIST('./data')
		self.trvec,self.train_labels = m.load_training()
	
    ### Clear the BrainCard of any existing memories
    def initAll(self):
        Braincard.write(CM1K,FORGET,0)
        time.sleep(0.1)
        if self.minif != 2:
            Braincard.write(CM1K,MINIF,self.minif)
            print "Set MINIF  to", self.minif
    
    ### Train the Braincard on a single row from the training data by index
    def learnItem(self,id):
		self.learn(self.trvecRed[id],self.train_labels[id])
        ### Learn a vector and categorize it by label

    # Learn a single image given its label
    def learn(self,img,lab):
		self.ncount = Braincard.learn(img,lab)
		print "learned ",lab, "committed:", self.ncount
    
    # learn a set of items from the training set 
    def learnSet(self,s,e):
		for x in range(s,e):
			self.learn(self.trvecRed[x],self.train_labels[x])

    # submit the vector v to the braincard and return the regoction details
    def recVec(self,v):
        respLevel,results=Braincard.recognize(v,5)
        return (respLevel,results)
    
    def compressAllTrvec(self):
        ic = image_converter()
        self.trvecRed = []
        for img in self.trvec:
            r =ic.downsample(img)
            self.trvecRed.append(r)
            print "converted ", len(self.trvecRed), 'images'
    def compressTrvecRange(self,cnt):
        ic = image_converter()
        self.trvecRed=[]
        for img in range(0,cnt):
            r =ic.downsample(img)
            self.trvecRed.append(r)
            print "converted ", len(self.trvecRed), 'images'   
    def recognizeReport(self,idx):
        r1,r2=self.recVec(self.trvecRed[idx])
        print "expected cat",self.train_labels[idx]
        self.printResponse(r1,r2)
    
    def calcTrainError(self):
        errorData={'successCount':0,'errorCount':0,'errorIds':[]}
        for x in range(0,len(self.trvecRed)):
            r1,r2 = self.recVec(self.trvecRed[x])
            if r1 > 0  and r2[0][1] == self.train_labels[x] :
                errorData['successCount'] = errorData['successCount']+1
                print "Success", x
            else:
                errorData['errorCount'] = errorData['errorCount'] + 1
                errorData['errorIds'].append(x)
                print "Error", x
        return errorData

    ### teach the braincard to do sums
    def printResponse(self,resp,results):
	    print resp,results
	    if resp > 0:
	        for i in range(0,resp):
                    print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]));
    
    def learnAdding(self):
	    self.trvec=[[1,255,0,128,0],[255,1,128,10],[255,255,255,0],[255,255,0,0],[0,0,255,255],[128,1,0,128],[128,128,255,1],[1,1,1,1],[255,128,0,255],[50,45]]	
	    self.train_labels= [sum(self.trvec[0]),sum(self.trvec[1]),sum(self.trvec[2]),sum(self.trvec[3]),sum(self.trvec[4]),sum(self.trvec[5]),sum(self.trvec[6]),sum(self.trvec[7]),sum(self.trvec[8]),sum(self.trvec[9])]  	
	    for x in range(0,len(self.trvec)):
	    	self.learnItem(x)
    
    def learnCompression(self):
        #self.initAll()
        c = compression_templates()
        self.ca = c.eightToOneByteCompressionAlgorithm()
        self.trvec =[]
        self.train_labels=[]
        for item in self.ca:
            self.trvec.append(item["x"])
            self.train_labels.append(item["y"])
        self.learnSet(0,len(self.trvec))
    
    def recItem(self,x):
	    respLevel, results=Braincard.recognize(self.trvec[x],5)
	    print respLevel,results
	    if respLevel > 0:
		for i in range(0,respLevel):
		    print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]))
	    print("Should be : ",self.train_labels[x])

    # display the contents of commit neurons
    def showNeurons(self):
	    ## display the content of the neurons
	    print("\n\nRead the content of the %u committed neurons" % self.ncount)
	    for i in range(0,self.ncount):
	    	ncr, model, aif, minif, cat = Braincard.reviewNeuron(i)
    		print("\nncr=%u \tcat=%u \taif=%u \tmodel:" % (ncr, cat, aif))
	    	for j in range(0,len(model) -1):
		    print("\t%u" % model[j]),        

    # Download the current nn state from braincard and save in a file "<name>.nn"
    def saveNetwork(self,name):
        nn = Braincard.readNeurons(self.ncount)
        filename=name + ".nn"
        with open(filename,'w') as f:
            json.dump(nn,f)
        print "saved " ,len(nn)  ,'weigths to ',filename
    
    def loadNetwork(self,name):
        #Braincard.
        pass

    def showDefault(self):
        value=Braincard.read(CM1K,MINIF);
        print ("Read default Minif=%u" % value);
        value=Braincard.read(CM1K,MAXIF);
        print ("Read default Maxif=%u" % value);
		## save knowledge
		## neuronsContent=Braincard.readNeurons(ncount);

class image_converter:
    keyframes=[]
    def train_downsampler(self):

        pass
    def downsample(self,vector):
        ptr =0
        reduced =[]
        ct = compression_templates()
        while ptr < len(vector):
            batch = vector[ptr :ptr+ 8]
            ptr = ptr + 8
            coin = ct.compressCpu(batch)
            reduced.append(coin)

        return reduced
    def load_keyframes(self):
        pass    
