##
## Simple Script to test access to the neurons of the BrainCard
##
## Refer to Docs/Test_SimpleScript.pdf from General Vision for
## details about this script.
##
import time
import Braincard
import json
from constants import *
from loader import MNIST
class brain_learn:
	Braincard.connect(500000);
	inputlen=750;
	trvec=None	
	train_labels =None
	ncount=0
	def loadMnist(self):
		m = MNIST('./data')
		self.trvec,self.train_labels = m.load_training()
	def initAll(self):
		
		Braincard.write(CM1K,FORGET,0);
		time.sleep(0.1)
	def learnItem(self,id):
		self.learn(self.trvec[id],self.train_labels[id])
	def learn(self,img,lab):
		self.ncount = Braincard.learn(img,lab)
		print "learned ",lab, "committed:", self.ncount
	def learnSet(self,s,e):
		for x in range(s,e):
			self.learn(self.trvec[x],self.train_labels[x])
	def recVec(self,v):
		respLevel, results=Braincard.recognize(v,5);
		print respLevel,results
		if respLevel > 0:
			for i in range(0,respLevel):
		    		print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]));
	def learnAdding(self):
		self.trvec=[[1,255,0,128,0],[255,1,128,10],[255,255,255,0],[255,255,0,0],[0,0,255,255],[128,1,0,128],[128,128,255,1],[1,1,1,1],[255,128,0,255],[50,45]]	
		self.train_labels= [sum(self.trvec[0]),sum(self.trvec[1]),sum(self.trvec[2]),sum(self.trvec[3]),sum(self.trvec[4]),sum(self.trvec[5]),sum(self.trvec[6]),sum(self.trvec[7]),sum(self.trvec[8]),sum(self.trvec[9])]  	
		for x in range(0,len(self.trvec)):
			self.learnItem(x)
	def recItem(self,x):
		respLevel, results=Braincard.recognize(self.trvec[x],5);
		print respLevel,results
		if respLevel > 0:
			for i in range(0,respLevel):
		    		print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]));
		print("Should be : ",self.train_labels[x]);
	def showNeurons(self):
		## display the content of the neurons
		print("\n\nRead the content of the %u committed neurons" % self.ncount);
		for i in range(0,self.ncount):
	    		ncr, model, aif, minif, cat = Braincard.reviewNeuron(i)
    			print("\nncr=%u \tcat=%u \taif=%u \tmodel:" % (ncr, cat, aif)),
	    		for j in range(0,len(model) -1):
			        print("\t%u" % model[j]),        
	def showDefault(self):
		value=Braincard.read(CM1K,MINIF);
		print ("Read default Minif=%u" % value);

		value=Braincard.read(CM1K,MAXIF);
		print ("Read default Maxif=%u" % value);
	def learnSample(self):
		vector=[0 for i in range(self.inputlen)]

		print("\nLearn as category 55 the vector "),
		for i in range(0,self.inputlen):
		    vector[i]=11
		    print("%u, " % (vector[i])),
		Braincard.learn(vector,55);

		print("\nLearn as category 33 the vector "),
		for i in range(0,self.inputlen):
		    vector[i]=15
		    print("%u, " % (vector[i])),
		Braincard.learn(vector,33);

		print("\nLearn as category 100 the vector "),
		for i in range(0,self.inputlen):
		    vector[i]=20
		    print("%u, " % (vector[i])),
		ncount=Braincard.learn(vector,100);
	def showContentSample(self,ncount,img):
		## display the content of the neurons
		print("\n\nRead the content of the %u committed neurons" % ncount);
		for i in range(0,ncount):
		    ncr, model, aif, minif, cat = Braincard.reviewNeuron(i)
		    print("\nncr=%u \tcat=%u \taif=%u \tmodel:" % (ncr, cat, aif)),
		    for j in range(0,10):
			print("\t%u" % model[j]),        

		## In case of multiple firing, read the response of
		## at least the top 3 firing neurons
		K=3;

		print("\n\nBroadcast image "),
		respLevel, results=Braincard.recognize(img,K);
		for i in range(0,respLevel):
		    print ("nid=%u \tcat=%u \tdist=%u" % (results[i][2], results[i][1], results[i][0]));
		print("Observation: recognized by neurons 1 and 2, but closer to 1\n");
		## save knowledge
		## neuronsContent=Braincard.readNeurons(ncount);
class image_converter:
    keyframes=[]
    def train_downsampler(self):

        pass
    def downsample(self,vector):
        pass
    def load_keyframes(self):
    
